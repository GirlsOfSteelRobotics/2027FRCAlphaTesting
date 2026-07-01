import wpilib
from commands2 import Subsystem, Command
from wpilib import SmartDashboard

class ChassisSubsystem(Subsystem):

    def __init__(self):
        self.front_left = wpilib.ExpansionHubMotor(1, 3)
        self.back_left = wpilib.ExpansionHubMotor(1, 2)

        self.back_right = wpilib.ExpansionHubMotor(1, 1)
        self.back_right.setReversed(True)
        self.front_right = wpilib.ExpansionHubMotor(1, 0)
        self.front_right.setReversed(True)
        self.imu = wpilib.OnboardIMU(wpilib.OnboardIMU.MountOrientation.FLAT)

        self.mech_drive = wpilib.MecanumDrive(self.front_left.setThrottle, self.back_left.setThrottle, self.front_right.setThrottle, self.back_right.setThrottle)

    def reset_imu(self):
        self.imu.resetYaw()

    def drive(self, x: float, y: float, rot: float):

        self.mech_drive.driveCartesian(x, y, rot, -self.imu.getRotation2d())
        SmartDashboard.putNumber("drive x", x)
        SmartDashboard.putNumber("drive y", y)
        SmartDashboard.putNumber("drive rot", rot)

    def create_reset_imu_command(self) -> Command:
        return self.runOnce(self.reset_imu)

    def periodic(self) -> None:
        SmartDashboard.putNumber("imu yaw", -self.imu.getYaw())
