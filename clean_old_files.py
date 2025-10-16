#!/usr/bin/env python3
"""
清理脚本，用于清除 result、txt、json 目录中的旧文件，默认保留最新的十条数据
"""

import os
import glob
from pathlib import Path
import argparse

# 定义需要清理的目录
DIRECTORIES = {
    "result": r"D:\test\result",
    "txt": r"D:\test\txt",
    "json": r"D:\test\json"
}

def get_sorted_files(directory):
    """获取目录中按修改时间排序的文件列表（最新的在前）"""
    try:
        files = list(Path(directory).glob("*"))
        # 按修改时间排序，最新的文件排在前面
        files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        return files
    except Exception as e:
        print(f"获取目录 {directory} 文件列表时出错: {e}")
        return []

def clean_directory(directory, keep_count):
    """清理指定目录，保留最新的keep_count个文件"""
    print(f"正在清理目录: {directory}")
    
    if not os.path.exists(directory):
        print(f"目录 {directory} 不存在，跳过清理")
        return
    
    files = get_sorted_files(directory)
    print(f"目录 {directory} 中共有 {len(files)} 个文件")
    
    if len(files) <= keep_count:
        print(f"文件数量 ({len(files)}) 不超过保留数量 ({keep_count})，无需清理")
        return
    
    # 需要删除的文件数量
    to_delete = files[keep_count:]
    print(f"需要删除 {len(to_delete)} 个旧文件")
    
    # 删除旧文件
    deleted_count = 0
    for file_path in to_delete:
        try:
            os.remove(file_path)
            print(f"已删除: {file_path}")
            deleted_count += 1
        except Exception as e:
            print(f"删除文件 {file_path} 时出错: {e}")
    
    print(f"目录 {directory} 清理完成，共删除 {deleted_count} 个文件")

def clean_old_files(keep_count=10, target_dirs=None):
    """清理旧文件的主函数"""
    if target_dirs is None:
        target_dirs = DIRECTORIES.keys()
    
    print("=" * 50)
    print("文件清理工具")
    print("=" * 50)
    print(f"保留最新的 {keep_count} 个文件")
    print(f"目标目录: {', '.join(target_dirs)}")
    print()
    
    # 清理指定的目录
    for dir_name in target_dirs:
        if dir_name in DIRECTORIES:
            clean_directory(DIRECTORIES[dir_name], keep_count)
        else:
            print(f"未知目录: {dir_name}")
    
    print()
    print("清理完成!")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="清理 result、txt、json 目录中的旧文件，默认保留最新的10个文件")
    parser.add_argument("-k", "--keep", type=int, default=10, help="保留的文件数量（默认: 10）")
    parser.add_argument("-d", "--dirs", nargs="+", help="指定要清理的目录（result, txt, json），默认清理所有目录")
    
    args = parser.parse_args()
    keep_count = args.keep
    target_dirs = args.dirs if args.dirs else DIRECTORIES.keys()
    
    clean_old_files(keep_count, target_dirs)

if __name__ == "__main__":
    main()
