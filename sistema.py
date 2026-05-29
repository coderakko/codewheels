import tkinter as tk
from tkinter import messagebox
import json
import os
import subprocess
import pyglet

pyglet.font.add_file("Wheel Turn.otf")

ARQUIVO_USUARIOS = "usuarios.json"


def criar_card_arredondado(janela, largura, altura, raio=30):

    canvas = tk.Canvas(
        janela,
        width=largura,
        height=altura,
        bg="#D9D9D9",
        highlightthickness=0
    )

    pontos = [
        raio, 0,
        largura-raio, 0,
        largura, 0,
        largura, raio,
        largura, altura-raio,
        largura, altura,
        largura-raio, altura,
        raio, altura,
        0, altura,
        0, altura-raio,
        0, raio,
        0, 0
    ]

    canvas.create_polygon(
        pontos,
        smooth=True,
        fill="white",
        outline="white"
    )

    frame = tk.Frame(
        canvas,
        bg="white",
        width=largura-20,
        height=altura-20
    )

    canvas.create_window(
        10,
        10,
        anchor="nw",
        window=frame
    )

    frame.pack_propagate(False)

    return canvas, frame


def carregar_usuarios():

    if os.path.exists(ARQUIVO_USUARIOS):

        with open(
            ARQUIVO_USUARIOS,
            "r",
            encoding="utf-8"
        ) as arquivo:

            return json.load(arquivo)

    return {}


def salvar_usuarios():

    with open(
        ARQUIVO_USUARIOS,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            usuarios,
            arquivo,
            indent=4
        )


usuarios = carregar_usuarios()


def limpar_card():

    for widget in conteudo.winfo_children():

        widget.destroy()


def criar_placeholder(campo, texto, senha=False):

    campo.insert(0, texto)

    campo.config(
        fg="#AAAAAA",
        show=""
    )

    def ao_clicar(event):

        if campo.get() == texto:

            campo.delete(0, tk.END)

            campo.config(fg="black")

            if senha:

                campo.config(show="*")

    def ao_sair(event):

        if campo.get() == "":

            campo.insert(0, texto)

            campo.config(
                fg="#AAAAAA",
                show=""
            )

    campo.bind("<FocusIn>", ao_clicar)

    campo.bind("<FocusOut>", ao_sair)


def login():

    nome = entrada_usuario.get()

    senha = entrada_senha.get()

    if nome == "Nome de usuário" or senha == "Senha":

        messagebox.showerror(
            "Erro",
            "Preencha todos os campos."
        )

        return

    if nome in usuarios and usuarios[nome] == senha:

        messagebox.showinfo(
            "Sucesso",
            "Login realizado!"
        )

        janela.destroy()

        subprocess.Popen(
            ["py", "menu.py", nome]
        )

    else:

        messagebox.showerror(
            "Erro",
            "Usuário ou senha incorretos."
        )


def cadastrar():

    nome = entrada_usuario.get()

    senha = entrada_senha.get()

    confirmar = entrada_confirmar.get()

    if (
        nome == "Nome de usuário"
        or senha == "Senha"
        or confirmar == "Confirme a senha"
    ):

        messagebox.showerror(
            "Erro",
            "Preencha todos os campos."
        )

        return

    if senha != confirmar:

        messagebox.showerror(
            "Erro",
            "As senhas não coincidem."
        )

        return

    if nome in usuarios:

        messagebox.showerror(
            "Erro",
            "Usuário já existe."
        )

        return

    usuarios[nome] = senha

    salvar_usuarios()

    messagebox.showinfo(
        "Sucesso",
        "Usuário cadastrado!"
    )

    mostrar_login()


def esqueceu_senha():

    messagebox.showinfo(
        "CodeWheels",
        "Procure o administrador do sistema."
    )


