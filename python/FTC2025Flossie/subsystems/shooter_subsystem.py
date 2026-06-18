import wpilib
from commands2 import Subsystem, Command
from wpilib import SmartDashboard


class ShooterSubsystem(Subsystem):
    def __init__(self):
        self.shooter_motor = wpilib.ExpansionHubMotor(0, 0)
        self.shooter_motor.setReversed(True)

    def shoot(self):
        self.shooter_motor.setThrottle(1)

    def stop(self):
        self.shooter_motor.setThrottle(0)

    def reverse(self):
        self.shooter_motor.setThrottle(-1)

    def create_shoot_ball_command(self) -> Command:
        return self.runEnd(self.shoot, self.stop).withName("shoot ball")

    def add_shooter_debug_commands(self):
        SmartDashboard.putData(self.create_shoot_ball_command())
