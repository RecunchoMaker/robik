/*

Copyright (C) 2016 RecunchoMaker - http://recunchomaker.org

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
USA.

See LICENSE.txt for details
*/


#include <Servo.h>
//#include "Shell.h"
#include "Robot.h"
#include "CuboControl.h"

#include "Cmd.h"
//#include <Stepper.h> 
//#include <AccelStepper.h> 

// change this to the number of steps on your motor
//# el pequenito 32, el de la impresora 48
//#define STEPS 48 
#define STEPS 32 

// create an instance of the stepper class, specifying
// the number of steps of the motor and the pins it's
// attached to
//Stepper stepper(STEPS, 2, 5, 4, 3);
//AccelStepper grua(4, 2,5,4,3);
//AccelStepper base(4, 6,8,9,7);
Robot myRobot;


//Servo servoMuneca;  // create servo object to control a servo
//Servo servoPinza;  // create servo object to control a servo

int motor;
char junk;  // mierda que puede entrar por el serie

int i,j,k;

CuboControl cc(myRobot);
//Shell myShell(1);

void setup()
{

/*
        void preparaY();
                void preparaX(int giros);
                        void preparaGiro();
*/
  cmdInit(9600);
  myRobot.init();

  cc.init(myRobot);

  
  cmdAdd(const_cast<char *>("ss"), local_set_speed, const_cast<char *>("local_set_speed"));
  cmdAdd(const_cast<char *>("st"), local_giraBase , const_cast<char *>("local gira base 1 paso"));

  cmdAdd(const_cast<char *>("pa"), local_pa, const_cast<char *>("pinzaAbierta"));
  cmdAdd(const_cast<char *>("pc"), local_pc, const_cast<char *>("pinzaCerrada"));
  cmdAdd(const_cast<char *>("pm"), local_pm, const_cast<char *>("pinzaMitad"));

  cmdAdd(const_cast<char *>("sm"), local_setMuneca, const_cast<char *>("setMuneca(int)"));

  cmdAdd(const_cast<char *>("sg"), local_set_Grua, const_cast<char *>("set_Grua(position)"));
  cmdAdd(const_cast<char *>("gu"), local_set_GruaUP, const_cast<char *>("grua up"));
  cmdAdd(const_cast<char *>("gd"), local_down_set_Grua, const_cast<char *>("grua down"));
  cmdAdd(const_cast<char *>("gm"), local_mitad_set_Grua, const_cast<char *>("grua mitad"));



  cmdAdd(const_cast<char *>("cc"), local_printCubo, const_cast<char *>("printCubo"));
  //cmdAdd("tp", local_test_pinza, "test pinza i1 i2");
  cmdAdd(const_cast<char *>("seq"), local_seq, const_cast<char *>("seq 'string'"));
  cmdAdd(const_cast<char *>("gb"), local_giraBase, const_cast<char *>("local_giraBase"));
  cmdAdd(const_cast<char *>("init"), local_cubo_init);

/*
  cmdAdd("pY", local_preparaY, "prepara Y");
  cmdAdd("pX", local_preparaX, "prepara X (num giros de -1 a 2");
  cmdAdd("pG", local_preparaGiro, "prepara Giro");
  cmdAdd("tX", local_traslacionX, "traslacion X (num giros de -1 a 2");
  */
  cmdAdd(const_cast<char *>("tX"), local_traslacionX, const_cast<char *>("traslacion X (num giros de -1 a 2"));

  cmdAdd(const_cast<char *>("demo"), local_demo);
}

void local_demo(int arg_cnt, char **args) {
    static int rant=1;
    int r,s,t;

    for (t=1; t<atoi(args[1]); t++) {
        while ((r=random(2,5))==rant);

        switch (r) {
            case 1: // giro abajo
                // no hago nada
                break;
            case 2: // giro arriba
                while ((s=random(-1,2))==0);
                myRobot.preparaX(s*2);
                myRobot.traslacionX(s*2);
                break;
            case 3: // giro de front o bak
                while ((s=random(-1,2))==0);
                myRobot.preparaX(s);
                myRobot.traslacionX(s);
                break;
            case 4: // giro left o right
                while ((s=random(-1,2))==0);
                myRobot.preparaY();
                myRobot.giraBase(s);
                while ((s=random(-1,2))==0);
                myRobot.preparaX(s);
                myRobot.traslacionX(s);
                break;
        }

        while ((s=random(-2,3))==0);
        myRobot.preparaGiro();
        myRobot.giraBase(s);
        myRobot.setServo(myRobot.servoPinza,PINZA_MITAD, false);
        rant=r;
    }
}

