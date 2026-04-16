import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
import sys
import subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modules.conversor import dividir_pdf, obtener_num_paginas

BG       = "#f0f4f8"
VERDE    = "#16a085"
BLANCO   = "#ffffff"
GRIS_TX  = "#444444"
GRIS_SUB = "#888888"


class AppDividirPDF:
    def __init__(self, root):
        self.root = root
        self.root.title("Dividir PDF")
        self.root.geometry("500x520")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)
        self.archivo     = ""
        self.num_paginas = 0
        self._construir_ui()

    def _construir_ui(self):
        # ── Encabezado ──────────────────────────────────
        header = tk.Frame(self.root, bg=VERDE, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="  Dividir PDF",
            font=("Helvetica", 18, "bold"),
            bg=VERDE, fg=BLANCO
        ).place(relx=0.5, rely=0.45, anchor="center")

        tk.Label(
            header,
            text="Separa un PDF en partes o páginas individuales",
            font=("Helvetica", 9),
            bg=VERDE, fg="#a2d9ce"
        ).place(relx=0.5, rely=0.82, anchor="center")

        # ── Botón seleccionar ────────────────────────────
        tk.Button(
            self.root,
            text="  Seleccionar PDF",
            font=("Helvetica", 11),
            bg=VERDE, fg=BLANCO,
            padx=10, pady=8,
            relief="flat", cursor="hand2",
            command=self._seleccionar
        ).pack(pady=18)

        # ── Info archivo ─────────────────────────────────
        self.label_archivo = tk.Label(
            self.root,
            text="Ningún archivo seleccionado",
            font=("Helvetica", 9),
            bg=BG, fg=GRIS_SUB,
            wraplength=420,
            justify="center"
        )
        self.label_archivo.pack()

        # ── Modo de división ─────────────────────────────
        marco_modo = tk.Frame(self.root, bg=BLANCO,
                              highlightthickness=1,
                              highlightbackground="#dce6ef")
        marco_modo.pack(padx=30, pady=12, fill="x")

        tk.Label(
            marco_modo,
            text="Modo de división:",
            font=("Helvetica", 10, "bold"),
            bg=BLANCO, fg=GRIS_TX
        ).pack(anchor="w", padx=12, pady=(10, 4))

        self.modo = tk.StringVar(value="todas")

        tk.Radiobutton(
            marco_modo,
            text="Extraer todas las páginas por separado",
            variable=self.modo,
            value="todas",
            font=("Helvetica", 10),
            bg=BLANCO, fg=GRIS_TX,
            activebackground=BLANCO,
            selectcolor=BLANCO,
            command=self._actualizar_modo
        ).pack(anchor="w", padx=20, pady=2)

        tk.Radiobutton(
            marco_modo,
            text="Extraer un rango de páginas",
            variable=self.modo,
            value="rango",
            font=("Helvetica", 10),
            bg=BLANCO, fg=GRIS_TX,
            activebackground=BLANCO,
            selectcolor=BLANCO,
            command=self._actualizar_modo
        ).pack(anchor="w", padx=20, pady=2)

        # ── Frame rango ──────────────────────────────────
        self.frame_rango = tk.Frame(marco_modo, bg=BLANCO)
        self.frame_rango.pack(anchor="w", padx=40, pady=(2, 10))

        tk.Label(
            self.frame_rango,
            text="Desde página:",
            font=("Helvetica", 9),
            bg=BLANCO, fg=GRIS_TX
        ).grid(row=0, column=0, padx=4, pady=4)

        self.entrada_desde = tk.Entry(
            self.frame_rango,
            font=("Helvetica", 10),
            width=6,
            justify="center"
        )
        self.entrada_desde.insert(0, "1")
        self.entrada_desde.grid(row=0, column=1, padx=4)

        tk.Label(
            self.frame_rango,
            text="Hasta página:",
            font=("Helvetica", 9),
            bg=BLANCO, fg=GRIS_TX
        ).grid(row=0, column=2, padx=4)

        self.entrada_hasta = tk.Entry(
            self.frame_rango,
            font=("Helvetica", 10),
            width=6,
            justify="center"
        )
        self.entrada_hasta.insert(0, "1")
        self.entrada_hasta.grid(row=0, column=3, padx=4)

        self.label_total_pags = tk.Label(
            self.frame_rango,
            text="",
            font=("Helvetica", 8),
            bg=BLANCO, fg=GRIS_SUB
        )
        self.label_total_pags.grid(row=1, column=0, columnspan=4, pady=2)

        # Ocultar rango al inicio
        self.frame_rango.pack_forget()

        # ── Botón dividir ────────────────────────────────
        self.btn_dividir = tk.Button(
            self.root,
            text="  Dividir PDF",
            font=("Helvetica", 12, "bold"),
            bg="#95a5a6", fg=BLANCO,
            padx=15, pady=10,
            relief="flat", cursor="hand2",
            command=self._dividir,
            state="disabled"
        )
        self.btn_dividir.pack(pady=12)

        # ── Estado ───────────────────────────────────────
        self.label_estado = tk.Label(
            self.root, text="",
            font=("Helvetica", 10),
            bg=BG, fg=VERDE
        )
        self.label_estado.pack()

    def _actualizar_modo(self):
        if self.modo.get() == "rango":
            self.frame_rango.pack(anchor="w", padx=40, pady=(2, 10))
        else:
            self.frame_rango.pack_forget()

    def _seleccionar(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar PDF",
            filetypes=[("Archivos PDF", "*.pdf")]
        )
        if ruta:
            try:
                self.num_paginas = obtener_num_paginas(ruta)
                self.archivo = ruta
                nombre = os.path.basename(ruta)
                self.label_archivo.config(
                    text=f"  {nombre}  —  {self.num_paginas} página(s)",
                    fg="#27ae60"
                )
                self.entrada_hasta.delete(0, tk.END)
                self.entrada_hasta.insert(0, str(self.num_paginas))
                self.label_total_pags.config(
                    text=f"El PDF tiene {self.num_paginas} páginas en total"
                )
                self.btn_dividir.config(state="normal", bg=VERDE)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el PDF:\n{e}")

    def _dividir(self):
        self.btn_dividir.config(state="disabled")
        self.label_estado.config(text="Dividiendo PDF...", fg=VERDE)
        threading.Thread(target=self._proceso).start()

    def _proceso(self):
        try:
            ruta_salida_dir = filedialog.askdirectory(
                title="Seleccionar carpeta donde guardar las partes"
            )
            if not ruta_salida_dir:
                self.root.after(0, lambda: self.label_estado.config(text=""))
                self.root.after(0, lambda: self.btn_dividir.config(state="normal"))
                return

            if self.modo.get() == "todas":
                archivos = dividir_pdf(self.archivo, ruta_salida_dir)
            else:
                try:
                    desde = int(self.entrada_desde.get())
                    hasta = int(self.entrada_hasta.get())
                except ValueError:
                    raise ValueError("Los números de página deben ser enteros.")

                archivos = dividir_pdf(
                    self.archivo,
                    ruta_salida_dir,
                    paginas=[(desde, hasta)]
                )

            self.root.after(0, lambda: self._exito(ruta_salida_dir, len(archivos)))
        except Exception as e:
            self.root.after(0, lambda: self._error(str(e)))

    def _exito(self, carpeta, total):
        self.label_estado.config(
            text=f" {total} archivo(s) generado(s)", fg="#27ae60"
        )
        self.btn_dividir.config(state="normal")
        if messagebox.askyesno(
            "¿Comprimir?",
            f"Se generaron {total} archivo(s) exitosamente.\n\n¿Deseas comprimir alguno para reducir su tamaño?"
        ):
            subprocess.Popen(
                [sys.executable, "app_comprimir.py"],
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
        else:
            if messagebox.askyesno("¡Listo!", f"Archivos guardados en:\n{carpeta}\n\n¿Deseas abrir la carpeta?"):
                os.startfile(carpeta)

    def _error(self, msg):
        self.label_estado.config(text=" Error al dividir", fg="red")
        self.btn_dividir.config(state="normal")
        messagebox.showerror("Error", f"Ocurrió un error:\n{msg}")


if __name__ == "__main__":
    root = tk.Tk()
    app  = AppDividirPDF(root)
    root.mainloop()