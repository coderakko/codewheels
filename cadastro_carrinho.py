import tkinter as tk
from tkinter import messagebox
import json
import pyglet

pyglet.font.add_file("Wheel Turn.otf")

ARQUIVO_CARRINHO = "carrinho.json"


def salvar_carrinho():
    nome = entrada_nome.get()
    ip = entrada_ip.get()

    if nome == "" or ip == "":
        messagebox.showerror("Erro", "Preencha todos os campos.")
        return

    dados = {
        "nome": nome,
        "ip": ip
    }

    with open(ARQUIVO_CARRINHO, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4)

    messagebox.showinfo("Sucesso", "Carrinho cadastrado com sucesso!")


janela = tk.Tk()
janela.title("CodeWheels - Cadastro do Carrinho")
janela.geometry("700x520")
janela.configure(bg="#D9D9D9")
janela.resizable(False, False)

titulo = tk.Label(
    janela,
    text="💻CodeWheels🚗",
    font=("Wheel Turn", 30),
    bg="#D9D9D9",
    fg="#6E6E6E"
)
titulo.pack(pady=25)

card = tk.Frame(
    janela,
    bg="white",
    width=450,
    height=330
)
card.pack()
card.pack_propagate(False)

topo = tk.Frame(
    card,
    bg="#F0F0F0",
    width=450,
    height=70
)
topo.pack(fill="x")

texto_topo = tk.Label(
    topo,
    text="🚙 Cadastro do Carrinho",
    font=("Arial", 18),
    bg="#F0F0F0",
    fg="#6E6E6E"
)
texto_topo.pack(pady=18)

label_nome = tk.Label(
    card,
    text="Nome do Carrinho",
    font=("Arial", 12),
    bg="white",
    fg="#6E6E6E"
)
label_nome.pack(pady=(35, 5))

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
    text="IP do Carrinho / ESP32",
    font=("Arial", 12),
    bg="white",
    fg="#6E6E6E"
)
label_ip.pack(pady=(25, 5))

entrada_ip = tk.Entry(
    card,
    font=("Arial", 12),
    width=30,
    bg="#F1F1F1",
    bd=0
)
entrada_ip.pack(ipady=10)

botao = tk.Button(
    card,
    text="Cadastrar Carrinho",
    font=("Arial", 13, "bold"),
    bg="#BFC5CC",
    fg="#2E2E2E",
    bd=0,
    width=20,
    height=1,
    cursor="hand2",
    command=salvar_carrinho
)
botao.pack(pady=35)

janela.mainloop()