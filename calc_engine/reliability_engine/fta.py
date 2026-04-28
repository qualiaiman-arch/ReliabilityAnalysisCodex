from __future__ import annotations

from .models import FTANode, RBDModel


def derive_fta_from_rbd(rbd: RBDModel) -> FTANode:
    node_map = {n.id: n for n in rbd.nodes}
    children: dict[str, list[str]] = {n.id: [] for n in rbd.nodes}
    for connection in rbd.connections:
        children[connection.source].append(connection.target)

    def build(node_id: str) -> FTANode:
        node = node_map[node_id]
        node_children = children.get(node_id, [])

        if not node_children:
            return FTANode(id=f"be_{node_id}", name=f"Failure of {node.name}", gate_type="BASIC")

        child_fta = [build(c) for c in node_children]

        gate = "OR" if node.operator == "series" else "AND"
        return FTANode(
            id=f"gate_{node_id}",
            name=f"Failure logic for {node.name}",
            gate_type=gate,
            children=child_fta,
        )

    return build(rbd.root_node_id)
