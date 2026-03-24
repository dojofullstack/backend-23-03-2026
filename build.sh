#!/usr/bin/env bash
# Script de build para Render.com
set -o errexit   # Aborta si cualquier comando falla

# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Recolectar archivos estáticos
python manage.py collectstatic --no-input

# 3. Aplicar migraciones pendientes
python manage.py migrate
