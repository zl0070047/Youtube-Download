import qrcode
from PIL import Image, ImageDraw, ImageFont

def create_sample_qrcode():
    """创建一个示例二维码图片"""
    # 创建二维码（可以替换为您的公众号链接）
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data('https://example.com/公众号')
    qr.make(fit=True)
    
    # 创建白底
    img = qr.make_image(fill_color="black", back_color="white")
    
    # 调整大小
    img = img.resize((300, 300))
    
    # 保存图片
    img.save("qrcode.png")
    print("已生成示例二维码 qrcode.png")
    print("请替换为您的实际公众号二维码图片")

if __name__ == "__main__":
    try:
        create_sample_qrcode()
    except ImportError:
        print("请先安装qrcode库: pip install qrcode[pil]")
        print("然后再运行此脚本生成示例二维码") 