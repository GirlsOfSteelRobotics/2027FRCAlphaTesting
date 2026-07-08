#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#
from typing import Optional

import commands2
import hal._wpiHal
import wpilib
from commands2.button import CommandNiDsXboxController, CommandGenericHID
from wpilib import RobotBase
from wpilib.simulation import DriverStationSim

from commands import basic_drive_command
from commands.combined_commands import CombinedCommands
from commands.basic_drive_command import BasicDriveCommand
from subsystems import chassis_subsystem
from subsystems.chassis_subsystem import ChassisSubsystem
from subsystems.feeder_subsystem import FeederSubsystem
from subsystems.intake_subsystem import IntakeSubsystem
from subsystems.shooter_subsystem import ShooterSubsystem
from subsystems.hood_subsystem import HoodSubsystem



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
        self.autonomous_command: Optional[commands2.Command] = None

        self.intake_subsystem = IntakeSubsystem()
        self.shooter_subsystem = ShooterSubsystem()
        self.feeder_subsystem = FeederSubsystem()
        self.hood_subsystem = HoodSubsystem()
        self.chassis_subsystem = ChassisSubsystem()

        self.combined_commands = CombinedCommands(
            self.intake_subsystem, self.shooter_subsystem, self.feeder_subsystem, self.hood_subsystem
        )

        self.driver_controller = CommandNiDsXboxController(0)
        CommandGenericHID
        self.operator_controller = CommandNiDsXboxController(1)

        self.intake_subsystem.add_intake_debug_commands()
        self.shooter_subsystem.add_shooter_debug_commands()
        self.feeder_subsystem.add_feeder_debug_commands()
        self.hood_subsystem.add_hood_debug_commands()
        self.chassis_subsystem.add_chassis_debug_commands()

        self.combined_commands.add_combined_commands_debug_commands()

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
        1/0: hood
        1: feeder (treat like motor)
        """

        # Initialize data logging.
        wpilib.DataLogManager.start()

        if RobotBase.isSimulation():
            DriverStationSim.setAllianceStationId(hal._wpiHal.AllianceStationID.BLUE_1)
            DriverStationSim.setRobotMode(hal._wpiHal._RobotMode.TELEOPERATED)
            DriverStationSim.setEnabled(True)
            DriverStationSim.notifyNewData()

        self.configureBindings()

    def configureBindings(self) -> None:
        self.chassis_subsystem.setDefaultCommand(BasicDriveCommand(self.chassis_subsystem, self.driver_controller))
        self.driver_controller.start().and_(self.driver_controller.a()).whileTrue(self.chassis_subsystem.create_reset_imu_command())

        self.driver_controller.rightTrigger().whileTrue(self.shooter_subsystem.create_pid_shoot_command())
        self.driver_controller.leftTrigger().whileTrue(self.intake_subsystem.create_intake_command())


    def robotPeriodic(self) -> None:
        """This function is called once each time the robot enters Disabled mode."""
        commands2.CommandScheduler.getInstance().run()

    def disabledInit(self) -> None:
        """This function is called once each time the robot enters Disabled mode."""
        pass

    def disabledPeriodic(self) -> None:
        pass

    def autonomousInit(self) -> None:
        self.autonomous_command = self.get_autonomous_command()

        if self.autonomous_command is not None:
            self.autonomous_command.schedule()

    def autonomousPeriodic(self) -> None:
        """This function is called periodically during autonomous."""
        pass

    def teleopInit(self) -> None:
        # This makes sure that the autonomous stops running when
        # teleop starts running. If you want the autonomous to
        # continue until interrupted by another command, remove
        # this line or comment it out.
        if self.autonomous_command is not None:
            self.autonomous_command.cancel()

    def teleopPeriodic(self) -> None:
        """This function is called periodically during operator control."""
        pass

    def utilityInit(self) -> None:
        # Cancels all running commands at the start of utility mode.
        commands2.CommandScheduler.getInstance().cancelAll()

    def utilityPeriodic(self) -> None:
        """This function is called periodically during utility mode."""
        pass

    def get_autonomous_command(self) -> Optional[commands2.Command]:
        return None
