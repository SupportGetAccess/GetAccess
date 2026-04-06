import sys
sys.path.insert(0, r'C:\Users\guill\eventos_tickets_full\backend')

# Importar la función directamente
import importlib.util
spec = importlib.util.spec_from_file_location("main", r"C:\Users\guill\eventos_tickets_full\backend\main.py")
module = importlib.util.module_from_spec(spec)

# Ahora ejecutar la función directamente
from backend.main import enviar_codigo_verificacion

result = enviar_codigo_verificacion("guilles10@yahoo.com.ar", "123456", "Willy")
print(f"Resultado: {result}")
