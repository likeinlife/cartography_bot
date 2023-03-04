import unittest
from classes import Numenculat

from find_geograph import CoordinatePair, Degrees, find_coordinate_bounds, get_part, get_first, get_quarter, IncorrectData
from re_compilated import re


class TestCoords(unittest.TestCase):

    @unittest.skip('TODO')
    def testFirstPart(self):
        param_list = (
            (('D', '58'), (12, 162), (16, 168)),
            (('C', '35'), (8, 24), (12, 30)),
            (('M', '45'), (48, 84), (52, 90)),
        )
        for numenculat, first, second in param_list:
            with self.subTest('numenculature to degrees', numenculat=numenculat):
                result = get_first(numenculat)
                expected_result = CoordinatePair(*first), CoordinatePair(*second)
                self.assertEqual(result, expected_result)

    def testFindingParts(self):
        numenculat = Numenculat(CoordinatePair(12, 162), CoordinatePair(16, 168), 'N-44')
        result = get_part('19', numenculat, 12)
        expected = Numenculat(CoordinatePair(Degrees(15, 20), 165), CoordinatePair(Degrees(15, 40), Degrees(165, 30)),
                              'N-44-19')
        self.assertEqual(result, expected)

    @unittest.skip('TODO')
    def testQuarter(self):
        param_list = ((
            'А',
            (
                CoordinatePair(Degrees(15, 20), Degrees(165)),
                CoordinatePair(Degrees(15, 40), Degrees(165, 30)),
            ),
            (
                CoordinatePair(Degrees(15, 30), Degrees(165)),
                CoordinatePair(Degrees(15, 40), Degrees(165, 15)),
            ),
        ), (
            'г',
            (
                CoordinatePair(Degrees(15, 30), Degrees(165)),
                CoordinatePair(Degrees(15, 40), Degrees(165, 15)),
            ),
            (
                CoordinatePair(Degrees(15, 30), Degrees(165, 7, 30)),
                CoordinatePair(Degrees(15, 35), Degrees(165, 15)),
            ),
        ))
        for part, bounds, expected_result in param_list:
            with self.subTest(quarter=part):
                result = get_quarter(part, bounds)
                self.assertEqual(result, expected_result)

    @unittest.skip('TODO')
    def testRaiseFirstLetterError(self):
        param_list = ('К-39-37-А', 'Ы-24-25')
        for numenculat in param_list:
            with self.subTest(numenculat=numenculat):
                with self.assertRaises(IncorrectData):
                    find_coordinate_bounds(numenculat)

    @unittest.skip('TODO')
    def testFindBounds(self):
        param_list = (
            (
                'N-50-78-Г-в-1',
                CoordinatePair(Degrees(53, 42, 30), Degrees(116, 45)),
                CoordinatePair(Degrees(53, 45), Degrees(116, 48, 45)),
            ),
            (
                'K-39-37-А',
                CoordinatePair(Degrees(42, 50), Degrees(48)),
                CoordinatePair(Degrees(43), Degrees(48, 15)),
            ),
            (
                'D-58-19-А-г-1',
                CoordinatePair(Degrees(15, 32, 30), Degrees(165, 7, 30)),
                CoordinatePair(Degrees(15, 35), Degrees(165, 11, 15)),
            ),
        )
        for numenculat, first_pair, second_pair in param_list:
            with self.subTest(name=numenculat):
                self.assertEqual(
                    find_coordinate_bounds(numenculat),
                    (first_pair, second_pair),
                )


class TestDegree(unittest.TestCase):

    def testFindDegreesCenter(self):
        param_list = (
            (
                (15, 20),
                (15, 40),
                (15, 30),
            ),
            (
                (165, 7, 30),
                (165, 15),
                (165, 11, 15),
            ),
            (
                (165,),
                (165, 15),
                (165, 7, 30),
            ),
        )

        for first_values, second_values, expected_values in param_list:
            with self.subTest():
                first = Degrees(*first_values)
                second = Degrees(*second_values)
                expected_result = Degrees(*expected_values)
                result = Degrees.findCenter(first, second)
                self.assertEqual(result, expected_result)

    def testAdd(self):
        param_list = (
            (
                (15, 20),
                (0, 10),
                (15, 30),
            ),
            (
                (320, 10, 15),
                (0, 10, 20),
                (320, 20, 35),
            ),
            (
                (0,),
                (20, 20, 20),
                (20, 20, 20),
            ),
        )
        for first_value, second_value, expected_value in param_list:
            with self.subTest():
                first = Degrees(*first_value)
                second = Degrees(*second_value)
                result = first + second
                expected = Degrees(*expected_value)
                self.assertEqual(result, expected)

    def testSub(self):
        first = Degrees(10, 10, 10)
        second = Degrees(0, 20, 10)
        result = first - second
        expected = Degrees(9, 50)
        self.assertEqual(result, expected)

    def testLess(self):
        first = Degrees(10, 10, 10)
        second = Degrees(20, 20, 20)
        expected = True
        self.assertEqual(first < second, expected)

    def testGreater(self):
        first = Degrees(360, 10, 10)
        second = Degrees(20, 20, 20)
        expected = True
        self.assertEqual(first > second, expected)
