from __future__ import annotations

from pydantic import BaseModel, Field


class ComponentCreate(BaseModel):
    name: str
    critical: bool = True
    lambda_active: float
    kp: float = 0.1
    kr: float = 0.025
    source: str = ""
    notes: str = ""


class AssemblyCreate(BaseModel):
    name: str
    active_time: float = 0.0
    passive_time: float = 0.0
    rest_time: float = 0.0
    redundancy_type: str = "1oo1"
    unintended_operation_probability: float = 0.0
    direct_lambda_active: float | None = None
    source: str = ""
    notes: str = ""
    components: list[ComponentCreate] = Field(default_factory=list)


class SystemCreate(BaseModel):
    name: str
    description: str = ""
    mission: str = ""
    lifetime_hours: float = 0.0
    operating_environment: str = ""
    assemblies: list[AssemblyCreate] = Field(default_factory=list)


class CalculationResponse(BaseModel):
    system_name: str
    system_r: float
    system_q: float
    assemblies: list[dict]
    recommendations: list[str]
