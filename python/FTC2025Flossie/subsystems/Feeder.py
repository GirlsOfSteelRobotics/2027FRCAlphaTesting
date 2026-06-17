import wpilib
from commands2 import Subsystem, Command
from wpilib import SmartDashboard


class Feeder(Subsystem):
    def __init__(self):
        self.feeder_motor = wpilib._wpilib.ExpansionHubCRServo(1, 1)

    def feed(self):
        self.feeder_motor.setThrottle(1)

    def stop(self):
        self.feeder_motor.setThrottle(0)

    def create_feed_command(self) -> Command:
        return self.runEnd(self.feed, self.stop).withName("feed")

    def add_feeder_debug_commands(self):

        SmartDashboard.putData("feed", self.create_feed_command())

