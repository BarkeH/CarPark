#include <EasyUltrasonic.h>
#include <LiquidCrystal_I2C.h>
#include <Servo.h>

LiquidCrystal_I2C lcd(0x27,16,2);

const int threshold = 30;

Servo gateServo;

typedef struct{
  int redLED;
  int greenLED;
  int framesOn;
  int ultraPin;
  EasyUltrasonic ultrasonic;
}carSpot;

const int numCarParks = 1;
carSpot spotArray[1] = {{2,3,0,4}};

void setup() {
  Serial.begin(9600);

  lcd.init();
  lcd.clear();
  lcd.backlight();

  gateServo.attach(9);

  for (int i = 0; i < numCarParks; i++){
    pinMode(spotArray[i].redLED,OUTPUT);
    pinMode(spotArray[i].greenLED,OUTPUT);
    digitalWrite(spotArray[i].greenLED, HIGH);
    digitalWrite(spotArray[i].redLED, LOW);

    spotArray[i].ultrasonic.attach(spotArray[i].ultraPin,spotArray[i].ultraPin);
  }
    
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0){

    String dataType = Serial.readStringUntil(',');
    String data = Serial.readStringUntil('\n');
    
    Serial.print("You sent me: ");
    Serial.println(dataType+data);

    if (dataType == "pay"){
      lcd.clear();
      lcd.setCursor(0,0);
      
      lcd.print("You Owe:");
      lcd.setCursor(0,1);
      lcd.print(data);
      
    }else if (dataType == "gate"){
      if (data == "open"){
        gateServo.write(70);
      }else if (data == "close"){
        gateServo.write(0);
      }
    }
    
  }

  for (int i = 0; i < numCarParks; i++){
    
    float distanceCM = convertToCM(spotArray[i].ultrasonic.getDistanceIN());
    //Serial.println("you made it her");
    if (distanceCM < threshold){
      digitalWrite(spotArray[i].greenLED, LOW);
      digitalWrite(spotArray[i].redLED, HIGH);
    }else {
      digitalWrite(spotArray[i].greenLED, HIGH);
      digitalWrite(spotArray[i].redLED, LOW);
    }
  }
  
  
  
}
