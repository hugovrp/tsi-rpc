import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import customtkinter as ctk 
from client.operations import Operations
from client.rpc_exception import RPCServerNotFound

# Tema e Cores
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class RPCGui:
    def __init__(self, root):
        self.root = root
        self.root.title("RPC Multi-Server Interface")
        self.root.geometry("1680x820") 
        
        self.op = Operations()
        
        self.stored_value = None
        self.pending_operator = None  
        self.waiting_for_next = False 
        
        self._setup_ui()

    def _setup_ui(self):
        self.root.grid_columnconfigure(0, weight=3) # Coluna da Calculadora
        self.root.grid_columnconfigure(1, weight=2) # Coluna do Solver/Logs
        self.root.grid_rowconfigure(0, weight=1)

        # Frame Calculadora
        self.calc_frame = ctk.CTkFrame(self.root, corner_radius=15)
        self.calc_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        
        self.display = ctk.CTkEntry(self.calc_frame, font=("Consolas", 42), height=90, justify="right", corner_radius=10, border_width=2)
        self.display.pack(fill="x", padx=20, pady=(20, 10))
        self.display.insert(0, "0")

        # Grid dos botões numéricos e operadores
        self.btns_container = ctk.CTkFrame(self.calc_frame, fg_color="transparent")
        self.btns_container.pack(expand=True, fill="both", padx=10, pady=10)

        buttons = [
            ('C', 0, 0, "gray"), ('←', 0, 1, "gray"), ('!', 0, 2, "#d35400"), ('/', 0, 3, "#d35400"),
            ('7', 1, 0, None),   ('8', 1, 1, None),   ('9', 1, 2, None),     ('*', 1, 3, "#d35400"),
            ('4', 2, 0, None),   ('5', 2, 1, None),   ('6', 2, 2, None),     ('-', 2, 3, "#d35400"),
            ('1', 3, 0, None),   ('2', 3, 1, None),   ('3', 3, 2, None),     ('+', 3, 3, "#d35400"),
            ('0', 4, 0, None),   ('.', 4, 1, None),   ('?', 4, 2, "#d35400"), ('=', 4, 3, "#2980b9")
        ]

        for (text, r, c, color) in buttons:
            cmd = lambda t=text: self._on_button_click(t)
            btn = ctk.CTkButton(self.btns_container, text=text, width=80, height=80, font=("Arial", 22, "bold"), command=cmd, fg_color=color if color else "#333333")
            btn.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")

        for i in range(4): self.btns_container.grid_columnconfigure(i, weight=1)
        for i in range(5): self.btns_container.grid_rowconfigure(i, weight=1)

        # Frame Solver/Logs
        self.side_frame = ctk.CTkFrame(self.root, corner_radius=15)
        self.side_frame.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")

        # Dica
        self.hint_frame = ctk.CTkFrame(self.side_frame, fg_color="#2980b9", corner_radius=10)
        self.hint_frame.pack(fill="x", padx=20, pady=(20,10))

        hint_text = "DICA: Para expressões complexas\n(parênteses, raiz, etc.), uso o Solver abaixo."
        self.hint_label = ctk.CTkLabel(self.hint_frame, text=hint_text, font=("Arial", 14, "bold"))
        self.hint_label.pack(pady=10)

        ctk.CTkLabel(self.side_frame, text="IA Solver", font=("Arial", 18, "bold")).pack(pady=(20, 5))
        self.solver_entry = ctk.CTkEntry(self.side_frame, placeholder_text="Descreva o problema...", height=45)
        self.solver_entry.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkButton(self.side_frame, text="Resolver com IA", fg_color="#27ae60", command=self.do_solver).pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(self.side_frame, text="Notícias Atualizadas", fg_color="#16a085", command=self.get_news).pack(pady=5, padx=20, fill="x")

        self.log_area = scrolledtext.ScrolledText(self.side_frame, bg="#111", fg="#0f0", font=("Consolas", 10), borderwidth=0)
        self.log_area.pack(fill="both", expand=True, padx=20, pady=20)

    def _on_button_click(self, char):
        if char.isdigit() or char == '.':
            self._press_digit(char)
        elif char == 'C':
            self._clear()
        elif char == '←':
            self._backspace()
        elif char in ['+', '-', '*', '/']:
            self._handle_operator(char)
        elif char == '=':
            self._execute_calc()
        elif char in ['!', '?']:
            self._handle_unary(char)

    def _press_digit(self, d):
        if self.waiting_for_next:
            self.display.delete(0, tk.END)
            self.waiting_for_next = False
        
        current = self.display.get()
        if current == "0" and d != ".": self.display.delete(0, tk.END)
        self.display.insert(tk.END, d)

    def _clear(self):
        self.display.delete(0, tk.END)
        self.display.insert(0, "0")
        self.stored_value = None
        self.pending_operator = None

    def _backspace(self):
        val = self.display.get()
        if val != "0":
            self.display.delete(len(val)-1, tk.END)
            if not self.display.get(): self.display.insert(0, "0")

    def _handle_operator(self, op_char):
        # Mapeamento dos botões com as operações
        ops_map = {'+': self.op.sum, '-': self.op.sub, '*': self.op.prod, '/': self.op.div}
        
        current_val = float(self.display.get())

        # Encadeamento: Se já tem algo pendente, calcula primeiro
        if self.stored_value is not None and not self.waiting_for_next:
            self._execute_calc(next_op=ops_map[op_char])
        else:
            self.stored_value = current_val
            self.pending_operator = ops_map[op_char]
            self.waiting_for_next = True
            self._log(f"Operação: {current_val} {op_char}")

    def _execute_calc(self, next_op=None):
        if self.pending_operator is None: return

        val1 = self.stored_value
        val2 = float(self.display.get())
        
        self._log(f"Chamando RPC: {self.pending_operator.__name__}({val1}, {val2})")
        
        def task():
            try:
                res = self.pending_operator(val1, val2)
                self.root.after(0, lambda: self._update_ui_after_rpc(res, next_op))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Erro RPC", str(e)))

        threading.Thread(target=task, daemon=True).start()

    def _update_ui_after_rpc(self, result, next_op):
        self.display.delete(0, tk.END)
        self.display.insert(0, str(result))
        self._log(f"Resultado: {result}")
        
        self.stored_value = float(result) if next_op else None
        self.pending_operator = next_op
        self.waiting_for_next = True

    def _handle_unary(self, char):
        val = int(float(self.display.get()))
        func = self.op.fat if char == '!' else self.op.prim
        self._log(f"Processando {char} para {val}...")
        
        threading.Thread(target=lambda: self._run_unary(func, val), daemon=True).start()

    def _run_unary(self, func, val):
        try:
            res = func(val)
            self.root.after(0, lambda: self._update_ui_after_rpc(res, None))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro", str(e)))

    def do_solver(self):
        prob = self.solver_entry.get()
        if not prob: return
        self._log(f"IA Solver: {prob}")
        threading.Thread(target=lambda: self._run_solver(prob), daemon=True).start()

    def _run_solver(self, prob):
        try:
            res = self.op.solver(prob)
            self.root.after(0, lambda: self._log(f"IA Resposta: {res}"))
        except Exception as e:
            self.root.after(0, lambda: self._log(f"Erro IA: {e}"))

    def get_news(self):
        self._log("Buscando notícias...")
        threading.Thread(target=self._run_news, daemon=True).start()

    def _run_news(self):
        try:
            news = self.op.news()
            self.root.after(0, lambda: [self._log(f"• {n}") for n in news])
        except Exception as e:
            self.root.after(0, lambda: self._log(f"Erro Notícias: {e}"))

    def _log(self, msg):
        self.log_area.insert(tk.END, f"> {msg}\n")
        self.log_area.see(tk.END)

if __name__ == "__main__":
    root = ctk.CTk()
    app = RPCGui(root)
    root.mainloop()