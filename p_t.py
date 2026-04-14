from PIL import Image
import os


def compress_image(input_path, output_path, max_size_kb=250):
    """
    压缩图片到指定大小以下

    Args:
        input_path: 输入图片路径
        output_path: 输出图片路径
        max_size_kb: 最大文件大小（KB），默认250KB（留有余量）
    """
    max_size_bytes = max_size_kb * 1024

    # 打开图片
    img = Image.open(input_path)
    print(f"原始尺寸: {img.size}")
    print(f"原始大小: {os.path.getsize(input_path) / 1024:.2f} KB")

    # 如果已经是 PNG 且小于目标大小，直接复制
    if os.path.getsize(input_path) <= max_size_bytes:
        print("图片已经小于目标大小，无需压缩")
        return

    # 尝试不同的质量和尺寸组合
    quality = 95
    scale = 1.0

    while True:
        # 计算新尺寸
        if scale < 1.0:
            new_size = (int(img.width * scale), int(img.height * scale))
            resized_img = img.resize(new_size, Image.LANCZOS)
        else:
            resized_img = img

        # 保存为 PNG（优化压缩）
        resized_img.save(output_path, 'PNG', optimize=True)

        file_size = os.path.getsize(output_path)
        print(f"尝试 - 缩放比例: {scale:.2f}, 质量: {quality}, 大小: {file_size / 1024:.2f} KB")

        # 检查是否满足要求
        if file_size <= max_size_bytes:
            print(f"\n✅ 压缩成功！")
            print(f"最终尺寸: {resized_img.size}")
            print(f"最终大小: {file_size / 1024:.2f} KB")
            break

        # 调整参数继续尝试
        if scale > 0.5:
            scale -= 0.1
        else:
            # 如果缩小到 50% 还不够，转换为 JPEG
            print("\nPNG 压缩无法满足要求，尝试转换为 JPEG...")
            jpg_path = output_path.replace('.png', '.jpg')
            resized_img.convert('RGB').save(jpg_path, 'JPEG', quality=quality, optimize=True)
            jpg_size = os.path.getsize(jpg_path)
            print(f"JPEG 大小: {jpg_size / 1024:.2f} KB")

            if jpg_size <= max_size_bytes:
                print(f"\n✅ 使用 JPEG 格式压缩成功！")
                print(f"输出文件: {jpg_path}")
            else:
                quality -= 10
                if quality < 30:
                    print("\n❌ 无法压缩到目标大小，请手动处理")
                    break

            break


if __name__ == '__main__':
    input_file = 'icons/app_icon_fixed.png'
    output_file = 'icons/app_icon_compressed.png'

    if not os.path.exists(input_file):
        print(f"错误: 找不到文件 {input_file}")
        exit(1)

    compress_image(input_file, output_file, max_size_kb=250)
