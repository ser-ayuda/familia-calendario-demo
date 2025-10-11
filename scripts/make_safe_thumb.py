from PIL import Image
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / 'assets'
SRC_CANDIDATES = [
    ASSETS / 'experience_thumb.png',
    ASSETS / 'experience_square.png',
    ASSETS / 'experience_landscape.png',
    ASSETS / 'social_linkedin_landscape_safe.png',
    ASSETS / 'social_linkedin_landscape.png',
]

def fit_and_pad(img, target_w, target_h, bg=(255,255,255)):
    img_ratio = img.width / img.height
    target_ratio = target_w / target_h
    if img_ratio > target_ratio:
        # fit by width
        new_w = target_w
        new_h = int(target_w / img_ratio)
    else:
        new_h = target_h
        new_w = int(target_h * img_ratio)
    resized = img.resize((new_w, new_h), Image.LANCZOS)
    canvas = Image.new('RGB', (target_w, target_h), bg)
    x = (target_w - new_w)//2
    y = (target_h - new_h)//2
    canvas.paste(resized, (x,y))
    return canvas

def main():
    src = None
    for p in SRC_CANDIDATES:
        if p.exists():
            src = p
            break
    if not src:
        print('No source image found for thumbnail generation')
        return
    img = Image.open(src).convert('RGB')
    thumb = fit_and_pad(img, 300, 300, bg=(255,255,255))
    out = ASSETS / 'experience_thumb_safe.png'
    thumb.save(out, format='PNG', optimize=True)
    print('Saved', out)

if __name__ == '__main__':
    main()
