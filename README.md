# 🖼️ Renombrador de Imágenes (GUI)

Una aplicación de escritorio en Python que permite visualizar, renombrar, descartar o dejar para después imágenes de una carpeta, usando una interfaz gráfica simple.

---

## 🧰 Requisitos

Para ejecutar esta aplicación en Windows, necesitás:

- Python 3.10 o superior [🧩 Descargar](https://www.python.org/downloads/windows/)
- Pip (generalmente incluido con Python)
- Librerías necesarias:
  - `Pillow`
  - `tkinter` (ya viene incluido en Python para Windows)

---

## 💡 Recomendado: Usar entorno virtual (`venv`)

Para mantener tus dependencias ordenadas, usá un entorno virtual:

```bash
# Crear entorno virtual
python -m venv env

# Activar el entorno virtual (en Windows)
.\env\Scriptsctivate

# Instalar dependencias
pip install Pillow
```

---

## ▶️ Cómo ejecutar el script

Con el entorno virtual activado:

```bash
python image_renamer.py
```

Se abrirá una ventana gráfica para seleccionar la carpeta de imágenes.

---

## 🪄 Opcional: Crear un `.exe` para Windows

Podés generar un ejecutable para usar sin necesidad de abrir una terminal.

### 1. Instalar PyInstaller dentro del `venv`

```bash
pip install pyinstaller
```

### 2. Crear el ejecutable

```bash
pyinstaller --onefile --windowed image_renamer.py
```

Esto va a generar una carpeta `dist/` con el `.exe` listo para usar:

```
dist/
└── image_renamer.exe
```

> 📦 El `.exe` es independiente y no requiere el entorno virtual para funcionar.

---

## 📁 Estructura de carpetas generadas por la app

Al seleccionar la carpeta de imágenes, se crean automáticamente las siguientes carpetas dentro de `./salida`:

- `renombradas/`: Imágenes renombradas con éxito
- `descartadas/`: Imágenes descartadas manualmente
- `pendientes/`: Imágenes marcadas para revisar después

---

## ✅ Formatos soportados

- `.jpg`, `.jpeg`
- `.png`
- `.bmp`
- `.gif`
- `.webp`
- `.tiff`

---

## 🧠 Atajos de teclado

- `Enter`: Renombrar
- `→`: Renombrar (avanzar)
- `←`: Volver a la anterior
- `Ctrl+D` o `Cmd+D`: Descartar

