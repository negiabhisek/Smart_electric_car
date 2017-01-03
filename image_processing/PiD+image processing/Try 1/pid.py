import time


##PID Library
class PID(object):
    ##Constants used in some of the functions below
    pid_AUTOMATIC = 1
    pid_MANUAL = 0
    pid_DIRECT = 0
    pid_REVERSE = 1

    direction = 0

    def __init__(self, Setpoint, Kp, Ki, Kd, ControllerDirection):
        self.mySetpoint = Setpoint
        self.inAuto = 0
        self.myOutput=0
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.ControllerDirection = ControllerDirection
        self.SetOutputLimits(0, 255)
        self.SampleTime = 100
        self.myInput=0
        self.SetControllerDirection(self.ControllerDirection)
        self.lastTime = int(round(time.time() * 1000)) - self.SampleTime

    def Compute(self):
        if (self.inAuto == 0):
            return 0
        now = int(round(time.time() * 1000))
        timeChange = (now - self.lastTime)
        if (timeChange >= self.SampleTime):
            # /*Compute all the working error variables*/
            Input = self.myInput
            error = self.mySetpoint - Input
            self.ITerm += (self.Ki * error)
            if (self.ITerm > self.outMax):
                self.ITerm = self.outMax
            elif (self.ITerm < self.outMin):
                self.ITerm = self.outMin
            dInput = (Input - self.lastInput)

            # /*Compute PID Output*/
            self.output = self.Kp * error + self.ITerm - self.Kd * dInput

            if (self.output > self.outMax):
                self.output = self.outMax
            elif (self.output < self.outMin):
                self.output = self.outMin
            self.myOutput = self.output

                # /*Remember some variables for next time*/
            self.lastInput = Input
            self.lastTime = now
            return 1

        else:
            return 0

    def SetTunings(self, Kp, Ki, Kd):

        if (Kp < 0 or Ki < 0 or Kd < 0):
            return 0

        SampleTimeInSec = (float(self.SampleTime) / 1000)
        self.Kp = Kp
        self.Ki = Ki * SampleTimeInSec
        self.Kd = Kd / SampleTimeInSec

        if (self.controllerDirection == self.pid_REVERSE):
            self.Kp = (0 - self.Kp)
            self.Ki = (0 - self.Ki)
            self.Kd = (0 - self.Kd)

    def SetSampleTime(self, NewSampleTime):
        if (NewSampleTime > 0):
            ratio = float(NewSampleTime) / float(self.SampleTime)
            self.Ki *= ratio
            self.Kd /= ratio
            self.SampleTime = long(NewSampleTime)

    def SetOutputLimits(self, Min, Max):
        if Min >= Max:
            return 0
        self.outMin = Min
        self.outMax = Max

        if self.inAuto:
            if (self.myOutput > self.outMax):
                self.myOutput = self.outMax
            elif (self.myOutput < self.outMin):
                self.myOutput = self.outMin

            if (self.ITerm > self.outMax):
                self.ITerm = self.outMax
            elif (self.ITerm < self.outMin):
                self.ITerm = self.outMin

    def SetMode(self, Mode):
        newAuto = (Mode == self.pid_AUTOMATIC)
        if (newAuto != self.inAuto):
            self.Initialize()
        self.inAuto = newAuto

    def Initialize(self):
        self.ITerm = self.myOutput
        self.lastInput = self.myInput
        if self.ITerm > self.outMax:
            self.ITerm = self.outMax
        elif self.ITerm < self.outMin:
            self.ITerm = self.outMin

    def SetControllerDirection(self, Direction):
        if self.inAuto and Direction != self.controllerDirection:
            self.Kp = (0 - self.Kp)
            self.Ki = (0 - self.Ki)
            self.Kd = (0 - self.Kd)
        self.controllerDirection = Direction
