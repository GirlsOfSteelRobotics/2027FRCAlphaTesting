from wpilib import SmartDashboard

from subsystems.Feeder import Feeder
from subsystems.Intake import Intake
from subsystems.Shooter import Shooter


class CombinedCommands():
    def __init__(self, intake: Intake, shooter: Shooter, feeder: Feeder):
        self.intake = intake
        self.shooter = shooter
        self.feeder = feeder

    def create_intake_and_shoot_command(self):
        return (self.intake.create_intake_command()
         .alongWith(self.feeder.create_feed_command())
         .alongWith(self.shooter.create_shoot_ball_command()))

    def add_combined_commands_debug_commands(self):
        SmartDashboard.putData("feed and shoot", self.create_intake_and_shoot_command())