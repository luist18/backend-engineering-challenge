import os
from unittest import TestCase

from unbabel_cli.algorithm.queue_moving_average_algorithm import QueueMovingAverageAlgorithm

from .util import read_input_file, read_output_file

RESOURCES_PATH = "./tests/resources/"


class QueueMovingAverageTest(TestCase):
    def setUp(self):
        self.algorithm = QueueMovingAverageAlgorithm()

    def __test_file(self, algorithm, input_name, output_name, window=10):
        input = read_input_file(os.path.join(RESOURCES_PATH, "input", input_name))
        expected_output = read_output_file(os.path.join(RESOURCES_PATH, "output", output_name))

        output = algorithm.moving_average(input, window=window)

        self.assertEqual(len(expected_output), len(output))

        for o1, o2 in zip(expected_output, output):
            self.assertEqual(o1, o2)

    def test_big_event_gap(self):
        self.__test_file(self.algorithm, "big_event_gap.json", "big_event_gap.json")

    def test_different_window_size0(self):
        self.__test_file(self.algorithm, "different_window_size.json", "window_0.json", window=0)

    def test_different_window_size5(self):
        self.__test_file(self.algorithm, "different_window_size.json", "window_5.json", window=5)

    def test_empty(self):
        self.__test_file(self.algorithm, "empty.json", "empty.json")

    def test_end_year(self):
        self.__test_file(self.algorithm, "end_year.json", "end_year.json")

    def test_leap_year(self):
        self.__test_file(self.algorithm, "leap_year.json", "leap_year.json")

    def test_multiple_events_window_1(self):
        self.__test_file(self.algorithm, "multiple_events_window_1.json", "multiple_events_window_1.json", window=1)

    def test_multiple(self):
        self.__test_file(self.algorithm, "multiple.json", "multiple.json")

    def test_non_leap_year(self):
        self.__test_file(self.algorithm, "non_leap_year.json", "non_leap_year.json")

    def test_one(self):
        self.__test_file(self.algorithm, "one.json", "one.json")

    def test_sample(self):
        self.__test_file(self.algorithm, "sample.json", "sample.json")
