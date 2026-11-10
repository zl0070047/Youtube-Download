# YouTube 下载器项目结构

## 文件结构

```
.
├── YouTube download.py    # 主程序文件
├── create_qrcode.py      # 二维码生成工具
├── requirements.txt      # 项目依赖
├── README.md            # 项目说明文档
└── qrcode.png           # 公众号二维码
```

## 核心模块

### 1. 主程序模块 (YouTube download.py)

#### 1.1 类结构
- `YouTubeDownloader`：主类，负责整个应用的初始化和控制
  - `__init__`：初始化GUI界面和变量
  - `create_widgets`：创建界面组件
  - `setup_layout`：设置界面布局
  - `setup_bindings`：设置事件绑定

#### 1.2 功能模块
- **视频信息获取**
  - `check_video`：检查视频信息
  - `get_video_info`：获取视频详细信息
  - `update_video_info`：更新视频信息显示

- **下载功能**
  - `start_download`：开始下载
  - `download_video`：视频下载实现
  - `download_audio`：音频下载实现
  - `progress_hook`：下载进度回调

- **界面交互**
  - `browse_save_path`：选择保存路径
  - `update_format_info`：更新格式信息
  - `update_thumbnail`：更新缩略图
  - `show_copyright_disclaimer`：显示版权声明

- **历史记录**
  - `add_to_history`：添加历史记录
  - `load_history`：加载历史记录
  - `save_history`：保存历史记录

### 2. 二维码生成模块 (create_qrcode.py)
- 生成示例二维码
- 支持自定义二维码内容

## 依赖关系

### 主要依赖
- `yt-dlp`：YouTube视频下载核心库
- `tkinter`：GUI界面框架
- `Pillow`：图像处理
- `requests`：网络请求
- `qrcode`：二维码生成

## 数据流

1. **输入流程**
   - 用户输入YouTube链接
   - 系统验证链接有效性
   - 获取视频信息

2. **处理流程**
   - 解析视频信息
   - 获取可用格式
   - 用户选择下载选项
   - 开始下载任务

3. **输出流程**
   - 显示下载进度
   - 保存文件
   - 更新历史记录

## 安全特性

- SSL证书验证
- 错误处理机制
- 重试机制
- 版权声明和法律提示

## 用户界面

### 主要组件
- 视频链接输入框
- 视频信息显示区
- 格式选择区
- 下载进度条
- 历史记录列表
- 保存路径选择器

### 交互功能
- 拖放支持
- 剪贴板操作
- 实时进度显示
- 错误提示 