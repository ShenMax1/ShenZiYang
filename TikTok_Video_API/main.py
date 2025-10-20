#!/usr/bin/env python3
"""
音视频处理主程序
整合下载、转文本、AI分析和文件清理功能
"""

import os
import sys
import time
from pathlib import Path

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def print_header():
    """打印程序标题"""
    print("=" * 60)
    print("音视频自动化处理系统")
    print("=" * 60)

def get_user_input():
    """获取用户输入的文本内容"""
    print("\n请输入抖音链接文本（可包含多个链接）：")
    user_input = input().strip()
    return user_input

def run_download_module(user_input):
    """运行视频下载模块"""
    print("执行下载模块中...")
    
    try:
        import download_douyin_video
        result = download_douyin_video.main(user_input)
        if result:
            print("下载完成")
            return True
        else:
            print("下载失败")
            return False
    except Exception as e:
        print(f"下载模块执行失败: {str(e)}")
        return False

def run_transcribe_module():
    """运行音视频转文本模块"""
    print("执行转文本模块中...")
    
    try:
        import video_to_text
        result = video_to_text.main()
        if result:
            print("转文本完成")
            return True
        else:
            print("转文本失败")
            return False
    except Exception as e:
        print(f"转文本模块执行失败: {str(e)}")
        return False

def run_analysis_module():
    """运行AI分析模块"""
    print("执行api调用模块中...")
    
    try:
        import analyze_transcript
        result = analyze_transcript.main()
        if result:
            print("API调用完成")
            return True
        else:
            print("API调用失败")
            return False
    except Exception as e:
        print(f"API调用模块执行失败: {str(e)}")
        return False

def run_clean_module():
    """运行文件清理模块"""
    print("内容释放中...")
    
    try:
        import clean_old_files
        # 修改清理路径
        clean_old_files.DIRECTORIES = {
            "video": r"D:\test\TikTok_Video_API\video",
            "txt": r"D:\test\TikTok_Video_API\txt", 
            "json": r"D:\test\TikTok_Video_API\json",
            "result": r"D:\test\TikTok_Video_API\result"
        }
        clean_old_files.clean_old_files()
        print("清理完成")
        return True
    except Exception as e:
        print(f"清理模块执行失败: {str(e)}")
        return False

def main():
    """主函数"""
    print_header()
    
    # 获取用户输入
    user_input = get_user_input()
    
    if not user_input:
        print("输入内容为空，程序退出。")
        return
    
    # 执行下载模块
    if not run_download_module(user_input):
        print("下载模块执行失败，程序退出。")
        return
    
    # 等待一段时间确保文件写入完成
    time.sleep(2)
    
    # 执行转文本模块
    if not run_transcribe_module():
        print("转文本模块执行失败，程序退出。")
        return
    
    # 等待一段时间确保文件写入完成
    time.sleep(2)
    
    # 执行AI分析模块
    if not run_analysis_module():
        print("API调用模块执行失败，程序退出。")
        return
    
    # 等待一段时间确保文件写入完成
    time.sleep(2)
    
    # 执行清理模块
    run_clean_module()
    
    print("结束保存至路径")

if __name__ == "__main__":
    main()