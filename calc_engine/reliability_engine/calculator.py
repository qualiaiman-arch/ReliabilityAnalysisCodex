from __future__ import annotations

import math
from dataclasses import dataclass

from .models import AssemblyInput, ComponentInput, RedundancyType


@dataclass
class ReliabilityResult:
    h: float
    r: float
    q: float


def calculate_component(component: ComponentInput) -> ReliabilityResult:
    lambda_passive = component.lambda_active * component.kp
    lambda_rest = component.lambda_active * component.kr
    h = (
        component.lambda_active * component.t_active
        + lambda_passive * component.t_passive
        + lambda_rest * component.t_rest
    )
    r = math.exp(-h)
    return ReliabilityResult(h=h, r=r, q=1 - r)


def _direct_assembly_result(assembly: AssemblyInput) -> ReliabilityResult:
    if assembly.direct_lambda_active is None:
        raise ValueError("direct_lambda_active is required for direct assembly calculations")
    lambda_passive = assembly.direct_lambda_active * 0.1
    lambda_rest = assembly.direct_lambda_active * 0.025
    h = (
        assembly.direct_lambda_active * assembly.t_active
        + lambda_passive * assembly.t_passive
        + lambda_rest * assembly.t_rest
    )
    r = math.exp(-h)
    return ReliabilityResult(h=h, r=r, q=1 - r)


def calculate_assembly(assembly: AssemblyInput) -> ReliabilityResult:
    if assembly.components:
        component_results = [calculate_component(c) for c in assembly.components]

        if assembly.redundancy_type == RedundancyType.ONE_OO_ONE:
            r_assembly = 1.0
            for res in component_results:
                r_assembly *= res.r
            q_assembly = 1 - r_assembly
            return ReliabilityResult(h=0.0, r=r_assembly, q=q_assembly)

        if assembly.redundancy_type == RedundancyType.ONE_OO_TWO_ACTIVE:
            if len(component_results) != 2:
                raise ValueError("1oo2 active redundancy requires exactly two components")
            q_1oo2 = component_results[0].q * component_results[1].q
            r_1oo2 = 1 - q_1oo2
            return ReliabilityResult(h=0.0, r=r_1oo2, q=q_1oo2)

        raise ValueError(f"Unsupported redundancy type: {assembly.redundancy_type}")

    return _direct_assembly_result(assembly)


def calculate_system(assemblies: list[AssemblyInput]) -> ReliabilityResult:
    r_system = 1.0
    for assembly in assemblies:
        r_system *= calculate_assembly(assembly).r
    return ReliabilityResult(h=0.0, r=r_system, q=1 - r_system)
