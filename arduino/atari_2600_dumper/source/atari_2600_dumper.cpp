//---------------------------------------------------------------------------

#include "mariamole_auto_generated.h"

unsigned int LAST_ADDRESS = 4096; // Reads up to 4K from the ROM chip

const unsigned int ADDRESS_PINS_TOTAL = 12;
const unsigned int DATA_PINS_TOTAL = 8;
//										     A0  A1	 A2	 A3  A4  A5  A6  A7  A8  A9  A10 A11                                         
const int ADDRESS_PIN[ADDRESS_PINS_TOTAL] = {39, 41, 43, 45, 47, 49, 51, 53, 48, 46, 42, 44};
const int DATA_PIN[DATA_PINS_TOTAL] = {37, 35, 33, 8, 32, 34, 36, 38};
//const int A12_PIN = 40; // The last address pin is used to select the ship

unsigned char readRomAddress(int address)
{
	// Set the ROM address pins
	bool value = false;
	for (unsigned int bit=0; bit < ADDRESS_PINS_TOTAL; bit++) {
		value = (address & (1 << bit)) > 0;
		digitalWrite(ADDRESS_PIN[bit], value);
	}
	
	// Wait until the circuit settles down
	delay(10);
	
	// Read the memory byte from the ROM data pins	
	unsigned char result = 0;
	for (unsigned int bit=0; bit < DATA_PINS_TOTAL; bit++) {
		bool bitSet = (digitalRead(DATA_PIN[bit]) != 0);
		if (bitSet) {
			result += (1 << bit);
		}		
	}
	
	return result;	
}

void setup() 
{   		
	for (unsigned int i=0; i < ADDRESS_PINS_TOTAL; i++) {
		pinMode(ADDRESS_PIN[i], OUTPUT);
	}	
	
	for (unsigned int i=0; i < DATA_PINS_TOTAL; i++) {
		pinMode(DATA_PIN[i], INPUT);
	}		
	
	Serial.begin(115200);
	while (!Serial) {
		; // wait for serial port to connect. Needed for Native USB only
	}	
	
	Serial.println("*** Starting dump...");
	
	char dumpLine[100] = "";
	char strValue[3] = "";
	bool waitingToDump = true; 
	for (unsigned int address=0; address < LAST_ADDRESS; address++) {
		unsigned char value = readRomAddress(address);
		if (address % 16 == 0) {
			if (strlen(dumpLine) != 0) {
				Serial.println(dumpLine);				
				waitingToDump = false;
			}			
			sprintf(dumpLine, "%04X:", address);
		}
		sprintf(strValue, "%02X", value);
		strcat(dumpLine, strValue);		
		waitingToDump = true;
	}
	
	if (waitingToDump) {
		// make sure the last line is dumped even if is not complete
		Serial.println(dumpLine);						
	}
}

//---------------------------------------------------------------------------

void loop() {
	Serial.println("+++ Dump finished!");
	delay(3000);
}

//---------------------------------------------------------------------------