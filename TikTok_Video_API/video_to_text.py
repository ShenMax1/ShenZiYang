#!/usr/bin/env python3
"""
音视频转文本脚本
使用Whisper对D:\test\video路径下的音视频文件进行音频转文字处理
"""

import os
import whisper
import datetime
from pathlib import Path
import opencc

# 设置视频文件目录和输出目录
VIDEO_DIR = r"D:\test\TikTok_Video_API\video"
OUTPUT_DIR = r"D:\test\TikTok_Video_API\txt"

# 繁体中文转简体中文转换器
cc = opencc.OpenCC('t2s')

def get_latest_video_file():
    """获取最新的视频文件"""
    if not os.path.exists(VIDEO_DIR):
        raise FileNotFoundError(f"视频目录 {VIDEO_DIR} 不存在")
    
    # 支持的音视频文件扩展名
    supported_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.wav', '.mp3', '.m4a'}
    
    # 获取目录下所有音视频文件，并按修改时间排序（最新优先）
    video_files = []
    for file in os.listdir(VIDEO_DIR):
        if Path(file).suffix.lower() in supported_extensions:
            full_path = os.path.join(VIDEO_DIR, file)
            video_files.append(full_path)
    
    # 按修改时间排序，最新的文件排在前面
    video_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    
    if not video_files:
        raise FileNotFoundError(f"在目录 {VIDEO_DIR} 中未找到支持的音视频文件")
    
    # 返回最新的文件
    return video_files[0]

def read_prompt_file():
    """读取提示词文件内容"""
    prompt_file = r"D:\test\TikTok_Video_API\提示词.txt"
    try:
        with open(prompt_file, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"警告: 提示词文件 {prompt_file} 不存在，将使用默认提示词")
        return ""
    except Exception as e:
        print(f"警告: 读取提示词文件时出错: {e}，将使用默认提示词")
        return ""

def convert_video_to_text(video_path: str, output_dir: str) -> str:
    """
    将音视频文件转换为文本
    
    Args:
        video_path: 音视频文件路径
        output_dir: 输出目录路径
        
    Returns:
        生成的文本文件路径
    """
    print(f"正在处理文件: {video_path}")
    
    # 加载Whisper模型（使用turbo模型，速度优先）
    print("正在加载Whisper模型...")
    model = whisper.load_model("turbo")  # 使用turbo模型以提高处理速度
    
    # 读取提示词文件内容
    initial_prompt = read_prompt_file()
    
    # Whisper参数配置（流式处理优化）
    whisper_params = {
        "fp16": False,           # 禁用FP16以避免警告
        "language": "zh",        # 指定语言为中文
        "task": "transcribe",    # 任务类型：转录
        "temperature": 0.0,      # 温度参数，0.0表示最确定性结果
        # 滑动窗口流式处理参数
        "condition_on_previous_text": True,  # 基于前文内容进行预测
        "prepend_punctuations": "\"'“¿([{-",  # 在单词前添加标点符号
        "append_punctuations": "\"'.。,，!！?？:：”)]}、",  # 在单词后添加标点符号
    }
    
    # 如果有提示词，则添加到参数中
    if initial_prompt:
        whisper_params["initial_prompt"] = initial_prompt
    
    # 预留参数空间，方便后续扩展
    # whisper_params["beam_size"] = 5         # 集束搜索大小
    # whisper_params["patience"] = 1.0        # 集束搜索耐心值
    # whisper_params["length_penalty"] = 1.0  # 长度惩罚
    # whisper_params["suppress_tokens"] = "-1" # 抑制标记
    # whisper_params["without_timestamps"] = False  # 是否包含时间戳
    # whisper_params["max_initial_timestamp"] = 1.0 # 最大初始时间戳
    
    # 使用Whisper转录音频（流式处理）
    print("正在进行音频转文字（流式处理）...")
    result = model.transcribe(video_path, **whisper_params)
    
    # 繁体中文转简体中文
    simplified_text = cc.convert(result["text"])
    
    # 提取文件名（不含扩展名）
    filename = Path(video_path).stem
    
    # 生成输出文件路径，使用精确到分钟的时间戳
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    output_filename = f"{timestamp}_{filename}_transcript.txt"
    output_path = os.path.join(output_dir, output_filename)
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 将转录结果写入文件
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"文件: {video_path}\n")
        f.write(f"处理时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n")
        f.write(simplified_text)
    
    # 同时保存到 D:\test\TikTok_Video_API\result 目录
    result_output_dir = r"D:\test\TikTok_Video_API\result"
    result_output_path = os.path.join(result_output_dir, output_filename)
    os.makedirs(result_output_dir, exist_ok=True)
    
    # 将转录结果写入 result 目录
    with open(result_output_path, "w", encoding="utf-8") as f:
        f.write(f"文件: {video_path}\n")
        f.write(f"处理时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n")
        f.write(simplified_text)
    
    # 删除源视频文件
    try:
        os.remove(video_path)
        print(f"已删除源视频文件: {video_path}")
    except Exception as e:
        print(f"删除源视频文件 {video_path} 时出错: {str(e)}")
    
    print(f"转文字完成，结果已保存至: {output_path}")
    return output_path

def process_latest_video():
    """处理目录下最新的一个音视频文件后自动结束程序"""
    print("=" * 50)
    print("音视频转文字工具")
    print("=" * 50)
    
    try:
        # 获取最新的视频文件
        latest_video_file = get_latest_video_file()
        print(f"找到最新视频文件: {os.path.basename(latest_video_file)}")
        
        # 处理最新视频文件
        result_path = convert_video_to_text(latest_video_file, OUTPUT_DIR)
        print("\n文件处理完成，程序即将退出。")
        return result_path
    except Exception as e:
        print(f"处理文件时出错: {str(e)}")
        return None

def main():
    """主函数"""
    return process_latest_video()

if __name__ == "__main__":
    main()