#ifndef CUBOCONTROL_H
#define CUBOCONTROL_H

#include <Arduino.h>
#include "Robot.h"

class CuboControl {

    public:

        
        CuboControl(Robot myRobot);
        ~CuboControl();
        void init(Robot myRobot);


        void Y(int *array);
        void Yp(int *array);
        void X(int *array);
        void Xp(int *array);
        void move(char m, int cantidad);

        void printState();

        int caras[3];
        int colores[3];
    private:
        Robot myRobot;
        int opuesto(int c);

};

#endif
