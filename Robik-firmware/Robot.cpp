#include <Servo.h>
#include "Robot.h"

/*
 * Constructor
 */

Robot::Robot() {
}

/*
 * Destructor
 */

Robot::~Robot() {
  // Nada que destruir
}
void Robot::init() {

    int valorMedio;
    int lectura;
    int i;

    // Se inicializan pines
    servoPinza.attach(SERVOPINZA);
    servoMuneca.attach(SERVOMUNECA);
    servoGrua.attach(SERVOGRUA);
    base.position=150;
    base.pin[0]=BASE0;
    base.pin[1]=BASE1;
    base.pin[2]=BASE2;
    base.pin[3]=BASE3;

    for (i=0; i<=3; i++) {
        pinMode(base.pin[i],OUTPUT);
    }

    // Inicializo servos
    setServo(servoPinza,PINZA_ABIERTA,false);
    setServo(servoMuneca,MUNECA1,false);
    setServo(servoGrua,GRUA_ARRIBA,500);
    setServo(servoGrua,GRUA_ABAJO,500);

    // Inicializo motor de la base
    apagarMotor(base);
    base.indexStep=0;
    base.speed=SPEED;

    desfase=-0.20;
    actualDesfase=0;


}

void Robot::setSpeed(int i) {
    Serial.println("preparaY");
    base.speed = i;
}

/*
 * Traslacion Y: la base gira, con las pinzas abiertas
 */
void Robot::preparaY() {
    Serial.println("preparaY");
    setServo(servoPinza, PINZA_ABIERTA, 230);
    // Solo lo hara para hacer luego una X, asi que ya pongo la grua
    setServo(servoGrua, GRUA_MITAD,230);
}

/*
 * Giro: giro normal de la cara de abajo
 */
void Robot::preparaGiro() {
    Serial.println("* preparaGiro");
    if (servoPinza.read()!=PINZA_SEMI)
        setServo(servoPinza, PINZA_SEMI, 80);
    setServo(servoGrua, GRUA_MITAD, 120);
    setServo(servoPinza, PINZA_CERRADA, 170);
}

/*
 * Traslacion X: utilizando grua arriba y abajo
 */
void Robot::preparaX(int giros) {
    Serial.print("* preparaX");
    Serial.println(giros);
    setServo(servoPinza, PINZA_SEMI, 100);
    setServo(servoGrua, GRUA_ABAJO, 140);
    if (giros==2 && servoMuneca.read()==MUNECA1) {
        // Solo preparo la muneca esta en el centro
        setServo(servoMuneca, MUNECA0, 350);
    } else if (giros==1 && servoMuneca.read()>MUNECA1) {
        setServo(servoMuneca, MUNECA1, 250);
    } else if (giros==-1 && servoMuneca.read()<MUNECA1) {
        setServo(servoMuneca, MUNECA1, 250);
    } else {
        // sin no movi los servos, espero un poquito por la grua
        Serial.println("no movi los servos");
        //delay(100);
    }

    setServo(servoPinza, PINZA_CERRADA, 250);
}

void Robot::traslacionX(int giros) {
    Serial.print("* traslacion X");
    Serial.println(giros);
    setServo(servoGrua, GRUA_ARRIBA, 70);
    switch (giros) {
        case 2:
            setServo(servoMuneca, servoMuneca.read()==MUNECA0?MUNECA2:MUNECA0, 350);
            setServo(servoGrua, GRUA_ABAJO, 190);
            break;
        case -1:
            setServo(servoMuneca, servoMuneca.read()+ giros*70,200);
            setServo(servoGrua, GRUA_ABAJO, 190);
            setServo(servoMuneca, servoMuneca.read()+ giros*20,150);
            break;
        case 1:
            setServo(servoMuneca, servoMuneca.read()+ giros*90,210);
            setServo(servoGrua, GRUA_ABAJO, 190);
            break;
    }

    setServo(servoPinza, PINZA_SEMI, 90);

}


/*
 * Mueve el servo a la posicion indicada, esperando los milisegundos
 * que se indican
 * Si el servo ya esta colocado, no hace nada
 */
