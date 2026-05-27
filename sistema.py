import tkinter as tk
from tkinter import messagebox
import json
import os
import subprocess
import pyglet

pyglet.font.add_file("Wheel Turn.otf")

ARQUIVO_USUARIOS = "usuarios.json"


def carregar_usuarios():
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    return {}


def salvar_usuarios():
    with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as arquivo:
        json.dump(usuarios, arquivo, indent=4)


usuarios = carregar_usuarios()


def limpar_card():
    for widget in conteudo.winfo_children():
        widget.destroy()


def criar_placeholder(campo, texto, senha=False):
    campo.insert(0, texto)
    campo.config(fg="#AAAAAA", show="")

    def ao_clicar(event):
        if campo.get() == texto:
            campo.delete(0, tk.END)
            campo.config(fg="black")
            if senha:
                campo.config(show="*")

    def ao_sair(event):
        if campo.get() == "":
            campo.insert(0, texto)
            campo.config(fg="#AAAAAA", show="")

    campo.bind("<FocusIn>", ao_clicar)
    campo.bind("<FocusOut>", ao_sair)


def login():
    nome = entrada_usuario.get()
    senha = entrada_senha.get()

    if nome == "Username or e-mail" or senha == "Password":
        messagebox.showerror("Erro", "Preencha todos os campos.")
        return

    if nome in usuarios and usuarios[nome] == senha:
        messagebox.showinfo("Sucesso", "Login realizado!")
        subprocess.run(["py", "menu.py", nome])
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos.")


def cadastrar():
    nome = entrada_usuario.get()
    senha = entrada_senha.get()
    confirmar = entrada_confirmar.get()

    if nome == "Username or e-mail" or senha == "Password" or confirmar == "Confirm password":
        messagebox.showerror("Erro", "Preencha todos os campos.")
        return

    if senha != confirmar:
        messagebox.showerror("Erro", "As senhas não coincidem.")
        return

    if nome in usuarios:
        messagebox.showerror("Erro", "Usuário já existe.")
        return

    usuarios[nome] = senha
    salvar_usuarios()

    messagebox.showinfo("Sucesso", "Usuário cadastrado!")
    mostrar_login()


def esqueceu_senha():
    messagebox.showinfo(
        "CodeWheels",
        "Procure o administrador do sistema."
    )


def mostrar_login():
    global entrada_usuario, entrada_senha

    limpar_card()

    botao_topo_login.config(bg="white", fg="#6E6E6E")
    botao_topo_register.config(bg="#F0F0F0", fg="#999999")

    icone = tk.Label(
        conteudo,
        text="👤",
        font=("Arial", 60),
        bg="white",
        fg="#AAAAAA"
    )
    icone.pack(pady=25)

    entrada_usuario = tk.Entry(
        conteudo,
        font=("Arial", 12),
        bg="#F1F1F1",
        bd=0,
        width=34
    )
    entrada_usuario.pack(ipady=12, pady=8)
    criar_placeholder(entrada_usuario, "Username or e-mail")

    entrada_senha = tk.Entry(
        conteudo,
        font=("Arial", 12),
        bg="#F1F1F1",
        bd=0,
        width=34
    )
    entrada_senha.pack(ipady=12, pady=8)
    criar_placeholder(entrada_senha, "Password", senha=True)

    linha = tk.Frame(conteudo, bg="white")
    linha.pack(fill="x", padx=75, pady=8)

    lembrar = tk.Checkbutton(
        linha,
        text="Remember me",
        bg="white",
        fg="#999999",
        font=("Arial", 9)
    )
    lembrar.pack(side="left")

    esqueci = tk.Button(
        linha,
        text="I forgot password",
        bg="white",
        fg="#999999",
        bd=0,
        font=("Arial", 9),
        cursor="hand2",
        command=esqueceu_senha
    )
    esqueci.pack(side="right")

    botao = tk.Button(
        conteudo,
        text="Sign In",
        font=("Arial", 15),
        bg="#BFC5CC",
        fg="#2E2E2E",
        bd=0,
        width=17,
        height=1,
        cursor="hand2",
        command=login
    )
    botao.pack(pady=28)

    trocar = tk.Button(
        conteudo,
        text="register",
        bg="white",
        fg="#999999",
        bd=0,
        font=("Arial", 10, "bold"),
        cursor="hand2",
        command=mostrar_register
    )
    trocar.pack()


def mostrar_register():
    global entrada_usuario, entrada_senha, entrada_confirmar

    limpar_card()

    botao_topo_login.config(bg="#F0F0F0", fg="#999999")
    botao_topo_register.config(bg="white", fg="#6E6E6E")

    icone = tk.Label(
        conteudo,
        text="👤",
        font=("Arial", 60),
        bg="white",
        fg="#AAAAAA"
    )
    icone.pack(pady=25)

    entrada_usuario = tk.Entry(
        conteudo,
        font=("Arial", 12),
        bg="#F1F1F1",
        bd=0,
        width=34
    )
    entrada_usuario.pack(ipady=12, pady=8)
    criar_placeholder(entrada_usuario, "Username or e-mail")

    entrada_senha = tk.Entry(
        conteudo,
        font=("Arial", 12),
        bg="#F1F1F1",
        bd=0,
        width=34
    )
    entrada_senha.pack(ipady=12, pady=8)
    criar_placeholder(entrada_senha, "Password", senha=True)

    entrada_confirmar = tk.Entry(
        conteudo,
        font=("Arial", 12),
        bg="#F1F1F1",
        bd=0,
        width=34
    )
    entrada_confirmar.pack(ipady=12, pady=8)
    criar_placeholder(entrada_confirmar, "Confirm password", senha=True)

    botao = tk.Button(
        conteudo,
        text="Register",
        font=("Arial", 15),
        bg="#BFC5CC",
        fg="#2E2E2E",
        bd=0,
        width=17,
        height=1,
        cursor="hand2",
        command=cadastrar
    )
    botao.pack(pady=30)

    trocar = tk.Button(
        conteudo,
        text="sign in",
        bg="white",
        fg="#999999",
        bd=0,
        font=("Arial", 10, "bold"),
        cursor="hand2",
        command=mostrar_login
    )
    trocar.pack()


janela = tk.Tk()
janela.title("CodeWheels")
janela.geometry("760x620")
janela.configure(bg="#D9D9D9")
janela.resizable(False, False)

titulo = tk.Label(
    janela,
    text="💻CodeWheels🚗",
    font=("Wheel Turn", 32),
    bg="#D9D9D9",
    fg="#6E6E6E"
)
titulo.pack(pady=25)

card = tk.Frame(
    janela,
    bg="white",
    width=500,
    height=500
)
card.pack()
card.pack_propagate(False)

topo = tk.Frame(
    card,
    bg="#F0F0F0",
    width=500,
    height=75
)
topo.pack(fill="x")

botao_topo_login = tk.Button(
    topo,
    text="↪  Sign In",
    font=("Arial", 18),
    bg="white",
    fg="#6E6E6E",
    bd=0,
    width=15,
    height=2,
    cursor="hand2",
    command=mostrar_login
)
botao_topo_login.place(x=0, y=0)

botao_topo_register = tk.Button(
    topo,
    text="☼  Register",
    font=("Arial", 18),
    bg="#F0F0F0",
    fg="#999999",
    bd=0,
    width=15,
    height=2,
    cursor="hand2",
    command=mostrar_register
)
botao_topo_register.place(x=250, y=0)

conteudo = tk.Frame(
    card,
    bg="white",
    width=500,
    height=425
)
conteudo.pack(fill="both", expand=True)

mostrar_login()

janela.mainloop()