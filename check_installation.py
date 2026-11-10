#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安装验证脚本
用于检查 YouTube 下载器的所有依赖包是否正确安装
"""

import sys

def check_package(package_name, import_name=None):
    """检查包是否已安装"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"✅ {package_name} - 已安装")
        return True
    except ImportError:
        print(f"❌ {package_name} - 未安装")
        return False

def check_ffmpeg():
    """检查 ffmpeg 是否已安装"""
    try:
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ ffmpeg - 已安装")
            return True
        else:
            print("⚠️  ffmpeg - 未安装 (可选，但推荐)")
            return False
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  ffmpeg - 未安装 (可选，但推荐)")
        return False

def main():
    """主函数"""
    print("🔍 检查 YouTube 下载器依赖包安装状态...")
    print("=" * 50)
    
    # 检查必需的依赖包
    required_packages = [
        ("yt-dlp", "yt_dlp"),
        ("Pillow", "PIL"),
        ("requests", "requests"),
        ("qrcode", "qrcode"),
        ("tkinter", "tkinter")
    ]
    
    all_installed = True
    
    for package_name, import_name in required_packages:
        if not check_package(package_name, import_name):
            all_installed = False
    
    # 检查可选的 ffmpeg
    ffmpeg_installed = check_ffmpeg()
    
    print("=" * 50)
    
    if all_installed:
        print("🎉 所有必需依赖包都已正确安装！")
        if ffmpeg_installed:
            print("🎬 ffmpeg 也已安装，将获得最佳下载体验！")
        else:
            print("💡 提示: 可以运行 'python3 install_ffmpeg.py' 安装 ffmpeg 以获得更好体验")
        print("📝 您现在可以运行以下命令启动程序：")
        print("   python3 \"YouTube download.py\"")
    else:
        print("⚠️  部分依赖包未安装，请运行以下命令安装：")
        print("   pip install -r requirements.txt")
        print("   如果遇到 SSL 证书问题，请使用：")
        print("   pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt")

if __name__ == "__main__":
    main() 