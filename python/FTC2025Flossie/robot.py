#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import commands2
import hal._wpiHal
import wpilib
from ntcore import NetworkTable, NetworkTableInstance
from wpilib import RobotBase, SmartDashboard, Field2d
from wpilib._wpilib import DriverStation
from wpilib.simulation import DriverStationSim
from wpimath import Pose2d

from commands.combined_commands import CombinedCommands
from subsystems.intake_subsystem import IntakeSubsystem
from subsystems.shooter_subsystem import ShooterSubsystem
from subsystems.feeder_subsystem import FeederSubsystem


class MyRobot(commands2.TimedCommandRobot):
    """The methods in this class are called automatically corresponding to each mode, as
    described in the TimedRobot documentation. If you change the name of this class or the
    package after creating this project, you must also update the Main.java file in the
    project.
    """

    def __init__(self) -> None:

        """This function is run when the robot is first started up and should be used for any
        initialization code.
        """
        super().__init__()
        self.CombinedCommands = None
        self.autonomousCommand = None
        self.IntakeSubsystem = IntakeSubsystem()
        self.ShooterSubsystem = ShooterSubsystem()
        self.FeederSubsystem = FeederSubsystem()
        self.CombinedCommands = CombinedCommands(self.IntakeSubsystem, self.ShooterSubsystem, self.FeederSubsystem)

        self.IntakeSubsystem.add_intake_debug_commands()
        self.ShooterSubsystem.add_shooter_debug_commands()
        self.FeederSubsystem.add_feeder_debug_commands()

        self.CombinedCommands.add_combined_commands_debug_commands()

        """
        0/0 is shooter (and backwards)
        0/1 is spindexer
        0/2 is intake
        0/3 is nothing
        
        1/0 is fr and backwards
        1/1 is br and backwards
        1/2 is bl
        1/3 is fl
        
        servos:
        0: hood
        1: feeder (treat like motor)
        """

        # Initialize data logging.
        wpilib.DataLogManager.start()

        if RobotBase.isSimulation():
            DriverStationSim.setAllianceStationId(hal._wpiHal.AllianceStationID.BLUE_1)
            DriverStationSim.setRobotMode(hal._wpiHal._RobotMode.TELEOPERATED)
            DriverStationSim.setEnabled(True)
            DriverStationSim.notifyNewData()

        self.temp_pub = NetworkTableInstance.getDefault().getTable("TEMP").getStructTopic("Hello", Pose2d).publish()
        self.temp_pub.set(Pose2d(0, 0, 0))


    def robotPeriodic(self) -> None:
        """This function is called once each time the robot enters Disabled mode."""
        commands2.CommandScheduler.getInstance().run()

    def disabledInit(self) -> None:
        """This function is called once each time the robot enters Disabled mode."""
        pass

    def disabledPeriodic(self) -> None:
        pass

    def autonomousInit(self) -> None:
        self.autonomousCommand = self.get_autonomous_command()

        if self.autonomousCommand is not None:
            self.autonomousCommand.schedule()

    def autonomousPeriodic(self) -> None:
        """This function is called periodically during autonomous."""
        pass

    def teleopInit(self) -> None:
        # This makes sure that the autonomous stops running when
        # teleop starts running. If you want the autonomous to
        # continue until interrupted by another command, remove
        # this line or comment it out.
        if self.autonomousCommand is not None:
            self.autonomousCommand.cancel()

    def teleopPeriodic(self) -> None:
        """This function is called periodically during operator control."""
        pass

    def utilityInit(self) -> None:
        # Cancels all running commands at the start of utility mode.
        commands2.CommandScheduler.getInstance().cancelAll()

    def utilityPeriodic(self) -> None:
        """This function is called periodically during utility mode."""
        pass

    def get_autonomous_command(self):
        return None