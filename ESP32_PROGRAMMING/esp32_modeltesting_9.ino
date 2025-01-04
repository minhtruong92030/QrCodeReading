#include <WebServer.h>
#include <WiFi.h>
#include <Servo.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Webserver
const char* WIFI_SSID = "Aris_1168";
const char* WIFI_PASS = "1234567899";

WebServer server(80);

//lcd display
LiquidCrystal_I2C lcd(0x27, 16, 2);
int coca = 0;
int pepsi = 0;
int fanta = 0;
int sl = 0;

// ESP32 control
int button = 33;
int reset = 27;
int sensor0 = 35;
int sensor1 = 34;
int sensor2 = 32;
int dendo = 2;
int denvang = 4;
int denxanh = 16;
int in1 = 18;
int in2 = 19;
int enA = 5;
int buttonrelay = 15;
int i = 0;
int a[2] = {0,0};
int temp_swap = 0;
static const int servoPin1 = 14;
static const int servoPin2 = 12;
Servo servo1;
Servo servo2;
bool sl_temp = false;
bool pr_temp = false;
bool running = false;
bool fa_temp = false;

String product = "";
String SysRun = "";

unsigned long startTime1 = 0;
unsigned long startTime2 = 0;
unsigned long waitStartTime1 = 0;
unsigned long waitStartTime2 = 0;
const unsigned long duration = 1700;
const unsigned long waitTime = 800;

bool temp1 = 0;
bool temp2 = 0;
bool isWaiting1 = false;
bool isWaiting2 = false;

//Biến cho sensor0
unsigned long sensor0WaitStartTime = 0;
unsigned long sensor0PauseStartTime = 0;
const unsigned long sensor0WaitDuration = 1900;
const unsigned long sensor0PauseDuration = 3000;
bool sensor0Waiting = false;
bool sensor0Paused = false;

void handlePost_product() {
  if (server.hasArg("name")) {
    product = server.arg("name");
    server.send(200, "success");
    i++;
    Serial.print("i = ");
    Serial.println(i);
    Serial.print("product = ");
    Serial.println(product);

    for (int n = 0; n <= 1; n++){
      Serial.print(a[n]); 
      Serial.print(" ");
    }
    Serial.println("");
    if (i > 1){
      i = 0;
    }
  } else {
    server.send(400, "Missing product name");
  }
}

void handlePost_SysRun() {
  if (server.hasArg("name")) {
    SysRun = server.arg("name");
    server.send(200, "success");
  } else {
    server.send(400, "Missing product name");
  }
}

