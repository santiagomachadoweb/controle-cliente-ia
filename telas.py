import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import csv
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

USUARIO_ADMIN = "admin"
SENHA_ADMIN = "1234"

def centralizar_janela(janela, largura, altura):
    janela.update_idletasks()
    tela_largura = janela.winfo_screenwidth()
    tela_altura = janela.winfo_screenheight()
    x = (tela_largura // 2) - (largura // 2)
    y = (tela_altura // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

# ================= LOGIN =================
class TelaLogin:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login")
        self.root.configure(bg="#e5e5e5")
        centralizar_janela(self.root, 400, 260)

        frame = tk.Frame(self.root, bg="#e5e5e5")
        frame.pack(expand=True)

        tk.Label(frame, text="Usuário").pack(pady=5)
        self.entry_user = tk.Entry(frame, width=30)
        self.entry_user.pack(ipady=6)

        tk.Label(frame, text="Senha").pack(pady=5)
        self.entry_pass = tk.Entry(frame, show="*", width=30)
        self.entry_pass.pack(ipady=6)

        btn = tk.Button(frame, text="Entrar", width=20, cursor="hand2",
                        command=self.validar_login)
        btn.pack(pady=15, ipady=4)

        self.root.bind("<Return>", lambda event: self.validar_login())
        self.root.mainloop()

    def validar_login(self):
        if self.entry_user.get() == USUARIO_ADMIN and self.entry_pass.get() == SENHA_ADMIN:
            self.root.destroy()
            TelaSistema()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos")

# ================= SISTEMA =================
class TelaSistema:
    def __init__(self):
        self.conn = sqlite3.connect("clientes.db")
        self.cursor = self.conn.cursor()
        self.cliente_em_edicao = None
        self.pagina_atual = 0
        self.linhas_por_pagina = 10

        self.root = tk.Tk()
        self.root.title("Controle de Clientes")
        self.root.configure(bg="#f2f2f2")
        centralizar_janela(self.root, 1100, 650)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", rowheight=28)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

        # ===== HEADER =====
        header = tk.Frame(self.root, bg="#dddddd", height=45)
        header.pack(fill="x")

        tk.Label(header, text="Sistema de Clientes", bg="#dddddd",
                 font=("Arial", 12, "bold")).pack(side="left", padx=10)

        img = Image.open("logout.png").resize((16,16))
        self.icone_logout = ImageTk.PhotoImage(img)

        tk.Button(header, text=" Logout", image=self.icone_logout,
                  compound="left", bd=0, bg="#dddddd",
                  cursor="hand2", command=self.logout).pack(side="right", padx=10)

        # ===== FORM =====
        form = tk.Frame(self.root, bg="#f2f2f2")
        form.pack(pady=10)

        def campo(label, col):
            tk.Label(form, text=label, bg="#f2f2f2").grid(row=0, column=col, sticky="w", padx=5)
            e = tk.Entry(form, width=25)
            e.grid(row=1, column=col, padx=5, ipady=6)
            return e

        self.entry_nome = campo("Nome", 0)
        self.entry_telefone = campo("Telefone", 1)
        self.entry_email = campo("Email", 2)

        self.btn_padrao(form, "Cadastrar", self.cadastrar_cliente, 3)
        self.btn_padrao(form, "Salvar", self.salvar_edicao, 4)

        # ===== BUSCA =====
        busca = tk.Frame(self.root, bg="#f2f2f2")
        busca.pack(pady=5)

        tk.Label(busca, text="Buscar:", bg="#f2f2f2").grid(row=0, column=0, padx=5)
        self.entry_busca = tk.Entry(busca, width=30)
        self.entry_busca.grid(row=0, column=1, padx=5, ipady=6)

        self.btn_padrao(busca, "Buscar", self.buscar_cliente, 2)
        self.btn_padrao(busca, "Mostrar todos", self.mostrar_todos, 3)

        # ===== GRID =====
        frame_grid = tk.Frame(self.root)
        frame_grid.pack(fill="both", expand=True, padx=20, pady=10)

        self.tree_clientes = ttk.Treeview(frame_grid,
            columns=("ID","Nome","Telefone","Email"), show="headings", height=10)

        for col in ("ID","Nome","Telefone","Email"):
            self.tree_clientes.heading(col, text=col)
            self.tree_clientes.column(col, anchor="center")

        self.tree_clientes.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_grid, orient="vertical",
                                  command=self.tree_clientes.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree_clientes.configure(yscrollcommand=scrollbar.set)

        # ===== PAGINAÇÃO =====
        pag = tk.Frame(self.root, bg="#f2f2f2")
        pag.pack(pady=5)

        self.btn_padrao(pag, "Anterior", self.pagina_anterior, 0)
        self.lbl_pagina = tk.Label(pag, text="Página 1", bg="#f2f2f2")
        self.lbl_pagina.grid(row=1, column=1, padx=15)
        self.btn_padrao(pag, "Próxima", self.proxima_pagina, 2)

        # ===== AÇÕES =====
        acoes = tk.Frame(self.root, bg="#f2f2f2")
        acoes.pack(pady=10)

        self.btn_padrao(acoes, "Registrar Acesso", self.registrar_acesso, 0)
        self.btn_padrao(acoes, "Editar", self.editar_cliente, 1)
        self.btn_padrao(acoes, "Excluir", self.excluir_cliente, 2)
        self.btn_padrao(acoes, "Exportar Logs", self.exportar_logs_todos, 3)
        self.btn_padrao(acoes, "Gráfico", self.mostrar_grafico, 4)

        self.carregar_clientes()
        self.root.mainloop()

    def btn_padrao(self, frame, texto, comando, col):
        b = tk.Button(frame, text=texto, width=14,
                      bg="#e0e0e0", relief="flat",
                      cursor="hand2", command=comando)
        b.grid(row=1, column=col, padx=5, ipady=6)
        b.bind("<Enter>", lambda e: b.config(bg="#d0d0d0"))
        b.bind("<Leave>", lambda e: b.config(bg="#e0e0e0"))

    # ===== FUNÇÕES (INALTERADAS) =====
    def logout(self):
        self.root.destroy()
        TelaLogin()

    def registrar_log(self, cliente_id, acao):
        data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute("INSERT INTO logs (cliente_id, acao, data) VALUES (?, ?, ?)",
                            (cliente_id, acao, data))
        self.conn.commit()

    def carregar_clientes(self):
        self.tree_clientes.delete(*self.tree_clientes.get_children())
        offset = self.pagina_atual * self.linhas_por_pagina
        self.cursor.execute("SELECT * FROM clientes LIMIT ? OFFSET ?",
                            (self.linhas_por_pagina, offset))
        for row in self.cursor.fetchall():
            self.tree_clientes.insert("", "end", values=row)
        self.lbl_pagina.config(text=f"Página {self.pagina_atual+1}")

    def proxima_pagina(self):
        self.pagina_atual += 1
        self.carregar_clientes()

    def pagina_anterior(self):
        if self.pagina_atual > 0:
            self.pagina_atual -= 1
            self.carregar_clientes()

    def cadastrar_cliente(self):
        nome = self.entry_nome.get()
        telefone = self.entry_telefone.get()
        email = self.entry_email.get()
        if not nome:
            return
        self.cursor.execute("INSERT INTO clientes (nome, telefone, email) VALUES (?, ?, ?)",
                            (nome, telefone, email))
        self.conn.commit()
        self.registrar_log(self.cursor.lastrowid, "Cadastro")
        self.limpar_campos()
        self.carregar_clientes()

    def limpar_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)

    def buscar_cliente(self):
        termo = self.entry_busca.get()
        self.tree_clientes.delete(*self.tree_clientes.get_children())
        self.cursor.execute("SELECT * FROM clientes WHERE nome LIKE ?", (f"%{termo}%",))
        for row in self.cursor.fetchall():
            self.tree_clientes.insert("", "end", values=row)

    def mostrar_todos(self):
        self.entry_busca.delete(0, tk.END)
        self.pagina_atual = 0
        self.carregar_clientes()

    def registrar_acesso(self):
        item = self.tree_clientes.selection()
        if not item:
            return
        cliente_id = self.tree_clientes.item(item)["values"][0]
        self.registrar_log(cliente_id, "Acesso")
        messagebox.showinfo("OK", "Acesso registrado")

    def editar_cliente(self):
        item = self.tree_clientes.selection()
        if not item:
            return
        valores = self.tree_clientes.item(item)["values"]
        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(0, valores[1])
        self.entry_telefone.delete(0, tk.END)
        self.entry_telefone.insert(0, valores[2])
        self.entry_email.delete(0, tk.END)
        self.entry_email.insert(0, valores[3])
        self.cliente_em_edicao = valores[0]

    def salvar_edicao(self):
        if self.cliente_em_edicao is None:
            return
        self.cursor.execute(
            "UPDATE clientes SET nome=?, telefone=?, email=? WHERE id=?",
            (self.entry_nome.get(), self.entry_telefone.get(),
             self.entry_email.get(), self.cliente_em_edicao)
        )
        self.conn.commit()
        self.registrar_log(self.cliente_em_edicao, "Edição")
        self.cliente_em_edicao = None
        self.limpar_campos()
        self.carregar_clientes()

    def excluir_cliente(self):
        item = self.tree_clientes.selection()
        if not item:
            return
        cliente_id = self.tree_clientes.item(item)["values"][0]
        if messagebox.askyesno("Confirmação", "Excluir cliente?"):
            self.cursor.execute("DELETE FROM clientes WHERE id=?", (cliente_id,))
            self.cursor.execute("DELETE FROM logs WHERE cliente_id=?", (cliente_id,))
            self.conn.commit()
            self.carregar_clientes()

    def exportar_logs_todos(self):
        self.cursor.execute("""
            SELECT clientes.id, clientes.nome, clientes.telefone, clientes.email,
                   logs.acao, logs.data
            FROM logs JOIN clientes ON logs.cliente_id = clientes.id
        """)
        dados = self.cursor.fetchall()
        self.salvar_csv(dados, "logs.csv")

    def salvar_csv(self, dados, nome):
        arquivo = filedialog.asksaveasfilename(defaultextension=".csv", initialfile=nome)
        if not arquivo:
            return
        with open(arquivo, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["ID","Nome","Telefone","Email","Ação","Data"])
            writer.writerows(dados)

    def mostrar_grafico(self):
        self.cursor.execute("""
            SELECT substr(data,1,10), COUNT(*) FROM logs
            GROUP BY substr(data,1,10)
        """)
        dados = self.cursor.fetchall()
        if not dados:
            return
        datas = [d[0] for d in dados]
        valores = [d[1] for d in dados]
        plt.bar(datas, valores)
        plt.xticks(rotation=45)
        plt.title("Registros por dia")
        plt.show()

if __name__ == "__main__":
    TelaLogin()
