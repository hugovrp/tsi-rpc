import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from client.operations import Operations
from client.rpc_exception import RPCServerNotFound

# Configurações de aparência
ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")

class RPCGui:
    """
        Interface Gráfica CustomTkinter para o sistema RPC.
        Gerencia a entrada do usuário, exibição de resultados e logs de operações remotas.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("RPC Multi-Server Interface")
        self.root.geometry("680x820")
        
        # Inicializa o RPC
        self.op = Operations()
        self._setup_ui()

    def _setup_ui(self):
        """
            Constrói e organiza todos os elementos visuais da interface gráfica.
            
            Este método utiliza uma combinação de 'grid' para o layout principal e 'pack' para agrupamentos internos.
            
            Componentes inicializados:
                1. Configuração de Grid: Define pesos (weight) para permitir expansão vertical da área de logs.
                2. Visor (Display): CTkEntry estilizado com fontes grandes para exibição de números e resultados rpc.
                3. Middle Frame: Container para o Teclado Numérico (grid 3x4) e para a coluna lateral de Operações Aritméticas.
                4. Solver Frame: Painel com cantos arredondados contendo um campo de texto dedicado para problemas matemáticos 
                complexos (processados por IA) e um botão para busca de notícias.
                5. Log Area (CTkTextbox): Área de texto rica para exibir o histórico de operações e manchetes de notícias formatadas.
        """
        # Configuração de Grid Principal
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(4, weight=1)

        # Visor de entrada/resultado
        self.display = ctk.CTkEntry(
            self.root, 
            height=60, 
            font=("Inter", 32, "bold"), 
            justify='right',
            corner_radius=10,
            border_width=2
        )
        self.display.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        # Container para Teclado e Operações
        middle_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        middle_frame.grid(row=1, column=0, padx=20, sticky="nsew")
        middle_frame.grid_columnconfigure(0, weight=3)
        middle_frame.grid_columnconfigure(1, weight=1)

        # Teclado Numérico 
        keypad_frame = ctk.CTkFrame(middle_frame, fg_color="transparent")
        keypad_frame.grid(row=0, column=0, sticky="nsew")

        buttons = [
            '7', '8', '9',
            '4', '5', '6',
            '1', '2', '3',
            '0', '.', 'C'
        ]

        row, col = 0, 0
        for button in buttons:
            color = "#3d3d3d" if button != 'C' else "#e74c3c"
            hover = "#505050" if button != 'C' else "#c0392b"
            
            btn = ctk.CTkButton(
                keypad_frame, text=button, width=80, height=60, 
                font=("Inter", 18, "bold"),
                fg_color=color, hover_color=hover,
                command=lambda x=button: self._click_button(x)
            )
            btn.grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 2:
                col = 0
                row += 1

        # Botões das Operações
        ops_frame = ctk.CTkFrame(middle_frame, fg_color="transparent")
        ops_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        commands = [
            ("+", self.do_sum),
            ("-", self.do_sub),
            ("*", self.do_prod),
            ("/", self.do_div),
            ("!", self.do_fat),
            ("Prm", self.do_prime),
        ]

        for text, cmd in commands:
            ctk.CTkButton(
                ops_frame, text=text, width=70, height=38, 
                font=("Inter", 14, "bold"),
                fg_color="#1f538d",
                command=cmd
            ).pack(pady=3, fill="x")

        # Widget para Solver e Notícias
        solver_frame = ctk.CTkFrame(self.root, corner_radius=15)
        solver_frame.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        
        ctk.CTkLabel(solver_frame, text="AI Solver & Global News", font=("Inter", 14, "bold")).pack(pady=5)
        
        self.solver_text = ctk.CTkEntry(solver_frame, placeholder_text="Descreva seu problema matemático...", height=40)
        self.solver_text.pack(fill="x", padx=15, pady=5)
        
        btn_container = ctk.CTkFrame(solver_frame, fg_color="transparent")
        btn_container.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkButton(btn_container, text="Resolver com IA", fg_color="#27ae60", hover_color="#219150", command=self.do_solver).pack(side="left", expand=True, padx=5)
        ctk.CTkButton(btn_container, text="Ver Notícias", fg_color="#8e44ad", hover_color="#732d91", command=self.get_news).pack(side="left", expand=True, padx=5)

        # Área de Histórico/Log
        self.log_area = ctk.CTkTextbox(self.root, font=("Consolas", 12), corner_radius=10, border_width=1)
        self.log_area.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="nsew")

    def _click_button(self, char):
        """
            Gerencia a entrada de caracteres no visor da calculadora.
            
            Args:
                char (str): O caractere do botão pressionado ('0'-'9', '.', ou 'C' para limpar).
        """
        if char == 'C':
            self.display.delete(0, tk.END)
        else:
            self.display.insert(tk.END, char)

    def _get_args(self):
        """
            Extrai e limpa os argumentos numéricos do visor.
            
            Returns:
                list[float]: Uma lista de números processados a partir da string do visor.
        """
        data = self.display.get().replace(',', ' ').split()
        try:
            return [float(x) for x in data]
        except ValueError:
            return []

    def _log(self, message):
        """
            Adiciona uma entrada formatada na área de texto (log/histórico).
            
            Args:
                message (str): A mensagem ou resultado a ser exibido.
        """
        self.log_area.insert(tk.END, f"> {message}\n")
        self.log_area.see(tk.END)

    def _final_log(self, message):
        """
            Utilizado somente para fazer uma separação da área de texto (log/histórico).
        """
        self.log_area.insert(tk.END, f"{message}")
        self.log_area.see(tk.END)

    def _handle_rpc_call(self, func, *args):
        """
            Wrapper genérico para chamadas RPC que gerencia exceções de rede e interface.
            
            Executa a função de operação, atualiza o visor com o resultado e exibe caixas de diálogo em caso de erro de conexão.

            Args:
                func (callable): O método da classe Operations a ser chamado.
                *args: Argumentos a serem passados para a função.
        """
        try:
            result = func(*args)
            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))
            self._log(f"Sucesso: {result}")
        except RPCServerNotFound as e:
            messagebox.showerror("Erro de Conexão", f"Servidor offline: {e}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def do_sum(self):
        self._handle_rpc_call(self.op.sum, *self._get_args())

    def do_sub(self):
        self._handle_rpc_call(self.op.sub, *self._get_args())

    def do_prod(self):
        self._handle_rpc_call(self.op.prod, *self._get_args())

    def do_div(self):
        self._handle_rpc_call(self.op.div, *self._get_args())

    def do_fat(self):
        val = self._get_args()
        if val: self._handle_rpc_call(self.op.fat, int(val[0]))
        else: self._log("Erro: Insira um número")

    def do_prime(self):
        args = [int(x) for x in self._get_args()]
        self._handle_rpc_call(self.op.prim, *args)

    def get_news(self):
        try:
            news = self.op.news()
            self._log("--- Manchetes UOL ---")
            for item in news:
                self._log(f"• {item}")
            self._final_log("\n")
        except Exception as e:
            self._log(f"Erro ao buscar notícias: {e}")

    def do_solver(self):
        problem = self.solver_text.get()
        if not problem: return
        self._log(f"Resolvendo: {problem}...")
        self._handle_rpc_call(self.op.solver, problem)

if __name__ == "__main__":
    app_root = ctk.CTk()
    app = RPCGui(app_root)
    app_root.mainloop()