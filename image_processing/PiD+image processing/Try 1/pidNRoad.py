import pid
import roadDetection
import cv2


def steeringDegree(angle):
    steering = cv2.imread('steering_wheel.jpg')
    rows, cols, extra = steering.shape
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    dst = cv2.warpAffine(steering, M, (cols, rows))
    cv2.namedWindow('Steering')
    cv2.imshow('Steering', dst)

if __name__ == "__main__":
    road = roadDetection.imageProcessing('vid2.mp4', 0, 0)
    road.showWindows()
    Kp=2
    Kd=0.01
    Ki=0.001
    setpoint=0
    pidob=pid.PID(setpoint,Kp,Kd,Ki,pid.PID.pid_DIRECT)
    pidob.SetMode(pid.PID.pid_AUTOMATIC)
    pidob.SetSampleTime(1)
    pidob.SetOutputLimits(-180,180)

    while 1:
        road.imagePreprocessing()
        road.drawCenterLine()
        road.drawMoment()
        pidob.mySetpoint=road.windowWid/2
        pidob.myInput=road.cxMoment
        print str(road.windowWid/2) + ' - ' + str(road.cxMoment) + ' = ' +  str(road.currentError)
        pidob.Compute()
        print pidob.output
        steeringDegree(pidob.output)
        road.printImage()
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
    road.destroy()
