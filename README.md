# Centro Azul — Acuática Inicial
## Migración Streamlit → Django (patrón MTV)

---

## Estructura del Proyecto (MTV)

```
centro_azul_django/
│
├── manage.py
├── requirements.txt
│
├── centro_azul_django/          # Configuración del proyecto
│   ├── settings.py              ← BD PostgreSQL, apps, auth
│   ├── urls.py                  ← Router principal
│   └── wsgi.py
│
├── apps/                        # Aplicaciones (M + T de MTV)
│   ├── usuarios/
│   │   ├── models.py            ← M: modelo Usuario (tabla 'usuarios', bcrypt)
│   │   ├── backends.py          ← Backend autenticación bcrypt
│   │   ├── forms.py             ← Validación Login y Registro
│   │   ├── views.py             ← T: vistas login/registro/logout
│   │   └── urls.py
│   │
│   ├── ninos/
│   │   ├── models.py            ← M: Nino, Tutor (tablas existentes)
│   │   ├── forms.py             ← Validación formulario registro niño
│   │   ├── views.py             ← T: lista y registro de niños
│   │   └── urls.py
│   │
│   ├── citas/
│   │   ├── models.py            ← M: Cita (tabla existente)
│   │   ├── forms.py             ← Validación agendar/editar cita
│   │   ├── views.py             ← T: menú, agenda, agendar, editar
│   │   └── urls.py
│   │
│   └── reportes/
│       ├── views.py             ← T: generación PDF con fpdf2
│       └── urls.py
│
├── templates/                   ← V (View) de MTV — HTML con Django Template
│   ├── base/
│   │   ├── base.html            ← Layout con sidebar y logo
│   │   └── menu.html
│   ├── usuarios/
│   │   ├── login.html
│   │   └── registro.html
│   ├── ninos/
│   │   ├── lista.html
│   │   └── registro.html
│   └── citas/
│       ├── agenda.html
│       ├── agendar.html
│       └── editar.html
│
└── static/
    ├── css/
    │   └── azul.css             ← Sistema diseño dark navy (mismo que Streamlit)
    └── img/
        └── logo.png             ← ⬅ AQUÍ agregas tu logo


```

---

## Correspondencia Streamlit → Django (MTV)

| Streamlit (original)              | Django (MTV)                          |
|-----------------------------------|---------------------------------------|
| `modelo/usuario_model.py`         | `apps/usuarios/models.py`             |
| `modelo/nino_model.py`            | `apps/ninos/models.py`                |
| `modelo/cita_model.py`            | `apps/citas/models.py`                |
| `controlador/auth_controller.py`  | `apps/usuarios/views.py` + `backends.py` |
| `controlador/nino_controller.py`  | `apps/ninos/views.py`                 |
| `controlador/reporte_controller.py` | `apps/reportes/views.py`            |
| `vista/login_view.py`             | `templates/usuarios/login.html`       |
| `vista/menu_view.py`              | `templates/base/menu.html`            |
| `vista/lista_ninos_view.py`       | `templates/ninos/lista.html`          |
| `vista/agenda_view.py`            | `templates/citas/agenda.html`         |
| `_inject_css()`                   | `static/css/azul.css`                 |

---

## Instalación

```bash
# 1. Crear entorno virtual
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS/Linux

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Agregar logo (tú lo haces)
#    Copia tu logo.png en:  static/img/logo.png

# 4. Sincronizar tablas existentes SIN borrar datos
#    (Django detecta las tablas ya creadas por el proyecto PHP/Streamlit)
python manage.py migrate --run-syncdb

# 5. Ejecutar servidor
python manage.py runserver
```

## URLs disponibles

| URL                   | Vista                  |
|-----------------------|------------------------|
| `/login/`             | Iniciar sesión         |
| `/registro/`          | Crear cuenta           |
| `/menu/`              | Panel principal        |
| `/ninos/`             | Lista de niños         |
| `/ninos/registro/`    | Registrar niño + tutor |
| `/citas/`             | Agenda de citas        |
| `/citas/agendar/`     | Nueva cita             |
| `/citas/editar/<id>/` | Editar estado cita     |
| `/reportes/citas/`    | Descargar PDF citas    |
| `/reportes/ninos/`    | Descargar PDF niños    |
| `/logout/`            | Cerrar sesión          |

---

## Base de datos

**Misma conexión** que el proyecto Streamlit/PHP original:

```
HOST: localhost
PORT: 5432
NAME: sistema_login
USER: postgres
```

Los modelos Django apuntan exactamente a las mismas tablas:
- `db_table = 'usuarios'`
- `db_table = 'tutores'`
- `db_table = 'ninos'`
- `db_table = 'citas'`

No se migran ni recrean — Django los usa tal como están.
