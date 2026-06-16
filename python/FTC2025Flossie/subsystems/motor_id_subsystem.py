import wpilib
from commands2 import Subsystem, Command
from wpilib import SmartDashboard


class MotorIdSubsystem(Subsystem):
    def __init__(self, bus_id, motor_id):
        self.name = f"[{bus_id}][{motor_id}]"
        self.motor = wpilib.ExpansionHubMotor(bus_id, motor_id)

        # self.motor.setDistancePerCount()

        SmartDashboard.putData(f"Run Motor {self.name}", self.create_run_motor_command().withName(self.name))


    def run_motor(self, throttle):
        self.motor.setThrottle(throttle)
        print(f"{self.name} - {throttle}")

    def create_run_motor_command(self) -> Command:
        return self.runEnd(lambda: self.run_motor(1), lambda: self.run_motor(0))