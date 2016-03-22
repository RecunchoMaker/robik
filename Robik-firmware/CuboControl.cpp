#include "CuboControl.h"

/*
#define BLUE 1
#define WHITE 2
#define RED 3
#define GREEN 0
#define YELLOW -1
#define ORANGE -2
*/
#define WHITE 1
#define RED 2
#define BLUE 3
#define YELLOW 0
#define ORANGE -1
#define GREEN -2

#define UP 1
#define FRONT 2
#define RIGHT 3
#define DOWN 0
#define BACK -1
#define LEFT -2

/*
 * La posicion del cubo se graba en 2 arrays distintos
 * Partimos de una posicion inicial en la que suponemos que los colores
 * de cada cara son los siguientes
 * 1   UP     BLANCO
 * 2   FRONT  ROJO
 * 3   RIGHT  AZUL
 * 0   DOWN   AMARILLO
 * -1  BACK   NARANJA
 * -2  LEFT   VERDE
 *
 *  Inicialmente, la posicion derecha/izquierda y front/back es mirando el
 *  robot desde el frente
 *
 *  Segun se va moviendo el cubo, cambian las caras y los colores.
 *  Con los movimientos estandard (U,R,F,B,L,D), los cambios en el array
 *  "caras" coinciden con los de "colores". Para las transiciones sueltas
 *  (X,Y,Z), sin embargo, solo cambian los colores (de eso se trata cuando
 *  en una secuencia aparece una notacion X, por ejemplo: rotamos el cubo
 *  en la mano y lo que antes era Down pasa a ser Front... etc
 *
 *  Nos bastan tres valores (lo minimo serian 2 pero complicaria bastante
 *  el codigo). Solo guardamos tres valores y, tal y como estan configurados
 *  los valores, lo que hay en el contrario de la cara 'i' es ese valor en
 *  negativo + 1
 *
 *  Ejemplo: lo contrario de green (-2) es --2+1=3 = blue
 *           lo contrario de down (0) es -0+1=1 = up
 *
 */

String colors[6]={"verde","naranja","amarillo","blanco","rojo","azul"};
//String colors[6]={"naranja","amarillo","verde","azul","blanco","rojo"};

            
/*
 * Constructor
 */

CuboControl::CuboControl(Robot r) {
}

/*
 * Destructor
 */

CuboControl::~CuboControl() {
  // Nada que destruir
}

void CuboControl::move(char m, int cantidad) {
    int cara;

    cara=-9; // valor imposible

    Serial.print(m);
    Serial.println(cantidad);
    switch (m) {
      case 'U': 
                cara=1; break; // bien
      case 'F': 
                cara=-1; break;
      case 'R': 
                cara=-2; break;
      case 'D': 
                cara=0; break; // bien
      case 'B': 
                cara=2; break;
      case 'L': 
                cara=3; break;
      case 'M':
                break;
      case 'X':
                // TODO estas traslaciones no funcionan
                X(colores);
                X(caras);
                break;
      case 'Y':
                Y(colores);
                Y(caras);
                break;
      case 'Z':
                break;
      default: 
                break;

    }

    if (cara!=-9) { // No es una traslacion simple, hay que hacer algo

        // Tengo que mover la cara de arriba?
        if (caras[0]==cara) {
            myRobot.preparaX(2);
            myRobot.traslacionX(2);
            X(colores);
            X(colores);
            X(caras);
            X(caras);
            // y ojo, tanto en este caso como si tengo que hacer
            // una sola X, el sentido de la base se cambia
        }
        // Tengo que mover derecha o izquierda?
        if (caras[2]==cara or caras[2]==opuesto(cara)) {
            // Hago una Y. La que mejor me venga en funcion de la muneca
            myRobot.preparaY();
            if (myRobot.servoMuneca.read()==MUNECA0) {
                myRobot.giraBase(-1);
                Yp(colores);
                Yp(caras);
            }
            else {
                myRobot.giraBase(1);
                Y(colores);
                Y(caras);
            }
        }

        // Tengo que mover front o back?
        if (caras[1]==cara or caras[1]==opuesto(cara)) {
            // Hago una X
            if (caras[1]==cara) {
                myRobot.preparaX(-1);
                myRobot.traslacionX(-1);
                Xp(colores);
                Xp(caras);
            } else {
                myRobot.preparaX(1);
                myRobot.traslacionX(1);
                X(colores);
                X(caras);
            }
        }

        // Aqui se supone que la cara de abajo es la buena!
        if (caras[0]!=opuesto(cara)) {
            Serial.print(caras[0]);
            Serial.println("ERROR 101 ***");
        }

        myRobot.preparaGiro();
        myRobot.giraBase(cantidad);

    }
}

void CuboControl::init(Robot r) {

    myRobot = r;

    myRobot.init();

    colores[0]=BLUE;
    colores[1]=WHITE;
    colores[2]=RED;

    caras[0]=UP;
    caras[1]=FRONT;
    caras[2]=RIGHT;
}

void CuboControl::Y(int *array) {
    // Con traslacion Y se rotan las colores 1 y 2
    int aux;
    aux=array[2];
    array[2]=array[1];
    array[1]=-aux+1;
}

void CuboControl::Yp(int *array) {
    // Con traslacion Y se rotan las colores 1 y 2
    int aux;
    aux=array[1];
    array[1]=array[2];
    array[2]=-aux+1;
}

void CuboControl::Xp(int *array) {
    int aux;
    aux=array[1];
    array[1]=array[0];
    array[0]=-aux+1;
}
void CuboControl::X(int *array) {
    int aux;
    aux=array[0];
    array[0]=array[1];
    array[1]=-aux+1;
}

void CuboControl::printState() {
    Serial.println("   _____________");
    Serial.println("  /            /");
    Serial.print(" /   ");
    Serial.println(colors[colores[0]+2]);
    Serial.println("/            / |");
    Serial.println("-------------  |");
    Serial.print("|           |");
    Serial.println(colors[colores[2]+2]);
    Serial.println("|           |  |");
    Serial.print("|   ");
    Serial.println(colors[colores[1]+2]);
    Serial.println("|           |  |");
    Serial.println("|           | /");
    Serial.println("|           |/");
    Serial.println("|___________/");

}

int CuboControl::opuesto(int c) {
    return -c+1;
}