void setup() {
  Serial.begin(115200);

  lcd.init();// Initialize the LCD
  lcd.backlight();// Turn on the backlight
  lcd.clear();// Clear the LCD screen

  servo1.attach(servoPin1);
  servo2.attach(servoPin2);

  pinMode(button, INPUT_PULLUP);
  pinMode(reset, INPUT_PULLUP);
  pinMode(sensor0, INPUT);
  pinMode(sensor1, INPUT);
  pinMode(sensor2, INPUT);
  pinMode(dendo, OUTPUT);
  pinMode(denvang, OUTPUT);
  pinMode(denxanh, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(enA, OUTPUT);
  pinMode(buttonrelay, OUTPUT);

  WiFi.persistent(false);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWifi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  server.on("/product1", HTTP_POST, handlePost_product);
  server.on("/sysrun", HTTP_POST, handlePost_SysRun);
  server.begin();
  Serial.println("HTTP server started");

}

void loop() {
  server.handleClient();

  bool button_status = digitalRead(button);
  bool reset_status = digitalRead(reset);

  //lcd display
  lcd.setCursor(0, 0);// Set the cursor to the first column and first row
  lcd.print("COCA:");
  lcd.print(coca);

  lcd.setCursor(8, 0);// Set the cursor to the first column and first row
  lcd.print("PEPSI:");
  lcd.print(pepsi);

  lcd.setCursor(0,1);
  lcd.print("FANTA:");
  lcd.print(fanta);

  lcd.setCursor(8,1);
  lcd.print("SL:");
  lcd.print(sl);

  if (reset_status == 0){
    digitalWrite(denvang, HIGH);
    lcd.clear();
    coca = 0;
    pepsi = 0;
    fanta = 0;
    sl = 0;
  }else{
    digitalWrite(denvang, LOW);
  }

  if (SysRun == "STOP"){
    digitalWrite(buttonrelay, HIGH);
  }

  if (SysRun == "START"){
    digitalWrite(buttonrelay, LOW);
  }

  if(button_status == 0) {
    delay(10);
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    analogWrite(enA, 255);
    digitalWrite(denxanh, HIGH);
    digitalWrite(dendo, LOW);
    running = true;
  }else{
    digitalWrite(denxanh, LOW);
    digitalWrite(dendo, HIGH);
  }

  while(running) {
    server.handleClient();

    lcd.setCursor(0, 0);// Set the cursor to the first column and first row
    lcd.print("COCA:");
    lcd.print(coca);

    lcd.setCursor(8, 0);// Set the cursor to the first column and first row
    lcd.print("PEPSI:");
    lcd.print(pepsi);

    lcd.setCursor(0,1);
    lcd.print("FANTA:");
    lcd.print(fanta);

    lcd.setCursor(8,1);
    lcd.print("SL:");
    lcd.print(sl);

    bool button_status = digitalRead(button);
    bool reset_status = digitalRead(reset);
    bool sensor0_status = digitalRead(sensor0);
    bool sensor1_status = digitalRead(sensor1);
    bool sensor2_status = digitalRead(sensor2);
    unsigned long currentTime = millis();
    
    // if (a[i] != 0){
    //   Serial.print("a[0] = ");
    //   Serial.print(a[0]);
    //   Serial.print(" ");
    //   Serial.print("a[1] = ");
    //   Serial.println(a[1]);
    // }

    if (a[0] == 0){
      temp_swap = a[0];
      a[0] = a[1];
      a[1] = temp_swap;
    }

    if (product == "COCA"){
      a[i] = 1;
      product = "";
    }

    if (product == "PEPSI"){
      a[i] = 2;
      product = "";
    }

    if (product == "FANTA"){
      a[i] = 3;
      product = "";
    }
    // if (sensor0_status == 0 && !sensor0Waiting && !sensor0Paused) {
    //   sensor0WaitStartTime = currentTime;
    //   sensor0Waiting = true;
    // }

    // if (sensor0Waiting && currentTime - sensor0WaitStartTime >= sensor0WaitDuration) {
    //   digitalWrite(in1, LOW);
    //   digitalWrite(in2, LOW);
    //   analogWrite(enA, 0);
    //   sensor0PauseStartTime = currentTime;
    //   sensor0Waiting = false;
    //   sensor0Paused = true;
    // }

    // if (sensor0Paused && currentTime - sensor0PauseStartTime >= sensor0PauseDuration) {
    //   digitalWrite(in1, HIGH);
    //   digitalWrite(in2, LOW);
    //   analogWrite(enA, 255);
    //   sensor0Paused = false;
    // }

    // if (sensor0_status == 0){
    //   sl++; 
    //   lcd.setCursor(0,1);
    //   lcd.print("SL:");
    //   lcd.print(sl);
    // }

    if (sensor0_status == 0){
      sl_temp = 1;
    }

    if (sl_temp == 1 && sensor0_status == 1){
      sl_temp = 0;
      sl++;
    }

    if (a[0] == 1 && sensor1_status == 0 && temp1 == 0 && !isWaiting1) {
      a[0] = 0;
      waitStartTime1 = currentTime;
      isWaiting1 = true;
    }
    if (isWaiting1 && currentTime - waitStartTime1 >= waitTime) {
      temp1 = 1;
      startTime1 = currentTime;
      servo1.write(0);
      coca++;
      isWaiting1 = false;
    }
    if (temp1 == 1) {
      if (currentTime - startTime1 < duration) {
      } else if (currentTime - startTime1 < 2 * duration) {
          servo1.write(180);
      } else {
          servo1.write(90);
          // product = "";
          temp1 = 0;
      }
    }

    if (a[0] == 2 && sensor1_status == 0){
      a[0] = 0;
      pr_temp = true;
    }

    if (a[0] == 3 && sensor2_status == 0){
      fa_temp = 1;
      a[0] = 0;
    }

    if(fa_temp == 1 && sensor2_status == 1){
      fa_temp = 0;
      fanta++;
    }

    if (pr_temp == true && sensor2_status == 0 && temp2 == 0 && !isWaiting2) {
      if (fa_temp == 0){
        pr_temp = false;
        waitStartTime2 = currentTime;
        isWaiting2 = true;
      }else{
        servo2.write(90);
      }  
    }

    // if (pr_temp == true && sensor2_status == 0 && temp2 == 0 && !isWaiting2) {
    //     pr_temp = false;
    //     waitStartTime2 = currentTime;
    //     isWaiting2 = true; 
    // }
    
    if (isWaiting2 && currentTime - waitStartTime2 >= waitTime) {
      temp2 = 1;
      startTime2 = currentTime;
      servo2.write(0);
      pepsi++;
      isWaiting2 = false;
    }
    if (temp2 == 1) {
      if (currentTime - startTime2 < duration) {
      } else if (currentTime - startTime2 < 2 * duration) {
          servo2.write(180);
      } else {
          servo2.write(90);
          // product = "";
          temp2 = 0;
      }
    }

    // if (product == "FANTA") {
    //   Serial.print(product);
    //   product = "";
    // }
    if (reset_status == 0){
      digitalWrite(denvang, HIGH);
      lcd.clear();
      coca = 0;
      pepsi = 0;
      fanta = 0;
      sl = 0;
    }else{
      digitalWrite(denvang, LOW);
    }

    if (SysRun == "STOP"){
      digitalWrite(buttonrelay, HIGH);
      product = "";
    }

    if (button_status == 1) {
      digitalWrite(in1, LOW);
      digitalWrite(in2, LOW);
      analogWrite(enA, 0);
      running = false;
      product = "";
    }
  }
}
