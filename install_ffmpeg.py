#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ffmpeg 安装脚本
提供多种安装 ffmpeg 的方法
"""

import subprocess
import sys
import os
import platform

def run_command(command, description):
    """运行命令并显示结果"""
    print(f"\n🔧 {description}")
    print(f"执行命令: {command}")
    print("-" * 50)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ 成功!")
            if result.stdout:
                print("输出:", result.stdout)
            return True
        else:
            print("❌ 失败!")
            if result.stderr:
                print("错误:", result.stderr)
            return False
    except Exception as e:
        print(f"❌ 执行出错: {e}")
        return False

def check_ffmpeg():
    """检查 ffmpeg 是否已安装"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ ffmpeg 已安装!")
            print("版本信息:")
            lines = result.stdout.split('\n')
            for line in lines[:3]:  # 只显示前3行
                if line.strip():
                    print(f"  {line}")
            return True
        else:
            return False
    except FileNotFoundError:
        return False

def main():
    """主函数"""
    print("🎬 ffmpeg 安装工具")
    print("=" * 50)
    
    # 检查系统信息
    system = platform.system()
    print(f"操作系统: {system}")
    print(f"Python 版本: {sys.version}")
    
    # 首先检查是否已安装
    if check_ffmpeg():
        print("\n🎉 ffmpeg 已经安装，无需重复安装!")
        return
    
    print("\n❌ ffmpeg 未安装，开始安装...")
    
    if system == "Darwin":  # macOS
        print("\n📋 在 macOS 上安装 ffmpeg")
        print("请选择安装方法:")
        print("1. 使用 Homebrew (推荐)")
        print("2. 使用 conda")
        print("3. 手动下载")
        
        choice = input("\n请选择 (1-3): ").strip()
        
        if choice == "1":
            # 方法1: Homebrew
            print("\n🚀 使用 Homebrew 安装...")
            
            # 检查 Homebrew 是否安装
            if run_command("brew --version", "检查 Homebrew"):
                # 跳过自动更新
                success = run_command(
                    "HOMEBREW_NO_AUTO_UPDATE=1 brew install ffmpeg",
                    "安装 ffmpeg"
                )
                if success:
                    print("\n🎉 ffmpeg 安装成功!")
                else:
                    print("\n⚠️  Homebrew 安装失败，尝试其他方法...")
                    choice = "2"
            else:
                print("\n❌ Homebrew 未安装，请先安装 Homebrew")
                print("安装命令: /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
                return
        
        if choice == "2":
            # 方法2: conda
            print("\n🚀 使用 conda 安装...")
            if run_command("conda --version", "检查 conda"):
                success = run_command("conda install -c conda-forge ffmpeg -y", "安装 ffmpeg")
                if success:
                    print("\n🎉 ffmpeg 安装成功!")
                else:
                    print("\n⚠️  conda 安装失败")
            else:
                print("\n❌ conda 未安装")
        
        if choice == "3":
            # 方法3: 手动下载
            print("\n📥 手动下载安装...")
            print("请访问以下网站下载 ffmpeg:")
            print("1. https://evermeet.cx/ffmpeg/")
            print("2. https://ffmpeg.org/download.html")
            print("\n下载后请将 ffmpeg 添加到系统 PATH 中")
    
    elif system == "Windows":
        print("\n📋 在 Windows 上安装 ffmpeg")
        print("推荐使用 Chocolatey 或手动下载:")
        print("1. 使用 Chocolatey: choco install ffmpeg")
        print("2. 手动下载: https://ffmpeg.org/download.html")
    
    elif system == "Linux":
        print("\n📋 在 Linux 上安装 ffmpeg")
        print("使用包管理器安装:")
        print("Ubuntu/Debian: sudo apt update && sudo apt install ffmpeg")
        print("CentOS/RHEL: sudo yum install ffmpeg")
        print("Arch: sudo pacman -S ffmpeg")
    
    # 最终检查
    print("\n🔍 最终检查...")
    if check_ffmpeg():
        print("\n🎉 ffmpeg 安装成功! 现在可以正常使用 YouTube 下载器了!")
    else:
        print("\n⚠️  ffmpeg 仍未安装成功")
        print("请手动安装 ffmpeg 后重新运行此脚本")

if __name__ == "__main__":
    main() 