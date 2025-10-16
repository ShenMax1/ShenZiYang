# 音视频自动化处理系统

这是一个集成了抖音视频下载、音视频转文本、AI内容分析和文件清理的自动化处理系统。

## 功能特性

- 抖音视频下载（支持从分享链接自动提取视频）
- 音视频转文本（使用Whisper模型进行语音识别）
- AI内容分析（使用DeepSeek API进行智能分析）
- 自动文件清理（保留最新文件，删除旧文件）
- 简化的一键式操作流程
- 支持从文本中自动提取抖音链接
- 集成繁体中文转简体中文功能
- 提示词优化转录和分析准确性

## 项目结构

```
d:\test\
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

## 使用方法

### 一键式运行（推荐）

```bash
python main.py
```

程序会提示你输入抖音分享链接或包含链接的文本，然后自动完成以下步骤：
1. 下载抖音视频
2. 将视频转换为文本
3. 使用AI分析文本内容
4. 清理旧文件，保留最新10个文件

### 分模块运行

#### 1. 抖音视频下载

```bash
python download_douyin_video.py
```

支持输入包含抖音链接的文本，例如：
```
2.89 复制打开抖音，看看【京牌大明白990的作品】车辆平移全教程来了，可以解决84天进京证办理的烦恼... https://v.douyin.com/yt1apvLRBTU/ nDH:/ 07/25 x@F.UY
```

#### 2. 音视频转文本

```bash
python video_to_text.py
```

自动处理video目录中最新的视频文件。

#### 3. AI内容分析

```bash
python analyze_transcript.py
```

自动分析txt目录中最新的转录文件。

#### 4. 文件清理

```bash
python clean_old_files.py
```

默认保留每个目录最新的10个文件，删除其余旧文件。

## 输出文件

- `video/`: 下载的视频文件存储目录
- `txt/`: 转录文本存储目录
- `result/`: AI分析结果存储目录
- `json/`: 视频信息JSON存储目录
- `提示词.txt`: AI分析提示词文件

## 注意事项

1. 请遵守相关法律法规和网站使用条款
2. 不要过于频繁地请求，以免给服务器造成压力
3. 抖音可能会更新网页结构，如果程序失效请及时反馈
4. Whisper模型较大，首次运行需要下载模型文件
5. DeepSeek API需要网络连接，请确保可以访问https://api.deepseek.com
6. 仅用于学习和研究目的，请勿用于商业用途

## 免责声明

本程序仅供学习交流使用，使用者需自行承担相关法律责任。