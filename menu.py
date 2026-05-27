import tkinter as tk
import subprocess
import socket
import sys
import json
import os
import pyglet

pyglet.font.add_file("Wheel Turn.otf")

PORTA = 5000
ARQUIVO_ROVER = "rover.json"

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


def testar_conexao():
    dados = carregar_rover()
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
    janela.destroy()
    subprocess.Popen(["py", "controle.py", usuario])


def abrir_cadastro():
    janela.destroy()
    subprocess.Popen(["py", "cadastro_rover.py", usuario])


def voltar_sistema():
    janela.destroy()
    subprocess.Popen(["py", "sistema.py"])


def atualizar_status():
    dados = carregar_rover()

    label_nome_rover.config(
        text=f"Rover: {dados['nome']}"
    )

    if dados["ip"] == "":
        label_ip.config(
            text="IP: não cadastrado"
        )

        label_status.config(
            text="Cadastre o rover para verificar a conexão",
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

label_topo = tk.Label(
    topo,
    text="🚗 Painel do Rover",
    font=("Arial", 20),
    bg="#F0F0F0",
    fg="#6E6E6E"
)

label_topo.pack(pady=20)

icone = tk.Label(
    card,
    text="🚙",
    font=("Arial", 60),
    bg="white",
    fg="#AAAAAA"
)

icone.pack(pady=12)

label_usuario = tk.Label(
    card,
    text=f"Usuário logado: {usuario}",
    font=("Arial", 14),
    bg="white",
    fg="#777777"
)

label_usuario.pack(pady=4)

label_nome_rover = tk.Label(
    card,
    text="Rover: carregando...",
    font=("Arial", 13),
    bg="white",
    fg="#777777"
)

label_nome_rover.pack(pady=4)

label_ip = tk.Label(
    card,
    text="IP: carregando...",
    font=("Arial", 13),
    bg="white",
    fg="#777777"
)

label_ip.pack(pady=4)

label_status = tk.Label(
    card,
    text="Verificando conexão...",
    font=("Arial", 14, "bold"),
    bg="white",
    fg="#999999"
)

label_status.pack(pady=10)

botao_controle = tk.Button(
    card,
    text="Abrir Controle",
    font=("Arial", 15, "bold"),
    bg="#BFC5CC",
    fg="#2E2E2E",
    bd=0,
    width=20,
    cursor="hand2",
    command=abrir_controle
)

botao_controle.pack(pady=7)

botao_cadastro = tk.Button(
    card,
    text="Cadastrar Rover",
    font=("Arial", 15, "bold"),
    bg="#BFC5CC",
    fg="#2E2E2E",
    bd=0,
    width=20,
    cursor="hand2",
    command=abrir_cadastro
)

botao_cadastro.pack(pady=7)

botao_voltar = tk.Button(
    card,
    text="Sair para Tela de Login",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="#999999",
    bd=0,
    cursor="hand2",
    command=voltar_sistema
)

botao_voltar.pack(pady=4)

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

botao_sair.pack(pady=2)

atualizar_status()

janela.mainloop()