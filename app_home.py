import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os
 
# ── Colores ──────────────────────────────────────────────
BG        = "#f0f4f8"
AZUL      = "#2E86AB"
BLANCO    = "#ffffff"
GRIS_TX   = "#444444"
GRIS_SUB  = "#888888"
HOVER_BG  = "#e1eef6"
 
HERRAMIENTAS = [
    {
        "icono": "📊",
        "titulo": "Excel a Reporte PDF",
        "desc": "Genera reportes con gráficas desde Excel o CSV",
        "color": "#2E86AB",
        "modulo": "app"
    },
    {
        "icono": "🖼️",
        "titulo": "Imagen a PDF",
        "desc": "Convierte JPG, PNG y otros formatos a PDF",
        "color": "#27ae60",
        "modulo": "app_imagen_pdf"
    },
    {
        "icono": "📄",
        "titulo": "PDF a Word",
        "desc": "Convierte documentos PDF a formato Word",
        "color": "#8e44ad",
        "modulo": "app_pdf_word"
    },
    {
        "icono": "📝",
        "titulo": "Word a PDF",
        "desc": "Convierte documentos Word a formato PDF",
        "color": "#e67e22",
        "modulo": "app_word_pdf"
    },
    {
        "icono": "🔗",
        "titulo": "Combinar PDFs",
        "desc": "Une varios archivos PDF en uno solo",
        "color": "#c0392b",
        "modulo": "app_combinar_pdf"
    },
    {
        "icono": "✂️",
        "titulo": "Dividir PDF",
        "desc": "Separa un PDF en partes o páginas individuales",
        "color": "#16a085",
        "modulo": "app_dividir_pdf"
    },
    {
        "icono": "🗜️",
        "titulo": "Comprimir archivo",
        "desc": "Reduce el tamaño de PDFs e imágenes JPG/PNG",
        "color": "#2980b9",
        "modulo": "app_comprimir"
    },
]
 
 
class AppHome:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Report Generator")
        self.root.geometry("700x580")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)
        self._construir_ui()
 
    def _construir_ui(self):
        # ── Encabezado ──────────────────────────────────
        header = tk.Frame(self.root, bg=AZUL, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
 
        tk.Label(
            header,
            text="Auto Report Generator",
            font=("Helvetica", 20, "bold"),
            bg=AZUL, fg=BLANCO
        ).place(relx=0.5, rely=0.42, anchor="center")
 
        tk.Label(
            header,
            text="Selecciona una herramienta para comenzar",
            font=("Helvetica", 10),
            bg=AZUL, fg="#d0e8f5"
        ).place(relx=0.5, rely=0.78, anchor="center")
 
        # ── Grid de herramientas ─────────────────────────
        contenedor = tk.Frame(self.root, bg=BG)
        contenedor.pack(pady=25, padx=30)
 
        for i, h in enumerate(HERRAMIENTAS):
            fila = i // 3
            col  = i % 3
            self._tarjeta(contenedor, h, fila, col)
 
        # ── Pie de página ────────────────────────────────
        tk.Label(
            self.root,
            text="v1.0  ·  Auto Report Generator",
            font=("Helvetica", 8),
            bg=BG, fg=GRIS_SUB
        ).pack(side="bottom", pady=8)
 
    def _tarjeta(self, padre, datos, fila, col):
        # Marco exterior con borde de color
        marco = tk.Frame(
            padre,
            bg=BLANCO,
            bd=0,
            highlightthickness=2,
            highlightbackground="#dce6ef",
            cursor="hand2",
            width=185,
            height=155
        )
        marco.grid(row=fila, column=col, padx=10, pady=10)
        marco.pack_propagate(False)
 
        # Barra de color superior
        barra = tk.Frame(marco, bg=datos["color"], height=5)
        barra.pack(fill="x")
 
        # Ícono
        tk.Label(
            marco,
            text=datos["icono"],
            font=("Helvetica", 28),
            bg=BLANCO
        ).pack(pady=(12, 2))
 
        # Título
        tk.Label(
            marco,
            text=datos["titulo"],
            font=("Helvetica", 10, "bold"),
            bg=BLANCO,
            fg=GRIS_TX,
            wraplength=160,
            justify="center"
        ).pack(padx=8)
 
        # Descripción
        tk.Label(
            marco,
            text=datos["desc"],
            font=("Helvetica", 8),
            bg=BLANCO,
            fg=GRIS_SUB,
            wraplength=160,
            justify="center"
        ).pack(padx=8, pady=(3, 0))
 
        # Efectos hover y clic
        modulo = datos["modulo"]
        color  = datos["color"]
 
        def on_enter(e):
            marco.config(highlightbackground=color)
            barra.config(height=7)
 
        def on_leave(e):
            marco.config(highlightbackground="#dce6ef")
            barra.config(height=5)
 
        def on_click(e, m=modulo):
            self._abrir_herramienta(m)
 
        for widget in [marco, barra] + list(marco.winfo_children()):
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", on_click)
 
    def _abrir_herramienta(self, modulo):
        # Módulos ya construidos
        disponibles = ["app", "app_imagen_pdf", "app_pdf_word", "app_word_pdf", "app_combinar_pdf", "app_dividir_pdf", "app_comprimir"]
 
        if modulo in disponibles:
            subprocess.Popen([sys.executable, f"{modulo}.py"],
                             cwd=os.path.dirname(os.path.abspath(__file__)))
        else:
            messagebox.showinfo(
                "Próximamente",
                "Esta herramienta está en construcción.\n¡Pronto estará disponible!"
            )
 
 
if __name__ == "__main__":
    root = tk.Tk()
    app  = AppHome(root)
    root.mainloop()