#include <Servo.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

int button = 33;
int reset = 27;
int ena = 5;
int in1 = 18;
int in2 = 19;
int dendo = 2;
int denvang = 4;
int denxanh = 16;
int sensor0 = 35;
int sensor1 = 34;
int sensor2 = 32;

//LCD display
LiquidCrystal_I2C lcd(0x27, 16, 2);

static const int servoPin1 = 12;
static const int servoPin2 = 14;
Servo servo1;
Servo servo2;

void setup() {
  Serial.begin(115200);
  
  servo1.attach(servoPin1);
  servo2.attach(servoPin2);
  pinMode(button, INPUT_PULLUP);
  pinMode(reset, INPUT_PULLUP);
  pinMode(sensor0, INPUT);
  pinMode(sensor1, INPUT);
  pinMode(sensor2, INPUT);
  pinMode(ena, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(dendo, OUTPUT);
  pinMode(denvang, OUTPUT);
  pinMode(denxanh, OUTPUT);

  lcd.init();// Initialize the LCD
  lcd.backlight();// Turn on the backlight
  lcd.clear();// Clear the LCD screen
}

void loop() {
  bool button_status = digitalRead(button);
  bool reset_status = digitalRead(reset);
  bool sensor0_status = digitalRead(sensor0);
  bool sensor1_status = digitalRead(sensor1);
  bool sensor2_status = digitalRead(sensor2);

  if (sensor0_status == 0){
    digitalWrite(denvang, HIGH);
    delay(1000);
    digitalWrite(denvang,LOW);
    // Serial.print("Sensor0 status = ");
    // Serial.println(sensor0_status);
  }

  if (sensor1_status == 0){
    servo2.write(180);
    delay(2000);
    servo2.write(90);
    // Serial.print("Sensor1 status = ");
    // Serial.println(sensor1_status);
  }

  if (sensor2_status == 0){
    servo1.write(180);
    delay(2000);
    servo1.write(90);
    // Serial.print("Sensor2 status = ");
    // Serial.println(sensor2_status);
  }
  if (reset_status == 0){
    digitalWrite(denvang, HIGH);
  }else{
    digitalWrite(denvang, LOW);
  }

  if (button_status == 0){
    lcd.setCursor(0, 0);// Set the cursor to the first column and first row
    lcd.print("1");
    digitalWrite(denxanh, HIGH);
    digitalWrite(dendo, LOW);
    delay(10);
    analogWrite(ena, 255);
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);

  } else{
    lcd.setCursor(0, 0);// Set the cursor to the first column and first row
    lcd.print("0");
    digitalWrite(dendo, HIGH);
    digitalWrite(denxanh, LOW);
    delay(10);
    analogWrite(ena, 0);
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);

  }
}
