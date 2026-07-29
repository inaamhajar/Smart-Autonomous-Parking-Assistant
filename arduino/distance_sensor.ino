int trig = 10;
int echo = 9;
int red = 2;
int green = 8;
int yellow = 7;
int buzzer = 11;
float distance;
float duration;

void setup() {
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);
  pinMode(red, OUTPUT);
  pinMode(yellow, OUTPUT);
  pinMode(green, OUTPUT);
  pinMode(buzzer, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // --- measure distance ---
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);

  duration = pulseIn(echo, HIGH);
  distance = duration * 0.0343 / 2.0;
  Serial.println(distance);

  // --- decide state based on distance ---
  if (distance < 10) {
    // too close: red + buzzer
    digitalWrite(red, HIGH);
    digitalWrite(yellow, LOW);
    digitalWrite(green, LOW);
    tone(buzzer, 1000);
    delay(300);
  } else if (distance < 30) {
    // medium: yellow, no buzzer
    digitalWrite(red, LOW);
    digitalWrite(yellow, HIGH);
    digitalWrite(green, LOW);
    tone(buzzer, 700);
    delay(200);

  } else {
    // safe: green, no buzzer
    digitalWrite(red, LOW);
    digitalWrite(yellow, LOW);
    digitalWrite(green, HIGH);
    noTone(buzzer);
  }

  delay(100);
}