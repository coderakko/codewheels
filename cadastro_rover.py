import tkinter as tk
from tkinter import messagebox
import json
import socket
import sys
import subprocess
import pyglet

pyglet.font.add_file("Wheel Turn.otf")

ARQUIVO_ROVER = "rover.json"
PORTA = 5000

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


def validar_ip(ip):
    partes = ip.split(".")

    if len(partes) != 4:
        return False

    for parte in partes:
        if not parte.isdigit():
            return False

        numero = int(parte)

        if numero < 0 or numero > 255:
            return False

    return True


def testar_rover(ip):
    try:
        cliente = socket.socket()
        cliente.settimeout(3)
        cliente.connect((ip, PORTA))
        cliente.close()
        return True
    except:
        return False


def salvar_rover():
    nome = entrada_nome.get().strip()
    ip = entrada_ip.get().strip()

    if nome == "" or ip == "":
        label_resultado.config(
            text="Erro: preencha todos os campos.",
            fg="#E74C3C"
        )
        messagebox.showerror("Erro", "Preencha todos os campos.")
        return

    if len(nome) < 3:
        label_resultado.config(
            text="Erro: nome inválido.",
            fg="#E74C3C"
        )
        messagebox.showerror(
            "Erro",
            "O nome do rover deve ter pelo menos 3 caracteres."
        )
        return

    if not validar_ip(ip):
        label_resultado.config(
            text="Erro: IP inválido.",
            fg="#E74C3C"
        )
        messagebox.showerror(
            "Erro",
            "Digite um IP válido. Exemplo: 192.168.0.25"
        )
        return

    label_resultado.config(
        text="Verificando se o rover está online...",
        fg="#6E6E6E"
    )
    janela.update()

    if not testar_rover(ip):
        label_resultado.config(
            text="Rover não encontrado ou desconectado.",
            fg="#E74C3C"
        )
        messagebox.showerror(
            "Erro",
            "Não foi possível conectar ao rover. Verifique se o ESP32 está ligado, na mesma rede Wi-Fi e usando o IP correto."
        )
        return

    dados = {
        "nome": nome,
        "ip": ip
    }

    with open(ARQUIVO_ROVER, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4)

    label_resultado.config(
        text=f"Rover '{nome}' cadastrado e conectado!",
        fg="#2ECC71"
    )

    messagebox.showinfo(
        "Sucesso",
        "Rover cadastrado corretamente e está online!"
    )


def voltar_menu():
    janela.destroy()
    subprocess.Popen(["py", "menu.py", usuario])


janela = tk.Tk()
janela.title("CodeWheels - Cadastro do Rover")
janela.geometry("700x560")
janela.configure(bg="#D9D9D9")
janela.resizable(False, False)

titulo = tk.Label(
    janela,
    text="💻Code Wheels🚗",
    font=("Wheel Turn", 30),
    bg="#D9D9D9",
    fg="#6E6E6E"
)
titulo.pack(pady=25)

card_canvas, card = criar_card_arredondado(
    janela,
    450,
    390
)
card_canvas.pack()

topo = tk.Frame(
    card,
    bg="#F0F0F0",
    width=430,
    height=70
)
topo.pack(fill="x")

label_topo = tk.Label(
    topo,
    text="🚙 Cadastro do Rover",
    font=("Arial", 18),
    bg="#F0F0F0",
    fg="#6E6E6E"
)
label_topo.pack(pady=18)

label_nome = tk.Label(
    card,
    text="Nome do Rover",
    font=("Arial", 12),
    bg="white",
    fg="#6E6E6E"
)
label_nome.pack(pady=(25, 5))

entrada_nome = tk.Entry(
    card,
    font=("Arial", 12),
    width=30,
    bg="#F1F1F1",
    bd=0
)
entrada_nome.pack(ipady=10)

label_ip = tk.Label(
    card,
    text="IP do Rover / ESP32",
    font=("Arial", 12),
    bg="white",
    fg="#6E6E6E"
)
label_ip.pack(pady=(18, 5))

entrada_ip = tk.Entry(
    card,
    font=("Arial", 12),
    width=30,
    bg="#F1F1F1",
    bd=0
)
entrada_ip.pack(ipady=10)

botao_confirmar = tk.Button(
    card,
    text="Confirmar Cadastro do Rover",
    font=("Arial", 13, "bold"),
    bg="#BFC5CC",
    fg="#2E2E2E",
    bd=0,
    width=24,
    cursor="hand2",
    command=salvar_rover
)
botao_confirmar.pack(pady=18)

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
botao_voltar.pack(pady=3)

label_resultado = tk.Label(
    card,
    text="",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="#777777"
)
label_resultado.pack(pady=5)

janela.mainloop()