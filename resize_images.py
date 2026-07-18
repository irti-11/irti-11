from PIL import Image, ImageFilter

files = ["stylebazaar", "mrcone", "32smiles"]

TARGET_W = 800
TARGET_H = 440   # 1.818:1 aspect — matches typical wide screenshots better

for name in files:
    im = Image.open(f"{name}_original.jpg").convert("RGB")
    w, h = im.size
    src_ratio = w / h
    target_ratio = TARGET_W / TARGET_H

    # Center-crop to target aspect ratio BEFORE resizing (avoids losing side content unevenly)
    if src_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        im = im.crop((left, 0, left + new_w, h))
    else:
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        im = im.crop((0, top, w, top + new_h))

    im = im.resize((TARGET_W, TARGET_H), Image.LANCZOS)
    im = im.filter(ImageFilter.SHARPEN)
    im.save(f"{name}.jpg", "JPEG", quality=92, optimize=True)
    print(f"{name}.jpg done")