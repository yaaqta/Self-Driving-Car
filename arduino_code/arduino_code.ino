int in1 = 8, in2 = 9;
int in3 = 10, in4 = 11;
int activate = 7;
int esp0 = 12, esp1 = 13;

void setup() {
  // put your setup code here, to run once:
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  pinMode(activate, INPUT);
  pinMode(esp0, INPUT);
  pinMode(esp1, INPUT);
}

void leftBackward(){
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW); 
}

void rightBackward(){
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
}

void leftForward(){
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
}

void rightForward(){
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
}

void leftStop(){
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
}

void rightStop(){
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}

void goForward(int t){
  rightForward();
  leftForward();
  delay(t);
  stopAll();
}

void goBackward(int t){
  rightBackward();
  leftBackward();
  delay(t);
  stopAll();
}

void turnLeft(int t){
  rightForward();
  delay(t);
  stopAll();
}

void turnRight(int t){
  leftForward();
  delay(t);
  stopAll();
}

void stopAll(){
  rightStop();
  leftStop();
}

void loop() {
  // put your main code here, to run repeatedly:
  int runTime = 50;
  int turnTime = 100;
  int state = digitalRead(activate);
  if(state == HIGH){
    int stateESP0 = digitalRead(esp0);
    int stateESP1 = digitalRead(esp1);
    if(stateESP0 == HIGH && stateESP1 == HIGH){
      goForward(runTime);
    }
    else if(stateESP0 == LOW && stateESP1 == LOW){
      goBackward(runTime);
    }
    else if(stateESP0 == LOW && stateESP1 == HIGH){
      turnLeft(turnTime);
    }
    else if(stateESP0 == HIGH && stateESP1 == LOW){
      turnRight(turnTime);
    }
  }
}