void local_set_speed(int arg_cnt, char **args) {
    myRobot.setSpeed(atoi(args[1]));
}
      
void local_preparaX(int arg_cnt, char **args) {
    myRobot.preparaX(atoi(args[1]));
}
void local_preparaY(int arg_cnt, char **args) {
    myRobot.preparaY();
}
void local_preparaGiro(int arg_cnt, char **args) {
    myRobot.preparaGiro();
}


void local_traslacionX(int arg_cnt, char **args) {
    myRobot.preparaX(atoi(args[1]));
    myRobot.traslacionX(atoi(args[1]));
}

void local_cubo_init(int arg_cnt, char **args) {
    cc.init(myRobot);
    }
void local_test_pinza(int arg_cnt, char **args) {
    for (int l=1; l<6; l++) {
        myRobot.setServo(myRobot.servoPinza, atoi(args[1]), false);
        delay(1000);
        myRobot.setServo(myRobot.servoPinza, atoi(args[2]), false);
        delay(1000);
    }
}
void local_seq(int arg_cnt, char **args)

/* 1   UP     BLANCO
 * 2   FRONT  ROJO
 * 3   RIGHT  AZUL
 * 0   DOWN   AMARILLO
 * -1  BACK   NARANJA
 * -2  LEFT   VERDE
 */
{
  char c;
  int cara;
  int cantidad=1;
  for (i=0; (c=args[1][i])!=0; i++) {
    cantidad = args[1][i+1]=='\''?-1:args[1][i+1]=='2'?2:1;
    cc.move(c,cantidad);
    /*
    Serial.print("move cara ");
    Serial.print(cara);
    Serial.print(" cantidad ");
    Serial.println(cantidad);
    */
    if (cantidad!=1) i++;
  }

  myRobot.setServo(myRobot.servoPinza, PINZA_ABIERTA, false);

}

void local_printCubo(int arg_cnt, char **args)
{
  cc.printState();
}
void local_set_GruaUP(int arg_cnt, char **args)
{
  myRobot.setServo(myRobot.servoGrua,GRUA_ARRIBA, false);
}
void local_down_set_Grua(int arg_cnt, char **args) {
  myRobot.setServo(myRobot.servoGrua,GRUA_ABAJO, false);
}

void local_mitad_set_Grua(int arg_cnt, char **args) {
  myRobot.setServo(myRobot.servoGrua, GRUA_MITAD, false);
}
      
void local_set_Grua(int arg_cnt, char **args)
{
  myRobot.setServo(myRobot.servoGrua,atoi(args[1]), false);
}
void local_setGrua(int arg_cnt, char **args)
{
  myRobot.setServo(myRobot.servoGrua,atoi(args[1]), false);
}
void local_setMuneca(int arg_cnt, char **args)
{
  myRobot.setServo(myRobot.servoMuneca,atoi(args[1]), false);
}
void local_setPinza(int arg_cnt, char **args)
{
  myRobot.setServo(myRobot.servoPinza, atoi(args[1]), false);
}
void local_pm(int arg_cnt, char **args)
{
  myRobot.setServo(myRobot.servoPinza,PINZA_MITAD, false);
}
void local_pc(int arg_cnt, char **args)
{
  myRobot.setServo(myRobot.servoPinza, PINZA_CERRADA, false);
}
void local_pa(int arg_cnt, char **args)
{
  myRobot.setServo(myRobot.servoPinza, PINZA_ABIERTA, false);
}




void local_setDesfase(int arg_cnt, char **args)
{
  myRobot.desfase=atof(args[1]);
}

void local_giraBase(int arg_cnt, char **args)                                             
{                                                                                
  myRobot.giraBase(atoi(args[1]));
  delay(200);
  myRobot.apagarMotor(myRobot.base);
}

void local_base(int arg_cnt, char **args) {
  Serial.write("Voy a qui");
  for (i=0; i<atoi(args[1]); i++) {
      Serial.write("Movi a pos ");
      Serial.println(myRobot.base.position);
      Serial.println(myRobot.base.speed);
      myRobot.do1step(&myRobot.base,atoi(args[1]));
      delay(myRobot.base.speed);
  }
  delay(200);
  myRobot.apagarMotor(myRobot.base);
}

void local_apagarMotores(int arg_cnt, char **args)                                             
{                                                                                
  myRobot.apagarMotor(myRobot.base);
  // myRobot.apagarMotor(myRobot.grua);
} 

