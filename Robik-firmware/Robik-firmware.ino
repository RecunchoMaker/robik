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

  //cmdAdd(const_cast<char *>("cc"), local_printCubo, const_cast<char *>("printCubo"));


  // Comandos del prompt
  cmdAdd(const_cast<char *>("init"), local_cubo_init);
  cmdAdd(const_cast<char *>("tx"), local_tx, const_cast<char *>("traslacion <X>"));

  cmdAdd(const_cast<char *>("seq"), local_seq, const_cast<char *>("seq <secuencia>"));

  cmdAdd(const_cast<char *>("ba"), local_ba, const_cast<char *>("giraBAse <x>"));

  cmdAdd(const_cast<char *>("m2"), local_m2, const_cast<char *>("muneca 180 grados"));
  cmdAdd(const_cast<char *>("m1"), local_m1, const_cast<char *>("muneca 90 grados"));
  cmdAdd(const_cast<char *>("m0"), local_m0, const_cast<char *>("muneca 0 grados"));
  
  cmdAdd(const_cast<char *>("gs"), local_gs, const_cast<char *>("gruaSemiarriba"));
  cmdAdd(const_cast<char *>("gb"), local_gb, const_cast<char *>("gruaaBajo"));
  cmdAdd(const_cast<char *>("ga"), local_ga, const_cast<char *>("gruaArriba"));

  cmdAdd(const_cast<char *>("ps"), local_ps, const_cast<char *>("pinzaSemicerrada"));
  cmdAdd(const_cast<char *>("pc"), local_pc, const_cast<char *>("pinzaCerrada"));
  cmdAdd(const_cast<char *>("pa"), local_pa, const_cast<char *>("pinzaAbierta"));

}

// Revisados

// Pinza abierta
void local_pa(int arg_cnt, char **args)
{
  myRobot.setServo(myRobot.servoPinza, PINZA_ABIERTA, false);
}

// Pinza cerrada
void local_pc(int arg_cnt, char **args)
{
  myRobot.setServo(myRobot.servoPinza, PINZA_CERRADA, false);
}

// Pinza semicerrada
void local_ps(int arg_cnt, char **args)
{
  myRobot.setServo(myRobot.servoPinza,PINZA_SEMI, false);
}

// Grua arriba
void local_ga(int arg_cnt, char **args)
{
  myRobot.setServo(myRobot.servoGrua,GRUA_ARRIBA, false);
}

// Grua abajo
void local_gb(int arg_cnt, char **args) {
  myRobot.setServo(myRobot.servoGrua,GRUA_ABAJO, false);
}

// Grua semiarriba
void local_gs(int arg_cnt, char **args) {
  myRobot.setServo(myRobot.servoGrua, GRUA_MITAD, false);
}

// Muneca 0 grados
void local_m0(int arg_cnt, char **args)
{
  myRobot.setServo(myRobot.servoMuneca,MUNECA0, false);
}

// Muneca 90 grados
void local_m1(int arg_cnt, char **args)
{
  myRobot.setServo(myRobot.servoMuneca,MUNECA1, false);
}

// Muneca 180 grados
void local_m2(int arg_cnt, char **args)
{
  myRobot.setServo(myRobot.servoMuneca,MUNECA2, false);
}

// Gira base los cuartos de vuelta especificados en el argumento
void local_ba(int arg_cnt, char **args)                                             
{                                                                                
  myRobot.giraBase(atoi(args[1]));
  delay(200);
  myRobot.apagarMotor(myRobot.base);
}

// Ejecuta la secuencia singmaster que se le pasa como parametro
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
    if (cantidad!=1) i++;
  }

  myRobot.setServo(myRobot.servoPinza, PINZA_ABIERTA, false);

}

// Descomentar declaracion arriba para utilizar estas funciones
void local_cubo_init(int arg_cnt, char **args) {
    cc.init(myRobot);
}


void local_printCubo(int arg_cnt, char **args)
{
  cc.printState();
}
      
// Funciones auxiliares
void local_tx(int arg_cnt, char **args) {
    myRobot.preparaX(atoi(args[1]));
    myRobot.traslacionX(atoi(args[1]));
}

void loop() 
{ 
 cmdPoll();  
} 
