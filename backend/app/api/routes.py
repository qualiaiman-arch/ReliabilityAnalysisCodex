from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.entities import AssemblyEntity, ComponentEntity, SystemEntity
from app.schemas.system import CalculationResponse, SystemCreate
from app.services.calculation_service import calculate_system_entity
from app.services.export_service import export_excel, export_powerpoint
from app.services.sample_loader import load_demo_data

router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.post("/systems")
def create_system(payload: SystemCreate, db: Session = Depends(get_db)) -> dict:
    system = SystemEntity(
        name=payload.name,
        description=payload.description,
        mission=payload.mission,
        lifetime_hours=payload.lifetime_hours,
        operating_environment=payload.operating_environment,
    )
    db.add(system)
    db.flush()

    for assembly_payload in payload.assemblies:
        assembly = AssemblyEntity(
            system_id=system.id,
            name=assembly_payload.name,
            active_time=assembly_payload.active_time,
            passive_time=assembly_payload.passive_time,
            rest_time=assembly_payload.rest_time,
            redundancy_type=assembly_payload.redundancy_type,
            unintended_operation_probability=assembly_payload.unintended_operation_probability,
            direct_lambda_active=assembly_payload.direct_lambda_active,
            source=assembly_payload.source,
            notes=assembly_payload.notes,
        )
        db.add(assembly)
        db.flush()

        for component_payload in assembly_payload.components:
            db.add(
                ComponentEntity(
                    assembly_id=assembly.id,
                    name=component_payload.name,
                    critical=component_payload.critical,
                    lambda_active=component_payload.lambda_active,
                    kp=component_payload.kp,
                    kr=component_payload.kr,
                    source=component_payload.source,
                    notes=component_payload.notes,
                )
            )

    db.commit()
    return {"id": system.id}


@router.get("/systems/{system_id}/calculate", response_model=CalculationResponse)
def calculate(system_id: int, db: Session = Depends(get_db)) -> dict:
    system = db.query(SystemEntity).filter(SystemEntity.id == system_id).first()
    if not system:
        raise HTTPException(status_code=404, detail="System not found")
    return calculate_system_entity(system)


@router.get("/systems/{system_id}/export/excel")
def export_system_excel(system_id: int, db: Session = Depends(get_db)) -> Response:
    system = db.query(SystemEntity).filter(SystemEntity.id == system_id).first()
    if not system:
        raise HTTPException(status_code=404, detail="System not found")
    calculation = calculate_system_entity(system)
    content = export_excel(calculation)
    return Response(
        content=content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=system_{system_id}_reliability.xlsx"},
    )


@router.get("/systems/{system_id}/export/pptx")
def export_system_pptx(system_id: int, db: Session = Depends(get_db)) -> Response:
    system = db.query(SystemEntity).filter(SystemEntity.id == system_id).first()
    if not system:
        raise HTTPException(status_code=404, detail="System not found")

    calculation = calculate_system_entity(system)
    system_payload = {
        "name": system.name,
        "mission": system.mission,
        "operating_environment": system.operating_environment,
    }
    content = export_powerpoint(system_payload=system_payload, calculation=calculation)
    return Response(
        content=content,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        headers={"Content-Disposition": f"attachment; filename=system_{system_id}_reliability.pptx"},
    )


@router.post("/seed/demo")
def seed_demo(db: Session = Depends(get_db)) -> dict:
    system_id = load_demo_data(db)
    return {"id": system_id}
