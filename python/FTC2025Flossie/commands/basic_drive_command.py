import wpimath
from commands2 import Command
from commands2.button import CommandNiDsXboxController
from wpilib._wpilib import Joystick

from subsystems.chassis_subsystem import ChassisSubsystem


class BasicDriveCommand(Command):
    def __init__(
        self,
        chassis: ChassisSubsystem,
        joystick: CommandNiDsXboxController,
    ):
        self.chassis = chassis
        self.joystick = joystick
        self.addRequirements(self.chassis)

    def execute(self):
        self.chassis.drive(
            wpimath.applyDeadband(-self.joystick.getLeftY(), .05),
            wpimath.applyDeadband(self.joystick.getLeftX(), .05),
            wpimath.applyDeadband(self.joystick.getRightX(), .05),
        )

    def isFinished(self):
        return False

    def end(self, interrupted: bool):
        self.chassis.drive(0, 0, 0)