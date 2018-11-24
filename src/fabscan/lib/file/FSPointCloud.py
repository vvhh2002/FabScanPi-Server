__author__ = "Mario Lukas"
__copyright__ = "Copyright 2017"
__license__ = "GPL v2"
__maintainer__ = "Mario Lukas"
__email__ = "info@mariolukas.de"

import os
import datetime
import logging
import struct
import numpy as np
from fabscan.FSConfig import ConfigInterface
from fabscan.lib.util.FSInject import inject
from fabscan.FSVersion import __version__


class PointCloudError(Exception):

    def __init__(self):
        Exception.__init__(self, "PointCloudError")


@inject(
    config=ConfigInterface
)
class FSPointCloud():

    def __init__(self, config, color=True):
        self.points = []
        self.texture = np.array([[],[],[]])
        self.file_name = None
        self._dir_name = None
        self.color = color
        self.config = config
        self._logger = logging.getLogger(__name__)


    def append_points(self, points):
        self.points += points
        #points = np.array(points)
        #self.points = np.concatenate((self.points, points), axis=1)
        #self.points = np.concatenate((self.points, points), axis=1)


    def append_texture(self, texture):
        texture = np.array(texture)
        self.texture = np.hstack((self.texture, texture))
        #self.texture = np.concatenate((self.texture, texture), axis=1)

    def get_size(self):
        return len(self.points)

    def writeHeader(self):
        pass

    def writePointsToFile(self):
        pass

    def calculateNormals(self):
        pass

    def saveAsFile(self, filename):
        basedir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self._dir_name = self.config.folders.scans+filename

        try:
            if not os.path.exists(self._dir_name):
                 os.makedirs(self._dir_name)

            with open(self._dir_name +'/scan_' +filename + '.ply', 'wb') as f:
                self.save_scene_stream(f)

        except Exception as e:
            self._logger.error(e)

        del self.points[:]
        self.points = []

    def save_scene_stream(self, stream, binary=False):

        frame = "ply\n"
        if binary:
            frame += "format binary_little_endian 1.0\n"
        else:
            frame += "format ascii 1.0\n"
        frame += "comment Generated by FabScanPi\n"
        frame += "comment version {0}\n".format(__version__)
        frame += "comment {0}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        frame += "element vertex {0}\n".format(self.get_size())
        frame += "property float x\n"
        frame += "property float y\n"
        frame += "property float z\n"
        frame += "property uchar red\n"
        frame += "property uchar green\n"
        frame += "property uchar blue\n"
        frame += "element face 0\n"
        frame += "property list uchar int vertex_indices\n"
        frame += "end_header\n"
        stream.write(frame)
        if self.get_size() > 0:
            if binary:
                for index, point in enumerate(self.points):
                    stream.write(struct.pack("<fffBBB",
                                            point[0], point[1], point[2],
                                            int(point[5]), int(point[4]), int(point[3])))
            else:
                for index, point in enumerate(self.points):
                    stream.write("{0} {1} {2} {3} {4} {5}\n".format(
                        point[0], point[1], point[2],
                        int(point[5]), int(point[4]), int(point[3])))