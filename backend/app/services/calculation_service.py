from __future__ import annotations

from calc_engine.reliability_engine.calculator import calculate_assembly, calculate_system
from calc_engine.reliability_engine.models import AssemblyInput, ComponentInput, RedundancyType
from calc_engine.reliability_engine.recommendations import generate_recommendations

from app.models.entities import AssemblyEntity, SystemEntity


def _to_assembly_input(assembly: AssemblyEntity) -> AssemblyInput:
    components = [
        ComponentInput(
            id=str(c.id),
            name=c.name,
            lambda_active=c.lambda_active,
            kp=c.kp,
            kr=c.kr,
            t_active=assembly.active_time,
            t_passive=assembly.passive_time,
            t_rest=assembly.rest_time,
            source=c.source,
            notes=c.notes,
            critical=c.critical,
        )
        for c in assembly.components
    ]
    return AssemblyInput(
        id=str(assembly.id),
        name=assembly.name,
        t_active=assembly.active_time,
        t_passive=assembly.passive_time,
        t_rest=assembly.rest_time,
        redundancy_type=RedundancyType.ONE_OO_TWO_ACTIVE
        if assembly.redundancy_type == "1oo2_active"
        else RedundancyType.ONE_OO_ONE,
        unintended_operation_probability=assembly.unintended_operation_probability,
        components=components,
        direct_lambda_active=assembly.direct_lambda_active,
        source=assembly.source,
        notes=assembly.notes,
    )


def calculate_system_entity(system: SystemEntity) -> dict:
    assembly_inputs = [_to_assembly_input(a) for a in system.assemblies]
    assembly_results = []

    for a in assembly_inputs:
        result = calculate_assembly(a)
        total_time = a.t_active + a.t_passive + a.t_rest
        assembly_results.append(
            {
                "id": a.id,
                "name": a.name,
                "r": result.r,
                "q": result.q,
                "unintended_operation_probability": a.unintended_operation_probability,
                "redundancy_type": a.redundancy_type.value,
                "active_fraction": (a.t_active / total_time) if total_time else 0,
                "single_point_of_failure": a.redundancy_type == RedundancyType.ONE_OO_ONE,
            }
        )

    system_result = calculate_system(assembly_inputs)
    recs = generate_recommendations(assembly_results=assembly_results, system_q=system_result.q)

    return {
        "system_name": system.name,
        "system_r": system_result.r,
        "system_q": system_result.q,
        "assemblies": assembly_results,
        "recommendations": recs,
    }
