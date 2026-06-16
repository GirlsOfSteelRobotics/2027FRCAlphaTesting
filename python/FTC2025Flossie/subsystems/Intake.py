import wpilib
from commands2 import Subsystem, Command
from wpilib import SmartDashboard

class Intake(Subsystem):
    def __init__(self):
        self.intake_motor = wpilib.ExpansionHubMotor(0, 2)
        self.spinner_motor = wpilib.ExpansionHubMotor(0, 1)

    def intake(self):
        self.intake_motor.setThrottle(1)
        self.spinner_motor.setThrottle(1)

    def outtake(self):
        self.intake_motor.setThrottle(-1)
        self.spinner_motor.setThrottle(-1)

    def stop(self):
        self.intake_motor.setThrottle(0)
        self.spinner_motor.setThrottle(0)


    def create_intake_command(self) -> Command:
        return self.runEnd(self.intake, self.stop)

    def create_outtake_command(self) -> Command:
        return self.runEnd(self.outtake, self.stop)


    def add_intake_debug_commands(self):

        SmartDashboard.putData("Intake", self.create_intake_command())
        SmartDashboard.putData("Outtake", self.create_outtake_command())