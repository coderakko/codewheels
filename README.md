# codewheels
Sistema de controle de rover via LAN utilizando Python e ESP32.

📌 Descrição

O CodeWheels é um sistema desktop desenvolvido para controlar um rover remotamente através da rede local (LAN).
A aplicação permite cadastro do rover, autenticação de usuários e controle de movimentação utilizando teclado ou interface gráfica.

⚙️ Tecnologias Utilizadas
Python
Tkinter
ESP32
Socket TCP/IP
JSON
C++ (Arduino IDE)
🖥️ Funcionalidades
Sistema de login e registro
Cadastro de rover
Verificação de conexão do ESP32
Controle do rover via teclado (W, A, S, D)
Comunicação em rede local
Interface gráfica moderna
Salvamento de dados em JSON
Detecção de rover online/offline
🎮 Controles
Tecla	Função
W	Frente
S	Ré
A	Esquerda
D	Direita
🌐 Comunicação LAN

O sistema utiliza conexão TCP/IP entre:

Notebook/Desktop (Sistema Python)
ESP32 (Rover)

Ambos devem estar conectados na mesma rede Wi-Fi.

CodeWheels/
│
├── sistema.py
├── menu.py
├── controle.py
├── cadastro_rover.py
├── codigo_lan.ino
├── rover.json
├── usuarios.json
├── Wheel Turn.otf
└── README.md