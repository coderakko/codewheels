// Projeto acadêmico desenvolvido com auxílio do Jarvis (ChatGPT) com autorização do professor Lucas Moreira
// para apoio na implementação, correções e integração entre Python e ESP32.
// O código foi revisado, testado e adaptado pela autora do projeto.

#include <WiFi.h>

// ===============================
// CONFIGURAÇÃO DO WI-FI
// ===============================

const char* ssid = "iPhone de Rafa";
const char* password = "SUA_SENHA_DO_WIFI";

// ===============================
// SERVIDOR LAN
// ===============================

WiFiServer server(5000);

// ===============================
// PINOS DOS MOTORES
// ===============================

// Motor esquerdo
const int motor1A = 18;
const int motor1B = 19;

// Motor direito
const int motor2A = 25;
const int motor2B = 26;


// ===============================
// FUNÇÕES DOS MOTORES
// ===============================

void pararMotores() {
  digitalWrite(motor1A, LOW);
  digitalWrite(motor1B, LOW);

  digitalWrite(motor2A, LOW);
  digitalWrite(motor2B, LOW);
}


void frente() {
  digitalWrite(motor1A, HIGH);
  digitalWrite(motor1B, LOW);

  digitalWrite(motor2A, HIGH);
  digitalWrite(motor2B, LOW);
}


void tras() {
  digitalWrite(motor1A, LOW);
  digitalWrite(motor1B, HIGH);

  digitalWrite(motor2A, LOW);
  digitalWrite(motor2B, HIGH);
}


void esquerda() {
  digitalWrite(motor1A, HIGH);
  digitalWrite(motor1B, LOW);

  digitalWrite(motor2A, LOW);
  digitalWrite(motor2B, HIGH);
}

void direita() {
  digitalWrite(motor1A, LOW);
  digitalWrite(motor1B, HIGH);

  digitalWrite(motor2A, HIGH);
  digitalWrite(motor2B, LOW);

}


// ===============================
// SETUP
// ===============================

void setup() {
  Serial.begin(115200);

  pinMode(motor1A, OUTPUT);
  pinMode(motor1B, OUTPUT);
  pinMode(motor2A, OUTPUT);
  pinMode(motor2B, OUTPUT);

  pararMotores();

  WiFi.mode(WIFI_STA);
  WiFi.setSleep(false);

  Serial.println();
  Serial.println("Iniciando WiFi...");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi conectado!");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());

  server.begin();

  delay(1000);

  Serial.println("Servidor iniciado na porta 5000");
  Serial.println("Aguardando conexão do CodeWheels...");
}


// ===============================
// LOOP PRINCIPAL
// ===============================

void loop() {
  WiFiClient client = server.available();

  if (client) {
    Serial.println("Cliente conectado");

    while (client.connected()) {
      if (client.available()) {
        char comando = client.read();

        Serial.print("Comando recebido: ");
        Serial.println(comando);

        if (comando == 'w' || comando == 'W') {
          Serial.println("Movendo para frente");
          frente();
        }

        else if (comando == 's' || comando == 'S') {
          Serial.println("Movendo para tras");
          tras();
        }

        else if (comando == 'a' || comando == 'A') {
          Serial.println("Virando para esquerda");
          esquerda();
        }

        else if (comando == 'd' || comando == 'D') {
          Serial.println("Virando para direita");
          direita();
        }

        else if (comando == 'p' || comando == 'P') {
          Serial.println("Parando motores");
          pararMotores();
        }
      }
    }

    pararMotores();

    client.stop();

    Serial.println("Cliente desconectado");
    Serial.println("Aguardando nova conexão...");
  }
}