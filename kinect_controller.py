import freenect
import cv2
import numpy as np
from depth_processing import depth2xyzuv, pretty_depth
from enum import Enum


class KinectImageType(Enum):
    RGB = 1
    DEPTH_COLORIZED = 2
    DEPTH_RAW = 3


class KinectLedStatus(Enum):
    OFF = 0
    GREEN = 1
    RED = 2
    YELLOW = 3
    BLINK_GREEN = 4
    BLINK_RED_YELLOW = 5


class KinectController:

    def __init__(self) -> None:
        self.current_return_type = KinectImageType.RGB
        self.context = freenect.init()

        self.device = None
        self.video_output_functions = {
            KinectImageType.RGB: self.get_video,
            KinectImageType.DEPTH_COLORIZED: self.get_depth_colorized,
            KinectImageType.DEPTH_RAW:self.get_depth_raw
        }
        self.depth_resolution_skip = 1  # 1 = no skip
        self.current_tilt_angle = 0
        self.set_tilt(self.current_tilt_angle)

    def __del__(self):
        freenect.shutdown(self.context)

    def _open_device(self):
        self.device = freenect.open_device(self.context, 0)

    def _close_device(self):
        freenect.close_device(self.device)
        self.device = None

    def _device_open(self):
        return self.device is not None

    def get_video(self):
        array, _ = freenect.sync_get_video()
        array = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
        return array

    def get_depth_colorized(self):
        array, _ = freenect.sync_get_depth()
        return pretty_depth(array)

    def get_depth_raw(self):
        array, _ = freenect.sync_get_depth()
        array = array.astype(np.uint8)
        return array

    def get_output_function(self):
        return self.video_output_functions[self.current_return_type]

    def get_jpg_image(self):
        output_function = self.get_output_function()
        ret, buffer = cv2.imencode('.jpg', output_function())
        return buffer

    def change_output_type(self, type: KinectImageType):
        self.current_return_type = type

    def set_skip(self, new_skip):
        self.depth_resolution_skip = new_skip

    def create_point_cloud(self):
        depth, _ = freenect.sync_get_depth()
        u, v = np.mgrid[:480:self.depth_resolution_skip,
                        :640:self.depth_resolution_skip]
        xyz, uv = depth2xyzuv(
            depth[::self.depth_resolution_skip, ::self.depth_resolution_skip], u, v)
        return xyz[::-1, 1], xyz[::-1, 2], xyz[::-1, 0]

    def set_tilt(self, value):
        self._open_device()
        freenect.set_tilt_degs(self.device, value)
        self._close_device()

    def set_led(self, status: KinectLedStatus):
        self._open_device()
        freenect.set_led(self.device, int(status))
        self._close_device()

    def increase_tilt(self, amount):
        tilt = self.current_tilt_angle + amount
        self.current_tilt_angle = 30 if tilt > 30 else tilt
        self.set_tilt(self.current_tilt_angle)

    def decrease_tilt(self, amount):
        tilt = self.current_tilt_angle - amount
        self.current_tilt_angle = 0 if tilt < 0 else tilt
        self.set_tilt(self.current_tilt_angle)
