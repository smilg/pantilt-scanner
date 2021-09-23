#include <Servo.h>

#define PAN_PIN 5
#define TILT_PIN 6
#define SENSOR_PIN A0

#define SERVO_CENTER 85
#define SENSOR_SAMPLES 3
#define MSEC_PER_DEG 20

Servo pan_servo;
Servo tilt_servo; 

int pan_deg;
int tilt_deg;

String command = "";

void setup() {
    Serial.begin(115200);
    pan_servo.attach(PAN_PIN);
    tilt_servo.attach(TILT_PIN);
    move_servo(pan_servo, SERVO_CENTER, SERVO_CENTER*MSEC_PER_DEG);
    move_servo(tilt_servo, SERVO_CENTER, SERVO_CENTER*MSEC_PER_DEG);
    tilt_deg = SERVO_CENTER;
    pan_deg = SERVO_CENTER;
    Serial.println("ready");
}

void loop() {
    if (Serial.available()) {
        char ch = Serial.read();

        if (ch == '\r') {
            parse_command();
            command = "";
        } else {
            command += ch;
        }
    }
}

void parse_command() {
    if (command.equals("READSENSOR")) {
        int readings[SENSOR_SAMPLES];
        for(int i = 0; i < SENSOR_SAMPLES; i++) {
            readings[i] = analogRead(SENSOR_PIN);
        }
        Serial.println(arr_min(readings, SENSOR_SAMPLES));
    } else if (command.startsWith("PAN|")) {
        String arg = command.substring(4);
        arg.trim();
        int new_deg = arg.toInt();
        move_servo(pan_servo, new_deg, abs(pan_deg-new_deg)*MSEC_PER_DEG);
        pan_deg = new_deg;
    } else if (command.startsWith("TILT|")) {
        String arg = command.substring(5);
        arg.trim();
        int new_deg = arg.toInt();
        move_servo(tilt_servo, new_deg, abs(tilt_deg-new_deg)*MSEC_PER_DEG);
        tilt_deg = new_deg;
    } else {
        Serial.println("unknown command!");
    }
    Serial.println("ready");
}

void move_servo(Servo serv, long angle, int wait) {
    serv.write(angle);
    delay(wait);
}

int arr_min(int arr[], int len) {
    int res = arr[0];
    for(int i = 1; i < len; ++i) {
        res = min(res, arr[i]);
    }
    return res;
}