import os
import time

import tinify
from PIL import Image

# 请将以下的 API key 更换为您自己的 API key
tinify.key = ""

# 定义各种尺寸的 mipmap icon 尺寸
mipmap_sizes = {
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192
}

def resize_icon(image_path, size, output_path):
    """
    调整图片大小并保存到输出路径
    """
    with Image.open(image_path) as img:
        img = img.resize((size, size), Image.LANCZOS)
        img.save(output_path)

def compress_image(input_path, output_path):
    """
    使用 Tinify API 压缩图片
    """
    source = tinify.from_file(input_path)
    source.to_file(output_path)
    time.sleep(0.2)


def replace_special_images(output_dir, image_fore, image_back):
    """
    压缩并替换 mipmap-xhdpi 目录下的两张特殊图片
    """
    xhdpi_dir = os.path.join(output_dir, "mipmap-xhdpi")
    output_path_fore = os.path.join(xhdpi_dir, "launcher_icon_foreground.png")
    compress_image(image_fore, output_path_fore)
    output_path_back = os.path.join(xhdpi_dir, "launcher_icon_background.png")
    compress_image(image_back, output_path_back)

def generate_mipmap_icons(image_path, output_dir, base_name,image_fore,image_back):
    """
    生成各种尺寸的 mipmap icon
    """
    with Image.open(image_path) as img:
        for folder_name, size in mipmap_sizes.items():
            output_name = base_name + ".png"
            output_path = os.path.join(output_dir, folder_name, output_name)
            if not os.path.exists(os.path.dirname(output_path)):
                os.makedirs(os.path.dirname(output_path))
            resize_icon(image_path, size, output_path)
            compress_image(output_path, output_path)
    replace_special_images(output_dir, image_fore, image_back)


if __name__ == "__main__":
    # icon目录
    image_path = "/Users/android.png"
    # 前景icon目录
    image_foreground = "/Users/icon1.png"
    # 后景icon目录
    image_background = "/Users/icon2.png"
    output_dir = "/Users/demo_android/app/src/tj/res"
    base_name = "launcher_icon"
    generate_mipmap_icons(image_path, output_dir, base_name, image_foreground, image_background)
