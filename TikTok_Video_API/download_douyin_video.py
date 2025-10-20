#!/usr/bin/env python3
"""
抖音视频下载脚本
用户输入抖音分享链接，程序爬取视频信息并提供下载选项
"""

import re
import json
import requests
import os
from typing import Dict, Any, Optional, List
from datetime import datetime

# 请求头，模拟移动端访问
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/121.0.2277.107 Version/17.0 Mobile/15E148 Safari/604.1'
}

def extract_douyin_urls(text: str) -> List[str]:
    """
    从文本中提取所有抖音链接
    
    Args:
        text: 包含抖音链接的文本
        
    Returns:
        抖音链接列表
    """
    # 提取分享链接，增强正则表达式以匹配更多格式
    # 匹配 v.douyin.com 或 www.iesdouyin.com 格式的链接
    urls = re.findall(r'https?://(?:v\.douyin\.com|www\.iesdouyin\.com/share/video)/[\w\d\-._?=&/]+', text)
    
    # 如果上面的模式没有匹配到，尝试更通用的匹配
    if not urls:
        urls = re.findall(r'https?://[\w\d\-._?=&/]*douyin[\w\d\-._?=&/]+', text)
    
    # 最后尝试匹配任何URL
    if not urls:
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    
    # 去重并保持顺序
    seen = set()
    unique_urls = []
    for url in urls:
        if url not in seen:
            seen.add(url)
            unique_urls.append(url)
    
    return unique_urls

def parse_douyin_share_url(share_text: str) -> Dict[str, Any]:
    """
    从抖音分享链接中解析视频信息
    
    Args:
        share_text: 包含抖音分享链接的文本
        
    Returns:
        包含视频信息的字典
    """
    # 提取分享链接，增强正则表达式以匹配更多格式
    # 匹配 v.douyin.com 或 www.iesdouyin.com 格式的链接
    urls = re.findall(r'https?://(?:v\.douyin\.com|www\.iesdouyin\.com/share/video)/[\w\d\-._?=&/]+', share_text)
    
    # 如果上面的模式没有匹配到，尝试更通用的匹配
    if not urls:
        urls = re.findall(r'https?://[\w\d\-._?=&/]*douyin[\w\d\-._?=&/]+', share_text)
    
    # 最后尝试匹配任何URL
    if not urls:
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', share_text)
    
    if not urls:
        raise ValueError("未找到有效的分享链接")
    
    share_url = urls[0]
    print(f"正在解析分享链接: {share_url}")
    
    # 如果是短链接，需要获取重定向后的URL以提取视频ID
    if 'v.douyin.com' in share_url:
        share_response = requests.get(share_url, headers=HEADERS)
        # 从重定向后的URL中提取视频ID
        video_id = share_response.url.split("?")[0].strip("/").split("/")[-1]
        share_url = f'https://www.iesdouyin.com/share/video/{video_id}'
    else:
        # 直接从URL中提取视频ID
        video_id = share_url.split("?")[0].strip("/").split("/")[-1]
    
    # 获取视频页面内容
    print("正在获取视频页面信息...")
    response = requests.get(share_url, headers=HEADERS)
    response.raise_for_status()
    
    # 使用正则表达式提取JSON数据
    pattern = re.compile(
        pattern=r"window\._ROUTER_DATA\s*=\s*(.*?)</script>",
        flags=re.DOTALL,
    )
    find_res = pattern.search(response.text)

    if not find_res or not find_res.group(1):
        raise ValueError("从HTML中解析视频信息失败")

    # 解析JSON数据
    json_data = json.loads(find_res.group(1).strip())
    VIDEO_ID_PAGE_KEY = "video_(id)/page"
    NOTE_ID_PAGE_KEY = "note_(id)/page"
    
    if VIDEO_ID_PAGE_KEY in json_data["loaderData"]:
        original_video_info = json_data["loaderData"][VIDEO_ID_PAGE_KEY]["videoInfoRes"]
    elif NOTE_ID_PAGE_KEY in json_data["loaderData"]:
        original_video_info = json_data["loaderData"][NOTE_ID_PAGE_KEY]["videoInfoRes"]
    else:
        raise Exception("无法从JSON中解析视频或图集信息")

    data = original_video_info["item_list"][0]

    # 获取视频信息
    video_url = data["video"]["play_addr"]["url_list"][0].replace("playwm", "play")
    desc = data.get("desc", "").strip() or f"douyin_{video_id}"
    
    # 替换文件名中的非法字符
    desc = re.sub(r'[\\/:*?"<>|]', '_', desc)
    
    # 获取其他信息
    author_name = data.get("author", {}).get("nickname", "未知作者")
    like_count = data.get("statistics", {}).get("digg_count", 0)
    comment_count = data.get("statistics", {}).get("comment_count", 0)
    play_count = data.get("statistics", {}).get("play_count", 0)
    
    return {
        "url": video_url,
        "title": desc,
        "video_id": video_id,
        "author": author_name,
        "likes": like_count,
        "comments": comment_count,
        "plays": play_count
    }

