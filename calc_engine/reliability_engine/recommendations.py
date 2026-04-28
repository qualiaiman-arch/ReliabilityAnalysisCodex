from __future__ import annotations

from typing import Any


def generate_recommendations(
    assembly_results: list[dict[str, Any]],
    system_q: float,
    shared_resources: list[dict[str, Any]] | None = None,
) -> list[str]:
    recs: list[str] = []
    sorted_by_q = sorted(assembly_results, key=lambda x: x.get("q", 0.0), reverse=True)

    dominant = sorted_by_q[:3]
    if dominant:
        names = ", ".join(d["name"] for d in dominant)
        recs.append(f"Dominant Q contributors: {names}.")

    for a in sorted_by_q:
        if a.get("redundancy_type") == "1oo1" and a.get("q", 0) > 0.02:
            recs.append(f"Consider 1oo2 active redundancy for {a['name']}.")

    for a in assembly_results:
        if a.get("active_fraction", 0) > 0.7:
            recs.append(f"Reduce active duty cycle for {a['name']} to lower risk.")

    for a in assembly_results:
        if a.get("single_point_of_failure"):
            recs.append(f"{a['name']} is a single point of failure; add architectural mitigation.")

    for resource in shared_resources or []:
        if resource.get("q", 0) > 0.01:
            recs.append(
                f"Shared resource {resource['name']} dominates risk; consider separation or redundancy."
            )

    if system_q > 0.05:
        recs.append("Plan design verification and acceptance tests focused on dominant contributors.")

    return recs
