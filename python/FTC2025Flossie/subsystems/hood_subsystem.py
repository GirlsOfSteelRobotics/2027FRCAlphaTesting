import wpilib
from commands2 import Subsystem, Command
from wpilib import SmartDashboard

class HoodSubsystem(Subsystem):

    def __init__(self):
        self.hood_servo = wpilib.ExpansionHubServo(1, 0)
        self.current_position = 0

    def up(self):
        self.current_position += 0.1
        self.hood_servo.setPosition(self.current_position)

    def down(self):
        self.current_position -= 0.1
        self.hood_servo.setPosition(self.current_position - 0.1)

    def create_up_command(self) -> Command:
        return self.runOnce(self.up).withName("hood up")

    def create_down_command(self) -> Command:
        return self.runOnce(self.down).withName("hood down")

    def add_hood_debug_commands(self):
        SmartDashboard.putData(self.create_up_command())
        SmartDashboard.putData(self.create_down_command())

    def periodic(self):
        SmartDashboard.putNumber("hood current position", self.current_position)