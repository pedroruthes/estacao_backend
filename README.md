# Backend para Estações Meteorológicas com FastAPI

Este projeto implementa um backend para coletar e gerenciar dados de estações meteorológicas, utilizando FastAPI para a API, SQLAlchemy como ORM e PostgreSQL como banco de dados. A autenticação das estações é feita através de uma chave API (`X-Controller-Key`) enviada no cabeçalho das requisições.

## Pré-requisitos

Antes de iniciar, certifique-se de ter instalado:

* **Python 3.8+**
* **PostgreSQL**: Um servidor PostgreSQL em execução.

## Configuração do Ambiente

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
    cd seu-repositorio
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3.  **Instale as dependências Python:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**
    Crie um arquivo `.env` na raiz do projeto (na mesma pasta deste `README.md`) e adicione a URL de conexão do seu banco de dados PostgreSQL. Substitua `user`, `password`, `host`, `port` e `database_name` pelas suas credenciais.

    ```
    # .env
    DATABASE_URL="postgresql://user:password@host:port/database_name"
    ```

## Como Rodar o Backend

1.  **Certifique-se que seu servidor PostgreSQL está em execução.**

2.  **Rode a aplicação FastAPI:**
    Com o ambiente virtual ativado, execute o seguinte comando na raiz do projeto:

    ```bash
    uvicorn app.main:app --reload
    ```
    O parâmetro `--reload` é útil para desenvolvimento, pois reinicia o servidor automaticamente a cada alteração no código. Para produção, você usaria um comando diferente (e.g., com Gunicorn).

3.  **Acesse a documentação da API:**
    Uma vez que o servidor esteja rodando, você pode acessar a documentação interativa da API (Swagger UI) em:
    `http://127.0.0.1:8000/docs`

    Você também pode ver a documentação ReDoc em:
    `http://127.0.0.1:8000/redoc`

## Implementação no Código C++ do ESP8266 (Arduino IDE)

O código C++ no seu ESP8266 deve ser configurado para enviar requisições HTTP POST para o endpoint `/data` do seu backend.

### Bibliotecas Necessárias (Arduino IDE)

Certifique-se de ter as seguintes bibliotecas instaladas no seu Arduino IDE (via Gerenciador de Bibliotecas):

* `ESP8266WiFi` (já vem com o core ESP8266)
* `ESP8266HTTPClient` (já vem com o core ESP8266)
* `ArduinoJson` (instale a versão 6 ou superior)

### Exemplo de Código C++ para ESP8266

```cpp
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h> // Certifique-se de usar a v6 ou superior

// --- CONFIGURAÇÕES DA SUA ESTAÇÃO ---
const char* ssid = "SEU_WIFI_SSID";          // Nome da sua rede Wi-Fi
const char* password = "SEU_WIFI_PASSWORD";  // Senha da sua rede Wi-Fi

// URL do endpoint do seu backend para receber dados.
// Use o IP do seu servidor ou o domínio se já estiver em produção/teste com DNS.
// Ex: "[http://192.168.1.100:8000/sensors/meteo](http://192.168.1.100:8000/sensors/meteo)"
const char* serverUrl = "http://SEU_IP_OU_DOMINIO_DO_BACKEND:8000/sensors/meteo";

// A CHAVE DO CONTROLADOR GERADA PELO BACKEND (Copie e cole a 'key' aqui)
const char* controller_key = "SUA_CHAVE_DO_CONTROLADOR_AQUI"; // Ex: "Y2IzZjk3NzM5MWI0..."

// --- FIM DAS CONFIGURAÇÕES ---

void setup() {
  Serial.begin(115200);
  delay(10);
  Serial.println("\nConectando ao WiFi...");

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConectado ao WiFi!");
  Serial.print("Endereço IP do ESP8266: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    // --- SIMULAÇÃO DE LEITURA DE SENSORES (Substitua por suas leituras reais) ---
    float temperature = 25.0 + random(-50, 50) / 10.0; // Ex: 20.0 a 30.0
    float humidity = 65.0 + random(-100, 100) / 10.0;   // Ex: 55.0 a 75.0
    int dir_wind = random(0, 360);                      // Ex: 0 a 359 graus
    float vel_wind = 3.0 + random(0, 100) / 10.0;      // Ex: 3.0 a 13.0 m/s
    float pressure = 1010.0 + random(-50, 50) / 10.0;   // Ex: 1005.0 a 1015.0 hPa
    float rain_measure = random(0, 20) / 10.0;          // Ex: 0.0 a 2.0 mm

    // --- CRIAÇÃO DO PAYLOAD JSON ---
    // A capacidade do DynamicJsonDocument deve ser suficiente para seus dados.
    // Use o ArduinoJson Assistant ([https://arduinojson.org/v6/assistant/](https://arduinojson.org/v6/assistant/)) para calcular.
    DynamicJsonDocument doc(256);
    doc["temperature"] = temperature;
    doc["humidity"] = humidity;
    doc["dir_wind"] = dir_wind;
    doc["vel_wind"] = vel_wind;
    doc["pressure"] = pressure;
    doc["rain_measure"] = rain_measure;

    String jsonString;
    serializeJson(doc, jsonString);

    Serial.print("JSON a ser enviado: ");
    Serial.println(jsonString);

    // --- REQUISIÇÃO HTTP POST ---
    WiFiClient client;
    HTTPClient http;

    http.begin(client, serverUrl); // Inicia a conexão HTTP
    http.addHeader("Content-Type", "application/json"); // Define o tipo de conteúdo como JSON
    http.addHeader("X-Controller-Key", controller_key); // Adiciona a chave de autenticação no cabeçalho

    Serial.println("Enviando requisição POST...");
    int httpResponseCode = http.POST(jsonString); // Envia a requisição POST com o corpo JSON

    // --- TRATAMENTO DA RESPOSTA ---
    if (httpResponseCode > 0) {
      Serial.printf("[HTTP] Código de Resposta: %d\n", httpResponseCode);
      String payload = http.getString(); // Obtém o corpo da resposta
      Serial.println("Resposta do servidor:");
      Serial.println(payload);
    } else {
      Serial.printf("[HTTP] Erro na Requisição: %s\n", http.errorToString(httpResponseCode).c_str());
    }

    http.end(); // Fecha a conexão HTTP
  } else {
    Serial.println("WiFi Desconectado. Tentando reconectar...");
    WiFi.begin(ssid, password);
    // Adicione um delay ou lógica de retry aqui para evitar loops infinitos
  }

  // Esperar 10 minutos (10 * 60 * 1000 milissegundos) antes da próxima requisição
  Serial.println("Aguardando 10 minutos para a próxima leitura...");
  delay(10 * 60 * 1000);
}