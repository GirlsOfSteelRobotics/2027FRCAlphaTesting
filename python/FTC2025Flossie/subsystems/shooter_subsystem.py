import wpilib
from commands2 import Subsystem, Command
from wpilib import SmartDashboard


class ShooterSubsystem(Subsystem):
    def __init__(self):
        self.shooter_motor = wpilib.ExpansionHubMotor(0, 0)
        self.shooter_motor.setReversed(True)
        wpilib.Preferences.initFloat("shooter goal vel", 500)
        wpilib.Preferences.initFloat("kp", 0.01)
        wpilib.Preferences.initFloat("kf", 0.00065)

    def simple_shoot(self):
        self.shooter_motor.setThrottle(1)

    def calculate_error(self):
        shooter_goal_vel = wpilib.Preferences.getFloat("shooter goal vel")
        return shooter_goal_vel - self.shooter_motor.getEncoderVelocity()

    def pid_shoot(self, goal):
        error = self.calculate_error()
        kf = wpilib.Preferences.getFloat("kf")
        kp = wpilib.Preferences.getFloat("kp")
        velocity = kf * goal + kp * error
        self.shooter_motor.setThrottle(velocity)

    def get_goal(self):
        return wpilib.Preferences.getFloat("shooter goal vel")

    def stop(self):
        self.shooter_motor.setThrottle(0)

    def reverse(self):
        self.shooter_motor.setThrottle(-1)

    def create_simple_shoot_command(self) -> Command:
        return self.runEnd(self.simple_shoot, self.stop).withName("simple shoot")

    def create_pid_shoot_command(self) -> Command:
        return self.runEnd(lambda:self.pid_shoot(self.get_goal()), self.stop).withName("pid shoot")

    def add_shooter_debug_commands(self):
        SmartDashboard.putData(self.create_simple_shoot_command())
        SmartDashboard.putData(self.create_pid_shoot_command())

    def periodic(self) -> None:
        SmartDashboard.putNumber("shooter vel", self.shooter_motor.getEncoderVelocity())
