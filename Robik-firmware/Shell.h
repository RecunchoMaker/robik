#ifndef SHELL_H
#define SHELL_H

#include <Arduino.h>

#define MAX_INPUT_LENGTH 50
#define MAX_TOKENS 20

//#define MAX_INPUT_LENGTH 50
//#define MAX_TOKENS 10

/*
char inData[MAX_INPUT_LENGTH]; // Allocate some space for the string
char inChar=-1; // Where to store the character read
byte index = 0; // Index into array; where to store the character



int i;

*/

class Shell {

    public:
        Shell(byte a);
        ~Shell();
        void init();
        void start();
        void showPrompt();
        char getSerialStr();
        char *getToken(byte a);
        int getIntToken(byte a); 
        char getNumberOfTokens();
        char *getLastCommand();

    private:
        void tokenize();

        char inChar=-1; // Where to store the character read
        byte index = 0; // Index into array; where to store the character
        char inData[MAX_INPUT_LENGTH]; // Allocate some space for the string
        char lastCommand[MAX_INPUT_LENGTH]; // Allocate some space for the string
        int ntokens;
        char *strtokptr;
        char *tokentmp;
        char token[MAX_TOKENS][MAX_INPUT_LENGTH];
        char *sep;
        char *saveptr;


};

#endif
