const int NUM_SLIDERS = 3;
const int analogInputs[NUM_SLIDERS] = {A0, A1, A2};

#define led 6
#define buton 10

int analogSliderValues[NUM_SLIDERS];
int prevSliderValues[NUM_SLIDERS];


void setup() { 
  for (int i = 0; i < NUM_SLIDERS; i++) {
    pinMode(analogInputs[i], INPUT);
  }

  pinMode(led, OUTPUT);
  pinMode(buton, INPUT);
  Serial.begin(9600);

  for(int i = 0; i < NUM_SLIDERS; i++){
    prevSliderValues[i] = analogRead(analogInputs[1]);
  }

}

void loop() {

  if(digitalRead(buton) == HIGH){
    digitalWrite(led, HIGH);
    Serial.write("button pressed");
  }else{
    digitalWrite(led, LOW);
  }

  updateSliderValues();

  if(anySliderValueChanged()){
    sendSliderValues();
  }


  // sendSliderValues(); // Actually send data (all the time)
  // printSliderValues(); // For debug
  delay(10);

}


void updateSliderValues() {
  for (int i = 0; i < NUM_SLIDERS; i++) {
     analogSliderValues[i] = analogRead(analogInputs[i]);
    // analogSliderValues[i] = map(analogRead(analogInputs[i]), 1, 1006, 0, 1023);
  }
}

bool anySliderValueChanged(){
  for (int i = 0; i < NUM_SLIDERS; i++) {
    if (analogSliderValues[i] != prevSliderValues[i]) {
      // Değer değişmiş
      // Şimdi önceki değeri güncelle
      prevSliderValues[i] = analogSliderValues[i];
      return true;
    }
  }
  return false;
}

void sendSliderValues() {
  String builtString = String("");

  for (int i = 0; i < NUM_SLIDERS; i++) {
    builtString += String((int)analogSliderValues[i]);

    if (i < NUM_SLIDERS - 1) {
      builtString += String("|");
    }
  }
  
  Serial.println(builtString);
}

void printSliderValues() {
  for (int i = 0; i < NUM_SLIDERS; i++) {
    String printedString = String("Slider #") + String(i + 1) + String(": ") + String(analogSliderValues[i]) + String(" mV");
    Serial.write(printedString.c_str());

    if (i < NUM_SLIDERS - 1) {
      Serial.write(" | ");
    } else {
      Serial.write("\n");
    }
  }
}