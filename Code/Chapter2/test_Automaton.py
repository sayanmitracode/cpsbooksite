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

    def test_post_action(self):
        # Test post_action with "inc"
        post_inc = self.A.post_action([IntVal(0)], "inc")
        self.assertEqual(post_inc, [[IntVal(1)]])
    
    def test_post(self):
        # Test post from a single state over all actions
        post_states = self.A.post([IntVal(0)])
        expected_states = [[IntVal(1)], [IntVal(-1)]]
        self.assertTrue(post_states == expected_states or post_states == [[IntVal(-1)], [IntVal(1)]])

    def test_incdec_tree_depth_2(self):
        G = self.A.reachability_tree(initial_state=[0], max_depth=2, all_actions=True)

        # Root should be x=0
        root_key = (0,)
        assert root_key in G.nodes, "Root node not found"

        # x=0 should have 2 successors: x=1 and x=-1
        children = set(G.successors(root_key))
        expected = {(1,), (-1,)}
        assert children == expected, f"Unexpected successors of x=0: {children}"

        # Total nodes should be 5: 0, 1, -1, 2, -2
        assert len(G.nodes) == 5, f"Expected 5 nodes, got {len(G.nodes)}"

    def test_no_duplicate_keys(self):
        G = self.A.reachability_tree(initial_state=[0], max_depth=3, all_actions=True)
        assert len(G.nodes) == len(set(G.nodes)), "Duplicate keys found in IncDec"

        G2 = self.A.reachability_tree(initial_state=[False, False, False], max_depth=3, all_actions=True)
        assert len(G2.nodes) == len(set(G2.nodes)), "Duplicate keys found in BitFlip"

class TestCollatzAutomaton(unittest.TestCase):
    def setUp(self):
        self.A = Automaton(
            Collatz.state_vars,
            Collatz.action_names,
            Collatz.init_predicate,
            Collatz.collatz_transition
        )

    def test_collatz_first_step(self):
        s = self.A.post_one([IntVal(7)], "update")
        self.assertEqual(s[0].as_long(), 22)



if __name__ == '__main__':
    unittest.main()
