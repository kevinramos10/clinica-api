# 🏥 Clínica API

API REST para la gestión de una clínica: pacientes, médicos, especialidades, consultorios, citas, historiales médicos y usuarios con autenticación JWT. Desplegada en **Render** con base de datos **PostgreSQL en Neon**.

🔗 **API en producción:** `https://TU-APP.onrender.com` <!-- TODO: reemplazar -->

## ✨ Características

- **CRUD completo** de pacientes, médicos, especialidades, consultorios, citas e historiales.
- **Autenticación con JWT** (Flask-JWT-Extended): registro, login y eliminación de usuarios.
- **Recuperación de contraseña por correo**: reset y confirmación de contraseña, con envío de emails mediante **Resend**.
- **Contraseñas protegidas** con hash **bcrypt**.
- **Validación de datos** con **Pydantic v2** (tipos, longitudes, emails, rangos) y respuestas de error claras (`400`).
- **Control de duplicados**: DNI, colegiatura y correo únicos (`409 Conflict`) con `rollback` ante errores de base de datos.
- **Paginación** en los listados (`?page=1&perPage=10`).
- **Relación médico–especialidad** (muchos a muchos), con endpoints para agregar y quitar especialidades.
- **Reglas de negocio**: por ejemplo, no se registra un historial para una cita cancelada ni se duplica el historial de una misma cita.
- **Eliminación lógica** de médicos (cambio de estado en lugar de borrar el registro).
- **Migraciones** de base de datos con Alembic (Flask-Migrate).
- **Zona horaria de Lima** para las fechas de registro.

## 🛠️ Tecnologías

| Área | Herramientas |
|---|---|
| Lenguaje | Python |
| Framework | Flask, Flask-RESTful |
| Base de datos | PostgreSQL (Neon), SQLAlchemy, Flask-SQLAlchemy |
| Migraciones | Alembic, Flask-Migrate |
| Validación | Pydantic v2, email-validator |
| Seguridad | Flask-JWT-Extended, bcrypt, cryptography (Fernet) |
| Correos | Resend |
| Despliegue | Render, Gunicorn |
| Pruebas manuales | Bruno |

## 📁 Estructura del proyecto

```
clinica-api/
├── app/                # Código de la API (modelos, schemas, controllers, utilidades)
├── migrations/         # Migraciones de Alembic
├── .env.example        # Plantilla de variables de entorno
├── requirements.txt
└── run.py              # Punto de entrada
```

<!-- TODO: pega aquí la salida de `tree app` para detallar las carpetas -->

## 🚀 Instalación y ejecución local

**Requisitos:** Python 3.10 o superior y PostgreSQL.

```bash
# 1. Clonar el repositorio
git clone https://github.com/kevinramos10/clinica-api.git
cd clinica-api

# 2. Crear y activar el entorno virtual
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux / macOS

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env         # y completa tus valores

# 5. Crear las tablas con las migraciones
flask db upgrade

# 6. Ejecutar la API
python run.py
```

### Variables de entorno

| Variable | Descripción |
|---|---|
| `DATABASE_URL` | URL de conexión a PostgreSQL |
| `JWT_SECRET_KEY` | Clave secreta para firmar los tokens JWT |
| `FERNET_KEY` | Clave de cifrado (Fernet) |
| `RESEND_API_KEY` | API key de Resend para enviar correos |
| `EMAIL` | Remitente de los correos |

## 📡 Módulos y endpoints

| Módulo | Operaciones |
|---|---|
| Pacientes | Listar, crear, actualizar |
| Médicos | CRUD, búsqueda y paginación |
| Especialidades | CRUD |
| Médico-Especialidades | Agregar y eliminar especialidades de un médico |
| Consultorios | CRUD |
| Citas | Listar, crear, actualizar, eliminar |
| Historiales | Listar, crear, ver detalle |
| Usuarios | Registro, login, listar, actualizar contraseña, reset y confirmación de contraseña, eliminar |

La autenticación se envía en el header:

```
Authorization: Bearer <token>
```

## 🧪 Pruebas

Los endpoints se probaron con **Bruno**. <!-- TODO: si exportas la colección a una carpeta del repo, menciónala aquí -->

## 🔮 Próximas mejoras

- Permisos por roles (administrador, médico, recepción).
- Pruebas automáticas con pytest.
- Documentación interactiva con Swagger/OpenAPI.
- Dockerización del proyecto.
- Rate limiting en el login.
- Refresh tokens para JWT.

## 👤 Autor

**Kevin Ramos** · [GitHub](https://github.com/kevinramos10)
