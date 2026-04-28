from calc_engine.reliability_engine.fta import derive_fta_from_rbd
from calc_engine.reliability_engine.models import RBDConnection, RBDModel, RBDNode


def test_fta_conversion_series_to_or_parallel_to_and():
    rbd = RBDModel(
        nodes=[
            RBDNode(id="root", name="System", node_type="gate", operator="series"),
            RBDNode(id="redundant", name="Redundant block", node_type="gate", operator="parallel"),
            RBDNode(id="a", name="A", node_type="assembly"),
            RBDNode(id="b", name="B", node_type="assembly"),
        ],
        connections=[
            RBDConnection(source="root", target="redundant"),
            RBDConnection(source="redundant", target="a"),
            RBDConnection(source="redundant", target="b"),
        ],
        root_node_id="root",
    )

    fta = derive_fta_from_rbd(rbd)
    assert fta.gate_type == "OR"
    assert len(fta.children) == 1
    assert fta.children[0].gate_type == "AND"
    assert all(c.gate_type == "BASIC" for c in fta.children[0].children)
