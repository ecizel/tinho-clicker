import sys
import os
import ctypes
import tkinter as tk
import pydirectinput as pdi
import keyboard as kb
from time import sleep
from multiprocessing import Process, freeze_support

# --- FUNÇÃO PARA CORRIGIR CAMINHO NO .EXE ---
def resource_path(relative_path):
    try:
        # Caminho temporário do PyInstaller
        base_path = sys._MEIPASS
    except Exception:
        # Caminho em .py (dev)
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- FIX DE NITIDEZ DA TELA ---
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    try: ctypes.windll.user32.SetProcessDPIAware()
    except: pass

# a lógica de clicar
def loop_de_cliques(intervalo, duracao):
    # tira delay do pydirectinput
    pdi.PAUSE = 0
    try:
        if duracao == 0:
            while True:
                pdi.click(None, None, 1, intervalo, 'left')
        else:
            while True:
                pdi.mouseDown()
                sleep(duracao)
                pdi.mouseUp()
                sleep(intervalo)
    except:
        pass

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("TinhoClicker")

        self.root.attributes("-topmost", True)

        self.root.bind("<FocusIn>", self.ganhar_foco)
        self.root.bind("<FocusOut>", self.perder_foco)

        largura, altura = 320, 300
        cor_fundo = "#FFE8D8"  
        cor_linha_topo = "#FF4400" 
        cor_linha_menu = "#F96F38" 
        
        self.root.configure(bg=cor_fundo)
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (largura // 2)
        y = int((screen_height // 2) - (altura // 2) - (screen_height * 0.05))
        y = max(0, y)
        
        self.root.geometry(f"{largura}x{altura}+{x}+{y}")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)

        self.processo = None
        fonte_texto = ("Segoe UI", 10)
        fonte_status = ("Segoe UI", 12, "bold")

        tk.Frame(root, height=2, bg=cor_linha_topo, bd=0).pack(fill='x', side='top')

        tk.Label(root, text="TINHO CLICKER", font=("Segoe UI", 14, "bold"), 
                 bg=cor_fundo, fg="#333").pack(pady=(10, 5))
        
        tk.Frame(root, height=1, bg=cor_linha_menu, bd=0).pack(fill='x', padx=50, pady=(0, 10))

        tk.Label(root, text="Intervalo entre clicks:", font=fonte_texto, bg=cor_fundo).pack()
        self.ent_intervalo = tk.Entry(root, font=fonte_texto, justify='center', width=10)
        self.ent_intervalo.insert(0, "0.05")
        self.ent_intervalo.pack(pady=2)

        tk.Label(root, text="Duração do click:", font=fonte_texto, bg=cor_fundo).pack()
        self.ent_duracao = tk.Entry(root, font=fonte_texto, justify='center', width=10)
        self.ent_duracao.insert(0, "0.0")
        self.ent_duracao.pack(pady=2)

        tk.Label(root, text="Atalho: F8", font=fonte_texto, bg=cor_fundo, fg="#444").pack(pady=5)

        self.lbl_status = tk.Label(root, text="STATUS: PARADO", font=fonte_status, 
                                   bg=cor_fundo, fg="#CC0000")
        self.lbl_status.pack(pady=10)

        kb.add_hotkey('f8', self.alternar)

    def ganhar_foco(self, event=None):
        self.root.attributes("-topmost", True)

    def perder_foco(self, event=None):
        self.root.attributes("-topmost", False)

    def alternar(self, event=None):
        sleep(0.1) # delay ao segurar f8
        if self.processo is None or not self.processo.is_alive():
            try:
                txt_int = self.ent_intervalo.get().replace(',', '.')
                val_intervalo = float(txt_int)
                
                txt_dur = self.ent_duracao.get().replace(',', '.')
                val_duracao = float(txt_dur)
            except ValueError:
                val_intervalo = 0.05
                val_duracao = 0.0
            
            self.processo = Process(target=loop_de_cliques, args=(val_intervalo, val_duracao))
            self.processo.daemon = True
            self.processo.start()
            self.lbl_status.config(text="STATUS: RODANDO", fg="#005500")
        else:
            self.parar_processo()

    def parar_processo(self):
        if self.processo:
            self.processo.terminate()
            self.processo.join()
            self.processo = None
            try:
                if self.root.winfo_exists():
                    self.lbl_status.config(text="STATUS: PARADO", fg="#CC0000")
            except:
                pass

if __name__ == '__main__':
    freeze_support()
    
    root = tk.Tk()
    app = App(root)
    
    try:
        root.mainloop()
    finally:
        app.parar_processo()