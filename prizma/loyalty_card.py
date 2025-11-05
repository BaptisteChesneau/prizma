# loyalty_card.py
from PIL import Image, ImageDraw
import barcode
from barcode.writer import ImageWriter
from io import BytesIO

def generate_loyalty_card(member_id: str, width=400, height=250):
    """
    Génère une carte fidélité pour un membre avec code-barres au centre
    """
    # Carte blanche
    card = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(card)

    # Bordure marron-orange (#B45309)
    border_color = "#B45309"
    border_width = 8
    for i in range(border_width):
        draw.rectangle([i, i, width-1-i, height-1-i], outline=border_color)

    # Générer code-barres
    code128 = barcode.get("code128", member_id, writer=ImageWriter())
    barcode_io = BytesIO()
    code128.write(barcode_io)
    barcode_io.seek(0)
    barcode_img = Image.open(barcode_io)

    # Redimensionner pour la carte
    max_barcode_width = width - 60
    ratio = max_barcode_width / barcode_img.width
    barcode_height = int(barcode_img.height * ratio)
    barcode_img = barcode_img.resize((max_barcode_width, barcode_height))

    # Coller code-barres au centre
    x = (width - barcode_img.width) // 2
    y = (height - barcode_img.height) // 2
    card.paste(barcode_img, (x, y))

    return card
