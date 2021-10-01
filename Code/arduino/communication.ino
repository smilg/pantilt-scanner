#include <Servo.h>

#define PAN_PIN 5
#define TILT_PIN 6
#define SENSOR_PIN A0

#define SERVO_CENTER 85
#define SENSOR_SAMPLES 10
#define MSEC_PER_DEG 20     // the servo is rated for 17 ms/deg unloaded, 20 seems ok when testing
                            // with stuff mounted on it

// initialize servo objects globally so they can be passed around easily
Servo pan_servo;
Servo tilt_servo; 

// keep track of the current facing
int pan_deg;
int tilt_deg;

String command = "";

void setup() {
    Serial.begin(115200);
    pan_servo.attach(PAN_PIN);
    tilt_servo.attach(TILT_PIN);
    pan_deg = 0;
    tilt_deg = 0;
    Serial.println("ready");
}

void loop() {
    // constantly read serial input buffer
    if (Serial.available()) {
        char ch = Serial.read();
        // carriage return means a command has finished sending, so parse it and reset the string
        if (ch == '\r') {
            parse_command();
            command = "";
        } else {    // otherwise continue building the string
            command += ch;
        }
    }
}

void parse_command() {
    if (command.equals("READSENSOR")) { // send back a sensor reading
        // take whatever number of readings and use the minimum to account for noise
        int readings[SENSOR_SAMPLES];
        for(int i = 0; i < SENSOR_SAMPLES; i++) {
            readings[i] = analogRead(SENSOR_PIN);
        }
        Serial.print("X");Serial.println(pan_deg);
        Serial.print("Y");Serial.println(tilt_deg);
        Serial.print("Z");Serial.println(arr_min(readings, SENSOR_SAMPLES));
    } else if (command.startsWith("PAN|")) {    // pan to a specified angle
        // extract the location from the command
        String arg = command.substring(4);
        arg.trim();
        int new_deg = arg.toInt();

        // pan to the location
        move_servo(pan_servo, new_deg, abs(pan_deg-new_deg)*MSEC_PER_DEG);
        pan_deg = new_deg;
    } else if (command.startsWith("TILT|")) {   // tilt to a specified angle
        // extract the location from the command
        String arg = command.substring(5);
        arg.trim();
        int new_deg = arg.toInt();

        // pan to the location
        move_servo(tilt_servo, new_deg, abs(tilt_deg-new_deg)*MSEC_PER_DEG);
        tilt_deg = new_deg;
    } else if (command.startsWith("DELAY|")) {  // this one is mostly for debugging purposes
        // extract the amount of delay from the command
        String arg = command.substring(6);
        arg.trim();
        delay(arg.toInt());
    } else {    // communicate if a bad command is received
        Serial.println("unknown command!");
    }
    // send ready when finished so the controller knows when it can send another instruction
    Serial.println("ready");
}

void move_servo(Servo serv, long angle, int wait) {
// move a servo to a specific angle, then wait for some amount of time in msec (to allow the
//      servo to finish moving)
    serv.write(angle);
    delay(wait);
}

int arr_min(int arr[], int len) {
// get the minimum value of an array
    int res = arr[0];
    for(int i = 1; i < len; ++i) {
        res = min(res, arr[i]);
    }
    return res;
}