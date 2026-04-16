"""
conversor.py — Módulo de conversión de archivos
Auto Report Generator · Windows
 
Funciones:
  - imagen_a_pdf(rutas_imagenes, ruta_salida)
  - pdf_a_word(ruta_pdf, ruta_salida)
  - word_a_pdf(ruta_docx, ruta_salida)
  - combinar_pdfs(lista_pdfs, ruta_salida)
  - dividir_pdf(ruta_pdf, ruta_salida_dir, paginas=None)
 
Instalación de dependencias:
  pip install pypdf pdf2docx docx2pdf Pillow img2pdf
"""
 
import os
from pathlib import Path
 
 
# ─────────────────────────────────────────────
# 1. IMAGEN → PDF
# ─────────────────────────────────────────────
def imagen_a_pdf(rutas_imagenes: list[str], ruta_salida: str) -> str:
    """
    Convierte una o varias imágenes (JPG, PNG, BMP, TIFF, WEBP) a un PDF.
    Si se pasan varias imágenes, cada una se convierte en una página.
 
    Parámetros:
        rutas_imagenes : lista de rutas absolutas o relativas a las imágenes
        ruta_salida    : ruta del PDF de salida (debe terminar en .pdf)
 
    Retorna:
        ruta_salida si tuvo éxito.
 
    Lanza:
        FileNotFoundError si alguna imagen no existe.
        ValueError        si la lista está vacía.
        RuntimeError      si la conversión falla.
    """
    try:
        import img2pdf
        from PIL import Image
    except ImportError as e:
        raise RuntimeError(
            "Faltan dependencias. Ejecuta: pip install img2pdf Pillow"
        ) from e
 
    if not rutas_imagenes:
        raise ValueError("La lista de imágenes está vacía.")
 
    # Verificar que todos los archivos existen
    for ruta in rutas_imagenes:
        if not os.path.isfile(ruta):
            raise FileNotFoundError(f"Imagen no encontrada: {ruta}")
 
    # Convertir WEBP / imágenes con transparencia a PNG temporal
    # porque img2pdf no soporta todos los formatos directamente
    rutas_procesadas = []
    temporales = []
    for ruta in rutas_imagenes:
        ext = Path(ruta).suffix.lower()
        img = Image.open(ruta)
 
        # RGBA / P (paleta con transparencia) → RGB antes de convertir
        if img.mode in ("RGBA", "P", "LA"):
            fondo = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            fondo.paste(img, mask=img.split()[-1] if img.mode in ("RGBA", "LA") else None)
            img = fondo
 
        # WEBP y otros formatos no soportados por img2pdf → guardar como PNG temporal
        if ext in (".webp", ".bmp", ".tiff", ".tif"):
            tmp = ruta + "__tmp__.png"
            img.save(tmp, format="PNG")
            rutas_procesadas.append(tmp)
            temporales.append(tmp)
        else:
            img.close()
            rutas_procesadas.append(ruta)
 
    try:
        with open(ruta_salida, "wb") as f:
            f.write(img2pdf.convert(rutas_procesadas))
    except Exception as e:
        raise RuntimeError(f"Error al convertir imagen a PDF: {e}") from e
    finally:
        # Eliminar archivos temporales
        for tmp in temporales:
            if os.path.exists(tmp):
                os.remove(tmp)
 
    return ruta_salida
 
 
