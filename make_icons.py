"""Generate PWA icons (192x192 and 512x512 PNG) for Property Pulse."""
from PIL import Image, ImageDraw
import math, os

def draw_icon(size, maskable=False):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = size / 512  # scale factor

    # ── Gradient background (simulate with horizontal/vertical blend) ──
    bg = Image.new("RGBA", (size, size))
    bd = ImageDraw.Draw(bg)
    c1 = (59, 130, 246)   # #3b82f6
    c2 = (99, 102, 241)   # #6366f1
    for i in range(size):
        t = i / size
        col = tuple(int(c1[j] + (c2[j] - c1[j]) * t) for j in range(3)) + (255,)
        bd.line([(i, 0), (i, size)], fill=col)

    # Rounded-rect mask for background
    corner_r = int(96 * r) if not maskable else 0
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, size - 1, size - 1], radius=corner_r, fill=255)
    bg.putalpha(mask)
    img.paste(bg, mask=bg)

    d = ImageDraw.Draw(img)
    pad = int(size * 0.1) if maskable else 0

    def s(x):
        return int(x * r) + pad

    def rr(x, y, w, h, fill, rad=4):
        d.rounded_rectangle([s(x), s(y), s(x) + int(w * r) - 1, s(y) + int(h * r) - 1],
                             radius=int(rad * r), fill=fill)

    # Main building (white)
    rr(68, 185, 148, 267, "white", rad=8)

    # Roof triangle
    d.polygon([(s(48), s(185)), (s(236), s(185)), (s(142), s(98))],
              fill=(255, 255, 255, 235))

    # Windows — main building
    blue = (59, 130, 246)
    for wy in [215, 272, 329]:
        for wx in [92, 148]:
            rr(wx, wy, 38, 32, blue, rad=4)

    # Door
    rr(112, 398, 44, 54, (37, 99, 235), rad=5)

    # Medium building
    rr(236, 258, 116, 194, (255, 255, 255, 224), rad=8)
    indigo = (99, 102, 241)
    for wy in [284, 330]:
        for wx in [256, 304]:
            rr(wx, wy, 32, 26, indigo, rad=3)

    # Small building
    rr(372, 305, 80, 147, (255, 255, 255, 189), rad=8)
    violet = (129, 140, 248)
    for wy in [328, 372]:
        for wx in [388, 424]:
            rr(wx, wy, 24, 22, violet, rad=3)

    return img


os.makedirs("icons", exist_ok=True)

for size, name, maskable in [
    (192,  "icons/icon-192.png",      False),
    (512,  "icons/icon-512.png",      False),
    (512,  "icons/icon-maskable.png", True),
]:
    img = draw_icon(size, maskable)
    img.save(name, "PNG")
    print(f"  ✓  {name}  ({size}×{size})")

print("Done.")
