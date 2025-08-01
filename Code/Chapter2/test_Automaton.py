import unittest
from z3 import *
import Incdec
import Collatz
from Automaton import Automaton
from State import State

class TestStateClass(unittest.TestCase):
    """Unit tests for the State class with 3 boolean variables."""
    def setUp(self):
        self.s = State([
            ("b0", BoolSort(), BoolVal(False)),
            ("b1", BoolSort(), BoolVal(True)),
            ("b2", BoolSort(), BoolVal(False)),
        ])

    def test_str_and_repr(self):
        self.assertEqual(str(self.s), "(b0=False, b1=True, b2=False)")
        self.assertEqual(repr(self.s), "State([('b0', Bool, False), ('b1', Bool, True), ('b2', Bool, False)])")

    def test_get_value(self):
        self.assertEqual(str(self.s.get_values("b0")), "False")
        self.assertEqual(str(self.s.get_values("b1")), "True")
        with self.assertRaises(KeyError):
            self.s.get_values("b3")

    def test_equality_and_hashing(self):
        s2 = State([
            ("b0", BoolSort(), BoolVal(False)),
            ("b1", BoolSort(), BoolVal(True)),
            ("b2", BoolSort(), BoolVal(False)),
        ])
        s3 = State([
            ("b0", BoolSort(), BoolVal(True)),
            ("b1", BoolSort(), BoolVal(True)),
            ("b2", BoolSort(), BoolVal(False)),
        ])
        self.assertEqual(self.s, s2)
        self.assertNotEqual(self.s, s3)
        self.assertEqual(hash(self.s), hash(s2))
        self.assertNotEqual(hash(self.s), hash(s3))





if __name__ == '__main__':
    unittest.main()
