#include "Shell.h"



#include <string.h>

#define PROMPT "robik$ "
#define MAX_INPUT_LENGTH 50

/*
 * Constructor
 */

Shell::Shell(byte a) {

    sep=" ";
}

/*
 * Destructor
 */

Shell::~Shell() {

  // Nada que destruir

}

void Shell::init() {
    Serial.begin(9600);
    Serial.setTimeout(5000);

    Serial.write("Arduino shell");
    Serial.println("");
    Serial.write("'h' for help");
    Serial.println("");
    Serial.println("");
}

void Shell::showPrompt() {
    Serial.print(PROMPT);
}


char Shell::getSerialStr() {

    inChar = -1;
    index = 0;
    
    while (true) {
        while (Serial.available() > 0 ) // Don't read unless
                                       // there you know there is data
        {
            if(index < MAX_INPUT_LENGTH - 1)
            {
                inChar = Serial.read(); // Read a character
                inData[index] = inChar; // Store it
                index++; // Increment where to write next
                inData[index] = '\0'; // Null terminate the string
            }


        }
        if (inChar == '\r' ) {
           // Terminate with \0 to allow commands without parameters
           inData[index-1] = '\0';
           break;
        }
    }
    strcpy(lastCommand, inData);
    if (index != 1)  // Enter, just repeat last command
      this->tokenize();
    return 0;
}

char *Shell::getToken(byte a) {
    return token[a];
}

int Shell::getIntToken(byte a) {
    return atoi(token[a]);
}
char *Shell::getLastCommand() {
    return lastCommand;
}

char Shell::getNumberOfTokens() {
    return index;
}

void Shell::tokenize() {
    ntokens=0;
    for (strtokptr = inData; ; strtokptr=NULL) {
      tokentmp = strtok_r(strtokptr, sep, &saveptr);
      if (tokentmp == NULL) {
         break;
      }
      else {
//j         Serial.println("Token encontrado");
         strcpy(token[ntokens++],tokentmp);
  //       Serial.println(token[ntokens-1]);
   //      Serial.println(tokentmp);
         }
    }
    /*j
    for (int i=0; i<ntokens; i++) {
      Serial.print("token ");
      Serial.print(i);
      Serial.print(" = ");
      Serial.print(token[i]);
      Serial.println("");
    }
    */
}
// comentadas
/*

String serialIn;

*/

// Constructor
/*
void setup() {
    Serial.begin(9600);
    Serial.setTimeout(5000);

    Serial.println("Ardunino shell - robik");
    Serial.println("'h' for help");
    Serial.println("");

    sep = " ";
    token=(char **) malloc(MAX_TOKENS * sizeof(char *));
}


char getSerialStr() {

    inChar = -1;
    index = 0;
    
    while (true) {
        while (Serial.available() > 0 ) // Don't read unless
                                       // there you know there is data
        {
            if(index < MAX_INPUT_LENGTH - 1)
            {
                inChar = Serial.read(); // Read a character
                inData[index] = inChar; // Store it
                index++; // Increment where to write next
                inData[index] = '\0'; // Null terminate the string
            }


        }
        if (inChar == '\r' ) 
           break;
    }
    return 0;
}


char Comp(char* This) {
    while (Serial.available() > 0) // Don't read unless
                                   // there you know there is data
    {
        if(index < 19) // One less than the size of the array
        {
            inChar = Serial.read(); // Read a character
            if (inChar == '\r') {
              Serial.write("Retorno");
            }
            inData[index] = inChar; // Store it
            index++; // Increment where to write next
            inData[index] = '\0'; // Null terminate the string
        }

        Serial.write("Dentro de serial available");
        Serial.write(index);

    }

    if (strcmp(inData,This)  == 0) {
        for (int i=0;i<19;i++) {
            inData[i]=0;
        }
        index=0;
        return(0);
    }
    else {
        return(1);
    }
}

void loop()
{
    */
    /*
    if (Comp("m1 on")==0) {
        Serial.write("Motor 1 -> Online\n");
    }
    if (Comp("m1 off")==0) {
        Serial.write("Motor 1 -> Offline\n");
    }
    */
    /*j
    serialIn = Serial.readString();
    */
/*
    Serial.write(PROMPT);
    getSerialStr();
    Serial.print("\n\nComienzo parseo\n\n");
    Serial.print(inData);
    Serial.println();


    ntokens=0;
    for (strtokptr = inData; ; strtokptr=NULL) {
      tokentmp = strtok_r(strtokptr, sep, &saveptr);
      if (tokentmp == NULL)
         break;
      else {
         Serial.println("Token encontrado");
         strcpy(token[ntokens++],tokentmp);
         Serial.println(token[ntokens-1]);
         Serial.println(tokentmp);

         }
    }
    Serial.println((int) &token[0]);
    Serial.println((int) &token[1]);
    Serial.println((int) &token[2]);
    Serial.println((int) &token[3]);
    
    Serial.println(ntokens);
    for (i=0; i<ntokens; i++) {
      Serial.print("token ");
      Serial.print(i);
      Serial.print(" = ");
      Serial.print(token[i]);
      Serial.println("");
    }


}
*/
