#include "DHT.h"
#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "todo";
const char* password = "Todotodo";

// Replace with your server (local machine) IP and port
const char* serverName = "192.168.34.192";

#define DHTPIN 26      // Pin where DHT11 is connected
#define DHTTYPE DHT11 // DHT 11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
    Serial.begin(115200);   // Start the Serial communication
    WiFi.begin(ssid, password); // Connect to Wi-Fi

    while (WiFi.status() != WL_CONNECTED) {  // Wait for connection
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi");

    dht.begin();  // Initialize the DHT sensor
}

void loop() {
    delay(2000);  // Delay between readings
    float temperature = dht.readTemperature(); // Read temperature in Celsius
    float humidity = dht.readHumidity(); // Read humidity

    if (isnan(temperature) || isnan(humidity)) {  // Check for reading errors
        Serial.println("Failed to read from DHT sensor!");
        return;
    }

    // Print temperature and humidity values to the console
    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.print(" °C, Humidity: ");
    Serial.print(humidity);
    Serial.println(" %");

    // Send data to Flask server
    WiFiClient client;
    if (client.connect(serverName, 5000)) {
        String url = "/update?temperature=" + String(temperature) + "&humidity=" + String(humidity);
        client.print(String("GET ") + url + " HTTP/1.1\r\n" +
                    "Host: " + serverName + "\r\n" +
                    "Connection: close\r\n\r\n");
        delay(1000);  // Delay for stability
    }

    delay(4000);  // Send data every 4 seconds
}