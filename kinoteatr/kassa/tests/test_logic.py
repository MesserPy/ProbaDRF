# from django.test import TestCase
import unittest
from unittest import TestCase

from kassa.logic import operations


class LogicTestCase(TestCase):

    def test_plus(self):
        result = operations(6, 12, '+')
        self.assertEqual(18, result)

    def test_minus(self):
        result = operations(6, 12, '-')
        self.assertEqual(-6, result)
