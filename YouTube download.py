import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import yt_dlp
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os
import time
from datetime import datetime
import webbrowser
from PIL import Image, ImageTk
import io
import requests
import re
import sys

class YouTubeDownloader:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("YouTube下载器 - 高级版")
        self.window.geometry("900x750")
        self.window.configure(bg="#f5f5f7")  # 苹果风格的背景色
        
        # 设置主题样式
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f5f5f7")
        self.style.configure("TLabelframe", background="#f5f5f7")
        self.style.configure("TLabelframe.Label", background="#f5f5f7", font=("SF Pro Display", 11, "bold"))
        self.style.configure("TButton", font=("SF Pro Display", 10))
        self.style.configure("TLabel", background="#f5f5f7", font=("SF Pro Display", 10))
        self.style.configure("TRadiobutton", background="#f5f5f7", font=("SF Pro Display", 10))
        self.style.configure("TCombobox", font=("SF Pro Display", 10))
        
        # 初始化变量
        self.save_path = os.path.join(os.path.expanduser("~"), "Downloads")
        self.format_info = []
        self.format_details = {}
        self.current_download = None
        self.retry_count = 3
        self.thumbnail_data = None
        self.history = []
        self.max_history = 10
        
        # 下载类型选择
        self.download_type = tk.StringVar(value="video")
        self.video_format = tk.StringVar(value="mp4")
        
        # 显示版权声明
        self.show_copyright_disclaimer()
        
        # 创建UI组件
        self.create_widgets()
        self.load_history()

    def show_copyright_disclaimer(self):
        """显示版权和法律免责声明"""
        disclaimer_text = """
版权与法律声明

使用目的:
本工具仅供个人学习和研究目的使用。

版权责任:
• 通过本工具下载的所有内容的版权仍属于原始创作者或版权所有者
• 未经许可，下载受版权保护的内容可能违反相关法律法规
• 严禁将下载的内容用于商业目的
• 禁止在未获授权的情况下再分发下载的内容

免责声明:
• 开发者不对使用本工具产生的任何法律纠纷承担责任
• 用户应自行了解并遵守当地关于版权的法律法规
• 使用本工具即表示您同意自行承担使用过程中的全部法律责任

要继续使用本工具，请点击"我同意"，表示您已阅读并同意以上声明。
        """
        
        disclaimer_window = tk.Toplevel(self.window)
        disclaimer_window.title("版权免责声明")
        disclaimer_window.geometry("580x450")
        disclaimer_window.transient(self.window)
        disclaimer_window.grab_set()  # 模态窗口
        disclaimer_window.resizable(False, False)
        disclaimer_window.configure(bg="#f5f5f7")
        
        disclaimer_frame = ttk.Frame(disclaimer_window, padding="20")
        disclaimer_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(disclaimer_frame, text="版权与法律免责声明", 
                              font=("SF Pro Display", 16, "bold"))
        title_label.pack(pady=(0, 15))
        
        # 免责声明文本
        text_frame = ttk.Frame(disclaimer_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        disclaimer_text_widget = tk.Text(text_frame, wrap=tk.WORD, 
                                       font=("SF Pro Display", 11),
                                       padx=10, pady=10,
                                       height=15, width=60)
        disclaimer_text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame, command=disclaimer_text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        disclaimer_text_widget.configure(yscrollcommand=scrollbar.set)
        disclaimer_text_widget.insert('1.0', disclaimer_text)
        disclaimer_text_widget.configure(state='disabled')
        
        # 按钮区域
        button_frame = ttk.Frame(disclaimer_frame)
        button_frame.pack(pady=15)
        
        agree_button = ttk.Button(button_frame, text="我同意", width=15,
                                command=disclaimer_window.destroy)
        agree_button.pack(side=tk.LEFT, padx=5)
        
        disagree_button = ttk.Button(button_frame, text="不同意", width=15,
                                   command=lambda: self._exit_app(disclaimer_window))
        disagree_button.pack(side=tk.LEFT, padx=5)
        
        # 阻塞直到用户响应
        self.window.wait_window(disclaimer_window)
    
    def _exit_app(self, window):
        """退出应用程序"""
        window.destroy()
        self.window.destroy()
        sys.exit(0)

    def create_widgets(self):
        """创建主要UI组件"""
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 标题和图标
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_label = ttk.Label(header_frame, text="YouTube 视频下载器", 
                             font=("SF Pro Display", 18, "bold"))
        title_label.pack(side=tk.LEFT)
        
        # URL输入区域
        url_frame = ttk.LabelFrame(main_frame, text="视频地址", padding="10")
        url_frame.pack(fill=tk.X, pady=5)
        
        url_input_frame = ttk.Frame(url_frame)
        url_input_frame.pack(fill=tk.X)
        
        self.url_entry = ttk.Entry(url_input_frame, width=70, font=("SF Pro Display", 11))
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        paste_btn = ttk.Button(url_input_frame, text="粘贴", width=8,
                             command=self.paste_from_clipboard)
        paste_btn.pack(side=tk.LEFT, padx=2)
        
        clear_btn = ttk.Button(url_input_frame, text="清空", width=8,
                             command=lambda: self.url_entry.delete(0, tk.END))
        clear_btn.pack(side=tk.LEFT, padx=2)
        
        # 历史记录下拉菜单
        history_frame = ttk.Frame(url_frame)
        history_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Label(history_frame, text="历史记录:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.history_var = tk.StringVar()
        self.history_combo = ttk.Combobox(history_frame, 
                                        textvariable=self.history_var,
                                        state='readonly',
                                        width=70)
        self.history_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.history_combo.bind("<<ComboboxSelected>>", self.load_from_history)
        
        # 下载选项区域
        options_frame = ttk.LabelFrame(main_frame, text="下载选项", padding="10")
        options_frame.pack(fill=tk.X, pady=5)
        
        # 左侧：类型选择
        left_options = ttk.Frame(options_frame)
        left_options.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 下载类型单选按钮
        type_frame = ttk.Frame(left_options)
        type_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(type_frame, text="下载类型:").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(type_frame, text="视频", 
                       variable=self.download_type, 
                       value="video",
                       command=self.update_format_options).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(type_frame, text="仅音频", 
                       variable=self.download_type, 
                       value="audio",
                       command=self.update_format_options).pack(side=tk.LEFT, padx=5)
        
        # 格式选择
        format_frame = ttk.Frame(left_options)
        format_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(format_frame, text="文件格式:").pack(side=tk.LEFT, padx=(0, 10))
        self.format_combo = ttk.Combobox(format_frame, 
                                       textvariable=self.video_format,
                                       values=["mp4", "webm"],
                                       state='readonly', width=10)
        self.format_combo.pack(side=tk.LEFT, padx=5)
        
        # 质量选择
        quality_frame = ttk.Frame(left_options)
        quality_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(quality_frame, text="视频质量:").pack(side=tk.LEFT, padx=(0, 10))
        self.quality_var = tk.StringVar()
        self.quality_combo = ttk.Combobox(quality_frame,
                                        textvariable=self.quality_var,
                                        state='readonly',
                                        width=10)
        self.quality_combo.pack(side=tk.LEFT, padx=5)
        
        # 右侧：保存路径选择
        right_options = ttk.Frame(options_frame)
        right_options.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(20, 0))
        
        save_frame = ttk.Frame(right_options)
        save_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(save_frame, text="保存位置:").pack(side=tk.LEFT, padx=(0, 5))
        self.path_var = tk.StringVar(value=self.save_path)
        path_entry = ttk.Entry(save_frame, textvariable=self.path_var, width=30)
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        browse_btn = ttk.Button(save_frame, text="浏览", 
                              command=self.browse_save_path, width=8)
        browse_btn.pack(side=tk.LEFT)
        
        # 按钮区域
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        self.check_btn = ttk.Button(btn_frame, text="检查视频", 
                                  command=self.check_video, width=15)
        self.check_btn.pack(side=tk.LEFT, padx=5)
        
        self.download_btn = ttk.Button(btn_frame, text="开始下载",
                                     command=self.start_download,
                                     state='disabled', width=15)
        self.download_btn.pack(side=tk.LEFT, padx=5)
        
        self.cancel_btn = ttk.Button(btn_frame, text="取消下载",
                                   command=self.cancel_download,
                                   state='disabled', width=15)
        self.cancel_btn.pack(side=tk.LEFT, padx=5)
        
        open_folder_btn = ttk.Button(btn_frame, text="打开下载文件夹",
                                   command=self.open_download_folder, width=15)
        open_folder_btn.pack(side=tk.RIGHT, padx=5)
        
        # 视频信息区域
        info_frame = ttk.LabelFrame(main_frame, text="视频信息", padding="10")
        info_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 左侧显示缩略图
        thumbnail_frame = ttk.Frame(info_frame, width=320, height=180)
        thumbnail_frame.pack(side=tk.LEFT, padx=(0, 10), pady=5)
        thumbnail_frame.pack_propagate(False)
        
        self.thumbnail_label = ttk.Label(thumbnail_frame, background="#e0e0e0")
        self.thumbnail_label.pack(fill=tk.BOTH, expand=True)
        
        # 右侧显示视频信息
        info_text_frame = ttk.Frame(info_frame)
        info_text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.info_text = tk.Text(info_text_frame, height=12, wrap=tk.WORD, 
                               font=("SF Pro Display", 11))
        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        info_scrollbar = ttk.Scrollbar(info_text_frame, command=self.info_text.yview)
        info_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.info_text.configure(yscrollcommand=info_scrollbar.set)
        
        # 进度显示区域
        progress_frame = ttk.LabelFrame(main_frame, text="下载进度", padding="10")
        progress_frame.pack(fill=tk.X, pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame,
                                          variable=self.progress_var,
                                          maximum=100, length=600)
        self.progress_bar.pack(fill=tk.X, padx=5, pady=5)
        
        self.status_label = ttk.Label(progress_frame, text="等待中...", 
                                    font=("SF Pro Display", 10))
        self.status_label.pack(padx=5, pady=5)
        
        # 底部信息
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill=tk.X, pady=(10, 0))
        
        # 左侧版本信息和制作者信息
        info_frame = ttk.Frame(footer_frame)
        info_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        version_label = ttk.Label(info_frame, text="版本: 2.0.0", 
                                font=("SF Pro Display", 9))
        version_label.pack(side=tk.TOP, anchor=tk.W)
        
        author_label = ttk.Label(info_frame, text="制作者: 朱富贵", 
                               font=("SF Pro Display", 9))
        author_label.pack(side=tk.TOP, anchor=tk.W)
        
        # 右侧帮助按钮
        help_btn = ttk.Button(footer_frame, text="帮助", width=8,
                            command=self.show_help)
        help_btn.pack(side=tk.RIGHT, padx=5)
        
        # 公众号信息区域
        qrcode_frame = ttk.LabelFrame(main_frame, text="关注公众号，了解更多信息", padding="10")
        qrcode_frame.pack(fill=tk.X, pady=5)
        
        # 创建水平布局
        qrcode_content = ttk.Frame(qrcode_frame)
        qrcode_content.pack(fill=tk.X, padx=5, pady=5)
        
        # 公众号二维码图片（使用占位图）
        try:
            # 尝试加载外部二维码图片
            qrcode_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "qrcode.png")
            if os.path.exists(qrcode_path):
                img = Image.open(qrcode_path)
                img = img.resize((100, 100), Image.LANCZOS)
                qrcode_photo = ImageTk.PhotoImage(img)
                
                qrcode_label = ttk.Label(qrcode_content)
                qrcode_label.pack(side=tk.LEFT, padx=(0, 10))
                qrcode_label.configure(image=qrcode_photo)
                qrcode_label.image = qrcode_photo
            else:
                # 如果没有外部图片，创建一个占位标签
                placeholder = ttk.Label(qrcode_content, text="添加qrcode.png文件\n显示公众号二维码", 
                                     font=("SF Pro Display", 9), 
                                     background="#e0e0e0",
                                     width=15, anchor=tk.CENTER)
                placeholder.pack(side=tk.LEFT, padx=(0, 10))
        except Exception as e:
            print(f"加载二维码图片错误: {str(e)}")
            
        # 公众号描述文本
        desc_text = """
关注我的公众号，获取更多实用工具和教程！

• 最新软件更新和使用技巧
• YouTube视频下载专业指南
• 学习编程和实用工具开发
• 解答您的技术问题
        """
        
        desc_label = ttk.Label(qrcode_content, text=desc_text, 
                             font=("SF Pro Display", 10),
                             wraplength=400, justify=tk.LEFT)
        desc_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 初始界面状态设置
        self.update_format_options()

    def paste_from_clipboard(self):
        """从剪贴板粘贴文本"""
        try:
            text = self.window.clipboard_get()
            if text and ("youtube.com" in text or "youtu.be" in text):
                self.url_entry.delete(0, tk.END)
                self.url_entry.insert(0, text)
        except:
            pass

    def browse_save_path(self):
        """浏览并选择保存路径"""
        directory = filedialog.askdirectory(initialdir=self.save_path)
        if directory:
            self.save_path = directory
            self.path_var.set(directory)

    def update_format_options(self):
        """更新格式选项"""
        if self.download_type.get() == "audio":
            self.format_combo.set("mp3")
            self.format_combo['values'] = ["mp3", "m4a", "wav"]
        else:
            self.format_combo.set("mp4")
            self.format_combo['values'] = ["mp4", "webm"]
            
    def check_video(self):
        """检查视频并获取信息"""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("错误", "请输入视频地址")
            return
        
        # 标准化YouTube链接
        url = self.normalize_youtube_url(url)
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, url)
        
        self.check_btn.config(state='disabled')
        self.status_label.config(text="正在获取视频信息...")
        self.info_text.delete('1.0', tk.END)
        self.info_text.insert('1.0', "正在获取视频信息，请稍候...\n")
        
        # 清除缩略图显示
        self.thumbnail_label.configure(image='')
        self.thumbnail_data = None
        
        threading.Thread(target=self._check_video_thread, args=(url,), daemon=True).start()
        
    def normalize_youtube_url(self, url):
        """标准化YouTube URL"""
        # 处理移动版URL
        url = url.replace("m.youtube.com", "www.youtube.com")
        
        # 处理youtu.be短链接
        if "youtu.be" in url:
            video_id = url.split("/")[-1].split("?")[0]
            url = f"https://www.youtube.com/watch?v={video_id}"
            
        return url
        
    def _check_video_thread(self, url):
        """视频信息获取线程"""
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # 获取可用格式
                formats = info.get('formats', [])
                available_formats = []
                
                if self.download_type.get() == "audio":
                    # 音频格式过滤
                    for f in formats:
                        if f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                            available_formats.append({
                                'format_id': f['format_id'],
                                'ext': f.get('ext', ''),
                                'abr': f.get('abr', 0),
                                'filesize': f.get('filesize', 0)
                            })
                else:
                    # 视频格式过滤
                    for f in formats:
                        if f.get('height') and f.get('vcodec') != 'none':
                            available_formats.append({
                                'format_id': f['format_id'],
                                'ext': f.get('ext', ''),
                                'height': f.get('height', 0),
                                'filesize': f.get('filesize', 0)
                            })
                
                # 获取缩略图
                thumbnail_url = info.get('thumbnail')
                if thumbnail_url:
                    try:
                        response = requests.get(thumbnail_url)
                        if response.status_code == 200:
                            self.thumbnail_data = response.content
                    except:
                        pass
                
                self.format_info = available_formats
                self.window.after(0, self._update_video_info, info, available_formats)
                
        except Exception as e:
            self.window.after(0, self._show_error, str(e))
            
    def _update_video_info(self, info, formats):
        """更新视频信息显示"""
        # 更新质量选项
        quality_options = []
        if self.download_type.get() == "audio":
            quality_options = [f"{f['abr']}kbps" for f in formats if f['abr']]
        else:
            quality_options = [f"{f['height']}p" for f in formats if f['height']]
        
        self.quality_combo['values'] = sorted(set(quality_options), reverse=True)
        if quality_options:
            self.quality_var.set(quality_options[0])
        
        # 更新视频信息显示
        duration = info.get('duration', 0)
        duration_str = time.strftime('%H:%M:%S', time.gmtime(duration))
        upload_date = info.get('upload_date', '')
        if upload_date and len(upload_date) == 8:
            upload_date = f"{upload_date[0:4]}-{upload_date[4:6]}-{upload_date[6:8]}"
        
        info_text = (
            f"标题: {info.get('title', 'Unknown')}\n"
            f"时长: {duration_str}\n"
            f"上传者: {info.get('uploader', 'Unknown')}\n"
            f"上传日期: {upload_date}\n"
            f"观看次数: {format(info.get('view_count', 0), ',')}\n"
            f"点赞数: {format(info.get('like_count', 0), ',')}\n\n"
            f"简介: {info.get('description', '无简介')[:300]}"
            f"{'...' if info.get('description', '') and len(info.get('description', '')) > 300 else ''}\n"
        )
        
        self.info_text.delete('1.0', tk.END)
        self.info_text.insert('1.0', info_text)
        
        # 显示缩略图
        if self.thumbnail_data:
            try:
                img = Image.open(io.BytesIO(self.thumbnail_data))
                img = img.resize((320, 180), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.thumbnail_label.configure(image=photo)
                self.thumbnail_label.image = photo
            except Exception as e:
                print(f"缩略图显示错误: {str(e)}")
        
        # 添加到历史记录
        self.add_to_history(info.get('title', 'Unknown'), self.url_entry.get())
        
        self.download_btn.config(state='normal')
        self.check_btn.config(state='normal')
        self.status_label.config(text="准备下载")
    
    def add_to_history(self, title, url):
        """添加到历史记录"""
        for i, (t, u) in enumerate(self.history):
            if u == url:
                self.history.pop(i)
                break
                
        self.history.insert(0, (title, url))
        if len(self.history) > self.max_history:
            self.history = self.history[:self.max_history]
            
        self.update_history_dropdown()
        self.save_history()
    
    def update_history_dropdown(self):
        """更新历史记录下拉菜单"""
        self.history_combo['values'] = [f"{t} - {u}" for t, u in self.history]
    
    def load_from_history(self, event):
        """从历史记录加载URL"""
        selection = self.history_combo.current()
        if selection >= 0 and selection < len(self.history):
            _, url = self.history[selection]
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, url)
    
    def save_history(self):
        """保存历史记录"""
        try:
            history_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                      "download_history.txt")
            with open(history_file, "w", encoding="utf-8") as f:
                for title, url in self.history:
                    f.write(f"{title}\t{url}\n")
        except:
            pass
    
    def load_history(self):
        """加载历史记录"""
        try:
            history_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                      "download_history.txt")
            if os.path.exists(history_file):
                with open(history_file, "r", encoding="utf-8") as f:
                    for line in f:
                        parts = line.strip().split("\t")
                        if len(parts) == 2:
                            self.history.append((parts[0], parts[1]))
                self.update_history_dropdown()
        except:
            pass
            
    def start_download(self):
        """开始下载"""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("错误", "请输入视频地址")
            return
            
        download_type = self.download_type.get()
        selected_format = self.format_combo.get()
        selected_quality = self.quality_var.get()
        
        # 验证保存路径
        save_path = self.path_var.get()
        if not os.path.exists(save_path):
            try:
                os.makedirs(save_path)
            except:
                messagebox.showerror("错误", "保存路径无效或无权限创建文件夹")
                return
        
        self.save_path = save_path
        
        # 设置下载选项
        ydl_opts = {
            'format': self._get_format_string(download_type, selected_quality),
            'outtmpl': os.path.join(self.save_path, '%(title)s.%(ext)s'),
            'progress_hooks': [self.download_progress_hook],
        }
        
        if download_type == "audio":
            ydl_opts.update({
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': selected_format,
                    'preferredquality': '192',
                }]
            })
        elif download_type == "video" and selected_format == "mp4":
            ydl_opts.update({
                'merge_output_format': 'mp4',
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }]
            })
        
        self.download_btn.config(state='disabled')
        self.check_btn.config(state='disabled')
        self.cancel_btn.config(state='normal')
        self.progress_var.set(0)
        
        self.current_download = threading.Thread(
            target=self._download_thread, 
            args=(url, ydl_opts), 
            daemon=True
        )
        self.current_download.start()
        
    def _get_format_string(self, download_type, quality):
        """获取格式字符串"""
        if download_type == "audio":
            return "bestaudio/best"
        else:
            try:
                height = int(quality.replace('p', ''))
                selected_format = self.format_combo.get()
                return f"bestvideo[height<={height}][ext={selected_format}]+bestaudio/best"
            except:
                return "bestvideo+bestaudio/best"
            
    def _download_thread(self, url, opts):
        """下载处理线程"""
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
        except Exception as e:
            self.window.after(0, self._show_error, str(e))
        finally:
            self.window.after(0, self._reset_buttons)
            
    def download_progress_hook(self, d):
        """下载进度回调"""
        if d['status'] == 'downloading':
            try:
                total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
                downloaded = d.get('downloaded_bytes', 0)
                
                if total > 0:
                    progress = (downloaded / total) * 100
                    speed = d.get('speed', 0)
                    eta = d.get('eta', 0)
                    
                    self.window.after(0, self._update_progress, progress, speed, eta)
                    
            except Exception as e:
                print(f"Progress update error: {str(e)}")
                
        elif d['status'] == 'finished':
            self.window.after(0, self._download_complete)
            
    def _update_progress(self, progress, speed, eta):
        """更新进度显示"""
        self.progress_var.set(progress)
        
        speed_str = self._format_speed(speed)
        eta_str = self._format_time(eta)
        
        status_text = f"下载进度: {progress:.1f}% | 速度: {speed_str} | 剩余时间: {eta_str}"
        self.status_label.config(text=status_text)
        
    def _download_complete(self):
        """下载完成处理"""
        # 显示版权提醒
        self.show_copyright_reminder()
        self.status_label.config(text="下载完成")
        self._reset_buttons()
        
    def show_copyright_reminder(self):
        """显示下载后的版权提醒"""
        reminder_text = """
您已成功下载内容，请注意：

1. 下载内容的版权归原作者或版权所有者所有
2. 请仅将下载内容用于个人学习和研究目的
3. 请勿传播、分享或用于商业用途
4. 尊重原创，支持正版

感谢您的理解与合作！
        """
        
        messagebox.showinfo("下载完成 - 版权提醒", reminder_text)
        
    def _show_error(self, message):
        """显示错误信息"""
        messagebox.showerror("错误", message)
        self.status_label.config(text="发生错误")
        self._reset_buttons()
        
    def _reset_buttons(self):
        """重置按钮状态"""
        self.download_btn.config(state='normal')
        self.check_btn.config(state='normal')
        self.cancel_btn.config(state='disabled')
        
    def cancel_download(self):
        """取消下载"""
        if messagebox.askyesno("确认", "确定要取消当前下载吗？"):
            # 由于yt-dlp没有直接的取消方法，通过修改状态并在下一次检查时退出
            self.status_label.config(text="正在取消下载...")
            # Python无法直接终止线程，使用系统调用退出
            os._exit(0)  # 强制终止整个程序
        
    def _format_speed(self, bytes_per_second):
        """格式化速度显示"""
        if bytes_per_second <= 0:
            return "0 B/s"
        units = ['B/s', 'KB/s', 'MB/s', 'GB/s']
        unit_index = 0
        while bytes_per_second >= 1024 and unit_index < len(units) - 1:
            bytes_per_second /= 1024
            unit_index += 1
        return f"{bytes_per_second:.1f} {units[unit_index]}"
        
    def _format_time(self, seconds):
        """格式化时间显示"""
        if not seconds:
            return "计算中..."
        m, s = divmod(int(seconds), 60)
        h, m = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"
    
    def open_download_folder(self):
        """打开下载文件夹"""
        path = self.path_var.get()
        if os.path.exists(path):
            if os.name == 'nt':  # Windows
                os.startfile(path)
            elif os.name == 'posix':  # macOS 和 Linux
                if 'darwin' in os.sys.platform:  # macOS
                    os.system(f'open "{path}"')
                else:  # Linux
                    os.system(f'xdg-open "{path}"')
    
    def show_help(self):
        """显示帮助信息"""
        help_text = """
使用说明:

1. 输入YouTube视频地址（支持视频、播放列表）
2. 点击"检查视频"获取视频信息
3. 选择下载类型（视频或音频）和格式
4. 选择保存位置
5. 点击"开始下载"

支持的YouTube链接格式:
- 标准视频链接: https://www.youtube.com/watch?v=xxxx
- 短链接: https://youtu.be/xxxx
- 播放列表: https://www.youtube.com/playlist?list=xxxx

常见问题:
- 如果下载过程中断，可能是网络问题，请重试
- 部分高清视频可能需要较长下载时间
- 如果遇到格式问题，尝试选择不同格式

技术支持: yt-dlp (https://github.com/yt-dlp/yt-dlp)
"""
        help_window = tk.Toplevel(self.window)
        help_window.title("使用帮助")
        help_window.geometry("500x400")
        help_window.transient(self.window)
        help_window.resizable(False, False)
        
        help_text_widget = tk.Text(help_window, wrap=tk.WORD, 
                                 font=("SF Pro Display", 11),
                                 padx=10, pady=10)
        help_text_widget.pack(fill=tk.BOTH, expand=True)
        help_text_widget.insert('1.0', help_text)
        help_text_widget.config(state='disabled')
        
        ok_button = ttk.Button(help_window, text="确定", 
                             command=help_window.destroy)
        ok_button.pack(pady=10)
        
    def run(self):
        """运行程序"""
        self.window.mainloop()

if __name__ == "__main__":
    app = YouTubeDownloader()
    app.run()