def download_video(video_info: Dict[str, Any], save_path: str | None = None) -> str:
    """
    下载视频到本地
    
    Args:
        video_info: 视频信息字典
        save_path: 保存路径，如果为None则使用默认路径
        
    Returns:
        保存的文件路径
    """
    if save_path is None:
        # 使用当前日期时间（精确到分钟）和标题的第一个字符作为文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        first_char = video_info['title'][0] if video_info['title'] else 'video'
        filename = f"{timestamp}_{first_char}.mp4"
        # 修改保存路径为 D:\test\TikTok_Video_API\video
        save_path = os.path.join(r"D:\\test\\TikTok_Video_API\\video", filename)
    
    # 确保保存目录存在
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    print(f"正在下载视频: {video_info['title']}")
    print(f"保存位置: {save_path}")
    
    # 下载视频
    response = requests.get(video_info['url'], headers=HEADERS, stream=True)
    response.raise_for_status()
    
    # 获取文件大小
    total_size = int(response.headers.get('content-length', 0))
    downloaded = 0
    
    with open(save_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    progress = downloaded / total_size * 100
                    print(f"\r下载进度: {progress:.1f}%", end='', flush=True)
    
    print("\n视频下载完成!")
    return save_path

def process_multiple_links(share_text: str) -> List[str]:
    """
    处理包含多个链接的文本，逐个下载视频
    
    Args:
        share_text: 包含多个抖音链接的文本
        
    Returns:
        下载成功的文件路径列表
    """
    # 提取所有抖音链接
    urls = extract_douyin_urls(share_text)
    
    if not urls:
        print("未找到有效的抖音链接")
        return []
    
    print(f"找到 {len(urls)} 个抖音链接")
    downloaded_files = []
    
    # 逐个处理每个链接
    for i, url in enumerate(urls, 1):
        print(f"\n处理第 {i} 个链接: {url}")
        try:
            # 解析视频信息
            video_info = parse_douyin_share_url(url)
            
            # 显示视频信息
            print("\n" + "=" * 50)
            print("视频信息:")
            print("=" * 50)
            print(f"标题: {video_info['title']}")
            print(f"作者: {video_info['author']}")
            print(f"点赞数: {video_info['likes']}")
            print(f"评论数: {video_info['comments']}")
            print(f"播放数: {video_info['plays']}")
            print(f"视频ID: {video_info['video_id']}")
            print(f"无水印下载地址: {video_info['url']}")
            
            # 下载视频
            print("\n开始下载视频...")
            save_path = download_video(video_info)
            downloaded_files.append(save_path)
            print(f"视频已保存至: {save_path}")
            
            # 保存JSON信息到 D:\test\TikTok_Video_API\json 目录
            # 使用当前日期时间（精确到分钟）和标题的第一个字符作为文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            first_char = video_info['title'][0] if video_info['title'] else 'video'
            json_filename = f"{timestamp}_{first_char}.json"
            json_save_path = os.path.join(r"D:\\test\\TikTok_Video_API\\json", json_filename)
            
            # 确保JSON保存目录存在
            os.makedirs(os.path.dirname(json_save_path), exist_ok=True)
            
            # 写入JSON文件
            with open(json_save_path, 'w', encoding='utf-8') as f:
                json.dump(video_info, f, ensure_ascii=False, indent=2)
            print(f"视频信息已保存至: {json_save_path}")
            
        except Exception as e:
            print(f"处理链接 {url} 时出现错误: {str(e)}")
            print("继续处理下一个链接...")
            continue
    
    return downloaded_files

def main(share_link: Optional[str] = None):
    """主函数"""
    print("=" * 50)
    print("抖音视频下载工具")
    print("=" * 50)
    
    try:
        # 如果没有提供链接，则获取用户输入
        if share_link is None:
            share_link = input("\n请输入抖音分享链接: ").strip()
        
        if not share_link:
            print("请输入有效的分享链接!")
            return None
        
        # 处理多个链接
        downloaded_files = process_multiple_links(share_link)
        
        if downloaded_files:
            print(f"\n成功下载 {len(downloaded_files)} 个视频:")
            for file_path in downloaded_files:
                print(f"  - {file_path}")
            return downloaded_files
        else:
            print("没有成功下载任何视频")
            return None
            
    except KeyboardInterrupt:
        print("\n\n程序已被用户中断")
    except Exception as e:
        print(f"处理过程中出现错误: {str(e)}")
        print("请检查链接是否有效，或稍后重试")
        return None

if __name__ == "__main__":
    main()