void Robot::setServo(Servo servo, int nuevoEstado, int espera) {
    if (servo.read() != nuevoEstado) {
        servo.write(nuevoEstado);

        if (espera)
          delay(espera);
    }
}

void Robot::giraBase(int caras) {
    int abscaras;
    int aspeed;
    int pasos_retroceso;

    int i1,i2,i3,i4;

    Serial.print("gira base ");
    Serial.println(caras);
    abscaras=caras>0?caras:-caras;

    //maxspeed=10;
    //aspeed=10;
    i1=5;
    i2=i1*2;
    i3=abscaras*PASOS_POR_CARA + PASOS_RETROCESO - i2;
    i4=i3-i1;

    if (servoPinza.read() == PINZA_ABIERTA) {
        pasos_retroceso = 0;
    } else {
        pasos_retroceso = PASOS_RETROCESO;
    }



    for (i = 0; i<(abscaras * PASOS_POR_CARA + pasos_retroceso); i++) {
        do1step(&base, caras);
        //delay(i<i1?9:i<i2?6:i<i3?4:i<i4?6:9);
        delay(base.speed);

    }

    for (i = 0; i<pasos_retroceso; i++) {
        do1step(&base, -caras);
        delay(base.speed);
    }
    actualDesfase+=desfase*caras;
    while (actualDesfase >= 1) {
        actualDesfase-=1;
        do1step(&base, -1);
        delay(base.speed);
    }
    while (actualDesfase <= -1) {
        actualDesfase+=1;
        do1step(&base, 1);
        delay(base.speed);
    }
    setServo(servoPinza, PINZA_SEMI, 101);

    delay(300);
    apagarMotor(base);
}


void Robot::apagarMotor(s_motor motor) {
    for (i=0; i<=3; i++) 
        digitalWrite(motor.pin[i],LOW);
}


void Robot::do1step(s_motor* motor, int direccion) {

    if (direccion>0) {
        motor->indexStep=motor->indexStep==7?0:motor->indexStep+1;
        motor->position++;
    }
    else  {
        motor->indexStep=(motor->indexStep==0?7:motor->indexStep-1);
        motor->position--;
    }
    switch (motor->indexStep) {
        case 0:
            digitalWrite(motor->pin[0],HIGH);
            digitalWrite(motor->pin[1],HIGH);
            digitalWrite(motor->pin[2],LOW);
            digitalWrite(motor->pin[3],LOW);
            break;
        case 1:
            digitalWrite(motor->pin[0],LOW);
            digitalWrite(motor->pin[1],HIGH);
            digitalWrite(motor->pin[2],LOW);
            digitalWrite(motor->pin[3],LOW);
            break;
        case 2:
            digitalWrite(motor->pin[0],LOW);
            digitalWrite(motor->pin[1],HIGH);
            digitalWrite(motor->pin[2],HIGH);
            digitalWrite(motor->pin[3],LOW);
            break;
        case 3:
            digitalWrite(motor->pin[0],LOW);
            digitalWrite(motor->pin[1],LOW);
            digitalWrite(motor->pin[2],HIGH);
            digitalWrite(motor->pin[3],LOW);
            break;
        case 4:
            digitalWrite(motor->pin[0],LOW);
            digitalWrite(motor->pin[1],LOW);
            digitalWrite(motor->pin[2],HIGH);
            digitalWrite(motor->pin[3],HIGH);
            break;
        case 5:
            digitalWrite(motor->pin[0],LOW);
            digitalWrite(motor->pin[1],LOW);
            digitalWrite(motor->pin[2],LOW);
            digitalWrite(motor->pin[3],HIGH);
            break;
        case 6:
            digitalWrite(motor->pin[0],HIGH);
            digitalWrite(motor->pin[1],LOW);
            digitalWrite(motor->pin[2],LOW);
            digitalWrite(motor->pin[3],HIGH);
            break;
        case 7:
            digitalWrite(motor->pin[0],HIGH);
            digitalWrite(motor->pin[1],LOW);
            digitalWrite(motor->pin[2],LOW);
            digitalWrite(motor->pin[3],LOW);
            break;
    }

}
