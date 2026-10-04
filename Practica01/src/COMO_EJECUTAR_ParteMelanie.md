# Cómo ejecutar la Práctica 01

Todos los comandos se escriben en la terminal, **dentro de la carpeta `Practica01`**:
```bash
cd data-analytics-and-visualization/Practica01
```

## 1. Crear el entorno virtual (solo la primera vez)
Un entorno virtual es una carpeta `venv/` con un Python "aislado" para este proyecto. Así las librerías no se mezclan con las de otros proyectos. Git ya ignora esa carpeta.

```bash
python -m venv venv
```

## 2. Activar el entorno (cada vez que abras una terminal nueva)

| Sistema | Comando |
|---|---|
| Windows (PowerShell) | `venv\Scripts\Activate.ps1` |
| Windows (CMD) | `venv\Scripts\activate.bat` |
| Linux / macOS | `source venv/bin/activate` |

Sabrás que está activo porque aparece `(venv)` al inicio de la línea.

> Si PowerShell dice que "la ejecución de scripts está deshabilitada", ejecuta una vez
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` y vuelve a intentarlo.

## 3. Instalar las dependencias (solo la primera vez)
```bash
pip install -r src/requirements.txt
```

## 4. Ejecutar el notebook
**Opción A: VS Code**
1. Abre `Seccion_B_Melanie.ipynb`.
2. Arriba a la derecha, en *Select Kernel*, elige el Python de la carpeta `venv`.
3. Presiona **Run All**.

**Opción B: Jupyter en el navegador**
```bash
jupyter notebook
```
Abre `Seccion_B_Melanie.ipynb` y usa *Kernel → Restart & Run All*.

> El notebook debe abrirse desde la carpeta `Practica01`, porque usa rutas relativas (`src/`, `figuras/`, `data/processed/`).

## 5. Sobre los datasets
**No hay que descargar nada a mano.** La primera ejecución los descarga automáticamente:
- **CarDekho**, con `kagglehub`. Se guarda en caché en `~/.cache/kagglehub`, así que las siguientes ejecuciones no vuelven a descargar.
- **UCI Automobile**, con `ucimlrepo`.

Se necesita conexión a internet la primera vez. Si `kagglehub` pide credenciales, inicia sesión en Kaggle y sigue sus instrucciones (`kagglehub.login()`).

## 6. Qué genera la ejecución
| Archivo | Contenido |
|---|---|
| `data/processed/tabla_homologacion_marcas.csv` | Tabla de homologación de marcas (inciso 8) |
| `figuras/figura_B1_coincidencias.png` | Figura B.1 del reporte |

## Estructura
```text
Practica01/
├── Seccion_B_Melanie.ipynb        # Notebook de la Sección B (incisos 4–8)
├── src/
│   ├── homologacion.py            # Funciones de carga, renombrado y homologación
│   ├── requirements.txt           # Dependencias
│   └── COMO_EJECUTAR.md           # Esta guía
├── data/processed/                # Resultados generados (CSV)
└── figuras/                       # Figuras generadas para el reporte
```
