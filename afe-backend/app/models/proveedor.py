# app/models/proveedor.py
"""
Modelo Proveedor - Enterprise Edition

Gestiona proveedores con soporte para:
- Creación manual (interfaz web)
- Creación automática (desde facturas)
- Auditoría completa
- Rastreo de cambios


"""

from sqlalchemy import Column, BigInteger, String, DateTime, Boolean, text, Index, event
from sqlalchemy.sql import func
from app.db.base import Base
from sqlalchemy.orm import relationship, Session


class Proveedor(Base):
    """
    Modelo de Proveedor con soporte para auto-creación desde facturas.

    Campos principales:
    - id: Identificador único
    - nit: NIT normalizado (XXXXXXXXX-D format)
    - razon_social: Nombre del proveedor
    - contacto_email: Email del proveedor
    - telefono: Teléfono
    - direccion: Dirección
    - area: Área de la empresa
    - activo: Flag activo/inactivo

    Campos de auditoría:
    - creado_en: Timestamp de creación en BD
    - es_auto_creado: Flag que indica si fue auto-creado desde factura
    - creado_automaticamente_en: Timestamp de auto-creación (NULL si manual)

    Relaciones:
    - facturas: One-to-Many con Factura
    """

    __tablename__ = "proveedores"

    # ==================== PRIMARY KEY ====================
    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="Identificador único del proveedor"
    )

    # ==================== IDENTIFICACIÓN ====================
    nit = Column(
        String(64),
        nullable=False,
        unique=True,
        index=True,
        comment="NIT normalizado en formato XXXXXXXXX-D (ej: 8001854499)"
    )

    razon_social = Column(
        String(255),
        nullable=False,
        comment="Razón social del proveedor"
    )

    # ==================== INFORMACIÓN DE CONTACTO ====================
    area = Column(
        String(100),
        nullable=True,
        comment="Área o departamento de la empresa"
    )

    contacto_email = Column(
        String(255),
        nullable=True,
        comment="Email de contacto principal"
    )

    telefono = Column(
        String(50),
        nullable=True,
        comment="Teléfono de contacto"
    )

    direccion = Column(
        String(255),
        nullable=True,
        comment="Dirección física del proveedor"
    )

    # ==================== ESTADO ====================
    activo = Column(
        Boolean,
        server_default=text("true"),
        nullable=False,
        default=True,
        comment="Flag de estado activo/inactivo"
    )

    # ==================== AUDITORÍA ====================
    creado_en = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Timestamp de creación en BD"
    )

    # ==================== DEPRECATED: AUTO-CREACIÓN ====================
    # 🔒 SEGURIDAD 2025-12-15: Auto-creación deshabilitada por seguridad.
    # Estos campos se mantienen por auditoría histórica pero ya no se usan.
    # Todos los proveedores nuevos tendrán es_auto_creado=False.

    es_auto_creado = Column(
        Boolean,
        nullable=False,
        default=False,
        server_default=text("false"),
        index=True,
        comment="[DEPRECATED 2025-12-15] Flag auto-creación (ya no se usa, siempre False)"
    )

    creado_automaticamente_en = Column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
        comment="[DEPRECATED 2025-12-15] Timestamp auto-creación (ya no se usa, siempre NULL)"
    )

    # ==================== RELACIONES ====================
    # Relación one-to-many con facturas
    facturas = relationship(
        "Factura",
        back_populates="proveedor",
        lazy="selectin",
        cascade="all, delete-orphan"
    )

    # ==================== ÍNDICES COMPUESTOS ====================
    # Índice para auditoría de proveedores auto-creados
    __table_args__ = (
        Index(
            'idx_proveedor_auto_creado_fecha',
            'es_auto_creado',
            'creado_automaticamente_en'
        ),
    )

    # ==================== MÉTODOS PÚBLICOS ====================

    def __repr__(self) -> str:
        """Representación en string del proveedor."""
        estado = "ACTIVO" if self.activo else "INACTIVO"
        return f"<Proveedor(id={self.id}, nit={self.nit}, razon_social={self.razon_social}, estado={estado})>"


# ==================== SINCRONIZACIÓN BIDIRECCIONAL ====================

@event.listens_for(Proveedor, 'after_update')
def sincronizar_nits_cuando_cambia_proveedor(mapper, connection, target):
    """
    SINCRONIZACIÓN INVERSA: Proveedores → NITs (Propagación de Cambios).

    ARQUITECTURA PROFESIONAL:
    - Cuando cambia razon_social del proveedor, actualizar TODOS los NITs
    - Garantiza consistencia bidireccional
    - Propagación automática de cambios

    Se ejecuta DESPUÉS de UPDATE en proveedores.

    IMPORTANTE: Solo se ejecuta si razon_social cambió realmente.
    """
    from sqlalchemy.orm import object_session
    from sqlalchemy import inspect

    # Verificar si razon_social fue modificada
    state = inspect(target)
    history = state.get_history('razon_social', passive=True)

    # Si razon_social cambió, propagar a todos los NITs
    if history.has_changes() and target.razon_social:
        session = object_session(target)
        if session:
            # Importar aquí para evitar circular import
            from app.models.email_config import NitConfiguracion

            # Actualizar todos los NITs con este NIT
            nits = session.query(NitConfiguracion).filter(
                NitConfiguracion.nit == target.nit
            ).all()

            for nit_config in nits:
                nit_config.nombre_proveedor = target.razon_social

            # No hacer commit aquí - SQLAlchemy lo hará automáticamente
