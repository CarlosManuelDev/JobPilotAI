# JobPilotAI 🚀

Plataforma internacional de búsqueda de empleo potenciada con IA.

## Cómo correrlo

### 1. Abrir en VS Code
Abre VS Code → `Archivo` → `Abrir carpeta` → selecciona esta carpeta (`jobpilotai_full`).

### 2. Crear entorno virtual
Abre la terminal integrada (``Ctrl + ` ``) y ejecuta:

```bash
python -m venv .venv
```

Actívalo:
```bash
# Windows
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Correr el servidor
```bash
uvicorn main:app --reload
```

### 5. Probarlo
Abre en el navegador: **http://localhost:8000/docs**

Ahí verás la documentación interactiva. Puedes:
1. Probar `POST /api/auth/register` para crear una cuenta.
2. Probar `POST /api/auth/login` para iniciar sesión (te da un token).
3. Usar el botón "Authorize" 🔒 arriba a la derecha, pegar el `access_token`, y probar `GET /api/auth/me`.

## Estructura del proyecto

```
app/
  core/        → configuración y seguridad (JWT, hashing)
  database/    → conexión a la base de datos
  models/      → tablas (SQLAlchemy)
  schemas/     → validación de datos (Pydantic)
  services/    → lógica de negocio
  routers/     → endpoints de la API
  auth/        → dependencias de autenticación
main.py        → punto de entrada de la aplicación
```

## Próximos pasos sugeridos
- Integrar fuentes de empleo (Adzuna, Remotive) en un nuevo router `jobs`.
- Agregar análisis de CV con IA.
- Sistema de matching candidato-vacante.
