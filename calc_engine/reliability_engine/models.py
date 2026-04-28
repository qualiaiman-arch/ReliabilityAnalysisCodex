from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Literal


class RedundancyType(str, Enum):
    ONE_OO_ONE = "1oo1"
    ONE_OO_TWO_ACTIVE = "1oo2_active"


@dataclass
class ComponentInput:
    id: str
    name: str
    lambda_active: float
    t_active: float
    t_passive: float
    t_rest: float
    kp: float = 0.1
    kr: float = 0.025
    source: str = ""
    notes: str = ""
    critical: bool = True


@dataclass
class AssemblyInput:
    id: str
    name: str
    t_active: float
    t_passive: float
    t_rest: float
    redundancy_type: RedundancyType = RedundancyType.ONE_OO_ONE
    unintended_operation_probability: float = 0.0
    components: list[ComponentInput] = field(default_factory=list)
    direct_lambda_active: float | None = None
    source: str = ""
    notes: str = ""


@dataclass
class RBDNode:
    id: str
    name: str
    node_type: Literal["assembly", "gate", "resource"]
    operator: Literal["series", "parallel"] | None = None


@dataclass
class RBDConnection:
    source: str
    target: str


@dataclass
class RBDModel:
    nodes: list[RBDNode]
    connections: list[RBDConnection]
    root_node_id: str


@dataclass
class FTANode:
    id: str
    name: str
    gate_type: Literal["AND", "OR", "BASIC"]
    children: list["FTANode"] = field(default_factory=list)
