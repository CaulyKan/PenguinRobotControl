#!/usr/bin/python3
# -*- coding: utf-8 -*-

from serial import Serial


class SteeringGearControl:
    """
        与舵机控制板通讯，控制多个舵机的运动
    """

    def __init__(self):

        self.serial = Serial("/dev/ttyUSB0", 115200)
        self.gears = dict()
        self.in_action_group = False
        self.pending_actions = dict()

    def register(self, gear_name: str, index: int):
        """
        注册一个舵机

        :param gear_name: 舵机名称
        :param index: 舵机在控制板上的插槽编号
        """

        self.gears[gear_name] = index

    def move(self, gear_name: str, degrees: float, time: int = 1000):
        """
        转动指定的舵机

        :param gear_name: 舵机名
        :param degrees: 角度，0~180
        :param time: 时间
        """

        gear = self.gears.get(gear_name, None)

        if gear is None:
            raise IndexError('Unknown gear: ' + gear_name)

        if self.in_action_group:
            self.pending_actions[gear] = self._convert2pulse(degrees)

        else:
            command_str = self._getmovestring(gear, self._convert2pulse(degrees)) + 'T' + str(time) + '\r'
            self.serial.write(command_str.encode('ascii'))

    def position(self, gear_name) -> float:
        """
        返回指定舵机当前的位置

        :param gear_name: 舵机名
        :return: 当前的位置，0-180
        """

        gear = self.gears.get(gear_name, None)

        if gear is None:
            raise IndexError('Unknown gear: ' + gear_name)

        command_str = 'QP ' + str(gear) + '\r'

        self.serial.write(command_str.encode('ascii'))

        pos = ord(self.serial.read(1))

        return self._convert2degree(pos)

    def is_moving(self) -> bool:
        """
        返回舵机当前是否有动作

        :return:
        """

        command_str = 'Q\r'
        self.serial.write(command_str.encode('ascii'))

        return self.serial.read(1) == b'+'

    def start_action_group(self):
        """
        开始一组协调动作。该组动作中的多个舵机无论其当前位置，会在同一时间转动到指定角度。
        """

        self.in_action_group = True
        self.pending_actions = dict()

    def end_action_group(self, time: int):
        """
        开始执行动作组。

        :param time: 完成的时间
        """

        if len(self.pending_actions) > 0:
            command_str = ''.join([self._getmovestring(k, v) for k, v in self.pending_actions.items()])
            command_str += 'T' + str(time) + '\r'
            self.serial.write(command_str.encode('ascii'))

    def close(self):
        """
        关闭与舵机控制器的通讯
        """

        self.serial.close()

    @staticmethod
    def _getmovestring(index: int, pos: int):

        return '#' + str(index) + ' P' + str(pos) + ' '

    @staticmethod
    def _convert2pulse(degrees: float) -> int:

        pt = int(degrees / 180 * 2000 + 500)

        if pt > 2490:
            return 2480
        elif pt < 510:
            return 520
        else:
            return pt

    @staticmethod
    def _convert2degree(position: int) -> float:

        return (position * 10 - 500) / 2000 * 180
