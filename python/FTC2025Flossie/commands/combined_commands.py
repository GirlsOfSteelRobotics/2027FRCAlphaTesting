from commands2 import WaitUntilCommand
from wpilib import SmartDashboard

from subsystems.feeder_subsystem import FeederSubsystem
from subsystems.hood_subsystem import HoodSubsystem
from subsystems.intake_subsystem import IntakeSubsystem
from subsystems.shooter_subsystem import ShooterSubsystem


class CombinedCommands:
    def __init__(
        self,
        intake: IntakeSubsystem,
        shooter: ShooterSubsystem,
        feeder: FeederSubsystem,
        hood: HoodSubsystem,
    ):
        self.intake_subsystem = intake
        self.shooter_subsystem = shooter
        self.feeder_subsystem = feeder
        self.hood_subsystem = hood

    def create_intake_and_shoot_command(self):
        return (
            self.intake_subsystem.create_intake_command()
            .alongWith(self.feeder_subsystem.create_feed_command())
            .alongWith(self.shooter_subsystem.create_simple_shoot_command())
        )

    def create_shoot_command(self):
        return (
            self.shooter_subsystem.create_pid_shoot_command()
            .alongWith(WaitUntilCommand(self.shooter_subsystem.at_goal_speed)
                       .andThen(self.feeder_subsystem.create_feed_command()
                                .alongWith(self.intake_subsystem.create_intake_command())
                                .alongWith(self.hood_subsystem.create_set_position())))
            .withName("smart shoot")
        )

    def add_combined_commands_debug_commands(self):
        SmartDashboard.putData("feed and shoot", self.create_intake_and_shoot_command())
        SmartDashboard.putData("shooter/smart shoot", self.create_shoot_command())