# ─────────────────────────────────────────────
# 2. PDF → WORD
# ─────────────────────────────────────────────
def pdf_a_word(ruta_pdf: str, ruta_salida: str) -> str:
    """
    Convierte un PDF a un documento Word (.docx) intentando preservar
    el formato (texto, tablas, imágenes).
 
    Parámetros:
        ruta_pdf    : ruta al archivo PDF de entrada
        ruta_salida : ruta del .docx de salida
 
    Retorna:
        ruta_salida si tuvo éxito.
 
    Lanza:
        FileNotFoundError si el PDF no existe.
        RuntimeError      si la conversión falla.
    """
    try:
        from pdf2docx import Converter
    except ImportError as e:
        raise RuntimeError(
            "Falta la dependencia. Ejecuta: pip install pdf2docx"
        ) from e
 
    if not os.path.isfile(ruta_pdf):
        raise FileNotFoundError(f"PDF no encontrado: {ruta_pdf}")
 
    try:
        cv = Converter(ruta_pdf)
        cv.convert(ruta_salida, start=0, end=None)
        cv.close()
    except Exception as e:
        raise RuntimeError(f"Error al convertir PDF a Word: {e}") from e
 
    return ruta_salida
 
 
# ─────────────────────────────────────────────
# 3. WORD → PDF  (Windows: usa Microsoft Word)
# ─────────────────────────────────────────────
def word_a_pdf(ruta_docx: str, ruta_salida: str) -> str:
    """
    Convierte un archivo Word (.docx / .doc) a PDF.
    En Windows utiliza Microsoft Word vía docx2pdf (COM automation).
    Si Word no está instalado, intenta una conversión básica con python-docx
    + reportlab como alternativa (solo texto plano, sin estilos).
 
    Parámetros:
        ruta_docx   : ruta al archivo .docx de entrada
        ruta_salida : ruta del PDF de salida
 
    Retorna:
        ruta_salida si tuvo éxito.
 
    Lanza:
        FileNotFoundError si el .docx no existe.
        RuntimeError      si la conversión falla.
    """
    if not os.path.isfile(ruta_docx):
        raise FileNotFoundError(f"Archivo Word no encontrado: {ruta_docx}")
 
    # Intentar con docx2pdf (requiere Word instalado en Windows)
    try:
        from docx2pdf import convert
        convert(ruta_docx, ruta_salida)
        return ruta_salida
    except ImportError:
        pass  # docx2pdf no está instalado, intentar alternativa
    except Exception as e:
        raise RuntimeError(
            f"Error al convertir Word a PDF con docx2pdf: {e}\n"
            "Asegúrate de que Microsoft Word esté instalado."
        ) from e
 
    # Alternativa sin Word: extrae texto y genera PDF básico
    try:
        from docx import Document
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
 
        doc = Document(ruta_docx)
        pdf = SimpleDocTemplate(ruta_salida, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
 
        for para in doc.paragraphs:
            if para.text.strip():
                story.append(Paragraph(para.text, styles["Normal"]))
                story.append(Spacer(1, 6))
 
        pdf.build(story)
        return ruta_salida
    except Exception as e:
        raise RuntimeError(
            f"Error en conversión alternativa Word → PDF: {e}\n"
            "Instala docx2pdf y Microsoft Word para mejor resultado."
        ) from e
 
 
# ─────────────────────────────────────────────
# 4. COMBINAR PDFs
# ─────────────────────────────────────────────
def combinar_pdfs(lista_pdfs: list[str], ruta_salida: str) -> str:
    """
    Une varios archivos PDF en uno solo, en el orden de la lista.
 
    Parámetros:
        lista_pdfs  : lista de rutas a los PDFs a combinar (mínimo 2)
        ruta_salida : ruta del PDF combinado de salida
 
    Retorna:
        ruta_salida si tuvo éxito.
 
    Lanza:
        FileNotFoundError si algún PDF no existe.
        ValueError        si la lista tiene menos de 2 archivos.
        RuntimeError      si la combinación falla.
    """
    try:
        from pypdf import PdfWriter, PdfReader
    except ImportError as e:
        raise RuntimeError(
            "Falta la dependencia. Ejecuta: pip install pypdf"
        ) from e
 
    if len(lista_pdfs) < 2:
        raise ValueError("Se necesitan al menos 2 archivos PDF para combinar.")
 
    for ruta in lista_pdfs:
        if not os.path.isfile(ruta):
            raise FileNotFoundError(f"PDF no encontrado: {ruta}")
 
    try:
        writer = PdfWriter()
        for ruta in lista_pdfs:
            reader = PdfReader(ruta)
            for page in reader.pages:
                writer.add_page(page)
 
        with open(ruta_salida, "wb") as f:
            writer.write(f)
    except Exception as e:
        raise RuntimeError(f"Error al combinar PDFs: {e}") from e
 
    return ruta_salida
 
 
# ─────────────────────────────────────────────
# 5. DIVIDIR PDF
# ─────────────────────────────────────────────
def dividir_pdf(
    ruta_pdf: str,
    ruta_salida_dir: str,
    paginas: list[tuple[int, int]] | None = None,
) -> list[str]:
    """
    Divide un PDF en partes. Tiene dos modos:
 
    Modo A — Sin 'paginas' (None):
        Extrae cada página como un archivo separado.
        Genera: pagina_001.pdf, pagina_002.pdf, ...
 
    Modo B — Con 'paginas':
        Lista de tuplas (inicio, fin) con números de página (base 1, inclusivos).
        Genera un archivo por cada rango.
        Ejemplo: paginas=[(1,3), (4,6)] → parte_001.pdf (pp.1-3), parte_002.pdf (pp.4-6)
 
    Parámetros:
        ruta_pdf        : ruta al PDF a dividir
        ruta_salida_dir : directorio donde se guardarán los archivos generados
        paginas         : lista de tuplas (inicio, fin) o None para dividir por páginas
 
    Retorna:
        Lista de rutas de los archivos generados.
 
    Lanza:
        FileNotFoundError si el PDF no existe.
        ValueError        si los rangos de páginas son inválidos.
        RuntimeError      si la división falla.
    """
    try:
        from pypdf import PdfWriter, PdfReader
    except ImportError as e:
        raise RuntimeError(
            "Falta la dependencia. Ejecuta: pip install pypdf"
        ) from e
 
    if not os.path.isfile(ruta_pdf):
        raise FileNotFoundError(f"PDF no encontrado: {ruta_pdf}")
 
    os.makedirs(ruta_salida_dir, exist_ok=True)
 
    archivos_generados = []
 
    try:
        reader = PdfReader(ruta_pdf)
        total = len(reader.pages)
 
        if paginas is None:
            # Modo A: una página por archivo
            for i, page in enumerate(reader.pages):
                writer = PdfWriter()
                writer.add_page(page)
                nombre = os.path.join(ruta_salida_dir, f"pagina_{i + 1:03d}.pdf")
                with open(nombre, "wb") as f:
                    writer.write(f)
                archivos_generados.append(nombre)
        else:
            # Modo B: rangos definidos por el usuario
            for idx, (inicio, fin) in enumerate(paginas):
                if inicio < 1 or fin > total or inicio > fin:
                    raise ValueError(
                        f"Rango inválido ({inicio}-{fin}) para un PDF de {total} páginas."
                    )
                writer = PdfWriter()
                for i in range(inicio - 1, fin):  # pypdf usa índice base 0
                    writer.add_page(reader.pages[i])
                nombre = os.path.join(ruta_salida_dir, f"parte_{idx + 1:03d}.pdf")
                with open(nombre, "wb") as f:
                    writer.write(f)
                archivos_generados.append(nombre)
 
    except ValueError:
        raise
    except Exception as e:
        raise RuntimeError(f"Error al dividir el PDF: {e}") from e
 
    return archivos_generados
 
 
# ─────────────────────────────────────────────
# UTILIDAD: obtener número de páginas de un PDF
# ─────────────────────────────────────────────
def obtener_num_paginas(ruta_pdf: str) -> int:
    """
    Retorna el número de páginas de un PDF.
    Útil para validar rangos antes de llamar a dividir_pdf().
 
    Lanza:
        FileNotFoundError si el PDF no existe.
    """
    try:
        from pypdf import PdfReader
    except ImportError as e:
        raise RuntimeError("Ejecuta: pip install pypdf") from e
 
    if not os.path.isfile(ruta_pdf):
        raise FileNotFoundError(f"PDF no encontrado: {ruta_pdf}")
 
    return len(PdfReader(ruta_pdf).pages)
# ─────────────────────────────────────────────
# 6. COMPRIMIR PDF
# ─────────────────────────────────────────────
# Niveles de compresión:
#   "baja"  → calidad alta,  poca reducción de tamaño
#   "media" → balance entre calidad y tamaño
#   "alta"  → máxima reducción, algo de pérdida de calidad

NIVELES_PDF = {
    "baja":  150,   # DPI de imágenes internas
    "media":  96,
    "alta":   72,
}

def comprimir_pdf(ruta_pdf: str, ruta_salida: str, nivel: str = "media") -> dict:
    """
    Comprime un PDF reduciendo la resolución de sus imágenes internas.

    Parámetros:
        ruta_pdf    : ruta al PDF original
        ruta_salida : ruta del PDF comprimido
        nivel       : "baja", "media" o "alta"

    Retorna:
        dict con claves:
            - ruta        : ruta del archivo comprimido
            - tam_original: tamaño original en KB
            - tam_nuevo   : tamaño nuevo en KB
            - reduccion   : porcentaje de reducción
    """
    try:
        from pypdf import PdfReader, PdfWriter
        from PIL import Image
        import io
    except ImportError as e:
        raise RuntimeError("Ejecuta: pip install pypdf Pillow") from e

    if not os.path.isfile(ruta_pdf):
        raise FileNotFoundError(f"PDF no encontrado: {ruta_pdf}")

    if nivel not in NIVELES_PDF:
        raise ValueError(f"Nivel inválido. Usa: {list(NIVELES_PDF.keys())}")

    dpi_objetivo = NIVELES_PDF[nivel]
    tam_original = os.path.getsize(ruta_pdf)

    try:
        reader = PdfReader(ruta_pdf)
        writer = PdfWriter()

        for page in reader.pages:
            # Comprimir imágenes embebidas en cada página
            if "/Resources" in page and "/XObject" in page["/Resources"]:
                xobjects = page["/Resources"]["/XObject"].get_object()
                for obj_name in xobjects:
                    obj = xobjects[obj_name].get_object()
                    if obj.get("/Subtype") == "/Image":
                        try:
                            # Extraer imagen
                            data = obj.get_data()
                            width  = int(obj["/Width"])
                            height = int(obj["/Height"])

                            # Detectar modo de color
                            cs = obj.get("/ColorSpace", "/DeviceRGB")
                            if isinstance(cs, list):
                                cs = cs[0]
                            modo = "RGB" if "RGB" in str(cs) else "L"

                            # Abrir con Pillow
                            img = Image.frombytes(modo, (width, height), data)

                            # Calcular nuevo tamaño según DPI objetivo
                            factor = dpi_objetivo / 150.0
                            nuevo_w = max(1, int(width  * factor))
                            nuevo_ancho = max(1, int(height * factor))

                            if factor < 1.0:
                                img = img.resize(
                                    (nuevo_w, nuevo_ancho),
                                    Image.LANCZOS
                                )

                            # Recomprimir como JPEG
                            buffer = io.BytesIO()
                            calidad = {
                                "baja":  85,
                                "media": 65,
                                "alta":  45,
                            }[nivel]
                            img.convert("RGB").save(
                                buffer, format="JPEG", quality=calidad, optimize=True
                            )
                            buffer.seek(0)
                        except Exception:
                            pass  # Si falla una imagen, continúa con las demás

            writer.add_page(page)

        # Comprimir streams de texto
        writer.compress_identical_objects(remove_identicals=True, remove_orphans=True)

        with open(ruta_salida, "wb") as f:
            writer.write(f)

    except Exception as e:
        raise RuntimeError(f"Error al comprimir PDF: {e}") from e

    tam_nuevo   = os.path.getsize(ruta_salida)
    reduccion   = max(0.0, (1 - tam_nuevo / tam_original) * 100)

    return {
        "ruta":         ruta_salida,
        "tam_original": round(tam_original / 1024, 1),
        "tam_nuevo":    round(tam_nuevo    / 1024, 1),
        "reduccion":    round(reduccion, 1),
    }


# ─────────────────────────────────────────────
# 7. COMPRIMIR IMAGEN (JPG / PNG)
# ─────────────────────────────────────────────

NIVELES_IMG = {
    "baja":  85,   # calidad JPEG / PNG
    "media": 65,
    "alta":  40,
}

def comprimir_imagen(ruta_imagen: str, ruta_salida: str, nivel: str = "media") -> dict:
    """
    Comprime una imagen JPG o PNG.

    Parámetros:
        ruta_imagen : ruta a la imagen original
        ruta_salida : ruta de la imagen comprimida
        nivel       : "baja", "media" o "alta"

    Retorna:
        dict con claves:
            - ruta        : ruta del archivo comprimido
            - tam_original: tamaño original en KB
            - tam_nuevo   : tamaño nuevo en KB
            - reduccion   : porcentaje de reducción
    """
    try:
        from PIL import Image
    except ImportError as e:
        raise RuntimeError("Ejecuta: pip install Pillow") from e

    if not os.path.isfile(ruta_imagen):
        raise FileNotFoundError(f"Imagen no encontrada: {ruta_imagen}")

    if nivel not in NIVELES_IMG:
        raise ValueError(f"Nivel inválido. Usa: {list(NIVELES_IMG.keys())}")

    ext = Path(ruta_imagen).suffix.lower()
    tam_original = os.path.getsize(ruta_imagen)

    try:
        img = Image.open(ruta_imagen)

        # Convertir RGBA/P a RGB para poder guardar como JPEG
        if img.mode in ("RGBA", "P", "LA"):
            fondo = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            fondo.paste(img, mask=img.split()[-1] if img.mode in ("RGBA", "LA") else None)
            img = fondo

        calidad = NIVELES_IMG[nivel]

        if ext in (".jpg", ".jpeg"):
            img.save(ruta_salida, format="JPEG", quality=calidad, optimize=True)
        elif ext == ".png":
            # PNG usa compresión sin pérdida; reducimos con optimize
            # y opcionalmente convertimos a RGB para reducir canales
            compress_level = {"baja": 6, "media": 7, "alta": 9}[nivel]
            img.convert("RGB").save(
                ruta_salida, format="PNG",
                optimize=True, compress_level=compress_level
            )
        else:
            # Otros formatos → guardar como JPEG comprimido
            img.convert("RGB").save(
                ruta_salida, format="JPEG", quality=calidad, optimize=True
            )

    except Exception as e:
        raise RuntimeError(f"Error al comprimir imagen: {e}") from e

    tam_nuevo = os.path.getsize(ruta_salida)
    reduccion = max(0.0, (1 - tam_nuevo / tam_original) * 100)

    return {
        "ruta":         ruta_salida,
        "tam_original": round(tam_original / 1024, 1),
        "tam_nuevo":    round(tam_nuevo    / 1024, 1),
        "reduccion":    round(reduccion, 1),
    }


# ─────────────────────────────────────────────
# UTILIDAD: tamaño legible de archivo
# ─────────────────────────────────────────────
def tamaño_legible(ruta: str) -> str:
    """Retorna el tamaño de un archivo como string legible (KB o MB)."""
    if not os.path.isfile(ruta):
        return "0 KB"
    tam = os.path.getsize(ruta)
    if tam < 1024 * 1024:
        return f"{tam / 1024:.1f} KB"
    return f"{tam / (1024 * 1024):.2f} MB"
 