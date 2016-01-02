#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from BodyControl.SteeringGearControl import SteeringGearControl
from time import sleep


class TestSteeringGearControl(unittest.TestCase):

    def setUp(self):
        self.sgc = SteeringGearControl()
        self.sgc.register('A', 0)
        self.sgc.register('B', 1)

    def tearDown(self):
        self.sgc.close()

    def Test01_SimpleMove(self):
        self.sgc.move('A', 90, 2000)
        self.assertEqual(self.sgc.is_moving(), True)
        sleep(3)
        self.assertEqual(self.sgc.is_moving(), False)
        self.assertEqual(self.sgc.position('A'), 90)

        self.sgc.move('A', 0, 2000)
        self.assertEqual(self.sgc.is_moving(), True)
        sleep(3)
        self.assertEqual(self.sgc.is_moving(), False)
        self.assertEqual(self.sgc.position('A'), 1.8)

    def Test02_GroupAction(self):
        self.sgc.start_action_group()
        self.sgc.move('A', 90)
        self.sgc.move('B', 90)
        self.sgc.end_action_group(2000)
        self.assertEqual(self.sgc.is_moving(), True)
        sleep(3)
        self.assertEqual(self.sgc.is_moving(), False)
        self.assertEqual(self.sgc.position('A'), 90)
        self.assertEqual(self.sgc.position('B'), 90)

        self.sgc.start_action_group()
        self.sgc.move('A', 0)
        self.sgc.move('B', 0)
        self.sgc.end_action_group(2000)
        self.assertEqual(self.sgc.is_moving(), True)
        sleep(3)
        self.assertEqual(self.sgc.is_moving(), False)
        self.assertEqual(self.sgc.position('A'), 1.8)
        self.assertEqual(self.sgc.position('B'), 1.8)
