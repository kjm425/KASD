#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,20,4);  // set the LCD address to 0x27 for a 16 chars and 2 line display
/*********************************************************/
const byte numChars = 32;
char receivedChars[numChars];
boolean newData = false;
int line = 0;
int b = 1;

void setup()
{
  lcd.init();  //initialize the lcd
  lcd.backlight();  //open the backlight 
  Serial.begin(9600);
  pinMode(2, INPUT_PULLUP);
  lcd.setCursor ( 0, 0 );            // go to the top left corner
  lcd.print("&  #   Kyle's   #  &"); // write this string on the top row
  lcd.setCursor ( 0, 1 );            // go to the 2nd row
  lcd.print(" &#   Awesome    #& "); // pad string with spaces for centering
  lcd.setCursor ( 0, 2 );            // go to the third row
  lcd.print(" #&   Schedule   &# "); // pad with spaces for centering
  lcd.setCursor ( 0, 3 );            // go to the fourth row
  lcd.print("#  &  Display!  &  #");
  Serial.print("w");
}
/*********************************************************/
void loop() 
{
  int buttonVal= digitalRead(2);
  if ((buttonVal == LOW) && (b == 1)) {
    lcd.noBacklight();
    b = 0;
    delay(1000);
  } else if ((buttonVal == LOW) && (b == 0)){
    lcd.backlight();
    b = 1;
    delay(1000);
  }
  recvWithStartEndMarkers();
  if (newData == true){
    lcd.setCursor(0,line);
    lcd.print(receivedChars);
    newData = false;
    line++;
    if (line == 4){
      line=0;
    }
  }
}

void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;
 
    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

void showNewData() {
    if (newData == true) {
        lcd.println(receivedChars);
        newData = false;
    }
}

