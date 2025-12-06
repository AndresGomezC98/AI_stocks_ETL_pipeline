#!/bin/bash
set -e # <-- 1. DETENER en caso de error (Resiliencia)

# 2. Activar el Entorno Virtual (para usar Polars, MySQL, etc.)
source venv/bin/activate

# 3. Ejecutar el Pipeline principal de Python
python src/main.py

# 4. (Opcional) Desactivar el venv al terminar, solo por limpieza
deactivate