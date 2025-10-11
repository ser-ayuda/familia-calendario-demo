from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import math

ASSETS = Path(__file__).resolve().parent.parent / 'assets'
SS_DIR = Path(__file__).resolve().parent.parent / 'demo_screenshots'

def load_screenshots(max_imgs=3):
    imgs = []
    if SS_DIR.exists():
        for p in sorted(SS_DIR.iterdir(), key=lambda x: x.stat().st_mtime)[:max_imgs]:
            try:
                imgs.append(Image.open(p).convert('RGBA'))
            except Exception:
                continue
    return imgs

def make_collage(target_w, target_h, screenshots):
    canvas = Image.new('RGBA', (target_w, target_h), (255,255,255,255))
    n = len(screenshots)
    if n == 0:
        return canvas
    # Layout: if 1 image -> full; if 2 -> split; if 3+ -> tiled
    pad = 12
    if n == 1:
        img = screenshots[0].copy()
        img.thumbnail((target_w - pad*2, target_h - pad*2), Image.LANCZOS)
        x = (target_w - img.width)//2
        y = (target_h - img.height)//2
        canvas.paste(img, (x,y), img)
    elif n == 2:
        w = (target_w - pad*3)//2
        h = target_h - pad*2
        for i,img in enumerate(screenshots[:2]):
            tmp = img.copy()
            tmp.thumbnail((w,h), Image.LANCZOS)
            x = pad + i*(w+pad) + (w - tmp.width)//2
            y = pad + (h - tmp.height)//2
            canvas.paste(tmp, (x,y), tmp)
    else:
        # 3 images: left big, two stacked on right
        left_w = int(target_w * 0.6) - pad*2
        right_w = target_w - left_w - pad*3
        left_h = target_h - pad*2
        tmp = screenshots[0].copy(); tmp.thumbnail((left_w, left_h), Image.LANCZOS)
        x = pad; y = pad + (left_h - tmp.height)//2
        canvas.paste(tmp, (x,y), tmp)
        right_h = (target_h - pad*3)//2
        for i in range(2):
            tmp = screenshots[i+1].copy(); tmp.thumbnail((right_w, right_h), Image.LANCZOS)
            x = pad*2 + left_w
            y = pad + i*(right_h+pad) + (right_h - tmp.height)//2
            canvas.paste(tmp, (x,y), tmp)
    return canvas

def overlay_text(img, title='Familia Calendario', subtitle='Proyecto personal', font_path=None):
    draw = ImageDraw.Draw(img)
    w,h = img.size
    # semi-transparent gradient at bottom
    grad_h = int(h * 0.25)
    grad = Image.new('L', (1, grad_h))
    for i in range(grad_h):
        grad.putpixel((0,i), int(255 * (i/grad_h)))
    alpha = grad.resize((w, grad_h))
    black = Image.new('RGBA', (w, grad_h), (0,0,0,180))
    black.putalpha(alpha)
    img.paste(black, (0, h - grad_h), black)

    # fonts
    try:
        if font_path and Path(font_path).exists():
            title_font = ImageFont.truetype(font_path, size=int(h*0.06))
            sub_font = ImageFont.truetype(font_path, size=int(h*0.035))
        else:
            title_font = ImageFont.truetype(str(Path(__file__).resolve().parent.parent / 'assets' / 'DejaVuSans.ttf'), size=int(h*0.06))
            sub_font = ImageFont.truetype(str(Path(__file__).resolve().parent.parent / 'assets' / 'DejaVuSans.ttf'), size=int(h*0.035))
    except Exception:
        title_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()

    padding = int(h*0.03)
    tx = padding
    ty = h - grad_h + padding//2
    draw.text((tx, ty), title, font=title_font, fill=(255,255,255,255))
    # measure title height
    try:
        title_h = title_font.getbbox(title)[3] - title_font.getbbox(title)[1]
    except Exception:
        try:
            title_w, title_h = draw.textsize(title, font=title_font)
        except Exception:
            title_h = int(h*0.06)
    draw.text((tx, ty + title_h + 6), subtitle, font=sub_font, fill=(230,230,230,255))
    return img

def save_variants(collage, out_base):
    # landscape 1200x627
    land = collage.resize((1200,627), Image.LANCZOS)
    land = overlay_text(land)
    land.convert('RGB').save(out_base / 'experience_landscape.png', format='PNG', optimize=True)
    # square 400x400
    sq = collage.resize((1200,1200), Image.LANCZOS)
    sq_thumb = sq.resize((400,400), Image.LANCZOS)
    sq_thumb = overlay_text(sq_thumb)
    sq_thumb.convert('RGB').save(out_base / 'experience_square.png', format='PNG', optimize=True)
    # small thumb 300x300
    thumb = sq.resize((300,300), Image.LANCZOS)
    thumb = overlay_text(thumb)
    thumb.convert('RGB').save(out_base / 'experience_thumb.png', format='PNG', optimize=True)

def main():
    screenshots = load_screenshots(3)
    collage = make_collage(1600, 900, screenshots)
    if collage.getbbox() is None:
        # empty, generate blank background
        collage = Image.new('RGBA', (1600,900), (60,120,200,255))
    save_variants(collage, ASSETS)
    print('Saved experience images in', ASSETS)

if __name__ == '__main__':
    main()
