import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modules.conversor import comprimir_pdf, comprimir_imagen, tamaño_legible

BG       = "#f0f4f8"
COLOR    = "#2980b9"
BLANCO   = "#ffffff"
GRIS_TX  = "#444444"
GRIS_SUB = "#888888"


class AppComprimir:
    def __init__(self, root):
        self.root = root
        self.root.title("Comprimir archivo")
        self.root.geometry("500x530")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)
        self.archivo = ""
        self.tipo    = ""
        self._construir_ui()

    def _construir_ui(self):
        # ── Encabezado ──────────────────────────────────
        header = tk.Frame(self.root, bg=COLOR, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="  Comprimir archivo",
            font=("Helvetica", 18, "bold"),
            bg=COLOR, fg=BLANCO
        ).place(relx=0.5, rely=0.45, anchor="center")

        tk.Label(
            header,
            text="Reduce el tamaño de PDFs e imágenes JPG/PNG",
            font=("Helvetica", 9),
            bg=COLOR, fg="#d6eaf8"
        ).place(relx=0.5, rely=0.82, anchor="center")

        # ── Botón seleccionar ────────────────────────────
        tk.Button(
            self.root,
            text="  Seleccionar archivo",
            font=("Helvetica", 11),
            bg=COLOR, fg=BLANCO,
            padx=10, pady=8,
            relief="flat", cursor="hand2",
            command=self._seleccionar
        ).pack(pady=18)

        # ── Info archivo 
        self.label_archivo = tk.Label(
            self.root,
            text="Ningún archivo seleccionado",
            font=("Helvetica", 9),
            bg=BG, fg=GRIS_SUB,
            wraplength=420,
            justify="center"
        )
        self.label_archivo.pack()

        # ── Nivel de compresión 
        marco_nivel = tk.Frame(self.root, bg=BLANCO,
                               highlightthickness=1,
                               highlightbackground="#dce6ef")
        marco_nivel.pack(padx=30, pady=14, fill="x")

        tk.Label(
            marco_nivel,
            text="Nivel de compresión:",
            font=("Helvetica", 10, "bold"),
            bg=BLANCO, fg=GRIS_TX
        ).pack(anchor="w", padx=14, pady=(10, 6))

        # Slider
        self.nivel_var = tk.IntVar(value=1)
        frame_slider = tk.Frame(marco_nivel, bg=BLANCO)
        frame_slider.pack(padx=14, pady=(0, 4), fill="x")

        tk.Label(frame_slider, text="Baja", font=("Helvetica", 9),
                 bg=BLANCO, fg=GRIS_SUB).pack(side="left")

        self.slider = tk.Scale(
            frame_slider,
            from_=0, to=2,
            orient="horizontal",
            variable=self.nivel_var,
            showvalue=False,
            bg=BLANCO,
            fg=COLOR,
            highlightthickness=0,
            troughcolor="#dce6ef",
            activebackground=COLOR,
            command=self._actualizar_nivel
        )
        self.slider.pack(side="left", fill="x", expand=True, padx=8)

        tk.Label(frame_slider, text="Alta", font=("Helvetica", 9),
                 bg=BLANCO, fg=GRIS_SUB).pack(side="left")

        self.label_nivel = tk.Label(
            marco_nivel,
            text="⚖️  Media  —  Balance entre calidad y tamaño",
            font=("Helvetica", 9, "bold"),
            bg=BLANCO, fg=COLOR
        )
        self.label_nivel.pack(pady=(0, 10))

        # ── Resultado 
        self.marco_resultado = tk.Frame(self.root, bg="#eafaf1",
                                        highlightthickness=1,
                                        highlightbackground="#27ae60")
        self.marco_resultado.pack(padx=30, fill="x")
        self.marco_resultado.pack_forget()

        self.label_resultado = tk.Label(
            self.marco_resultado,
            text="",
            font=("Helvetica", 10),
            bg="#eafaf1", fg="#1e8449",
            justify="center", pady=10
        )
        self.label_resultado.pack()

        # ── Botón comprimir 
        self.btn_comprimir = tk.Button(
            self.root,
            text="▶  Comprimir",
            font=("Helvetica", 12, "bold"),
            bg="#95a5a6", fg=BLANCO,
            padx=15, pady=10,
            relief="flat", cursor="hand2",
            command=self._comprimir,
            state="disabled"
        )
        self.btn_comprimir.pack(pady=14)

        # ── Estado 
        self.label_estado = tk.Label(
            self.root, text="",
            font=("Helvetica", 10),
            bg=BG, fg=COLOR
        )
        self.label_estado.pack()

    def _actualizar_nivel(self, _=None):
        textos = [
            "  Baja  —  Mayor calidad, menor reducción",
            "  Media  —  Balance entre calidad y tamaño",
            "  Alta  —  Máxima reducción, algo de pérdida",
        ]
        self.label_nivel.config(text=textos[self.nivel_var.get()])

    def _nivel_str(self):
        return ["baja", "media", "alta"][self.nivel_var.get()]

    def _seleccionar(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=[
                ("Archivos compatibles", "*.pdf *.jpg *.jpeg *.png"),
                ("PDF", "*.pdf"),
                ("Imágenes", "*.jpg *.jpeg *.png"),
            ]
        )
        if ruta:
            self.archivo = ruta
            ext = os.path.splitext(ruta)[1].lower()
            self.tipo = "pdf" if ext == ".pdf" else "imagen"
            nombre = os.path.basename(ruta)
            tam    = tamaño_legible(ruta)
            self.label_archivo.config(
                text=f"✅  {nombre}  —  {tam}",
                fg="#27ae60"
            )
            self.btn_comprimir.config(state="normal", bg=COLOR)
            self.marco_resultado.pack_forget()
            self.label_estado.config(text="")

    def _comprimir(self):
        self.btn_comprimir.config(state="disabled")
        self.label_estado.config(text="Comprimiendo...", fg=COLOR)
        self.marco_resultado.pack_forget()
        threading.Thread(target=self._proceso).start()

    def _proceso(self):
        try:
            nombre_base = os.path.splitext(os.path.basename(self.archivo))[0]
            ext         = os.path.splitext(self.archivo)[1].lower()

            if self.tipo == "pdf":
                default_name = f"{nombre_base}_comprimido.pdf"
                ftypes = [("PDF", "*.pdf")]
            else:
                default_name = f"{nombre_base}_comprimido{ext}"
                ftypes = [("Imágenes", f"*{ext}")]

            ruta_salida = filedialog.asksaveasfilename(
                title="Guardar archivo comprimido como",
                defaultextension=ext if self.tipo == "imagen" else ".pdf",
                filetypes=ftypes,
                initialfile=default_name
            )
            if not ruta_salida:
                self.root.after(0, lambda: self.label_estado.config(text=""))
                self.root.after(0, lambda: self.btn_comprimir.config(state="normal"))
                return

            nivel = self._nivel_str()

            if self.tipo == "pdf":
                resultado = comprimir_pdf(self.archivo, ruta_salida, nivel)
            else:
                resultado = comprimir_imagen(self.archivo, ruta_salida, nivel)

            self.root.after(0, lambda: self._exito(resultado))
        except Exception as e:
            self.root.after(0, lambda: self._error(str(e)))

    def _exito(self, r):
        self.label_estado.config(text=" Archivo comprimido exitosamente", fg="#27ae60")
        self.btn_comprimir.config(state="normal")

        texto = (
            f"  Original:   {r['tam_original']} KB\n"
            f"  Comprimido: {r['tam_nuevo']} KB\n"
            f"   Reducción:  {r['reduccion']}%"
        )
        self.label_resultado.config(text=texto)
        self.marco_resultado.pack(padx=30, fill="x", before=self.btn_comprimir)

        if messagebox.askyesno("¡Listo!", f"Archivo guardado.\n\n{texto}\n\n¿Deseas abrirlo?"):
            os.startfile(os.path.abspath(r["ruta"]))

    def _error(self, msg):
        self.label_estado.config(text=" Error al comprimir", fg="red")
        self.btn_comprimir.config(state="normal")
        messagebox.showerror("Error", f"Ocurrió un error:\n{msg}")


if __name__ == "__main__":
    root = tk.Tk()
    app  = AppComprimir(root)
    root.mainloop()