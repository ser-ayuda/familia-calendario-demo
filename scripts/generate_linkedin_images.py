from PIL import Image
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / 'assets'
SVG = ASSETS / 'social.svg'
PNG = ASSETS / 'social.png'

def load_image():
    if PNG.exists():
        return Image.open(PNG).convert('RGBA')
    else:
        # fallback: try to rasterize SVG using cairosvg if available
        try:
            import cairosvg
            png_bytes = cairosvg.svg2png(url=str(SVG))
            from io import BytesIO
            return Image.open(BytesIO(png_bytes)).convert('RGBA')
        except Exception as e:
            raise RuntimeError('No social.png and SVG rasterization failed: ' + str(e))

def fit_and_pad(img, target_w, target_h, bg=(255,255,255,0)):
    # Resize preserving aspect ratio and pad to target size
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
    canvas = Image.new('RGBA', (target_w, target_h), bg)
    x = (target_w - new_w)//2
    y = (target_h - new_h)//2
    canvas.paste(resized, (x,y), resized)
    return canvas

def main():
    img = load_image()
    out_land = ASSETS / 'social_linkedin_landscape.png'
    out_port = ASSETS / 'social_linkedin_portrait.png'
    out_land_safe = ASSETS / 'social_linkedin_landscape_safe.png'
    out_square = ASSETS / 'social_linkedin_square.png'
    # Standard sizes
    land = fit_and_pad(img, 1200, 628)
    port = fit_and_pad(img, 1080, 1350)
    # LinkedIn recommended landscape is ~1200x627 (1.91:1). We'll also produce a 'safe' variant
    # where the content is scaled down slightly to leave an inner safe margin so LinkedIn cropping
    # doesn't cut important parts.
    land_safe = fit_and_pad(img, 1200, 627)
    # Create a square variant for feeds that crop to square
    square = fit_and_pad(img, 1200, 1200)

    land.convert('RGB').save(out_land, format='PNG', optimize=True)
    port.convert('RGB').save(out_port, format='PNG', optimize=True)
    # Save safe and square variants
    # To create an inner safe margin, shrink the image by a small percentage and paste on canvas
    def create_safe(canvas_w, canvas_h, shrink_percent=0.94):
        # shrink_percent controls how much of the canvas the image occupies (0-1)
        target_w = int(canvas_w * shrink_percent)
        target_h = int(canvas_h * shrink_percent)
        img_shrunk = fit_and_pad(img, target_w, target_h)
        canvas = Image.new('RGBA', (canvas_w, canvas_h), (255,255,255,0))
        x = (canvas_w - img_shrunk.width)//2
        y = (canvas_h - img_shrunk.height)//2
        canvas.paste(img_shrunk, (x,y), img_shrunk)
        return canvas

    safe_canvas = create_safe(1200, 627, shrink_percent=0.92)
    square_canvas = create_safe(1200, 1200, shrink_percent=0.92)

    land_safe.convert('RGB').save(out_land_safe, format='PNG', optimize=True)
    safe_canvas.convert('RGB').save(out_land_safe, format='PNG', optimize=True)
    square.convert('RGB').save(out_square, format='PNG', optimize=True)
    square_canvas.convert('RGB').save(out_square, format='PNG', optimize=True)
    print('Saved:', out_land, out_port)
    print('Also saved safe and square variants:', out_land_safe, out_square)

if __name__ == '__main__':
    main()
