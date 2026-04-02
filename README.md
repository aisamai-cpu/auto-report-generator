# 📊 Auto Report Generator

Herramienta de automatización en Python que lee datos de ventas desde un archivo CSV y genera automáticamente un reporte PDF con gráficas y tablas.

## 🚀 ¿Qué hace?

- Lee y procesa datos de ventas desde un archivo CSV
- Genera gráfica de barras de ventas por mes
- Genera gráfica de distribución por producto
- Exporta un reporte PDF profesional con resumen ejecutivo y tabla de detalle

## 🗂️ Estructura del proyecto
```
auto-report-generator/
├── data/
│   └── ventas.csv         # Datos de entrada
├── modules/
│   ├── lector.py          # Lectura y procesamiento de datos
│   ├── graficas.py        # Generación de gráficas
│   └── generador.py       # Creación del PDF
├── output/                # Reportes generados
├── main.py                # Punto de entrada
├── requirements.txt       # Dependencias
└── README.md
```

## ⚙️ Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/aisamai-cpu/auto-report-generator.gitcd auto-report-generator
```

2. Crea y activa el entorno virtual:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## ▶️ Uso
```bash
python main.py
```

El reporte se genera automáticamente en la carpeta `output/`.

## 🛠️ Tecnologías

- Python 3
- pandas
- matplotlib
- fpdf2
- openpyxl

## 📄 Ejemplo de reporte generado

El reporte PDF incluye:
- Resumen ejecutivo con métricas clave
- Gráfica de ventas por mes
- Distribución de ventas por producto
- Tabla detallada de ventas

---
Desarrollado por Aarón Isama