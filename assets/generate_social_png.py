from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 627
bg = (10,102,194)
text_color = (255,255,255)
accent = (255,255,255,40)

img = Image.new('RGB', (W, H), color=bg)
d = ImageDraw.Draw(img)

# Title
try:
    font_title = ImageFont.truetype('arial.ttf', 56)
    font_sub = ImageFont.truetype('arial.ttf', 24)
except Exception:
    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()

d.text((60, 80), 'Familia Calendario', font=font_title, fill=text_color)
d.text((60, 150), 'Demo — Gestión de tareas y calendario familiar', font=font_sub, fill=text_color)

d.rectangle([60,220,480,480], fill=(255,255,255,30))
d.text((80, 260), 'Demo: familia-calendario-demo.onrender.com', font=font_sub, fill=text_color)
d.text((80, 300), 'Usuario: demo   Contraseña: demo', font=font_sub, fill=text_color)

img.save('assets/social.png', format='PNG')
print('SOCIAL_PNG_CREATED')