void loop() 
{ 
 cmdPoll();  
  /*
  myShell.showPrompt();
  myShell.getSerialStr();
  Serial.write("\n-> ");
  Serial.write(myShell.getLastCommand());
  Serial.write("\n");

  if (strcmp(myShell.getToken(0),"m")==0) {          // muneca
    myRobot.setMuneca(myShell.getIntToken(1));
  } else if (strcmp(myShell.getToken(0),"seq1")==0) {   // traslacion
  } else if (strcmp(myShell.getToken(0),"g1")==0) {  // grua arriba
    myRobot.grua.speed=myShell.getIntToken(1);
    myRobot.setGrua(GRUA_VALOR_ARRIBA);
  } else if (strcmp(myShell.getToken(0),"g2")==0) {  // grua mitad
    myRobot.grua.speed=myShell.getIntToken(1);
    myRobot.setGrua(GRUA_VALOR_MITAD);
  } else if (strcmp(myShell.getToken(0),"g3")==0) {  // grua abajo
    myRobot.setGrua(GRUA_VALOR_ABAJO);
    myRobot.grua.speed=myShell.getIntToken(1);
  } else if (strcmp(myShell.getToken(0),"pa")==0) {  // robot pinza abierta
    myRobot.setPinza(PINZA_ABIERTA);
  } else if (strcmp(myShell.getToken(0),"pm")==0) {  // robot pinza mitad
    myRobot.setPinza(PINZA_MITAD);
  } else if (strcmp(myShell.getToken(0),"pc")==0) {  // robot pinza cerrada
    myRobot.setPinza(PINZA_CERRADA);
  } else if (strcmp(myShell.getToken(0),"b1")==0) {  //  gira base n veces
    myRobot.giraBase(myShell.getIntToken(1));
  } else if (strcmp(myShell.getToken(0),"ag")==0) {  //  gira step1
    myRobot.apagarMotor(myRobot.grua);
  } else if (strcmp(myShell.getToken(0),"s2")==0) {  //  gira step1
    myRobot.do1step(&myRobot.grua,1);
  } else if (strcmp(myShell.getToken(0),"s-1")==0) {  //  gira step1
    myRobot.do1step(&myRobot.base,-1);
  } else if (strcmp(myShell.getToken(0),"s1")==0) {  //  gira step1
    myRobot.do1step(&myRobot.base,1);
  } else if (strcmp(myShell.getToken(0),"ig")==0) {  //  init grua
    myRobot.initGrua();
//  } else if (strcmp(myShell.getToken(0),"gs")==0) {  // grua speed
//    grua.setSpeed(myShell.getIntToken(1));
  } else if (strcmp(myShell.getToken(0),"a0")==0) {  // analog read 0
    for (k=1; k<3000; k++) {
      Serial.println(analogRead(0));
    }
  } else if (strcmp(myShell.getToken(0),"michi")==0) {  // custom
    valGrua=myShell.getIntToken(1);
    for (k=1; k<myShell.getIntToken(2); k++) {
    digitalWrite(6,HIGH);
    digitalWrite(7,HIGH);
    digitalWrite(8,LOW);
    digitalWrite(9,LOW);
    delay(valGrua);
    digitalWrite(6,LOW);
    digitalWrite(7,HIGH);
    digitalWrite(8,HIGH);
    digitalWrite(9,LOW);
    delay(valGrua);
    digitalWrite(6,LOW);
    digitalWrite(7,LOW);
    digitalWrite(8,HIGH);
    digitalWrite(9,HIGH);
    delay(valGrua);
    digitalWrite(6,HIGH);
    digitalWrite(7,LOW);
    digitalWrite(8,LOW);
    digitalWrite(9,HIGH);
    delay(valGrua);
    }
    
//    grua.setSpeed(myShell.getIntToken(1));
//  } else if (strcmp(myShell.getToken(0),"b")==0) { // base  move
//    base.setMaxSpeed(myShell.getIntToken(2));
//    base.setAcceleration(myShell.getIntToken(3));
//    base.move(myShell.getIntToken(1));
//    while (base.speed() !=  0) {
//      base.run();
//      }
//  } else if (strcmp(myShell.getToken(0),"g")==0) {
//    grua.setMaxSpeed(myShell.getIntToken(2));
//    grua.setAcceleration(myShell.getIntToken(3));
//    grua.move(myShell.getIntToken(1));
//    while (grua.speed() !=  0) {
//      grua.run();
//      }
  } else {
    Serial.print("*** Comando no encontrado ***\n");
  }
*/
} 
