# 音视频自动化处理系统 (TikTok Video API)

这是一个集成了抖音视频下载、音视频转文本、AI内容分析和文件清理的自动化处理系统。

## 功能特性

- 抖音视频下载（支持从分享链接自动提取视频）
- 音视频转文本（使用Whisper模型进行语音识别）
- AI内容分析（使用DeepSeek API进行智能分析）
- 自动文件清理（保留最新文件，删除旧文件）
- 简化的一键式操作流程
- 支持从文本中自动提取多个抖音链接并逐个处理
- 集成繁体中文转简体中文功能
- 提示词优化转录和分析准确性

## 项目结构

```
D:\test\TikTok_Video_API\
├── main.py                 # 主程序入口
├── download_douyin_video.py # 抖音视频下载模块
├── video_to_text.py        # 音视频转文本模块
├── analyze_transcript.py   # AI内容分析模块
├── clean_old_files.py      # 文件清理模块
├── 提示词.txt              # AI分析提示词
├── video/                  # 视频文件存储目录
├── txt/                    # 转录文本存储目录
├── result/                 # AI分析结果存储目录
├── json/                   # 视频信息JSON存储目录
└── README.md              # 说明文档
```

## 安装依赖

程序需要以下Python库：

```bash
pip install requests beautifulsoup4 lxml openai-whisper opencc-python-reimplemented
```

注意：Whisper模型会自动下载，首次运行可能需要较长时间。

## 配置说明

### DeepSeek API密钥配置

本系统使用DeepSeek API进行AI内容分析，需要配置有效的API密钥才能正常使用分析功能。

1. 访问 [DeepSeek官网](https://www.deepseek.com/) 注册账号并获取API密钥
2. 在 [analyze_transcript.py](file:///d%3A/test/TikTok_Video_API/analyze_transcript.py) 文件中找到以下代码行：
   ```python
   DEEPSEEK_API_KEY = "your_api_key"
   ```
3. 将 `"your_api_key"` 替换为您自己的DeepSeek API密钥：
   ```python
   DEEPSEEK_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
   ```

### 提示词配置

系统使用 [提示词.txt](file:///d%3A/test/TikTok_Video_API/%E6%8F%90%E7%A4%BA%E8%AF%8D.txt) 文件来指导AI分析，您可以根据需要自定义分析要求。

## 使用方法

### 一键式运行（推荐）

```bash
python main.py
```

程序会提示你输入抖音分享链接或包含多个链接的文本，然后自动完成以下步骤：
1. 下载抖音视频到 `D:\test\TikTok_Video_API\video\`
2. 将视频转换为文本，保存到 `D:\test\TikTok_Video_API\txt\`
3. 使用AI分析文本内容，结果保存到 `D:\test\TikTok_Video_API\result\`
4. 视频信息JSON保存到 `D:\test\TikTok_Video_API\json\`
5. 清理旧文件，保留最新文件（result目录保留50个，其他目录保留10个）

### 分模块运行

#### 1. 抖音视频下载

```bash
python download_douyin_video.py
```

支持输入包含多个抖音链接的文本，例如：
```text
这里有几个抖音视频分享给大家：
第一个：https://v.douyin.com/yt1apvLRBTU/
第二个：https://v.douyin.com/abcd1234/
第三个：https://www.iesdouyin.com/share/video/1234567890123456789/
```

程序会自动提取所有链接并逐个下载视频，视频将保存到 `D:\test\TikTok_Video_API\video\` 目录中。

#### 2. 音视频转文本

```bash
python video_to_text.py
```

自动处理 `D:\test\TikTok_Video_API\video\` 目录中最新的视频文件，转录结果保存到 `D:\test\TikTok_Video_API\txt\` 和 `D:\test\TikTok_Video_API\result\` 目录中。

#### 3. AI内容分析

```bash
python analyze_transcript.py
```

自动分析 `D:\test\TikTok_Video_API\txt\` 目录中最新的转录文件，分析结果保存到 `D:\test\TikTok_Video_API\result\` 目录中。

#### 4. 文件清理

```bash
python clean_old_files.py
```

默认保留每个目录最新的文件：
- result目录保留最新的50个文件
- video、txt、json目录保留最新的10个文件
- 删除其余旧文件，从最旧的开始删除

## 输出文件

- `D:\test\TikTok_Video_API\video\`: 下载的视频文件存储目录
- `D:\test\TikTok_Video_API\txt\`: 转录文本存储目录
- `D:\test\TikTok_Video_API\result\`: AI分析结果存储目录
- `D:\test\TikTok_Video_API\json\`: 视频信息JSON存储目录
- `D:\test\TikTok_Video_API\提示词.txt`: AI分析提示词文件

## 注意事项

1. 请遵守相关法律法规和网站使用条款
2. 不要过于频繁地请求，以免给服务器造成压力
3. 抖音可能会更新网页结构，如果程序失效请及时反馈
4. Whisper模型较大，首次运行需要下载模型文件
5. DeepSeek API需要网络连接，请确保可以访问https://api.deepseek.com
6. 仅用于学习和研究目的，请勿用于商业用途

## 免责声明

本程序仅供学习交流使用，使用者需自行承担相关法律责任。
