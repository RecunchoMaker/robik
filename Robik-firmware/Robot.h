#ifndef ROBOT_H
#define ROBOT_H

#include <Arduino.h>
#include <Servo.h>

// Definicion de pines
#define SERVOPINZA 3
#define SERVOGRUA 5
#define SERVOMUNECA 6

#define BASE0 8
#define BASE1 9
#define BASE2 10
#define BASE3 11

#define PINZA_ABIERTA 90
#define PINZA_MITAD 35
#define PINZA_CERRADA 0

#define ESPERA_PINZA 200

#define MUNECA0 0
#define MUNECA1 90
#define MUNECA2 180

#define ESPERA_MUNECA 300

#define GRUA_ARRIBA 20
#define GRUA_MITAD 60
#define GRUA_ABAJO 120
#define GRUA_OFFSET 15 

#define ESPERA_GRUA 400

// 53  54
#define PASOS_POR_CARA 103
#define PASOS_RETROCESO 4
// eran 6 o 27

// Delay entre pasos
#define SPEED 3

/*
 * Estados del robot:
 * Definimos varios estados en los que quedan servos y motores despues
 * de los movimientos importantes
 * Para hacer Y (rotacion con pinzas abiertas) necesitamos un estado inicial de:
 *    -pinzas abiertas
 *    -grua en cualquier sitio
 *    -muneca en cualquier sitio
 * Para hacer X (traslacion con grua arriba y abajo) necesitamos incialmente:
 *    -grua abajo (centro del cubo)
 *    -pinzas cerradas
 *    -muneca lista para hacer los grados que se necesiten
 * Para hacer un giro necesitamos inicialmente:
 *    -grua mitad (un pelin mas arriba del centro)
 *    -pinzas cerradas
 *    -muneca en cualquier sitio
 *
 */

class Robot {

    public:

        
        Robot();
        ~Robot();
        void init();

        void setServo(Servo servo, int nuevoEstado, int espera);

        void preparaY();
        void preparaX(int giros);
        void preparaGiro();

        void traslacionX(int giros);

        void giraBase(int caras);
        struct s_motor {
            int pin[4];
            int indexStep;
            int position;
            int speed;
        } base ;
            

        //void setGrua(int nuevoEstado);
        //void levantaGrua();
        //void bajaGrua();
        void do1step(s_motor* motor, int direccion);
        void traslacion(int stepsGrua, int speed, int speed2); 

        void setSpeed(int speed);

        Servo servoMuneca;
        Servo servoPinza;    
        Servo servoGrua;

        void apagarMotor(s_motor motor);
        float desfase; // No hay un valor entero justo para un giro de 90 grados
        float actualDesfase; // No hay un valor entero justo para un giro de 90 grados

        char nombre;
    private:
        //char gruaEstaAbajo();

        //int gruaCellValorMedio; // valor medio, entre minimo y maximo de la fotocel

        // variables aux, para no tener que inicializar/destruir en llamadas
        int i;

};

#endif
