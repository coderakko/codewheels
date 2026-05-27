#código do professor #

#include <WiFi.h>

const char* ssid = "Rede Fessor";
const char* password = "12345678";

// IP FIXO DO CARRINHO
IPAddress local_IP(10, 151, 185, 105);
IPAddress gateway(10, 151, 185, 189);
IPAddress subnet(255, 255, 255, 0);

WiFiServer server(5000);

// ================= MOTORES =================
// Motor esquerdo
const int motor1A = 18;
const int motor1B = 19;

// Motor direito
const int motor2A = 25;
const int motor2B = 26;

void setup() {

  Serial.begin(115200);

  // CONFIGURA PINOS DOS MOTORES
  pinMode(motor1A, OUTPUT);
  pinMode(motor1B, OUTPUT);

  pinMode(motor2A, OUTPUT);
  pinMode(motor2B, OUTPUT);

  // GARANTE MOTORES PARADOS
  pararMotores();

  WiFi.config(local_IP, gateway, subnet);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi conectado");
  Serial.println(WiFi.localIP());

  server.begin();
}

void loop() {

  WiFiClient client = server.available();

  if (client) {

    while (client.connected()) {

      if (client.available()) {

        char comando = client.read();

        Serial.print("Recebido: ");
        Serial.println(comando);

        // FRENTE
        if (comando == 'w') {
          Serial.println("Movendo para frente");

          digitalWrite(motor1A, HIGH);
          digitalWrite(motor1B, LOW);

          digitalWrite(motor2A, HIGH);
          digitalWrite(motor2B, LOW);
        }

        // TRÁS
        if (comando == 's') {
          Serial.println("Movendo para trás");

          digitalWrite(motor1A, LOW);
          digitalWrite(motor1B, HIGH);

          digitalWrite(motor2A, LOW);
          digitalWrite(motor2B, HIGH);
        }

        // ESQUERDA
        if (comando == 'a') {
          Serial.println("Virando esquerda");

          digitalWrite(motor1A, LOW);
          digitalWrite(motor1B, HIGH);

          digitalWrite(motor2A, HIGH);
          digitalWrite(motor2B, LOW);
        }

        // DIREITA
        if (comando == 'd') {
          Serial.println("Virando direita");

          digitalWrite(motor1A, HIGH);
          digitalWrite(motor1B, LOW);

          digitalWrite(motor2A, LOW);
          digitalWrite(motor2B, HIGH);
        }

        // PARAR
        if (comando == 'p') {
          Serial.println("Parando");

          pararMotores();
        }
      }
    }

    client.stop();
  }
}

// ================= FUNÇÃO PARAR =================
void pararMotores() {

  digitalWrite(motor1A, LOW);
  digitalWrite(motor1B, LOW);

  digitalWrite(motor2A, LOW);
  digitalWrite(motor2B, LOW);
}
