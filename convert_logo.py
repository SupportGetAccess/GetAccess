from PIL import Image, ImageDraw

# Crear imagen
img = Image.new('RGB', (400, 400), color=(255, 255, 255))
draw = ImageDraw.Draw(img)

# Dibujar el logo
# Rectángulo grande (violeta)
draw.rectangle([40, 100, 360, 320], fill=(99, 102, 241))

# Círculos blancos
draw.ellipse([120, 200, 160, 240], fill=(255, 255, 255))
draw.ellipse([280, 200, 320, 240], fill=(255, 255, 255))

# Rectángulo blanco del medio
draw.rectangle([152, 180, 248, 220], fill=(255, 255, 255))

# Rectángulo pequeño arriba (violeta)
draw.rectangle([140, 60, 260, 120], fill=(99, 102, 241))

# Guardar como PNG
img.save('C:/Users/guill/eventos_tickets_full/logo_getaccess.png', 'PNG')
print('Logo guardado como PNG')