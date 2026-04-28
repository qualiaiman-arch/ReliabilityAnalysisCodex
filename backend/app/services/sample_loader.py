from __future__ import annotations

import json
from pathlib import Path

from sqlalchemy.orm import Session

from app.models.entities import AssemblyEntity, ComponentEntity, SystemEntity


def load_demo_data(db: Session) -> int:
    sample_path = Path(__file__).resolve().parents[3] / "sample_data" / "demo_system.json"
    payload = json.loads(sample_path.read_text())

    system = SystemEntity(
        name=payload["name"],
        description=payload.get("description", ""),
        mission=payload.get("mission", ""),
        lifetime_hours=payload.get("lifetime_hours", 0),
        operating_environment=payload.get("operating_environment", ""),
    )
    db.add(system)
    db.flush()

    for a in payload.get("assemblies", []):
        assembly = AssemblyEntity(
            system_id=system.id,
            name=a["name"],
            active_time=a.get("active_time", 0.0),
            passive_time=a.get("passive_time", 0.0),
            rest_time=a.get("rest_time", 0.0),
            redundancy_type=a.get("redundancy_type", "1oo1"),
            unintended_operation_probability=a.get("unintended_operation_probability", 0.0),
            direct_lambda_active=a.get("direct_lambda_active"),
            source=a.get("source", ""),
            notes=a.get("notes", ""),
        )
        db.add(assembly)
        db.flush()

        for c in a.get("components", []):
            db.add(
                ComponentEntity(
                    assembly_id=assembly.id,
                    name=c["name"],
                    critical=c.get("critical", True),
                    lambda_active=c["lambda_active"],
                    kp=c.get("kp", 0.1),
                    kr=c.get("kr", 0.025),
                    source=c.get("source", ""),
                    notes=c.get("notes", ""),
                )
            )

    db.commit()
    return system.id
