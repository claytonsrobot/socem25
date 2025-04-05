#include <digitalWriteFast.h>

#include <HX711.h>

#include "Arduino.h"
#include <digitalWriteFast.h>  // need to install this library (for reading encoder)
#include "HX711.h" // need to install library (for reading load cell amplifier)                              
#define c_EncoderInterrupt 0
#define c_EncoderPinA 2
#define c_EncoderPinB 3
#define DOUT 11
#define CLK 10
#define EncoderIsReversed

#define stepDis (1.80/360)*(0.46*PI) //distance (in.) stepper motor rotor travels from one step (for HES)
#define wheelD (32.35/359)
#define kg_lbs 2.20462262 //kg to lbs

float actualD;
float lbs;
int n;

volatile bool _EncoderBSet;
volatile long _EncoderTicks = 0;
long val; //need to be longs to be able to handle the amount of data from encoder
//long val2;
int rec;
char rbytes[1];
//int n = -1;
bool reset = true;
bool op = false;

//FOR LOAD CELL
//HX711 scale(DOUT, CLK); // NOTE: HX711 library was updated, if using newer version change to: HX711 scale;
HX711 scale; // NOTE: HX711 library was updated, if using newer version change to: HX711 scale;
String caliStr;
float calibra = -199750; // calibration factor: working well, but user can update in RPi GUI
bool caliLoop = false;
bool showF = false;
//float calibration_factor = -199750;201500 -199550 -195550 -198050 00

void setup()
{
  pinMode(c_EncoderPinA, INPUT);      // sets pin A as input
  pinMode(c_EncoderPinB, INPUT);      // sets pin B as input
  Serial.begin(115200);
  
  scale.set_scale();
  scale.tare(); //Reset the scale to 0

  long zero_factor = scale.read_average(); 
  
  // Left encoder
  
  digitalWrite(c_EncoderPinA, LOW);  // turn on pullup resistors
  
  digitalWrite(c_EncoderPinB, LOW);  // turn on pullup resistors
  attachInterrupt(c_EncoderInterrupt, rotation, RISING);  
}

void loop()
{ 
  rec = Serial.available(); // check if RPi has sent data

  if (rec > 0){ // data recieved!
    caliStr = ""; // clear calibration string
    
    for(n = 0; n < rec; n++){ // for every byte received
    rbytes[n] = Serial.read(); // read data

      if(rbytes[n] == 's'){//DATA COLLECTION BEGINS
        reset = false;
        op = true;
      }
      else if(rbytes[n] == 'x'){//DATA COLLECTION STOPS 
          Serial.flush();
          op = false;
          reset = true;
          rotation();   
      }
      else if (isDigit(rbytes[n]) || rbytes[n] == '-'){ // 'digit' = new load cell calibration has been sent
        caliStr += (char)rbytes[n]; // put calibration factor into string
        caliLoop = true; // to start calibration process (loop) after receiving full calibration factor (exiting for loop)
      }
      else if (rbytes[n] == 'd'){ // 'd' = end calibration process
        showF = false;
        caliLoop = false; // to stop calibration process

      }
       else if(rbytes[n] == 't'){// TARE 
         scale.set_scale();
         scale.tare(); //Reset the scale to 0
      }
    }
    if (caliLoop == true){ // starts calibration process (needs to be outside of for loop)
      showF = true;  
    }
  }
  delay(2); // delay might be important, provents several errors/bugs, need to test w/ sensors
  
  //MAIN OPERATION - Serial sending data to RPi
  if(op == true)
    {  
      scale.set_scale(calibra);//force sensor calibration
   
      val = _EncoderTicks; // get Encoder Ticks 
      val = map(val, 0, 1023, 0, 359); // convert to degrees
    
      actualD = val*wheelD; // convert to actual distance traveled
      Serial.print(actualD);
      Serial.print("|");

      lbs = scale.get_units()*kg_lbs; // convert to lbs.
      
      Serial.print(lbs, 3);// send lbs to 3 decimal places
      Serial.println();
   
      Serial.flush();//added 6/20/2019 to wait until data is written to Pi
      //delay(2); // delay needed?      
    }
  
  // Load Cell Calibration Process
  if (showF == true){
    calibra = caliStr.toFloat(); // convert calibra str to float
    scale.set_scale(calibra);//force sensor calibration
    lbs = scale.get_units()*kg_lbs; // convert to lbs.
    Serial.println(lbs, 3); // send lbs to 3 decimal places
    Serial.flush();
    //delay(50); // delay needed?
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
