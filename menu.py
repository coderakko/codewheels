import tkinter as tk
import subprocess
import socket
import sys
import pyglet

pyglet.font.add_file("Wheel Turn.otf")

IP_ESP32 = "192.168.7.149"
PORTA = 5000

usuario = "Usuário"

if len(sys.argv) > 1:
    usuario = sys.argv[1]


def testar_conexao():

    try:

        cliente = socket.socket()

        cliente.settimeout(2)

        cliente.connect((IP_ESP32, PORTA))

        cliente.close()

        return True

    except:

        return False


def abrir_controle():

    subprocess.run(["py", "controle.py"])


def atualizar_status():

    if testar_conexao():

        label_status.config(
            text="ESP32 ONLINE",
            fg="#2ECC71"
        )

    else:

        label_status.config(
            text="ESP32 OFFLINE - modo teste",
            fg="#E74C3C"
        )

    janela.after(3000, atualizar_status)


janela = tk.Tk()

janela.title("CodeWheels - Menu")

janela.geometry("760x620")

janela.configure(bg="#D9D9D9")

janela.resizable(False, False)

# ==========================================
# TÍTULO
# ==========================================

titulo = tk.Label(
    janela,
    text="💻CodeWheels🚗",
    font=("Wheel Turn", 32),
    bg="#D9D9D9",
    fg="#6E6E6E"
)

titulo.pack(pady=30)

# ==========================================
# CARD
# ==========================================

card = tk.Frame(
    janela,
    bg="white",
    width=500,
    height=430
)

card.pack()

card.pack_propagate(False)

# ==========================================
# TOPO
# ==========================================

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

# ==========================================
# ÍCONE
# ==========================================

icone = tk.Label(
    card,
    text="🚙",
    font=("Arial", 70),
    bg="white",
    fg="#AAAAAA"
)

icone.pack(pady=20)

# ==========================================
# USUÁRIO
# ==========================================

label_usuario = tk.Label(
    card,
    text=f"Usuário logado: {usuario}",
    font=("Arial", 14),
    bg="white",
    fg="#777777"
)

label_usuario.pack(pady=5)

# ==========================================
# STATUS
# ==========================================

label_status = tk.Label(
    card,
    text="Verificando conexão...",
    font=("Arial", 14, "bold"),
    bg="white",
    fg="#999999"
)

label_status.pack(pady=12)

# ==========================================
# BOTÃO CONTROLE
# ==========================================

botao_controle = tk.Button(
    card,
    text="Abrir Controle",
    font=("Arial", 15, "bold"),
    bg="#BFC5CC",
    fg="#2E2E2E",
    bd=0,
    width=18,
    height=1,
    cursor="hand2",
    command=abrir_controle
)

botao_controle.pack(pady=22)

# ==========================================
# BOTÃO SAIR
# ==========================================

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

# ==========================================
# ATUALIZAR STATUS
# ==========================================

atualizar_status()

janela.mainloop()