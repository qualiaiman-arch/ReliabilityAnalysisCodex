import math

from calc_engine.reliability_engine.calculator import calculate_assembly, calculate_component
from calc_engine.reliability_engine.models import AssemblyInput, ComponentInput, RedundancyType


def test_component_reliability_formula():
    c = ComponentInput(
        id="c1",
        name="Comp",
        lambda_active=2e-5,
        t_active=10,
        t_passive=5,
        t_rest=20,
    )
    result = calculate_component(c)
    expected_h = 2e-5 * 10 + (2e-5 * 0.1) * 5 + (2e-5 * 0.025) * 20
    assert math.isclose(result.h, expected_h, rel_tol=1e-9)
    assert math.isclose(result.r, math.exp(-expected_h), rel_tol=1e-9)


def test_1oo2_active_logic():
    c1 = ComponentInput("1", "A", 2e-5, 10, 0, 0)
    c2 = ComponentInput("2", "B", 2e-5, 10, 0, 0)
    a = AssemblyInput(
        id="a1",
        name="Assembly",
        t_active=10,
        t_passive=0,
        t_rest=0,
        redundancy_type=RedundancyType.ONE_OO_TWO_ACTIVE,
        components=[c1, c2],
    )
    res = calculate_assembly(a)
    q_single = 1 - math.exp(-(2e-5 * 10))
    assert math.isclose(res.q, q_single * q_single, rel_tol=1e-8)
