#!/usr/bin/env python3
"""
使用DeepSeek API分析转录文件内容
"""

import os
import json
import requests
from pathlib import Path
import datetime
import time

# DeepSeek API配置
DEEPSEEK_API_KEY = "sk-bb22df6e1051431983a6485d0454c0bb"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# 设置转录文件目录和结果目录
TXT_DIR = r"D:\test\txt"
RESULT_DIR = r"D:\test\result"  # 新增结果目录

def read_prompt_file():
    """读取提示词文件内容"""
    prompt_file = r"D:\test\提示词.txt"
    try:
        with open(prompt_file, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"警告: 提示词文件 {prompt_file} 不存在，将使用默认提示词")
        return ""
    except Exception as e:
        print(f"警告: 读取提示词文件时出错: {e}，将使用默认提示词")
        return ""

def get_latest_transcript_file():
    """获取最新的转录文件"""
    if not os.path.exists(TXT_DIR):
        raise FileNotFoundError(f"转录目录 {TXT_DIR} 不存在")
    
    # 获取所有txt文件
    txt_files = list(Path(TXT_DIR).glob("*.txt"))
    
    if not txt_files:
        raise FileNotFoundError(f"在目录 {TXT_DIR} 中未找到转录文件")
    
    # 按修改时间排序，最新的文件排在前面
    txt_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    return txt_files[0]

def read_transcript_file(file_path):
    """读取转录文件内容"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取实际的转录内容（跳过前几行的元数据）
    lines = content.split('\n')
    transcript_start = 0
    for i, line in enumerate(lines):
        if line.startswith("=" * 50):
            transcript_start = i + 1
            break
    
    transcript_content = '\n'.join(lines[transcript_start:])
    return transcript_content.strip()

def analyze_with_deepseek(content, max_retries=3):
    """使用DeepSeek API分析内容，包含重试机制"""
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 读取提示词
    prompt_text = read_prompt_file()
    
    # 如果没有提示词文件，则使用默认提示词
    if not prompt_text:
        system_prompt = "你是一个专业的文本分析助手，请对提供的文本内容进行分析，包括但不限于：主要内容总结、关键信息提取、情感倾向分析等。请用中文回答。"
    else:
        system_prompt = prompt_text
    
    # 限制内容长度以避免API超时
    if len(content) > 1000:
        content = content[:1000] + "\n\n[内容已截断以适应API限制]"
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"请分析以下文本内容：\n\n{content}"
            }
        ],
        "stream": False,
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    # 实现重试机制
    for attempt in range(max_retries):
        try:
            print(f"正在发送请求到DeepSeek API... (尝试 {attempt + 1}/{max_retries})")
            response = requests.post(
                DEEPSEEK_API_URL, 
                headers=headers, 
                json=payload,
                timeout=60  # 增加超时时间到60秒
            )
            print(f"API响应状态码: {response.status_code}")
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except requests.exceptions.Timeout:
            print(f"DeepSeek API调用超时 (尝试 {attempt + 1}/{max_retries})")
            if attempt < max_retries - 1:  # 如果不是最后一次尝试，等待一段时间再重试
                wait_time = 2 ** attempt  # 指数退避
                print(f"等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
            else:
                raise Exception("DeepSeek API调用超时，已达到最大重试次数")
        except requests.exceptions.RequestException as e:
            raise Exception(f"DeepSeek API网络请求失败: {str(e)}")
        except Exception as e:
            raise Exception(f"DeepSeek API调用失败: {str(e)}")
    
    raise Exception("DeepSeek API调用失败，已达到最大重试次数")

def save_analysis_result(file_path, analysis_result):
    """保存分析结果到文件"""
    # 生成分析结果文件名
    stem = Path(file_path).stem
    analysis_filename = f"{stem}_analysis.txt"
    
    # 确保结果目录存在
    os.makedirs(RESULT_DIR, exist_ok=True)
    
    # 将纯分析结果保存到result目录
    result_path = os.path.join(RESULT_DIR, analysis_filename)
    with open(result_path, 'w', encoding='utf-8') as f:
        f.write(analysis_result)
    
    print(f"分析结果已保存至: {result_path}")
    
    return result_path

def analyze_latest_transcript():
    """分析最新的转录文件"""
    print("=" * 50)
    print("转录内容AI分析工具")
    print("=" * 50)
    
    try:
        # 获取最新的转录文件
        latest_file = get_latest_transcript_file()
        print(f"找到最新转录文件: {latest_file.name}")
        
        # 读取转录内容
        transcript_content = read_transcript_file(latest_file)
        print(f"转录内容长度: {len(transcript_content)} 字符")
        
        # 使用DeepSeek API进行分析
        print("正在调用DeepSeek API进行分析...")
        analysis_result = analyze_with_deepseek(transcript_content)
        print("AI分析完成!")
        
        # 保存分析结果
        analysis_file_path = save_analysis_result(latest_file, analysis_result)
        print(f"分析结果已保存至: {analysis_file_path}")
        
        # 打印分析结果
        print("\n" + "=" * 50)
        print("AI分析结果:")
        print("=" * 50)
        print(analysis_result)
        
        return analysis_file_path
    except Exception as e:
        print(f"处理过程中出现错误: {str(e)}")
        # 提供一些解决建议
        print("\n解决建议:")
        print("1. 检查网络连接是否正常")
        print("2. 确认可以访问 https://api.deepseek.com")
        print("3. 如果问题持续存在，可以稍后再试")
        print("4. 检查API密钥是否正确配置")
        return None

def main():
    """主函数"""
    return analyze_latest_transcript()

if __name__ == "__main__":
    main()