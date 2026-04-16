import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
import sys
import subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modules.conversor import combinar_pdfs

BG       = "#f0f4f8"
ROJO     = "#c0392b"
BLANCO   = "#ffffff"
GRIS_TX  = "#444444"
GRIS_SUB = "#888888"


class AppCombinarPDF:
    def __init__(self, root):
        self.root = root
        self.root.title("Combinar PDFs")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)
        self.archivos = []
        self._construir_ui()

    def _construir_ui(self):
        # ── Encabezado ──────────────────────────────────
        header = tk.Frame(self.root, bg=ROJO, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="  Combinar PDFs",
            font=("Helvetica", 18, "bold"),
            bg=ROJO, fg=BLANCO
        ).place(relx=0.5, rely=0.45, anchor="center")

        tk.Label(
            header,
            text="Une varios archivos PDF en uno solo",
            font=("Helvetica", 9),
            bg=ROJO, fg="#f5b7b1"
        ).place(relx=0.5, rely=0.82, anchor="center")

        # ── Botones agregar / limpiar ────────────────────
        frame_botones = tk.Frame(self.root, bg=BG)
        frame_botones.pack(pady=15)

        tk.Button(
            frame_botones,
            text="  Agregar PDF(s)",
            font=("Helvetica", 11),
            bg=ROJO, fg=BLANCO,
            padx=10, pady=8,
            relief="flat", cursor="hand2",
            command=self._agregar
        ).grid(row=0, column=0, padx=8)

        tk.Button(
            frame_botones,
            text="🗑  Limpiar lista",
            font=("Helvetica", 11),
            bg="#95a5a6", fg=BLANCO,
            padx=10, pady=8,
            relief="flat", cursor="hand2",
            command=self._limpiar
        ).grid(row=0, column=1, padx=8)

        # ── Lista de archivos ────────────────────────────
        tk.Label(
            self.root,
            text="Orden de combinación (el PDF final respetará este orden):",
            font=("Helvetica", 9, "bold"),
            bg=BG, fg=GRIS_TX
        ).pack(padx=30, anchor="w")

        marco_lista = tk.Frame(self.root, bg=BLANCO,
                               highlightthickness=1,
                               highlightbackground="#dce6ef")
        marco_lista.pack(padx=30, fill="x", pady=4)

        self.lista_box = tk.Listbox(
            marco_lista,
            font=("Helvetica", 9),
            bg=BLANCO, fg=GRIS_TX,
            selectbackground=ROJO,
            height=8,
            bd=0,
            highlightthickness=0
        )
        self.lista_box.pack(fill="x", padx=5, pady=5)

        # ── Botones subir / bajar orden ──────────────────
        frame_orden = tk.Frame(self.root, bg=BG)
        frame_orden.pack(pady=4)

        tk.Button(
            frame_orden,
            text="⬆  Subir",
            font=("Helvetica", 9),
            bg="#ecf0f1", fg=GRIS_TX,
            padx=8, pady=4,
            relief="flat", cursor="hand2",
            command=self._subir
        ).grid(row=0, column=0, padx=6)

        tk.Button(
            frame_orden,
            text="⬇  Bajar",
            font=("Helvetica", 9),
            bg="#ecf0f1", fg=GRIS_TX,
            padx=8, pady=4,
            relief="flat", cursor="hand2",
            command=self._bajar
        ).grid(row=0, column=1, padx=6)

        tk.Button(
            frame_orden,
            text="  Quitar seleccionado",
            font=("Helvetica", 9),
            bg="#ecf0f1", fg=GRIS_TX,
            padx=8, pady=4,
            relief="flat", cursor="hand2",
            command=self._quitar
        ).grid(row=0, column=2, padx=6)

        self.label_info = tk.Label(
            self.root,
            text="Agrega al menos 2 archivos PDF",
            font=("Helvetica", 9),
            bg=BG, fg=GRIS_SUB
        )
        self.label_info.pack(pady=4)

        # ── Botón combinar ───────────────────────────────
        self.btn_combinar = tk.Button(
            self.root,
            text="  Combinar PDFs",
            font=("Helvetica", 12, "bold"),
            bg="#95a5a6", fg=BLANCO,
            padx=15, pady=10,
            relief="flat", cursor="hand2",
            command=self._combinar,
            state="disabled"
        )
        self.btn_combinar.pack(pady=8)

        # ── Estado ───────────────────────────────────────
        self.label_estado = tk.Label(
            self.root, text="",
            font=("Helvetica", 10),
            bg=BG, fg=ROJO
        )
        self.label_estado.pack()

    def _agregar(self):
        rutas = filedialog.askopenfilenames(
            title="Seleccionar PDFs",
            filetypes=[("Archivos PDF", "*.pdf")]
        )
        if rutas:
            for r in rutas:
                if r not in self.archivos:
                    self.archivos.append(r)
            self._actualizar_lista()

    def _actualizar_lista(self):
        self.lista_box.delete(0, tk.END)
        for i, r in enumerate(self.archivos, 1):
            self.lista_box.insert(tk.END, f"  {i}. {os.path.basename(r)}")

        total = len(self.archivos)
        if total >= 2:
            self.label_info.config(
                text=f" {total} archivos listos para combinar",
                fg="#27ae60"
            )
            self.btn_combinar.config(state="normal", bg=ROJO)
        else:
            self.label_info.config(
                text=f"{total} archivo(s) — agrega al menos 2",
                fg=GRIS_SUB
            )
            self.btn_combinar.config(state="disabled", bg="#95a5a6")

    def _limpiar(self):
        self.archivos = []
        self._actualizar_lista()
        self.label_estado.config(text="")

    def _subir(self):
        sel = self.lista_box.curselection()
        if sel and sel[0] > 0:
            i = sel[0]
            self.archivos[i - 1], self.archivos[i] = self.archivos[i], self.archivos[i - 1]
            self._actualizar_lista()
            self.lista_box.selection_set(i - 1)

    def _bajar(self):
        sel = self.lista_box.curselection()
        if sel and sel[0] < len(self.archivos) - 1:
            i = sel[0]
            self.archivos[i + 1], self.archivos[i] = self.archivos[i], self.archivos[i + 1]
            self._actualizar_lista()
            self.lista_box.selection_set(i + 1)

    def _quitar(self):
        sel = self.lista_box.curselection()
        if sel:
            self.archivos.pop(sel[0])
            self._actualizar_lista()

    def _combinar(self):
        self.btn_combinar.config(state="disabled")
        self.label_estado.config(text="Combinando PDFs...", fg=ROJO)
        threading.Thread(target=self._proceso).start()

    def _proceso(self):
        try:
            ruta_salida = filedialog.asksaveasfilename(
                title="Guardar PDF combinado como",
                defaultextension=".pdf",
                filetypes=[("PDF", "*.pdf")],
                initialfile="combinado.pdf"
            )
            if not ruta_salida:
                self.root.after(0, lambda: self.label_estado.config(text=""))
                self.root.after(0, lambda: self.btn_combinar.config(state="normal"))
                return

            combinar_pdfs(self.archivos, ruta_salida)
            self.root.after(0, lambda: self._exito(ruta_salida))
        except Exception as e:
            self.root.after(0, lambda: self._error(str(e)))

    def _exito(self, ruta):
        self.label_estado.config(text=" PDFs combinados exitosamente", fg="#27ae60")
        self.btn_combinar.config(state="normal")
        ruta_abs = os.path.abspath(ruta)
        if messagebox.askyesno(
            "¿Comprimir?",
            "PDFs combinados exitosamente.\n\n¿Deseas comprimir el archivo para reducir su tamaño?"
        ):
            subprocess.Popen(
                [sys.executable, "app_comprimir.py"],
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
        else:
            if messagebox.askyesno("¡Listo!", f"Ubicación:\n{ruta_abs}\n\n¿Deseas abrirlo?"):
                os.startfile(ruta_abs)

    def _error(self, msg):
        self.label_estado.config(text=" Error al combinar", fg="red")
        self.btn_combinar.config(state="normal")
        messagebox.showerror("Error", f"Ocurrió un error:\n{msg}")


if __name__ == "__main__":
    root = tk.Tk()
    app  = AppCombinarPDF(root)
    root.mainloop()