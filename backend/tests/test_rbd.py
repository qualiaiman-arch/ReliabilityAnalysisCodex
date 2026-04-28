import math

from calc_engine.reliability_engine.models import RBDConnection, RBDModel, RBDNode
from calc_engine.reliability_engine.rbd import solve_rbd


def test_rbd_series_parallel():
    rbd = RBDModel(
        nodes=[
            RBDNode(id="root", name="System", node_type="gate", operator="series"),
            RBDNode(id="par", name="Redundant Compute", node_type="gate", operator="parallel"),
            RBDNode(id="power", name="Power", node_type="assembly"),
            RBDNode(id="cpu_a", name="CPU A", node_type="assembly"),
            RBDNode(id="cpu_b", name="CPU B", node_type="assembly"),
        ],
        connections=[
            RBDConnection(source="root", target="par"),
            RBDConnection(source="root", target="power"),
            RBDConnection(source="par", target="cpu_a"),
            RBDConnection(source="par", target="cpu_b"),
        ],
        root_node_id="root",
    )

    block_r = {"cpu_a": 0.99, "cpu_b": 0.99, "power": 0.98}
    system_r = solve_rbd(rbd, block_r)
    expected_parallel = 1 - ((1 - 0.99) * (1 - 0.99))
    expected = expected_parallel * 0.98
    assert math.isclose(system_r, expected, rel_tol=1e-9)
