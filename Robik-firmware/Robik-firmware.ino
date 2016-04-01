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
#include "Robot.h"
#include "CuboControl.h"

#include "Cmd.h"

Robot myRobot;


int motor;

int i,j,k;

CuboControl cc(myRobot);

void setup()
{

  cmdInit(9600);
  myRobot.init();

  cc.init(myRobot);

  // Sin revisar
  cmdAdd(const_cast<char *>("ss"), local_set_speed, const_cast<char *>("local_set_speed"));
  cmdAdd(const_cast<char *>("st"), local_giraBase , const_cast<char *>("local gira base 1 paso"));


  cmdAdd(const_cast<char *>("sm"), local_setMuneca, const_cast<char *>("setMuneca(int)"));
  cmdAdd(const_cast<char *>("d1"), local_d1, const_cast<char *>("do1step"));

  cmdAdd(const_cast<char *>("sg"), local_set_Grua, const_cast<char *>("set_Grua(position)"));
  cmdAdd(const_cast<char *>("gu"), local_set_GruaUP, const_cast<char *>("grua up"));
  cmdAdd(const_cast<char *>("gd"), local_down_set_Grua, const_cast<char *>("grua down"));
  cmdAdd(const_cast<char *>("gm"), local_mitad_set_Grua, const_cast<char *>("grua mitad"));



  cmdAdd(const_cast<char *>("cc"), local_printCubo, const_cast<char *>("printCubo"));
  //cmdAdd("tp", local_test_pinza, "test pinza i1 i2");
  cmdAdd(const_cast<char *>("seq"), local_seq, const_cast<char *>("seq 'string'"));
  cmdAdd(const_cast<char *>("gb"), local_giraBase, const_cast<char *>("local_giraBase"));
  cmdAdd(const_cast<char *>("init"), local_cubo_init);

  cmdAdd(const_cast<char *>("tX"), local_traslacionX, const_cast<char *>("traslacion X (num giros de -1 a 2"));

  cmdAdd(const_cast<char *>("demo"), local_demo);

  // Comandos del prompt
  cmdAdd(const_cast<char *>("ps"), local_ps, const_cast<char *>("pinzaSemicerrada"));
  cmdAdd(const_cast<char *>("pc"), local_pc, const_cast<char *>("pinzaCerrada"));
  cmdAdd(const_cast<char *>("pa"), local_pa, const_cast<char *>("pinzaAbierta"));
  
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
        myRobot.setServo(myRobot.servoPinza,PINZA_SEMI, false);
        rant=r;
    }
}

// Revisados
void local_pa(int arg_cnt, char **args)
{
  myRobot.setServo(myRobot.servoPinza, PINZA_ABIERTA, false);
}
void local_pc(int arg_cnt, char **args)
{
  myRobot.setServo(myRobot.servoPinza, PINZA_CERRADA, false);
}
void local_ps(int arg_cnt, char **args)
{
  myRobot.setServo(myRobot.servoPinza,PINZA_SEMI, false);
}

// Sin revisar
void local_set_speed(int arg_cnt, char **args) {
    myRobot.setSpeed(atoi(args[1]));
}

void local_d1(int arg_cnt, char **args) {
    myRobot.do1step(&myRobot.base, atoi(args[1]));
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

void local_apagarMotores(int arg_cnt, char **args)                                             
{                                                                                
  myRobot.apagarMotor(myRobot.base);
} 

void loop() 
{ 
 cmdPoll();  
} 
