#!/usr/bin/env python3
"""
测试脚本，用于验证TikTok_Video_API目录中的所有模块是否能正常工作
"""

import os
import sys

def test_module_imports():
    """测试模块导入"""
    print("测试模块导入...")
    
    try:
        import download_douyin_video
        print("✓ download_douyin_video 模块导入成功")
    except Exception as e:
        print(f"✗ download_douyin_video 模块导入失败: {e}")
        return False
    
    try:
        import video_to_text
        print("✓ video_to_text 模块导入成功")
    except Exception as e:
        print(f"✗ video_to_text 模块导入失败: {e}")
        return False
        
    try:
        import analyze_transcript
        print("✓ analyze_transcript 模块导入成功")
    except Exception as e:
        print(f"✗ analyze_transcript 模块导入失败: {e}")
        return False
        
    try:
        import clean_old_files
        print("✓ clean_old_files 模块导入成功")
    except Exception as e:
        print(f"✗ clean_old_files 模块导入失败: {e}")
        return False
        
    return True

def test_directory_structure():
    """测试目录结构"""
    print("\n测试目录结构...")
    
    required_dirs = [
        r"D:\test\TikTok_Video_API\video",
        r"D:\test\TikTok_Video_API\txt",
        r"D:\test\TikTok_Video_API\json",
        r"D:\test\TikTok_Video_API\result"
    ]
    
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✓ 目录 {directory} 存在")
        else:
            print(f"✗ 目录 {directory} 不存在")
            return False
            
    return True

def test_file_paths():
    """测试文件路径配置"""
    print("\n测试文件路径配置...")
    
    try:
        import download_douyin_video
        import video_to_text
        import analyze_transcript
        import clean_old_files
        
        # 检查download_douyin_video路径
        # 读取文件内容检查路径配置
        with open("download_douyin_video.py", "r", encoding="utf-8") as f:
            content = f.read()
            if "TikTok_Video_API\\\\video" in content and "TikTok_Video_API\\\\json" in content:
                print("✓ download_douyin_video 路径配置正确")
            else:
                print("✗ download_douyin_video 路径配置不正确")
                return False
            
        # 检查video_to_text路径
        if "TikTok_Video_API" in video_to_text.VIDEO_DIR:
            print("✓ video_to_text 路径配置正确")
        else:
            print("✗ video_to_text 路径配置不正确")
            return False
            
        # 检查analyze_transcript路径
        if "TikTok_Video_API" in analyze_transcript.TXT_DIR:
            print("✓ analyze_transcript 路径配置正确")
        else:
            print("✗ analyze_transcript 路径配置不正确")
            return False
            
        # 检查clean_old_files路径
        if any("TikTok_Video_API" in path for path in clean_old_files.DIRECTORIES.values()):
            print("✓ clean_old_files 路径配置正确")
        else:
            print("✗ clean_old_files 路径配置不正确")
            return False
            
        return True
    except Exception as e:
        print(f"✗ 文件路径测试失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("TikTok_Video_API 模块测试")
    print("=" * 50)
    
    all_tests_passed = True
    
    # 运行所有测试
    all_tests_passed &= test_module_imports()
    all_tests_passed &= test_directory_structure()
    all_tests_passed &= test_file_paths()
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("所有测试通过！TikTok_Video_API 配置正确。")
    else:
        print("部分测试失败，请检查上述错误信息。")
    print("=" * 50)

if __name__ == "__main__":
    main()