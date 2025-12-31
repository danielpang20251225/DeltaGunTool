# make_icon.py - 生成合法 Delta 风格图标
from PIL import Image, ImageDraw

# 创建 256x256 透明画布
img = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# 画一个蓝色三角形（Delta 标志）
draw.polygon([(128, 40), (40, 216), (216, 216)], fill=(0, 100, 255))

# 可选：加白色边框
draw.line([(128, 40), (40, 216), (216, 216), (128, 40)], fill="white", width=8)

# 保存为多尺寸 ICO（16, 32, 48, 256）
img.save("delta.ico", format="ICO", sizes=[(16,16), (32,32), (48,48), (256,256)])
print("✅ delta.ico 已生成！路径: delta.ico")