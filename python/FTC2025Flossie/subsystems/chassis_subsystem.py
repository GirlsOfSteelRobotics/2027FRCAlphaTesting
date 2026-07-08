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

    def stop(self):
        self.drive(0, 0, 0)

    def create_reset_imu_command(self) -> Command:
        return self.runOnce(self.reset_imu)

    def create_drive_fl_command(self) -> Command:
        return self.runEnd(lambda:self.front_left.setThrottle(1), self.stop).withName("front left forward")

    def create_drive_fr_command(self) -> Command:
        return self.runEnd(lambda:self.front_right.setThrottle(1), self.stop).withName("front right forward")

    def create_drive_bl_command(self) -> Command:
        return self.runEnd(lambda:self.back_left.setThrottle(1), self.stop).withName("back left forward")

    def create_drive_br_command(self) -> Command:
        return self.runEnd(lambda:self.back_right.setThrottle(1), self.stop).withName("back right forward")

    def periodic(self) -> None:
        SmartDashboard.putNumber("imu yaw", -self.imu.getYaw())

    def add_chassis_debug_commands(self):
        SmartDashboard.putData("chassis/front left forward", self.create_drive_fl_command())
        SmartDashboard.putData("chassis/front right forward", self.create_drive_fr_command())
        SmartDashboard.putData("chassis/back left forward", self.create_drive_bl_command())
        SmartDashboard.putData("chassis/back right forward", self.create_drive_br_command())