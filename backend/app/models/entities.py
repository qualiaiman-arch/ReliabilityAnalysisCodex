from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class SystemEntity(Base):
    __tablename__ = "systems"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text, default="")
    mission: Mapped[str] = mapped_column(Text, default="")
    lifetime_hours: Mapped[float] = mapped_column(Float, default=0.0)
    operating_environment: Mapped[str] = mapped_column(Text, default="")

    assemblies = relationship("AssemblyEntity", back_populates="system", cascade="all, delete-orphan")


class AssemblyEntity(Base):
    __tablename__ = "assemblies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    system_id: Mapped[int] = mapped_column(ForeignKey("systems.id"))
    name: Mapped[str] = mapped_column(String(255))
    active_time: Mapped[float] = mapped_column(Float, default=0.0)
    passive_time: Mapped[float] = mapped_column(Float, default=0.0)
    rest_time: Mapped[float] = mapped_column(Float, default=0.0)
    redundancy_type: Mapped[str] = mapped_column(String(32), default="1oo1")
    unintended_operation_probability: Mapped[float] = mapped_column(Float, default=0.0)
    direct_lambda_active: Mapped[float | None] = mapped_column(Float, nullable=True)
    source: Mapped[str] = mapped_column(Text, default="")
    notes: Mapped[str] = mapped_column(Text, default="")

    system = relationship("SystemEntity", back_populates="assemblies")
    components = relationship("ComponentEntity", back_populates="assembly", cascade="all, delete-orphan")


class ComponentEntity(Base):
    __tablename__ = "components"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    assembly_id: Mapped[int] = mapped_column(ForeignKey("assemblies.id"))
    name: Mapped[str] = mapped_column(String(255))
    critical: Mapped[bool] = mapped_column(Boolean, default=True)
    lambda_active: Mapped[float] = mapped_column(Float)
    kp: Mapped[float] = mapped_column(Float, default=0.1)
    kr: Mapped[float] = mapped_column(Float, default=0.025)
    source: Mapped[str] = mapped_column(Text, default="")
    notes: Mapped[str] = mapped_column(Text, default="")

    assembly = relationship("AssemblyEntity", back_populates="components")
