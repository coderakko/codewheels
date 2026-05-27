import tkinter as tk
import socket
import json
import os
import pyglet

pyglet.font.add_file("Wheel Turn.otf")

PORTA = 5000
ARQUIVO_CARRINHO = "carrinho.json"

cliente = None
conectado = False


def carregar_carrinho():
    if os.path.exists(ARQUIVO_CARRINHO):
        with open(ARQUIVO_CARRINHO, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    return {
        "nome": "Carrinho não cadastrado",
        "ip": ""
    }


def conectar():
    global cliente, conectado

    dados = carregar_carrinho()
    ip = dados["ip"]

    label_nome_carrinho.config(text=f"Carrinho: {dados['nome']}")

    if ip == "":
        conectado = False
        label_status.config(text="IP do carrinho não cadastrado", fg="#E74C3C")
        return

    try:
        cliente = socket.socket()
        cliente.settimeout(2)
        cliente.connect((ip, PORTA))

        conectado = True
        label_status.config(text="ESP32 ONLINE", fg="#2ECC71")

    except:
        conectado = False
        label_status.config(text="ESP32 OFFLINE - modo teste", fg="#E74C3C")


def enviar(comando):
    global conectado

    if conectado:
        try:
            cliente.send(comando.encode())
            label_comando.config(text=f"Comando enviado: {comando.upper()}")

        except:
            conectado = False
            label_status.config(text="CONEXÃO PERDIDA", fg="#E74C3C")

    else:
        label_comando.config(text=f"Modo teste: {comando.upper()}")


def frente(event=None):
    enviar("w")


def tras(event=None):
    enviar("s")


def esquerda(event=None):
    enviar("a")


def direita(event=None):
    enviar("d")


janela = tk.Tk()
janela.title("CodeWheels - Controle")
janela.geometry("640x600")
janela.configure(bg="#D9D9D9")
janela.resizable(False, False)

titulo = tk.Label(
    janela,
    text="💻CodeWheels🚗",
    font=("Wheel Turn", 28),
    bg="#D9D9D9",
    fg="#6E6E6E"
)
titulo.pack(pady=18)

card = tk.Frame(
    janela,
    bg="white",
    width=460,
    height=470
)
card.pack()
card.pack_propagate(False)

topo = tk.Frame(
    card,
    bg="#F0F0F0",
    width=460,
    height=65
)
topo.pack(fill="x")

label_topo = tk.Label(
    topo,
    text="🎮 Controle do Carrinho",
    font=("Arial", 18),
    bg="#F0F0F0",
    fg="#6E6E6E"
)
label_topo.pack(pady=17)

label_nome_carrinho = tk.Label(
    card,
    text="Carrinho: carregando...",
    font=("Arial", 12),
    bg="white",
    fg="#777777"
)
label_nome_carrinho.pack(pady=8)

label_status = tk.Label(
    card,
    text="Verificando conexão...",
    font=("Arial", 13, "bold"),
    bg="white",
    fg="#999999"
)
label_status.pack(pady=8)

label_comando = tk.Label(
    card,
    text="Use W A S D ou clique nos botões",
    font=("Arial", 11),
    bg="white",
    fg="#777777"
)
label_comando.pack(pady=5)

frame = tk.Frame(card, bg="white")
frame.pack(pady=22)

botao_frente = tk.Button(
    frame,
    text="W\n↑",
    font=("Arial", 20, "bold"),
    bg="#BFC5CC",
    fg="#2E2E2E",
    bd=0,
    width=5,
    height=2,
    cursor="hand2",
    command=frente
)
botao_frente.grid(row=0, column=1, padx=8, pady=8)

botao_esquerda = tk.Button(
    frame,
    text="A\n←",
    font=("Arial", 20, "bold"),
    bg="#BFC5CC",
    fg="#2E2E2E",
    bd=0,
    width=5,
    height=2,
    cursor="hand2",
    command=esquerda
)
botao_esquerda.grid(row=1, column=0, padx=8, pady=8)

botao_tras = tk.Button(
    frame,
    text="S\n↓",
    font=("Arial", 20, "bold"),
    bg="#BFC5CC",
    fg="#2E2E2E",
    bd=0,
    width=5,
    height=2,
    cursor="hand2",
    command=tras
)
botao_tras.grid(row=1, column=1, padx=8, pady=8)

botao_direita = tk.Button(
    frame,
    text="D\n→",
    font=("Arial", 20, "bold"),
    bg="#BFC5CC",
    fg="#2E2E2E",
    bd=0,
    width=5,
    height=2,
    cursor="hand2",
    command=direita
)
botao_direita.grid(row=1, column=2, padx=8, pady=8)

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

janela.bind("<w>", frente)
janela.bind("<W>", frente)
janela.bind("<s>", tras)
janela.bind("<S>", tras)
janela.bind("<a>", esquerda)
janela.bind("<A>", esquerda)
janela.bind("<d>", direita)
janela.bind("<D>", direita)

janela.focus_force()

conectar()

janela.mainloop()