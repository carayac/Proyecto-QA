# Guia para correr el proyecto

Este proyecto es una aplicacion web hecha con Django para gestion de inventario.

## Requisitos

Antes de empezar, cada persona necesita tener instalado:

- Python 3.13 o compatible
- Git
- PowerShell, CMD o una terminal similar

El proyecto usa SQLite por defecto, asi que no es necesario instalar MySQL para correrlo localmente.

## 1. Clonar el repositorio

```powershell
git clone <URL_DEL_REPOSITORIO>
cd Proyecto-QA
```

Si ya tienes el proyecto descargado, solo entra a la carpeta:

```powershell
cd "C:\ruta\al\proyecto\Proyecto-QA"
```

## 2. Crear un entorno virtual

Desde la raiz del proyecto, ejecuta:

```powershell
python -m venv .venv
```

Activar el entorno virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activacion, ejecutar una vez:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Despues vuelve a activar:

```powershell
.\.venv\Scripts\Activate.ps1
```

Cuando el entorno esta activo, la terminal normalmente muestra `(.venv)` al inicio.

## 3. Instalar dependencias

Con el entorno virtual activo:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Crear el archivo `.env`

En la raiz del proyecto, crear un archivo llamado `.env`.

Puedes copiar el archivo de ejemplo:

```powershell
copy .env-example .env
```

El `.env` debe tener como minimo:

```env
SECRET_KEY=dev-secret-key-local
PASSWORD=dev-password-local
```

Para desarrollo local esos valores pueden quedarse asi.

## 5. Crear la base de datos

El proyecto usa SQLite por defecto. Solo hay que correr las migraciones:

```powershell
python manage.py migrate
```

Esto crea el archivo `db.sqlite3` localmente.

## 6. Crear un usuario administrador

Para entrar al panel de admin de Django:

```powershell
python manage.py createsuperuser
```

Django pedira:

- usuario
- correo, puede dejarse vacio
- contrasena

## 7. Correr el servidor

```powershell
python manage.py runserver
```

Luego abrir en el navegador:

```text
http://127.0.0.1:8000/
```

Rutas utiles:

```text
http://127.0.0.1:8000/register
http://127.0.0.1:8000/accounts/login/
http://127.0.0.1:8000/admin/
```

## Crear categorias

Las categorias que aparecen en el formulario de agregar stock se crean desde el panel de admin de Django.

Primero hay que tener un superusuario:

```powershell
python manage.py createsuperuser
```

Luego entrar en:

```text
http://127.0.0.1:8000/admin/
```

Pasos:

1. Iniciar sesion con el superusuario.
2. Buscar la seccion `Stock`.
3. Entrar a `Categorys` o `Categories`.
4. Dar clic en `Add`.
5. En el campo `group`, escribir el nombre de la categoria.
6. Guardar.

Despues de crear una categoria, ya aparece en el desplegable de:

```text
http://127.0.0.1:8000/add_stock
```

## Usar MySQL opcionalmente

No es necesario para correr el proyecto localmente. Pero si alguien quiere usar MySQL, debe tener MySQL instalado y una base de datos creada.

Agregar esto al `.env`:

```env
DB_ENGINE=mysql
DB_NAME=project
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
```

Luego crear la base de datos en MySQL:

```sql
CREATE DATABASE project CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Y ejecutar:

```powershell
python manage.py migrate
```

## Errores comunes

### `ModuleNotFoundError: No module named 'environ'`

Faltan dependencias o no esta activo el entorno virtual.

Solucion:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### `Set the SECRET_KEY environment variable`

Falta el archivo `.env` o no tiene `SECRET_KEY`.

Solucion:

```powershell
copy .env-example .env
```

### `Can't connect to server on 'localhost' (10061)`

Ese error pasa si el proyecto esta configurado para MySQL pero MySQL no esta corriendo.

Para evitarlo en desarrollo local, no pongas `DB_ENGINE=mysql` en el `.env`. Asi Django usa SQLite.

### El comando `python` no funciona

Prueba:

```powershell
py --version
py -m venv .venv
```

Y luego activa el entorno igual:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Resumen rapido

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env-example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
