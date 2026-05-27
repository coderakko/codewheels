import tkinter as tk
import socket
import json
import os
import sys
import subprocess
import pyglet

pyglet.font.add_file("Wheel Turn.otf")

PORTA = 5000
ARQUIVO_ROVER = "rover.json"

cliente = None
conectado = False
usuario = "Usuário"

if len(sys.argv) > 1:
    usuario = sys.argv[1]


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
        largura - raio, 0,
        largura, 0,
        largura, raio,
        largura, altura - raio,
        largura, altura,
        largura - raio, altura,
        raio, altura,
        0, altura,
        0, altura - raio,
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
        width=largura - 20,
        height=altura - 20
    )

    canvas.create_window(
        10,
        10,
        anchor="nw",
        window=frame
    )

    frame.pack_propagate(False)

    return canvas, frame


def carregar_rover():
    if os.path.exists(ARQUIVO_ROVER):
        with open(ARQUIVO_ROVER, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    return {
        "nome": "Rover não cadastrado",
        "ip": ""
    }


def conectar():
    global cliente, conectado

    dados = carregar_rover()
    ip = dados["ip"]

    label_nome_rover.config(
        text=f"Rover: {dados['nome']}"
    )

    if ip == "":
        conectado = False

        label_status.config(
            text="IP do rover não cadastrado",
            fg="#E74C3C"
        )

        return

    try:
        cliente = socket.socket()
        cliente.settimeout(2)
        cliente.connect((ip, PORTA))

        conectado = True

        label_status.config(
            text="ESP32 ONLINE",
            fg="#2ECC71"
        )

    except:
        conectado = False

        label_status.config(
            text="ESP32 OFFLINE - modo teste",
            fg="#E74C3C"
        )


def enviar(comando):
    global conectado

    if conectado:
        try:
            cliente.send(comando.encode())

            label_comando.config(
                text=f"Comando enviado: {comando.upper()}"
            )

        except:
            conectado = False

            label_status.config(
                text="CONEXÃO PERDIDA",
                fg="#E74C3C"
            )

    else:
        label_comando.config(
            text=f"Modo teste: {comando.upper()}"
        )


def frente(event=None):
    enviar("w")


def tras(event=None):
    enviar("s")


def esquerda(event=None):
    enviar("a")


def direita(event=None):
    enviar("d")


def voltar_menu():
    janela.destroy()
    subprocess.Popen(["py", "menu.py", usuario])


janela = tk.Tk()

janela.title("CodeWheels - Controle")

janela.geometry("640x600")

janela.configure(bg="#D9D9D9")

janela.resizable(False, False)

titulo = tk.Label(
    janela,
    text="💻Code Wheels🚗",
    font=("Wheel Turn", 28),
    bg="#D9D9D9",
    fg="#6E6E6E"
)

titulo.pack(pady=18)

card_canvas, card = criar_card_arredondado(
    janela,
    460,
    470
)

card_canvas.pack()

topo = tk.Frame(
    card,
    bg="#F0F0F0",
    width=440,
    height=65
)

topo.pack(fill="x")

label_topo = tk.Label(
    topo,
    text="🎮 Controle do Rover",
    font=("Arial", 18),
    bg="#F0F0F0",
    fg="#6E6E6E"
)

label_topo.pack(pady=17)

label_nome_rover = tk.Label(
    card,
    text="Rover: carregando...",
    font=("Arial", 12),
    bg="white",
    fg="#777777"
)

label_nome_rover.pack(pady=8)

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

frame = tk.Frame(
    card,
    bg="white"
)

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

botao_voltar = tk.Button(
    card,
    text="Voltar",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="#999999",
    bd=0,
    cursor="hand2",
    command=voltar_menu
)

botao_voltar.pack(pady=5)

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

botao_sair.pack(pady=5)

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