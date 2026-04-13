from PIL import Image
import os

# 项目根目录
base_dir = r"D:\project\create_app"


def analyze_original_image_text_precise(img_path, description=""):
    """精确分析原始图标图片中的文字颜色"""
    if not os.path.exists(img_path):
        print(f"文件不存在: {img_path}")
        return

    img = Image.open(img_path).convert('RGB')
    w, h = img.size

    print(f"\n{'=' * 70}")
    print(f"分析: {description}")
    print(f"文件: {os.path.basename(img_path)}")
    print(f"尺寸: {w}x{h}")
    print(f"{'=' * 70}")

    gray_pixels = []
    
    if "我的资产负债" in img_path:
        # 第一页：我的资产负债.png
        # 根据 HTML 坐标，但缩小范围只扫描白色覆盖区域内的文字
        # 总负债白色覆盖区域: top: 35.5%, left: 56.0%, width: 37.9%, height: 10.8%
        # 文字位置: top: 34.5%, left: 56.0%
        print("\n📍 扫描总负债文字 (精确区域)...")
        for y in range(int(h * 0.35), int(h * 0.38)):
            for x in range(int(w * 0.57), int(w * 0.85)):
                pixel = img.getpixel((x, y))
                # 只采集中等灰度像素 (50-200)，排除纯黑、纯白和深色背景
                if 50 <= pixel[0] <= 200 and 50 <= pixel[1] <= 200 and 50 <= pixel[2] <= 200:
                    # 确保是灰色（RGB 三个值接近）
                    if abs(pixel[0] - pixel[1]) < 10 and abs(pixel[1] - pixel[2]) < 10:
                        gray_pixels.append(pixel)
        
        # 贷款金额白色覆盖区域: top: 63.8%, left: 62.8%, width: 22.9%, height: 9.1%
        # 文字位置: top: 63.4%, left: 65.5%
        print("📍 扫描贷款金额文字 (精确区域)...")
        for y in range(int(h * 0.635), int(h * 0.67)):
            for x in range(int(w * 0.64), int(w * 0.82)):
                pixel = img.getpixel((x, y))
                if 50 <= pixel[0] <= 200 and 50 <= pixel[1] <= 200 and 50 <= pixel[2] <= 200:
                    if abs(pixel[0] - pixel[1]) < 10 and abs(pixel[1] - pixel[2]) < 10:
                        gray_pixels.append(pixel)
    
    elif "我的住房贷款" in img_path:
        # 第二页：我的住房贷款.png
        print("\n📍 扫描本金文字...")
        for y in range(int(h * 0.58), int(h * 0.61)):
            for x in range(int(w * 0.24), int(w * 0.42)):
                pixel = img.getpixel((x, y))
                if 50 <= pixel[0] <= 200 and 50 <= pixel[1] <= 200 and 50 <= pixel[2] <= 200:
                    if abs(pixel[0] - pixel[1]) < 10 and abs(pixel[1] - pixel[2]) < 10:
                        gray_pixels.append(pixel)
        
        print("📍 扫描还款金额文字...")
        for y in range(int(h * 0.745), int(h * 0.775)):
            for x in range(int(w * 0.30), int(w * 0.48)):
                pixel = img.getpixel((x, y))
                if 50 <= pixel[0] <= 200 and 50 <= pixel[1] <= 200 and 50 <= pixel[2] <= 200:
                    if abs(pixel[0] - pixel[1]) < 10 and abs(pixel[1] - pixel[2]) < 10:
                        gray_pixels.append(pixel)
    
    elif "还款计划" in img_path:
        # 第三页：还款计划.png
        print("\n📍 扫描第37期本金、利息、总额文字...")
        # 本金: top: 45.8%, left: 77.6%
        # 利息: top: 50.4%, left: 74.4%
        # 总额: top: 59.6%, left: 74.4%
        scan_regions = [
            (0.458, 0.776, 0.475, 0.85),  # 本金
            (0.504, 0.744, 0.520, 0.85),  # 利息
            (0.596, 0.744, 0.612, 0.85),  # 总额
        ]
        for top, left, bottom, right in scan_regions:
            for y in range(int(h * top), int(h * bottom)):
                for x in range(int(w * left), int(w * right)):
                    pixel = img.getpixel((x, y))
                    if 50 <= pixel[0] <= 200 and 50 <= pixel[1] <= 200 and 50 <= pixel[2] <= 200:
                        if abs(pixel[0] - pixel[1]) < 10 and abs(pixel[1] - pixel[2]) < 10:
                            gray_pixels.append(pixel)
    
    # 统计分析
    if gray_pixels:
        print(f"\n✅ 找到 {len(gray_pixels)} 个有效灰色像素点")
        
        # 统计最常见的颜色值
        color_count = {}
        for p in gray_pixels:
            key = f"#{p[0]:02X}{p[1]:02X}{p[2]:02X}"
            color_count[key] = color_count.get(key, 0) + 1
        
        sorted_colors = sorted(color_count.items(), key=lambda x: x[1], reverse=True)
        
        print("\n🎨 最常见的10种颜色:")
        for i, (color, count) in enumerate(sorted_colors[:10]):
            percentage = count / len(gray_pixels) * 100
            print(f"  {i+1}. {color} - {count}次 ({percentage:.1f}%)")
        
        # 计算平均颜色
        avg_r = sum(p[0] for p in gray_pixels) // len(gray_pixels)
        avg_g = sum(p[1] for p in gray_pixels) // len(gray_pixels)
        avg_b = sum(p[2] for p in gray_pixels) // len(gray_pixels)
        avg_hex = f"#{avg_r:02X}{avg_g:02X}{avg_b:02X}"
        print(f"\n⭐ 平均灰色: RGB({avg_r}, {avg_g}, {avg_b}) = {avg_hex}")
        
        # 中位数
        sorted_r = sorted([p[0] for p in gray_pixels])
        sorted_g = sorted([p[1] for p in gray_pixels])
        sorted_b = sorted([p[2] for p in gray_pixels])
        median_r = sorted_r[len(sorted_r) // 2]
        median_g = sorted_g[len(sorted_g) // 2]
        median_b = sorted_b[len(sorted_b) // 2]
        median_hex = f"#{median_r:02X}{median_g:02X}{median_b:02X}"
        print(f"⭐ 中位灰色: RGB({median_r}, {median_g}, {median_b}) = {median_hex}")
        
        # 推荐：取前5名的加权平均
        if len(sorted_colors) >= 5:
            weighted_r = 0
            weighted_g = 0
            weighted_b = 0
            total_weight = 0
            for color, count in sorted_colors[:5]:
                r = int(color[1:3], 16)
                g = int(color[3:5], 16)
                b = int(color[5:7], 16)
                weighted_r += r * count
                weighted_g += g * count
                weighted_b += b * count
                total_weight += count
            
            rec_r = weighted_r // total_weight
            rec_g = weighted_g // total_weight
            rec_b = weighted_b // total_weight
            rec_hex = f"#{rec_r:02X}{rec_g:02X}{rec_b:02X}"
            print(f"💡 推荐使用: RGB({rec_r}, {rec_g}, {rec_b}) = {rec_hex}")
    else:
        print("\n❌ 未找到有效灰色像素")


# 分析三张原始图标图片
analyze_original_image_text_precise(
    os.path.join(base_dir, "icons", "first_icons", "我的资产负债.png"),
    "第一页 - 我的资产负债.png"
)

analyze_original_image_text_precise(
    os.path.join(base_dir, "icons", "second_icons", "我的住房贷款.png"),
    "第二页 - 我的住房贷款.png"
)

analyze_original_image_text_precise(
    os.path.join(base_dir, "icons", "third_icons", "还款计划.png"),
    "第三页 - 还款计划.png"
)

print("\n\n✅ 分析完成！")
