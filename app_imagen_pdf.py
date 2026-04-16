import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
import sys
import subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modules.conversor import imagen_a_pdf

BG       = "#f0f4f8"
AZUL     = "#27ae60"
BLANCO   = "#ffffff"
GRIS_TX  = "#444444"
GRIS_SUB = "#888888"


class AppImagenPDF:
    def __init__(self, root):
        self.root = root
        self.root.title("Imagen a PDF")
        self.root.geometry("500x460")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)
        self.archivos = []
        self._construir_ui()

    def _construir_ui(self):
        # ── Encabezado ──────────────────────────────────
        header = tk.Frame(self.root, bg=AZUL, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🖼️  Imagen a PDF",
            font=("Helvetica", 18, "bold"),
            bg=AZUL, fg=BLANCO
        ).place(relx=0.5, rely=0.45, anchor="center")

        tk.Label(
            header,
            text="Convierte una o varias imágenes a un solo PDF",
            font=("Helvetica", 9),
            bg=AZUL, fg="#d0f0e0"
        ).place(relx=0.5, rely=0.82, anchor="center")

        # ── Botón seleccionar ────────────────────────────
        tk.Button(
            self.root,
            text="📂  Seleccionar imagen(es)",
            font=("Helvetica", 11),
            bg=AZUL, fg=BLANCO,
            padx=10, pady=8,
            relief="flat", cursor="hand2",
            command=self._seleccionar
        ).pack(pady=20)

        # ── Lista de archivos ────────────────────────────
        marco_lista = tk.Frame(self.root, bg=BLANCO,
                               highlightthickness=1,
                               highlightbackground="#dce6ef")
        marco_lista.pack(padx=30, fill="x")

        self.lista_box = tk.Listbox(
            marco_lista,
            font=("Helvetica", 9),
            bg=BLANCO, fg=GRIS_TX,
            selectbackground=AZUL,
            height=8,
            bd=0,
            highlightthickness=0
        )
        self.lista_box.pack(fill="x", padx=5, pady=5)

        self.label_info = tk.Label(
            self.root,
            text="Ninguna imagen seleccionada",
            font=("Helvetica", 9),
            bg=BG, fg=GRIS_SUB
        )
        self.label_info.pack(pady=5)

        # ── Botón convertir ──────────────────────────────
        self.btn_convertir = tk.Button(
            self.root,
            text="▶  Convertir a PDF",
            font=("Helvetica", 12, "bold"),
            bg="#95a5a6", fg=BLANCO,
            padx=15, pady=10,
            relief="flat", cursor="hand2",
            command=self._convertir,
            state="disabled"
        )
        self.btn_convertir.pack(pady=12)

        # ── Estado ───────────────────────────────────────
        self.label_estado = tk.Label(
            self.root, text="",
            font=("Helvetica", 10),
            bg=BG, fg=AZUL
        )
        self.label_estado.pack()

    def _seleccionar(self):
        rutas = filedialog.askopenfilenames(
            title="Seleccionar imágenes",
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif *.webp")]
        )
        if rutas:
            self.archivos = list(rutas)
            self.lista_box.delete(0, tk.END)
            for r in self.archivos:
                self.lista_box.insert(tk.END, f"  {os.path.basename(r)}")
            self.label_info.config(
                text=f"✅ {len(rutas)} imagen(es) seleccionada(s)",
                fg="#27ae60"
            )
            self.btn_convertir.config(state="normal", bg=AZUL)

    def _convertir(self):
        self.btn_convertir.config(state="disabled")
        self.label_estado.config(text="Convirtiendo...", fg=AZUL)
        threading.Thread(target=self._proceso).start()

    def _proceso(self):
        try:
            ruta_salida = filedialog.asksaveasfilename(
                title="Guardar PDF como",
                defaultextension=".pdf",
                filetypes=[("PDF", "*.pdf")],
                initialfile="imagenes_convertidas.pdf"
            )
            if not ruta_salida:
                self.root.after(0, lambda: self.label_estado.config(text=""))
                self.root.after(0, lambda: self.btn_convertir.config(state="normal"))
                return

            imagen_a_pdf(self.archivos, ruta_salida)
            self.root.after(0, lambda: self._exito(ruta_salida))
        except Exception as e:
            self.root.after(0, lambda: self._error(str(e)))

    def _exito(self, ruta):
        self.label_estado.config(text="✅ PDF generado exitosamente", fg="#27ae60")
        self.btn_convertir.config(state="normal")
        ruta_abs = os.path.abspath(ruta)
        if messagebox.askyesno(
            "¿Comprimir?",
            "PDF generado exitosamente.\n\n¿Deseas comprimir el archivo para reducir su tamaño?"
        ):
            subprocess.Popen(
                [sys.executable, "app_comprimir.py"],
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
        else:
            if messagebox.askyesno("¡Listo!", f"Ubicación:\n{ruta_abs}\n\n¿Deseas abrirlo?"):
                os.startfile(ruta_abs)

    def _error(self, msg):
        self.label_estado.config(text="❌ Error en la conversión", fg="red")
        self.btn_convertir.config(state="normal")
        messagebox.showerror("Error", f"Ocurrió un error:\n{msg}")


if __name__ == "__main__":
    root = tk.Tk()
    app  = AppImagenPDF(root)
    root.mainloop()