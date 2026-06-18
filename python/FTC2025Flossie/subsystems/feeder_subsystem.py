import wpilib
from commands2 import Subsystem, Command
from wpilib import SmartDashboard


class FeederSubsystem(Subsystem):
    def __init__(self):
        self.feeder_motor = wpilib._wpilib.ExpansionHubCRServo(1, 1)

    def feed(self):
        self.feeder_motor.setThrottle(1)

    def stop(self):
        self.feeder_motor.setThrottle(0)

    def reverse(self):
        self.feeder_motor.setThrottle(-1)

    def create_feed_command(self) -> Command:
        return self.runEnd(self.feed, self.stop).withName("feed")

    def create_reverse_feeder_command(self) -> Command:
        return self.runEnd(self.reverse, self.stop).withName("reverse feeder")

    def add_feeder_debug_commands(self):
        SmartDashboard.putData(self.create_feed_command())
        SmartDashboard.putData(self.create_reverse_feeder_command())