def mostrar_login():

    global entrada_usuario
    global entrada_senha

    limpar_card()

    botao_acessarconta.config(
        bg="white",
        fg="#6E6E6E"
    )

    botao_criarconta.config(
        bg="#F0F0F0",
        fg="#999999"
    )

    tk.Label(
        conteudo,
        text="👤",
        font=("Arial", 60),
        bg="white",
        fg="#AAAAAA"
    ).pack(pady=25)

    entrada_usuario = tk.Entry(
        conteudo,
        font=("Arial", 12),
        bg="#F1F1F1",
        bd=0,
        width=34
    )

    entrada_usuario.pack(ipady=12, pady=8)

    criar_placeholder(
        entrada_usuario,
        "Nome de usuário"
    )

    entrada_senha = tk.Entry(
        conteudo,
        font=("Arial", 12),
        bg="#F1F1F1",
        bd=0,
        width=34
    )

    entrada_senha.pack(ipady=12, pady=8)

    criar_placeholder(
        entrada_senha,
        "Senha",
        senha=True
    )

    linha = tk.Frame(
        conteudo,
        bg="white"
    )

    linha.pack(
        fill="x",
        padx=75,
        pady=8
    )

    esqueci = tk.Button(
        linha,
        text="Esqueci a senha",
        bg="white",
        fg="#999999",
        bd=0,
        font=("Arial", 9),
        cursor="hand2",
        command=esqueceu_senha
    )

    esqueci.pack(side="right")

    tk.Button(
        conteudo,
        text="Entrar",
        font=("Arial", 15),
        bg="#BFC5CC",
        fg="#2E2E2E",
        bd=0,
        width=17,
        height=2,
        cursor="hand2",
        command=login
    ).pack(pady=28)


def mostrar_register():

    global entrada_usuario
    global entrada_senha
    global entrada_confirmar

    limpar_card()

    botao_acessarconta.config(
        bg="#F0F0F0",
        fg="#999999"
    )

    botao_criarconta.config(
        bg="white",
        fg="#6E6E6E"
    )

    tk.Label(
        conteudo,
        text="👤",
        font=("Arial", 60),
        bg="white",
        fg="#AAAAAA"
    ).pack(pady=25)

    entrada_usuario = tk.Entry(
        conteudo,
        font=("Arial", 12),
        bg="#F1F1F1",
        bd=0,
        width=34
    )

    entrada_usuario.pack(ipady=12, pady=8)

    criar_placeholder(
        entrada_usuario,
        "Nome de usuário"
    )

    entrada_senha = tk.Entry(
        conteudo,
        font=("Arial", 12),
        bg="#F1F1F1",
        bd=0,
        width=34
    )

    entrada_senha.pack(ipady=12, pady=8)

    criar_placeholder(
        entrada_senha,
        "Senha",
        senha=True
    )

    entrada_confirmar = tk.Entry(
        conteudo,
        font=("Arial", 12),
        bg="#F1F1F1",
        bd=0,
        width=34
    )

    entrada_confirmar.pack(ipady=12, pady=8)

    criar_placeholder(
        entrada_confirmar,
        "Confirme a senha",
        senha=True
    )

    botao_registrar = tk.Button(
        conteudo,
        text="Registrar",
        font=("Arial", 15),
        bg="#BFC5CC",
        fg="#2E2E2E",
        bd=0,
        width=17,
        height=2,
        cursor="hand2",
        command=cadastrar
    )

    botao_registrar.pack(pady=20)


janela = tk.Tk()

janela.title("CodeWheels")

janela.geometry("760x620")

janela.configure(bg="#D9D9D9")

janela.resizable(False, False)

titulo = tk.Label(
    janela,
    text="💻Code Wheels🚗",
    font=("Wheel Turn", 32),
    bg="#D9D9D9",
    fg="#6E6E6E"
)

titulo.pack(pady=25)

card_canvas, card = criar_card_arredondado(
    janela,
    500,
    500
)

card_canvas.pack()

topo = tk.Frame(
    card,
    bg="#F0F0F0",
    width=480,
    height=75
)

topo.pack(fill="x")

botao_acessarconta = tk.Button(
    topo,
    text="Acessar conta",
    font=("Arial", 18),
    bg="white",
    fg="#6E6E6E",
    bd=0,
    cursor="hand2",
    command=mostrar_login
)

botao_acessarconta.place(
    x=0,
    y=0,
    width=240,
    height=75
)

botao_criarconta = tk.Button(
    topo,
    text="Criar conta",
    font=("Arial", 18),
    bg="#F0F0F0",
    fg="#999999",
    bd=0,
    cursor="hand2",
    command=mostrar_register
)

botao_criarconta.place(
    x=240,
    y=0,
    width=240,
    height=75
)

conteudo = tk.Frame(
    card,
    bg="white",
    width=480,
    height=405
)

conteudo.pack(
    fill="both",
    expand=True
)

mostrar_login()

janela.mainloop()