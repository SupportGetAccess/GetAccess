from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 1600
img = Image.new('RGB', (W, H), 'white')
draw = ImageDraw.Draw(img)

try:
    font_title = ImageFont.truetype("arial.ttf", 18)
    font_bold = ImageFont.truetype("arial.ttf", 14)
    font_text = ImageFont.truetype("arial.ttf", 12)
except:
    font_title = ImageFont.load_default()
    font_bold = ImageFont.load_default()
    font_text = ImageFont.load_default()

def draw_table(x, y, title, cols, color):
    w, h = 220, 30 + len(cols) * 22
    draw.rectangle([x, y, x+w, y+h], outline=color, width=2)
    draw.rectangle([x, y, x+w, y+30], fill=color)
    draw.text((x+10, y+7), title, fill='white', font=font_bold)
    for i, col in enumerate(cols):
        draw.text((x+10, y+35 + i*22), col, fill='black', font=font_text)
    return w, h

# Tablas
tables = [
    ('usuarios', 50, 50, [
        'id (PK) INTEGER',
        'email VARCHAR',
        'nombre VARCHAR(100)',
        'apellido VARCHAR(100)',
        'password VARCHAR',
        'verificado INTEGER',
        'rol TEXT'
    ], '#6366f1'),
    ('eventos', 50, 350, [
        'id (PK) INTEGER',
        'nombre VARCHAR(200)',
        'descripcion VARCHAR',
        'fecha DATETIME',
        'lugar VARCHAR(200)',
        'precio FLOAT',
        'capacidad INTEGER',
        'vendidos INTEGER',
        'imagen VARCHAR',
        'categoria TEXT'
    ], '#6366f1'),
    ('entradas', 350, 50, [
        'id (PK) INTEGER',
        'evento_id (FK) INTEGER',
        'usuario_id (FK) INTEGER',
        'cantidad INTEGER',
        'total FLOAT',
        'estado VARCHAR(50)',
        'preference_id VARCHAR',
        'usada INTEGER'
    ], '#10b981'),
    ('validaciones', 350, 350, [
        'id (PK) INTEGER',
        'entrada_id (FK) INTEGER',
        'scanner_id (FK) INTEGER',
        'cantidad_original INTEGER',
        'timestamp TEXT'
    ], '#f59e0b'),
    ('transferencias', 650, 50, [
        'id (PK) INTEGER',
        'entrada_id (FK) INTEGER',
        'usuario_origen (FK) INTEGER',
        'usuario_destino TEXT',
        'token TEXT',
        'estado TEXT',
        'created_at TEXT',
        'accepted_at TEXT'
    ], '#ec4899'),
    ('evento_imagenes', 650, 350, [
        'id (PK) INTEGER',
        'evento_id (FK) INTEGER',
        'url TEXT',
        'orden INTEGER'
    ], '#8b5cf6'),
    ('password_reset', 900, 50, [
        'id (PK) INTEGER',
        'email TEXT',
        'token TEXT',
        'usado INTEGER',
        'expires_at TEXT'
    ], '#64748b'),
]

for title, x, y, cols, color in tables:
    draw_table(x, y, title, cols, color)

# Líneas de relación
def draw_line(x1, y1, x2, y2):
    draw.line([x1, y1, x2, y2], fill='gray', width=1)

# evento -> entradas
draw_line(270, 450, 350, 200)
# usuario -> entradas
draw_line(270, 200, 350, 180)

# entradas -> validaciones
draw_line(570, 230, 650, 230)
# usuario -> validaciones
draw_line(270, 230, 350, 380)

# evento -> evento_imagenes
draw_line(270, 550, 650, 480)

# entradas -> transferencias
draw_line(570, 200, 650, 180)

# Título
draw.text((400, 20), 'DIAGRAMA ENTIDAD-RELACION - GetAccess', fill='black', font=font_title)

# Guardar
img.save('C:/Users/guill/eventos_tickets_full/DER_GetAccess.jpg', 'JPEG', quality=95)
print("DER_GetAccess.jpg creado")
