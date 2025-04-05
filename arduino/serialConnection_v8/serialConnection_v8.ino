
#include "Arduino.h"
#include <HX711.h>
#include <digitalWriteFast.h>
#define baudrate 115200 // 9600
#define wheelDiameter (32.35/359) //inches, yet wrong
#define kg_lbs 2.20462262 //kg to lbs
#define kg_Newtons 9.81 //kg to Newtons

//Bennett-era pin values, altered May 8, 2022
#define c_EncoderInterrupt 0 // not used
#define c_EncoderPinA 8
#define c_EncoderPinB 10

String sentByte;
int rec;
int n = 0;
int incomingbyte;
long value_encoderTicks;
long value_encoderDegrees;
volatile bool _EncoderBSet;
volatile long _EncoderTicks = 0;
bool started = false;
bool stopped = false;

bool reset = true;
bool op = false;
char rbytes[1];
float calibra = -199750;
float actualDiameter;
float Newtons;
float kgs;
HX711 scale;

void setup() {
  Serial.begin(baudrate);
  
  scale.set_scale(); //here is the problem
  scale.tare(); //Reset the scale to 0
  long zero_factor = scale.read_average(); 
  // Left encoder
  pinMode(c_EncoderPinA, INPUT);      // sets pin A as input
  digitalWrite(c_EncoderPinA, LOW);  // turn on pullup resistors
  pinMode(c_EncoderPinB, INPUT);      // sets pin B as input
  digitalWrite(c_EncoderPinB, LOW);  // turn on pullup resistors
  attachInterrupt(c_EncoderInterrupt, rotation, RISING);  
}
void loop() {
  delay(1);

  //rec = Serial.available(); // check if RPi has sent data
  //incomingbyte = Serial.read();
  //if (rec > 0){ // data recieved!
  if (Serial.available() > 0){ // data recieved!
    //for(n = 0; n < rec; n++){ // for every byte received
    rbytes[n] = Serial.read(); // read data
    //n++;
    incomingbyte = rbytes[n];
      if(rbytes[n] == 's'){//DATA COLLECTION BEGINS
        if(started == false){
          //sentByte=String(rbytes[n]);
          //Serial.print("n=");
          //delay(0.1);
          //Serial.println(n);
          Serial.println("Started!"); //Serial.println(sentByte);
          Serial.flush();
          n++;
          op = true;
          reset = false;
          started = true;
        }
      }
      else if(rbytes[n] == 'x'){//DATA COLLECTION STOPS 
          //sentByte=String(rbytes[n]);
          //Serial.print("n=");
          //Serial.println(n);
          Serial.println("Stopped!"); //Serial.println(sentByte); // this will be the last line, because the python says print(line); if line =="Stopped!": hasStopped = True;
          Serial.flush();
          n++;
          op = false;
          reset = true;
          rotation();   
      }
  }

  //}
  //delay(.5);
  //MAIN OPERATION - Serial sending data to RPi
  
  if(op == true){  
      scale.set_scale(calibra);//force sensor calibration
   
      value_encoderTicks = _EncoderTicks; // get Encoder Ticks 
      value_encoderDegrees = map(value_encoderTicks, 0, 1023, 0, 359); // convert to degrees
    
      actualDiameter = value_encoderDegrees*wheelDiameter; // convert to actual distance traveled
      Serial.print(actualDiameter);
      Serial.print("|");

      
      kgs = scale.get_units();
      Newtons = scale.get_units()*kg_Newtons; // convert to Newtons.
      
      Serial.print(Newtons, 3);// send lbs to 3 decimal places
      Serial.println();
   
      Serial.flush();//added 6/20/2019 to wait until data is written to Pi
      //delay(2); // delay needed?      
  }
}

// Encoder Function
void rotation()
{
  if (reset == false){

  _EncoderBSet = digitalReadFast(c_EncoderPinB);   // read the input pin
  
  #ifdef EncoderIsReversed
    _EncoderTicks += _EncoderBSet ? -1 : +1;
  #else
    _EncoderTicks -= _EncoderBSet ? -1 : +1;
  #endif
 }
 if(reset == true){
  
 _EncoderTicks = 0;

  }
}
