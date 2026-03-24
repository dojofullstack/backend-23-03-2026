

# Pasos para crear un proyecto con Django

## Fase 1 — Entorno

1. **Crear el entorno virtual**
   ```bash
   python -m venv venv
   ```

2. **Activar el entorno virtual**
   ```bash
   # Linux/macOS
   source venv/bin/activate
   # Windows
   venv\Scripts\activate
   ```

3. **Instalar Django**
   ```bash
   pip install django
   ```

4. **Guardar dependencias**
   ```bash
   pip freeze > requirements.txt
   ```

## Fase 2 — Proyecto

5. **Crear el proyecto Django**
   ```bash
   django-admin startproject nombre_proyecto .
   ```
   > El `.` al final evita una carpeta anidada innecesaria.

6. **Verificar que funciona**
   ```bash
   python manage.py runserver
   ```
   Abrir `http://127.0.0.1:8000/` — debería ver la página de bienvenida de Django.

## Fase 3 — Primera App

7. **Crear la primera app**
   ```bash
   python manage.py startapp nombre_app
   ```

8. **Registrar la app** en `nombre_proyecto/settings.py`, dentro de `INSTALLED_APPS`:
   ```python
   'nombre_app',
   ```

9. **Aplicar migraciones iniciales**
   ```bash
   python manage.py migrate
   ```

10. **Crear superusuario** (opcional para el admin)
    ```bash
    python manage.py createsuperuser
    ```

## Estructura resultante

```
venv/                  # entorno virtual (no subir a git)
requirements.txt       # dependencias
manage.py              # CLI de Django
nombre_proyecto/       # configuración global (settings.py, urls.py)
nombre_app/            # primera app (models.py, views.py, urls.py)
```

---

# Integrar DRF + django-rest-registration + JWT

## Fase 1 — Instalación

1. **Instalar las dependencias**
   ```bash
   pip install djangorestframework django-rest-registration djangorestframework-simplejwt
   pip freeze > requirements.txt
   ```

## Fase 2 — settings.py

2. **Agregar a `INSTALLED_APPS`**:
   ```python
   'rest_framework',
   'rest_registration',
   ```

3. **Configurar DRF con autenticación JWT por defecto**:
   ```python
   REST_FRAMEWORK = {
       'DEFAULT_AUTHENTICATION_CLASSES': (
           'rest_framework_simplejwt.authentication.JWTAuthentication',
       ),
       'DEFAULT_PERMISSION_CLASSES': (
           'rest_framework.permissions.IsAuthenticated',
       ),
   }
   ```

4. **Configurar `SIMPLE_JWT`**:
   ```python
   from datetime import timedelta

   SIMPLE_JWT = {
       'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
       'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
       'AUTH_HEADER_TYPES': ('Bearer',),
   }
   ```

5. **Configurar `REST_REGISTRATION`** (sin verificación por email en desarrollo):
   ```python
   REST_REGISTRATION = {
       'REGISTER_VERIFICATION_ENABLED': False,
       'RESET_PASSWORD_VERIFICATION_ENABLED': False,
       'REGISTER_EMAIL_VERIFICATION_ENABLED': False,
   }
   ```

## Fase 3 — URLs

6. **Actualizar `nombre_proyecto/urls.py`**:
   ```python
   from django.contrib import admin
   from django.urls import path, include
   from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

   urlpatterns = [
       path('admin/', admin.site.urls),
       path('api/auth/', include('rest_registration.api.urls')),
       path('api/token/', TokenObtainPairView.as_view()),
       path('api/token/refresh/', TokenRefreshView.as_view()),
   ]
   ```

## Fase 4 — Migraciones

7. **Aplicar migraciones**:
   ```bash
   python manage.py migrate
   ```

8. **Levantar el servidor**:
   ```bash
   python manage.py runserver
   ```

## Endpoints resultantes

| Método | URL | Descripción |
|--------|-----|-------------|
| POST | `/api/auth/register/` | Registro de usuario |
| POST | `/api/auth/login/` | Login (sesión) |
| POST | `/api/auth/logout/` | Logout |
| GET/PUT | `/api/auth/profile/` | Perfil del usuario |
| POST | `/api/auth/change-password/` | Cambiar contraseña |
| POST | `/api/token/` | Obtener JWT (access + refresh) |
| POST | `/api/token/refresh/` | Renovar access token |

## Verificación

- `POST /api/token/` con `{"username": "...", "password": "..."}` devuelve `access` y `refresh`
- `POST /api/auth/register/` crea el usuario correctamente
- Request con header `Authorization: Bearer <token>` a endpoint protegido retorna `200`
