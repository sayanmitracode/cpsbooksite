import unittest
from z3 import *
import Incdec
import Collatz
from Automaton import Automaton

class TestIncDecAutomaton(unittest.TestCase):
    def setUp(self):
        self.A = Automaton(
            Incdec.state_vars,
            Incdec.action_names,
            Incdec.init_pred,
            Incdec.incdec_transition
        )

    def test_inc(self):
        s = self.A.post_one([IntVal(0)], "inc")
        self.assertEqual(s[0].as_long(), 1)

    def test_dec(self):
        s = self.A.post_one([IntVal(0)], "dec")
        self.assertEqual(s[0].as_long(), -1)

    def test_all_next_steps(self):
        next_states = self.A.step_all([IntVal(0)], "inc") + self.A.step_all([IntVal(0)], "dec")
        next_values = sorted(s[0].as_long() for s in next_states)
        self.assertEqual(next_values, [-1, 1])

class TestCollatzAutomaton(unittest.TestCase):
    def setUp(self):
        self.A = Automaton(
            Collatz.state_vars,
            Collatz.action_names,
            Collatz.init_predicate,
            Collatz.collatz_transition
        )

    def test_collatz_first_step(self):
        s = self.A.post_one([IntVal(7)], "step")
        self.assertEqual(s[0].as_long(), 22)



if __name__ == '__main__':
    unittest.main()
