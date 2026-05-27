import tkinter as tk
import subprocess
import socket
import sys
import json
import os
import pyglet

pyglet.font.add_file("Wheel Turn.otf")

PORTA = 5000
ARQUIVO_CARRINHO = "carrinho.json"

usuario = "Usuário"

if len(sys.argv) > 1:
    usuario = sys.argv[1]


def carregar_carrinho():
    if os.path.exists(ARQUIVO_CARRINHO):
        with open(ARQUIVO_CARRINHO, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    return {
        "nome": "Carrinho não cadastrado",
        "ip": ""
    }


def testar_conexao():
    dados = carregar_carrinho()
    ip = dados["ip"]

    if ip == "":
        return False

    try:
        cliente = socket.socket()
        cliente.settimeout(2)
        cliente.connect((ip, PORTA))
        cliente.close()
        return True

    except:
        return False


def abrir_controle():
    subprocess.run(["py", "controle.py"])


def abrir_cadastro():
    subprocess.run(["py", "cadastro_carrinho.py"])
    atualizar_status()


def atualizar_status():
    dados = carregar_carrinho()

    label_nome_carrinho.config(
        text=f"Carrinho: {dados['nome']}"
    )

    if dados["ip"] == "":
        label_ip.config(
            text="IP: não cadastrado"
        )
        label_status.config(
            text="Cadastre o carrinho para verificar a conexão",
            fg="#E74C3C"
        )
    elif testar_conexao():
        label_ip.config(
            text=f"IP: {dados['ip']}"
        )
        label_status.config(
            text="ESP32 ONLINE",
            fg="#2ECC71"
        )
    else:
        label_ip.config(
            text=f"IP: {dados['ip']}"
        )
        label_status.config(
            text="ESP32 OFFLINE - modo teste",
            fg="#E74C3C"
        )

    janela.after(3000, atualizar_status)


janela = tk.Tk()

janela.title("CodeWheels - Menu")

janela.geometry("760x650")

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

label_topo = tk.Label(
    topo,
    text="🚗 Painel do Carrinho",
    font=("Arial", 20),
    bg="#F0F0F0",
    fg="#6E6E6E"
)

label_topo.pack(pady=20)

icone = tk.Label(
    card,
    text="🚙",
    font=("Arial", 65),
    bg="white",
    fg="#AAAAAA"
)

icone.pack(pady=15)

label_usuario = tk.Label(
    card,
    text=f"Usuário logado: {usuario}",
    font=("Arial", 14),
    bg="white",
    fg="#777777"
)

label_usuario.pack(pady=5)

label_nome_carrinho = tk.Label(
    card,
    text="Carrinho: carregando...",
    font=("Arial", 13),
    bg="white",
    fg="#777777"
)

label_nome_carrinho.pack(pady=5)

label_ip = tk.Label(
    card,
    text="IP: carregando...",
    font=("Arial", 13),
    bg="white",
    fg="#777777"
)

label_ip.pack(pady=5)

label_status = tk.Label(
    card,
    text="Verificando conexão...",
    font=("Arial", 14, "bold"),
    bg="white",
    fg="#999999"
)

label_status.pack(pady=12)

botao_controle = tk.Button(
    card,
    text="Abrir Controle",
    font=("Arial", 15, "bold"),
    bg="#BFC5CC",
    fg="#2E2E2E",
    bd=0,
    width=20,
    height=1,
    cursor="hand2",
    command=abrir_controle
)

botao_controle.pack(pady=10)

botao_cadastro = tk.Button(
    card,
    text="Cadastrar Carrinho",
    font=("Arial", 15, "bold"),
    bg="#BFC5CC",
    fg="#2E2E2E",
    bd=0,
    width=20,
    height=1,
    cursor="hand2",
    command=abrir_cadastro
)

botao_cadastro.pack(pady=10)

botao_sair = tk.Button(
    card,
    text="Sair",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="#999999",
    bd=0,
    cursor="hand2",
    command=janela.destroy
)

botao_sair.pack(pady=8)

atualizar_status()

janela.mainloop()