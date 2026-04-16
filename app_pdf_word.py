import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
import sys
import subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modules.conversor import pdf_a_word

BG       = "#f0f4f8"
MORADO   = "#8e44ad"
BLANCO   = "#ffffff"
GRIS_TX  = "#444444"
GRIS_SUB = "#888888"


class AppPDFWord:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF a Word")
        self.root.geometry("500x380")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)
        self.archivo = ""
        self._construir_ui()

    def _construir_ui(self):
        # ── Encabezado ──────────────────────────────────
        header = tk.Frame(self.root, bg=MORADO, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="📄  PDF a Word",
            font=("Helvetica", 18, "bold"),
            bg=MORADO, fg=BLANCO
        ).place(relx=0.5, rely=0.45, anchor="center")

        tk.Label(
            header,
            text="Convierte un documento PDF a formato Word (.docx)",
            font=("Helvetica", 9),
            bg=MORADO, fg="#e8d5f5"
        ).place(relx=0.5, rely=0.82, anchor="center")

        # ── Botón seleccionar ────────────────────────────
        tk.Button(
            self.root,
            text="📂  Seleccionar PDF",
            font=("Helvetica", 11),
            bg=MORADO, fg=BLANCO,
            padx=10, pady=8,
            relief="flat", cursor="hand2",
            command=self._seleccionar
        ).pack(pady=25)

        # ── Archivo seleccionado ─────────────────────────
        self.label_archivo = tk.Label(
            self.root,
            text="Ningún archivo seleccionado",
            font=("Helvetica", 9),
            bg=BG, fg=GRIS_SUB,
            wraplength=420,
            justify="center"
        )
        self.label_archivo.pack(pady=5)

        # ── Aviso ────────────────────────────────────────
        marco_aviso = tk.Frame(self.root, bg="#fef9e7",
                               highlightthickness=1,
                               highlightbackground="#f9ca24")
        marco_aviso.pack(padx=30, pady=10, fill="x")

        tk.Label(
            marco_aviso,
            text="⚠️  La conversión puede tardar unos segundos dependiendo\n"
                 "del tamaño del PDF. Los PDFs escaneados pueden no convertirse bien.",
            font=("Helvetica", 8),
            bg="#fef9e7", fg="#7d6608",
            justify="center", pady=8
        ).pack()

        # ── Botón convertir ──────────────────────────────
        self.btn_convertir = tk.Button(
            self.root,
            text="▶  Convertir a Word",
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
            bg=BG, fg=MORADO
        )
        self.label_estado.pack()

    def _seleccionar(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar PDF",
            filetypes=[("Archivos PDF", "*.pdf")]
        )
        if ruta:
            self.archivo = ruta
            nombre = os.path.basename(ruta)
            self.label_archivo.config(
                text=f"✅  {nombre}",
                fg="#27ae60"
            )
            self.btn_convertir.config(state="normal", bg=MORADO)

    def _convertir(self):
        self.btn_convertir.config(state="disabled")
        self.label_estado.config(text="Convirtiendo, por favor espera...", fg=MORADO)
        threading.Thread(target=self._proceso).start()

    def _proceso(self):
        try:
            nombre_base = os.path.splitext(os.path.basename(self.archivo))[0]
            ruta_salida = filedialog.asksaveasfilename(
                title="Guardar Word como",
                defaultextension=".docx",
                filetypes=[("Word", "*.docx")],
                initialfile=f"{nombre_base}.docx"
            )
            if not ruta_salida:
                self.root.after(0, lambda: self.label_estado.config(text=""))
                self.root.after(0, lambda: self.btn_convertir.config(state="normal"))
                return

            pdf_a_word(self.archivo, ruta_salida)
            self.root.after(0, lambda: self._exito(ruta_salida))
        except Exception as e:
            self.root.after(0, lambda: self._error(str(e)))

    def _exito(self, ruta):
        self.label_estado.config(text="✅ Documento Word generado", fg="#27ae60")
        self.btn_convertir.config(state="normal")
        ruta_abs = os.path.abspath(ruta)
        if messagebox.askyesno(
            "¿Comprimir?",
            "Documento Word generado exitosamente.\n\n¿Deseas comprimir el archivo para reducir su tamaño?"
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
    app  = AppPDFWord(root)
    root.mainloop()