import requests
from bs4 import BeautifulSoup
import json
import re
import os

class DouyinScraper:
    def __init__(self):
        # 设置请求头，模拟浏览器访问
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.douyin.com/',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get_video_info(self, share_url):
        """获取抖音视频的基本信息"""
        try:
            # 发送GET请求获取页面内容
            response = self.session.get(share_url, timeout=10)
            response.raise_for_status()
            
            # 使用BeautifulSoup解析HTML
            soup = BeautifulSoup(response.text, 'lxml')
            
            # 提取视频信息
            video_info = {}
            
            # 尝试从JSON数据中提取信息
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string and 'window._ROUTER_DATA' in script.string:
                    # 提取JSON数据
                    json_match = re.search(r'window\._ROUTER_DATA\s*=\s*({.*?});', script.string)
                    if json_match:
                        try:
                            data = json.loads(json_match.group(1))
                            # 尝试获取视频信息
                            video_detail = data.get('routeProps', {}).get('videoDetail', {})
                            if video_detail:
                                video_info['title'] = video_detail.get('title', '')
                                video_info['author'] = video_detail.get('authorInfo', {}).get('nickname', '')
                                video_info['duration'] = video_detail.get('duration', 0)
                                video_info['cover_url'] = video_detail.get('cover', '')
                                video_info['play_url'] = video_detail.get('playAddr', '')
                                video_info['like_count'] = video_detail.get('likeCount', 0)
                                video_info['comment_count'] = video_detail.get('commentCount', 0)
                                video_info['share_count'] = video_detail.get('shareCount', 0)
                                break
                        except json.JSONDecodeError:
                            pass
            
            # 如果没有从JSON中提取到信息，则尝试从HTML标签中提取
            if not video_info:
                # 提取标题
                title_tag = soup.find('title')
                if title_tag:
                    video_info['title'] = title_tag.text.strip()
                
                # 提取描述
                desc_tag = soup.find('meta', attrs={'name': 'description'})
                if desc_tag:
                    video_info['description'] = desc_tag.get('content', '')
                    
                # 提取作者
                author_tag = soup.find('meta', attrs={'property': 'og:video:author'})
                if author_tag:
                    video_info['author'] = author_tag.get('content', '')
                
                # 提取封面图
                cover_tag = soup.find('meta', attrs={'property': 'og:image'})
                if cover_tag:
                    video_info['cover_url'] = cover_tag.get('content', '')
                    
                # 提取视频链接
                video_tag = soup.find('meta', attrs={'property': 'og:video:url'})
                if video_tag:
                    video_info['play_url'] = video_tag.get('content', '')
            
            # 添加分享链接
            video_info['share_url'] = share_url
            
            return video_info
            
        except Exception as e:
            print(f"获取视频信息时出错: {str(e)}")
            return {}

    def download_video(self, video_url, filename):
        """下载视频文件"""
        try:
            if not video_url:
                print("视频链接为空")
                return False
                
            # 创建videos目录
            if not os.path.exists('videos'):
                os.makedirs('videos')
                
            # 完整文件路径
            filepath = os.path.join('videos', filename)
            
            # 下载视频
            print(f"正在下载视频: {filename}")
            response = self.session.get(video_url, stream=True, timeout=30)
            response.raise_for_status()
            
            # 保存视频文件
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            print(f"视频下载完成: {filepath}")
            return True
            
        except Exception as e:
            print(f"下载视频时出错: {str(e)}")
            return False

    def scrape(self, share_url):
        """爬取单个抖音视频信息和视频文件"""
        print(f"开始爬取抖音视频: {share_url}")
        
        # 获取视频信息
        video_info = self.get_video_info(share_url)
        
        if not video_info:
            print("未能获取视频信息")
            return None
            
        print("视频信息:")
        for key, value in video_info.items():
            print(f"  {key}: {value}")
            
        # 下载视频
        play_url = video_info.get('play_url', '')
        if play_url:
            # 生成文件名
            title = video_info.get('title', 'douyin_video')
            # 清理文件名中的非法字符
            filename = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', title)[:50] + '.mp4'
            
            # 下载视频
            success = self.download_video(play_url, filename)
            if success:
                video_info['download_path'] = os.path.join('videos', filename)
            else:
                print("视频下载失败")
        else:
            print("未找到视频播放地址")
            
        return video_info

def main():
    # 创建爬虫实例
    scraper = DouyinScraper()
    
    # 获取用户输入的抖音分享链接
    share_url = input("请输入抖音分享链接: ").strip()
    
    if not share_url:
        print("未提供抖音分享链接")
        return
    
    # 爬取抖音视频信息和视频文件
    result = scraper.scrape(share_url)
    
    if result:
        print("\n爬取完成！")
        # 保存结果到JSON文件
        with open('douyin_video.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print("视频信息已保存到 douyin_video.json")
        if 'download_path' in result:
            print(f"视频文件已保存到 {result['download_path']}")
    else:
        print("爬取失败，请检查链接是否有效")

if __name__ == "__main__":
    main()