# YouTube 视频下载器

一个简单易用的 YouTube 视频下载工具，支持下载视频和音频，拥有美观的用户界面和友好的交互体验。

<img width="895" alt="image" src="https://github.com/user-attachments/assets/caae72b3-7836-4f2a-858e-aa9a8aedaba9" />

## 主要功能

- 📹 下载 YouTube 视频，支持多种分辨率和格式
- 🎵 提取 YouTube 视频的音频，支持 MP3、M4A、WAV 等格式
- 📋 历史记录功能，便捷管理已下载的视频
- 🖼️ 视频信息预览，包括缩略图、时长、上传者等信息
- 📊 下载进度实时显示
- 💾 可自定义保存位置
- 🌐 支持多种 YouTube 链接格式（标准链接、短链接、移动版链接）

## 系统要求

- Python 3.6 或更高版本
- 依赖库：
  - yt-dlp
  - tkinter
  - Pillow
  - requests
  - qrcode

## 使用方法

### 安装依赖

```bash
pip install -r requirements.txt
```

### 生成示例二维码

如果需要生成示例二维码，可以运行以下命令：

```bash
python create_qrcode.py
```

将生成的`qrcode.png`替换为您的实际公众号二维码图片。

### 运行程序

```bash
python "YouTube download.py"
```

### 使用步骤

1. 输入或粘贴 YouTube 视频地址
2. 点击"检查视频"获取视频信息
3. 选择下载类型（视频或音频）和所需格式
4. 选择保存位置
5. 点击"开始下载"

## 支持的格式

### 视频格式
- MP4
- WebM

### 音频格式
- MP3
- M4A
- WAV

## 注意事项

- 下载高清视频可能需要较长时间，请耐心等待
- 部分视频可能因版权限制而无法下载
- 请确保您的网络连接稳定

## 版权与法律声明

### 使用目的

本工具仅供**个人学习和研究**目的使用。用户应当将本工具用于以下合法场景：
- 下载自己创作并上传的内容
- 下载获得了明确授权可供下载的内容
- 下载无版权或开放授权（如创作共用许可）的内容
- 在教育和研究领域内，遵循"合理使用"原则下载内容

### 版权责任

- **原始版权**：通过本工具下载的所有视频和音频内容的版权仍属于原始创作者或版权所有者。下载内容并不代表获得了该内容的版权或再分发权。
- **非授权下载**：未经版权所有者明确许可，下载受版权保护的内容可能违反相关法律法规，包括但不限于著作权法、版权法等。
- **商业使用**：严禁将下载的内容用于商业目的，包括但不限于销售、出租、公开表演等。
- **再分发限制**：禁止在未获授权的情况下分享、上传或以其他方式再分发下载的内容。

### 免责声明

- 本工具开发者不对用户使用本工具产生的任何法律纠纷或责任承担任何责任。
- 用户应自行了解并遵守所在国家/地区关于视频下载和版权的法律法规。
- 开发者不对因使用本工具下载内容而可能导致的任何版权纠纷或法律问题负责。
- 如版权所有者认为其内容被不当下载，请联系侵权行为实施者而非本工具开发者。

### 法律风险提示

使用本工具下载视频可能面临的法律风险包括但不限于：
1. 版权侵权诉讼
2. 民事赔偿责任
3. 在某些司法管辖区可能面临刑事责任
4. 侵犯相关平台的服务条款，可能导致账号封禁等后果

**使用本工具即表示您了解并同意自行承担使用过程中的全部法律责任。**

## 未来计划

- 批量下载功能
- 字幕下载与翻译
- 下载完成通知
- 暗黑模式

## 关于作者

- **制作者**：朱富贵
- **公众号**：关注公众号获取更多实用工具和教程
![WechatIMG685](https://github.com/user-attachments/assets/c1375480-6333-4896-942f-5827b53b537d)

## 许可证

此项目基于 MIT 许可证开源，但这仅适用于工具本身的代码，不适用于通过本工具下载的内容。 
