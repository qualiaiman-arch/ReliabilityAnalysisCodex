from __future__ import annotations

from .models import RBDModel


def solve_rbd(rbd: RBDModel, block_reliability: dict[str, float]) -> float:
    node_map = {n.id: n for n in rbd.nodes}
    children: dict[str, list[str]] = {n.id: [] for n in rbd.nodes}
    for connection in rbd.connections:
        children[connection.source].append(connection.target)

    visited: set[str] = set()
    stack: set[str] = set()

    def eval_node(node_id: str) -> float:
        if node_id in stack:
            raise ValueError("RBD loops are not supported")
        stack.add(node_id)

        node = node_map[node_id]
        node_children = children.get(node_id, [])

        if not node_children:
            if node_id not in block_reliability:
                raise ValueError(f"Missing block reliability for node {node_id}")
            value = block_reliability[node_id]
        else:
            child_values = [eval_node(child_id) for child_id in node_children]
            if node.operator == "series":
                value = 1.0
                for v in child_values:
                    value *= v
            elif node.operator == "parallel":
                q = 1.0
                for v in child_values:
                    q *= 1 - v
                value = 1 - q
            else:
                raise ValueError(f"Gate node {node_id} missing operator")

        stack.remove(node_id)
        visited.add(node_id)
        return value

    return eval_node(rbd.root_node_id)
