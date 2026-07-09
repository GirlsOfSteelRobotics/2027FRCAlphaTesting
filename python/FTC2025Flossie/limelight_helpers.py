import math

from ntcore import NetworkTableInstance
from wpilib import SmartDashboard
from wpimath import Pose2d, Translation2d, Rotation2d


class PoseEstimate:
    pose: Pose2d
    timestamp_seconds: float
    latency: float
    tag_count: int
    tag_span: float
    avg_tag_dist: float
    avg_tag_area: float
    is_mega_tag2: bool

class Limelight:
    def __init__(self, camera_name):
        self._limelight_table = NetworkTableInstance.getDefault().getTable(camera_name)
        self._megatag_subscriber = self._limelight_table.getDoubleArrayTopic("botpose").subscribe([])

        self._results_table = NetworkTableInstance.getDefault().getTable("Camera Results")
        self._pose2d_publisher = self._results_table.getStructTopic("RobotPose", Pose2d).publish()

        self._raw_array: list[float] = []

    def _try_extract_value(self, i, arr):
        if i < len(arr):
            return arr[i]

        return -999

    def _arr_to_pose(self, arr):
        if len(arr) < 6:
            return Pose2d()

        tran2d = Translation2d(arr[0], arr[1])
        r2d = Rotation2d(math.radians(arr[5]))
        return Pose2d(tran2d, r2d)


    def get_bot_pose(self) -> PoseEstimate:
        timestamped_array = self._megatag_subscriber.getAtomic()
        values = timestamped_array.value
        timestamp = timestamped_array.time

        pose_estimate = PoseEstimate()
        pose_estimate.pose = self._arr_to_pose(values)
        pose_estimate.latency = self._try_extract_value(6, values)
        pose_estimate.tag_count = int(self._try_extract_value(7, values))
        pose_estimate.tag_span = self._try_extract_value(8, values)
        pose_estimate.avg_tag_dist = self._try_extract_value(9, values)
        pose_estimate.avg_tag_area = self._try_extract_value(10, values)

        SmartDashboard.putNumber("Latency", pose_estimate.latency)
        SmartDashboard.putNumber("Tag Count", pose_estimate.tag_count)
        SmartDashboard.putNumber("Tag Span", pose_estimate.tag_span)
        SmartDashboard.putNumber("Tag Dist", pose_estimate.avg_tag_dist)
        SmartDashboard.putNumber("Tag Area", pose_estimate.avg_tag_area)
        # self._pose2d_publisher.set(Pose2d(1, 1, 0))
        self._pose2d_publisher.set(pose_estimate.pose)

        pose_estimate.timestamp_seconds = (timestamp / 1000000.0) - (pose_estimate.latency / 1000.0)

        return pose_estimate