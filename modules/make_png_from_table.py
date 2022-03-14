from PIL import Image, ImageDraw, ImageFont


def make_png(table_data, id):
    im = Image.new('RGB', (400, 275), color=('#000'))
    draw_text = ImageDraw.Draw(im)
    draw_text.text(
        (10, 10),
        table_data,
        fill='#fff')
    im.save(f"img/{id}.png")