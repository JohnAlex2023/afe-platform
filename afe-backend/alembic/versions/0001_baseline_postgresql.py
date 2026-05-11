"""baseline_postgresql

Revision ID: 0001
Revises: 
Create Date: 2026-05-11 14:30:09.473820

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
"""baseline_postgresql

Revision ID: 0001
Revises: 
Create Date: 2026-05-11 14:30:09.473820

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0001'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. ROLES (Seed Data)
    roles_table = op.create_table('roles',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('nombre', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nombre')
    )
    
    # Insert default roles
    op.bulk_insert(roles_table, [
        {"nombre": "superadmin"},
        {"nombre": "admin"},
        {"nombre": "responsable"},
        {"nombre": "contador"},
        {"nombre": "viewer"}
    ])

    # 2. SCHEMA
    op.create_table('audit_log',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('entidad', sa.String(length=64), nullable=False),
    sa.Column('entidad_id', sa.BigInteger(), nullable=False),
    sa.Column('accion', sa.String(length=50), nullable=False),
    sa.Column('usuario', sa.String(length=100), nullable=False),
    sa.Column('detalle', sa.JSON(), nullable=True),
    sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('grupos',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False, comment='Identificador único del grupo'),
    sa.Column('nombre', sa.String(length=150), nullable=False, comment='Nombre del grupo/sede'),
    sa.Column('codigo_corto', sa.String(length=20), nullable=False, comment='Código único (CAM, CAI, AVID, etc.)'),
    sa.Column('descripcion', sa.Text(), nullable=True, comment='Descripción detallada del grupo'),
    sa.Column('grupo_padre_id', sa.BigInteger(), nullable=True, comment='FK al grupo padre (NULL si es raíz)'),
    sa.Column('nivel', sa.Integer(), nullable=False, comment='Nivel en jerarquía (1=raíz, 2=hijo, etc.)'),
    sa.Column('ruta_jerarquica', sa.String(length=500), nullable=True, comment="Ruta completa: '1/5/12' para navegación"),
    sa.Column('correos_corporativos', sa.JSON(), nullable=True, comment='Array de correos corporativos del grupo'),
    sa.Column('permite_subsedes', sa.Boolean(), nullable=False, comment='¿Puede tener hijos?'),
    sa.Column('max_nivel_subsedes', sa.Integer(), nullable=False, comment='Profundidad máxima permitida'),
    sa.Column('activo', sa.Boolean(), server_default=sa.text('true'), nullable=False, comment='Estado activo/inactivo'),
    sa.Column('eliminado', sa.Boolean(), server_default=sa.text('false'), nullable=False, comment='Soft delete'),
    sa.Column('fecha_eliminacion', sa.DateTime(timezone=True), nullable=True, comment='Cuándo se eliminó'),
    sa.Column('eliminado_por', sa.String(length=255), nullable=True, comment='Usuario que eliminó'),
    sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='Timestamp de creación'),
    sa.Column('creado_por', sa.String(length=255), nullable=False, comment='Usuario que creó'),
    sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='Timestamp de última actualización'),
    sa.Column('actualizado_por', sa.String(length=255), nullable=True, comment='Usuario que actualizó'),
    sa.ForeignKeyConstraint(['grupo_padre_id'], ['grupos.id'], name='fk_grupo_padre'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_grupo_activo_eliminado', 'grupos', ['activo', 'eliminado'], unique=False)
    op.create_index('idx_grupo_codigo', 'grupos', ['codigo_corto'], unique=False)
    op.create_index('idx_grupo_padre', 'grupos', ['grupo_padre_id'], unique=False)
    op.create_index('idx_grupo_ruta', 'grupos', ['ruta_jerarquica'], unique=False)
    op.create_index(op.f('ix_grupos_activo'), 'grupos', ['activo'], unique=False)
    op.create_index(op.f('ix_grupos_codigo_corto'), 'grupos', ['codigo_corto'], unique=True)
    op.create_index(op.f('ix_grupos_eliminado'), 'grupos', ['eliminado'], unique=False)
    op.create_index(op.f('ix_grupos_grupo_padre_id'), 'grupos', ['grupo_padre_id'], unique=False)
    op.create_index(op.f('ix_grupos_nombre'), 'grupos', ['nombre'], unique=False)
    op.create_index(op.f('ix_grupos_ruta_jerarquica'), 'grupos', ['ruta_jerarquica'], unique=False)
    op.create_table('proveedores',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False, comment='Identificador único del proveedor'),
    sa.Column('nit', sa.String(length=64), nullable=False, comment='NIT normalizado en formato XXXXXXXXX-D (ej: 8001854499)'),
    sa.Column('razon_social', sa.String(length=255), nullable=False, comment='Razón social del proveedor'),
    sa.Column('area', sa.String(length=100), nullable=True, comment='Área o departamento de la empresa'),
    sa.Column('contacto_email', sa.String(length=255), nullable=True, comment='Email de contacto principal'),
    sa.Column('telefono', sa.String(length=50), nullable=True, comment='Teléfono de contacto'),
    sa.Column('direccion', sa.String(length=255), nullable=True, comment='Dirección física del proveedor'),
    sa.Column('activo', sa.Boolean(), server_default=sa.text('true'), nullable=False, comment='Flag de estado activo/inactivo'),
    sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='Timestamp de creación en BD'),
    sa.Column('es_auto_creado', sa.Boolean(), server_default=sa.text('false'), nullable=False, comment='[DEPRECATED 2025-12-15] Flag auto-creación (ya no se usa, siempre False)'),
    sa.Column('creado_automaticamente_en', sa.DateTime(timezone=True), nullable=True, comment='[DEPRECATED 2025-12-15] Timestamp auto-creación (ya no se usa, siempre NULL)'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_proveedor_auto_creado_fecha', 'proveedores', ['es_auto_creado', 'creado_automaticamente_en'], unique=False)
    op.create_index(op.f('ix_proveedores_creado_automaticamente_en'), 'proveedores', ['creado_automaticamente_en'], unique=False)
    op.create_index(op.f('ix_proveedores_es_auto_creado'), 'proveedores', ['es_auto_creado'], unique=False)
    op.create_index(op.f('ix_proveedores_nit'), 'proveedores', ['nit'], unique=True)

    op.create_table('cuentas_correo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False, comment='Email corporativo (Microsoft Graph)'),
    sa.Column('nombre_descriptivo', sa.String(length=255), nullable=True, comment="Nombre amigable: 'Angiografía de Colombia'"),
    sa.Column('max_correos_por_ejecucion', sa.Integer(), nullable=False, comment='Límite de seguridad por ejecución (no arbitrario)'),
    sa.Column('ventana_inicial_dias', sa.Integer(), nullable=False, comment='Días hacia atrás en primera ejecución'),
    sa.Column('ultima_ejecucion_exitosa', sa.DateTime(timezone=True), nullable=True, comment='Última ejecución exitosa (para extracción incremental)'),
    sa.Column('fecha_ultimo_correo_procesado', sa.DateTime(timezone=True), nullable=True, comment='Timestamp del último correo procesado'),
    sa.Column('activa', sa.Boolean(), nullable=False, comment='Si está activa para extracción'),
    sa.Column('organizacion', sa.String(length=100), nullable=True, comment="Organización: 'ANGIOGRAFIA', 'AVIDANTI', etc."),
    sa.Column('grupo_id', sa.BigInteger(), nullable=True, comment='Grupo empresarial al que pertenece esta cuenta de correo'),
    sa.Column('creada_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('actualizada_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('creada_por', sa.String(length=100), nullable=False, comment='Usuario que creó la configuración'),
    sa.Column('actualizada_por', sa.String(length=100), nullable=True, comment='Último usuario que modificó'),
    sa.CheckConstraint('max_correos_por_ejecucion > 0 AND max_correos_por_ejecucion <= 100000', name='check_max_correos_range'),
    sa.CheckConstraint('ventana_inicial_dias > 0 AND ventana_inicial_dias <= 365', name='check_ventana_inicial_range'),
    sa.ForeignKeyConstraint(['grupo_id'], ['grupos.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_cuenta_correo_activa_org', 'cuentas_correo', ['activa', 'organizacion'], unique=False)
    op.create_index(op.f('ix_cuentas_correo_activa'), 'cuentas_correo', ['activa'], unique=False)
    op.create_index(op.f('ix_cuentas_correo_email'), 'cuentas_correo', ['email'], unique=True)
    op.create_index(op.f('ix_cuentas_correo_grupo_id'), 'cuentas_correo', ['grupo_id'], unique=False)
    op.create_index(op.f('ix_cuentas_correo_id'), 'cuentas_correo', ['id'], unique=False)
    op.create_index(op.f('ix_cuentas_correo_organizacion'), 'cuentas_correo', ['organizacion'], unique=False)
    op.create_table('patrones_facturas',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('proveedor_id', sa.BigInteger(), nullable=False, comment='FK a proveedor'),
    sa.Column('concepto_normalizado', sa.String(length=200), nullable=False, comment='Concepto normalizado para matching'),
    sa.Column('concepto_hash', sa.String(length=32), nullable=False, comment='Hash MD5 del concepto para búsqueda rápida'),
    sa.Column('tipo_patron', sa.Enum('TIPO_A', 'TIPO_B', 'TIPO_C', name='tipopatron'), nullable=False, comment='Clasificación: TIPO_A (fijo), TIPO_B (fluctuante), TIPO_C (excepcional)'),
    sa.Column('pagos_analizados', sa.Integer(), nullable=False, comment='Cantidad de facturas analizadas'),
    sa.Column('meses_con_pagos', sa.Integer(), nullable=False, comment='Cantidad de meses diferentes con facturas'),
    sa.Column('monto_promedio', sa.Numeric(precision=15, scale=2), nullable=False, comment='Promedio de montos de facturas'),
    sa.Column('monto_minimo', sa.Numeric(precision=15, scale=2), nullable=False, comment='Monto mínimo histórico'),
    sa.Column('monto_maximo', sa.Numeric(precision=15, scale=2), nullable=False, comment='Monto máximo histórico'),
    sa.Column('desviacion_estandar', sa.Numeric(precision=15, scale=2), nullable=False, comment='Desviación estándar de los montos'),
    sa.Column('coeficiente_variacion', sa.Numeric(precision=5, scale=2), nullable=False, comment='CV = (desv_std / promedio) * 100, métrica de estabilidad'),
    sa.Column('rango_inferior', sa.Numeric(precision=15, scale=2), nullable=True, comment='Límite inferior esperado (promedio - 2*desv)'),
    sa.Column('rango_superior', sa.Numeric(precision=15, scale=2), nullable=True, comment='Límite superior esperado (promedio + 2*desv)'),
    sa.Column('frecuencia_detectada', sa.String(length=50), nullable=True, comment='Frecuencia detectada: mensual, quincenal, trimestral, etc.'),
    sa.Column('ultimo_pago_fecha', sa.DateTime(timezone=True), nullable=True, comment='Fecha de la última factura registrada'),
    sa.Column('ultimo_pago_monto', sa.Numeric(precision=15, scale=2), nullable=True, comment='Monto de la última factura'),
    sa.Column('pagos_detalle', sa.JSON(), nullable=True, comment='Array con últimos 12 meses: [{periodo, monto, factura_id}]'),
    sa.Column('fecha_analisis', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True, comment='Cuándo se realizó este análisis'),
    sa.Column('version_algoritmo', sa.String(length=20), server_default='1.0', nullable=False, comment='Versión del algoritmo de análisis'),
    sa.Column('puede_aprobar_auto', sa.Integer(), nullable=False, comment='1 si cumple criterios para aprobación automática, 0 si no'),
    sa.Column('umbral_alerta', sa.Numeric(precision=5, scale=2), nullable=True, comment='Porcentaje de desviación para generar alerta'),
    sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True, comment='Timestamp de creación'),
    sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True, comment='Timestamp de última actualización'),
    sa.ForeignKeyConstraint(['proveedor_id'], ['proveedores.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_patrones_facturas_concepto_hash'), 'patrones_facturas', ['concepto_hash'], unique=False)
    op.create_index(op.f('ix_patrones_facturas_concepto_normalizado'), 'patrones_facturas', ['concepto_normalizado'], unique=False)
    op.create_index(op.f('ix_patrones_facturas_proveedor_id'), 'patrones_facturas', ['proveedor_id'], unique=False)
    op.create_index(op.f('ix_patrones_facturas_tipo_patron'), 'patrones_facturas', ['tipo_patron'], unique=False)
    op.create_table('usuarios',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('usuario', sa.String(length=100), nullable=False),
    sa.Column('nombre', sa.String(length=150), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('area', sa.String(length=100), nullable=True),
    sa.Column('telefono', sa.String(length=50), nullable=True),
    sa.Column('activo', sa.Boolean(), server_default=sa.text('true'), nullable=False),
    sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
    sa.Column('role_id', sa.BigInteger(), nullable=False),
    sa.Column('hashed_password', sa.String(length=255), nullable=True),
    sa.Column('must_change_password', sa.Boolean(), server_default=sa.text('true'), nullable=False),
    sa.Column('auth_provider', sa.String(length=50), server_default=sa.text("'local'"), nullable=False),
    sa.Column('oauth_id', sa.String(length=255), nullable=True),
    sa.Column('oauth_picture', sa.String(length=500), nullable=True),
    sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], onupdate='CASCADE', ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('oauth_id'),
    sa.UniqueConstraint('usuario')
    )
    op.create_table('asignacion_nit_responsable',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('nit', sa.String(length=20), nullable=False, comment='NIT del proveedor'),
    sa.Column('responsable_id', sa.BigInteger(), nullable=False),
    sa.Column('area', sa.String(length=100), nullable=True, comment='Área responsable (TI, Operaciones, etc.)'),
    sa.Column('permitir_aprobacion_automatica', sa.Boolean(), nullable=True, comment='¿Permitir aprobación automática?'),
    sa.Column('requiere_revision_siempre', sa.Boolean(), nullable=True, comment='¿Siempre requiere revisión manual?'),
    sa.Column('monto_maximo_auto_aprobacion', sa.Numeric(precision=15, scale=2), nullable=True, comment='Monto máximo para auto-aprobar'),
    sa.Column('porcentaje_variacion_permitido', sa.Numeric(precision=5, scale=2), nullable=True, comment='% variación permitida para auto-aprobar'),
    sa.Column('emails_notificacion', sa.JSON(), nullable=True, comment='Emails adicionales a notificar'),
    sa.Column('tipo_servicio_proveedor', sa.String(length=50), nullable=True, comment='Clasificación del tipo de servicio para ajustar criterios de aprobación'),
    sa.Column('nivel_confianza_proveedor', sa.String(length=50), nullable=True, comment='Nivel de confianza (1-5) basado en antigüedad e historial'),
    sa.Column('fecha_inicio_relacion', sa.DateTime(), nullable=True, comment='Primera factura registrada del proveedor (para calcular antigüedad)'),
    sa.Column('coeficiente_variacion_historico', sa.Numeric(precision=7, scale=2), nullable=True, comment='CV% de variación de montos históricos'),
    sa.Column('requiere_orden_compra_obligatoria', sa.Boolean(), nullable=True, comment='Si TRUE, facturas sin OC no se auto-aprueban (para servicios por consumo)'),
    sa.Column('metadata_riesgos', sa.JSON(), nullable=True, comment='Metadata de análisis de riesgos: última evaluación, incidentes, etc.'),
    sa.Column('grupo_id', sa.BigInteger(), nullable=True, comment='Grupo específico (NULL = aplica a todos los grupos)'),
    sa.Column('activo', sa.Boolean(), nullable=True),
    sa.Column('creado_en', sa.DateTime(), nullable=True),
    sa.Column('actualizado_en', sa.DateTime(), nullable=True),
    sa.Column('creado_por', sa.String(length=255), nullable=True),
    sa.Column('actualizado_por', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['grupo_id'], ['grupos.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['responsable_id'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nit', 'responsable_id', 'grupo_id', name='uq_nit_responsable_grupo')
    )
    op.create_index('idx_asignacion_grupo', 'asignacion_nit_responsable', ['grupo_id'], unique=False)
    op.create_index('idx_asignacion_nit', 'asignacion_nit_responsable', ['nit'], unique=False)
    op.create_index('idx_asignacion_responsable', 'asignacion_nit_responsable', ['responsable_id'], unique=False)
    op.create_index(op.f('ix_asignacion_nit_responsable_activo'), 'asignacion_nit_responsable', ['activo'], unique=False)
    op.create_index(op.f('ix_asignacion_nit_responsable_grupo_id'), 'asignacion_nit_responsable', ['grupo_id'], unique=False)
    op.create_index(op.f('ix_asignacion_nit_responsable_nit'), 'asignacion_nit_responsable', ['nit'], unique=False)
    op.create_index(op.f('ix_asignacion_nit_responsable_nivel_confianza_proveedor'), 'asignacion_nit_responsable', ['nivel_confianza_proveedor'], unique=False)
    op.create_index(op.f('ix_asignacion_nit_responsable_responsable_id'), 'asignacion_nit_responsable', ['responsable_id'], unique=False)
    op.create_index(op.f('ix_asignacion_nit_responsable_tipo_servicio_proveedor'), 'asignacion_nit_responsable', ['tipo_servicio_proveedor'], unique=False)
    op.create_table('facturas',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('numero_factura', sa.String(length=50), nullable=False),
    sa.Column('fecha_emision', sa.Date(), nullable=False),
    sa.Column('proveedor_id', sa.BigInteger(), nullable=True),
    sa.Column('subtotal', sa.Numeric(precision=15, scale=2), nullable=True),
    sa.Column('iva', sa.Numeric(precision=15, scale=2), nullable=True),
    sa.Column('retenciones', sa.Numeric(precision=15, scale=2), server_default='0.00', nullable=False, comment='Retenciones aplicadas (ReteFuente, ReteIVA, ReteICA, etc.)'),
    sa.Column('pdf_filename', sa.String(length=255), nullable=True, comment='Nombre del archivo PDF (ej: ad08001365050512500067543.pdf) - guardado al extraer'),
    sa.Column('estado', sa.Enum('en_cuarentena', 'en_revision', 'aprobada', 'aprobada_auto', 'rechazada', 'validada_contabilidad', 'devuelta_contabilidad', name='estadofactura'), nullable=False),
    sa.Column('fecha_vencimiento', sa.Date(), nullable=True),
    sa.Column('cufe', sa.String(length=100), nullable=False),
    sa.Column('total_a_pagar', sa.Numeric(precision=15, scale=2), nullable=True),
    sa.Column('responsable_id', sa.BigInteger(), nullable=True),
    sa.Column('grupo_id', sa.BigInteger(), nullable=True, comment='Grupo empresarial al que pertenece la factura'),
    sa.Column('accion_por', sa.String(length=255), nullable=True, comment='Who approved/rejected the factura - synchronized from workflow'),
    sa.Column('estado_asignacion', sa.Enum('sin_asignar', 'asignado', 'huerfano', 'inconsistente', name='estadoasignacion'), nullable=False, comment='PHASE 3: Assignment status - sin_asignar/asignado/huerfano/inconsistente'),
    sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('confianza_automatica', sa.Numeric(precision=3, scale=2), nullable=True, comment='Confianza (0.00-1.00) para aprobación automática'),
    sa.Column('factura_referencia_id', sa.BigInteger(), nullable=True, comment='ID de factura del mes anterior usada como referencia'),
    sa.Column('motivo_decision', sa.String(length=500), nullable=True, comment='Razón de la decisión automática'),
    sa.Column('fecha_procesamiento_auto', sa.DateTime(timezone=True), nullable=True, comment='Cuándo se ejecutó el procesamiento automático'),
    sa.Column('concepto_principal', sa.String(length=500), nullable=True, comment='Descripción/concepto principal de la factura'),
    sa.Column('concepto_hash', sa.String(length=32), nullable=True, comment='Hash MD5 del concepto normalizado para matching rápido'),
    sa.Column('concepto_normalizado', sa.String(length=500), nullable=True, comment='Concepto sin stopwords y normalizado'),
    sa.Column('orden_compra_numero', sa.String(length=50), nullable=True, comment='Número de orden de compra asociada'),
    sa.Column('patron_recurrencia', sa.String(length=20), nullable=True, comment='Patrón: FIJO, VARIABLE, UNICO, DESCONOCIDO'),
    sa.Column('tipo_factura', sa.String(length=20), server_default='COMPRA', nullable=False, comment='Tipo: COMPRA, VENTA, NOTA_CREDITO, NOTA_DEBITO'),
    sa.ForeignKeyConstraint(['factura_referencia_id'], ['facturas.id'], ),
    sa.ForeignKeyConstraint(['grupo_id'], ['grupos.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['proveedor_id'], ['proveedores.id'], ),
    sa.ForeignKeyConstraint(['responsable_id'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cufe'),
    sa.UniqueConstraint('numero_factura', 'proveedor_id', name='uix_num_prov')
    )
    op.create_index(op.f('ix_facturas_accion_por'), 'facturas', ['accion_por'], unique=False)
    op.create_index(op.f('ix_facturas_concepto_hash'), 'facturas', ['concepto_hash'], unique=False)
    op.create_index(op.f('ix_facturas_estado_asignacion'), 'facturas', ['estado_asignacion'], unique=False)
    op.create_index(op.f('ix_facturas_grupo_id'), 'facturas', ['grupo_id'], unique=False)
    op.create_index(op.f('ix_facturas_orden_compra_numero'), 'facturas', ['orden_compra_numero'], unique=False)
    op.create_index(op.f('ix_facturas_pdf_filename'), 'facturas', ['pdf_filename'], unique=False)
    op.create_table('historial_extracciones',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cuenta_correo_id', sa.Integer(), nullable=False),
    sa.Column('fecha_ejecucion', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('correos_procesados', sa.Integer(), nullable=False, comment='Total de correos analizados'),
    sa.Column('facturas_encontradas', sa.Integer(), nullable=False, comment='Facturas XML encontradas'),
    sa.Column('facturas_creadas', sa.Integer(), nullable=False, comment='Nuevas facturas creadas'),
    sa.Column('facturas_actualizadas', sa.Integer(), nullable=False, comment='Facturas actualizadas'),
    sa.Column('facturas_ignoradas', sa.Integer(), nullable=False, comment='Facturas duplicadas/ignoradas'),
    sa.Column('exito', sa.Boolean(), nullable=False),
    sa.Column('mensaje_error', sa.String(length=1000), nullable=True, comment='Mensaje de error si falla'),
    sa.Column('tiempo_ejecucion_ms', sa.Integer(), nullable=True, comment='Tiempo de ejecución en milisegundos'),
    sa.Column('fetch_limit_usado', sa.Integer(), nullable=True),
    sa.Column('fetch_days_usado', sa.Integer(), nullable=True),
    sa.Column('nits_usados', sa.Integer(), nullable=True, comment='Cantidad de NITs activos en la extracción'),
    sa.Column('fecha_desde', sa.DateTime(timezone=True), nullable=True, comment='Fecha desde la cual se extrajeron correos'),
    sa.Column('fecha_hasta', sa.DateTime(timezone=True), nullable=True, comment='Fecha hasta la cual se extrajeron correos'),
    sa.Column('es_primera_ejecucion', sa.Boolean(), nullable=False, comment='Si fue la primera ejecución de esta cuenta'),
    sa.ForeignKeyConstraint(['cuenta_correo_id'], ['cuentas_correo.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_historial_cuenta_fecha', 'historial_extracciones', ['cuenta_correo_id', 'fecha_ejecucion'], unique=False)
    op.create_index('idx_historial_fecha_exito', 'historial_extracciones', ['fecha_ejecucion', 'exito'], unique=False)
    op.create_index(op.f('ix_historial_extracciones_cuenta_correo_id'), 'historial_extracciones', ['cuenta_correo_id'], unique=False)
    op.create_index(op.f('ix_historial_extracciones_fecha_ejecucion'), 'historial_extracciones', ['fecha_ejecucion'], unique=False)
    op.create_index(op.f('ix_historial_extracciones_id'), 'historial_extracciones', ['id'], unique=False)
    op.create_table('nit_configuracion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cuenta_correo_id', sa.Integer(), nullable=False),
    sa.Column('nit', sa.String(length=20), nullable=False, comment='NIT del proveedor/emisor a filtrar'),
    sa.Column('nombre_proveedor', sa.String(length=255), nullable=True, comment='Nombre del proveedor (opcional)'),
    sa.Column('activo', sa.Boolean(), nullable=False, comment='Si este NIT está activo para filtrado'),
    sa.Column('notas', sa.String(length=500), nullable=True, comment='Notas adicionales sobre este NIT'),
    sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('actualizado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('creado_por', sa.String(length=100), nullable=False),
    sa.Column('actualizado_por', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['cuenta_correo_id'], ['cuentas_correo.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cuenta_correo_id', 'nit', name='uq_cuenta_nit')
    )
    op.create_index('idx_nit_activo', 'nit_configuracion', ['nit', 'activo'], unique=False)
    op.create_index(op.f('ix_nit_configuracion_cuenta_correo_id'), 'nit_configuracion', ['cuenta_correo_id'], unique=False)
    op.create_index(op.f('ix_nit_configuracion_id'), 'nit_configuracion', ['id'], unique=False)
    op.create_index(op.f('ix_nit_configuracion_nit'), 'nit_configuracion', ['nit'], unique=False)
    op.create_table('responsable_grupo',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False, comment='Identificador único'),
    sa.Column('responsable_id', sa.BigInteger(), nullable=False, comment='FK a usuarios'),
    sa.Column('grupo_id', sa.BigInteger(), nullable=False, comment='FK a grupos'),
    sa.Column('activo', sa.Boolean(), server_default=sa.text('true'), nullable=False, comment='Flag de pertenencia activa'),
    sa.Column('asignado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='Cuándo se asignó el responsable al grupo'),
    sa.Column('asignado_por', sa.String(length=100), nullable=True, comment='Usuario que asignó (username/email)'),
    sa.Column('actualizado_en', sa.DateTime(timezone=True), nullable=True, comment='Última actualización'),
    sa.Column('actualizado_por', sa.String(length=100), nullable=True, comment='Usuario que actualizó (username/email)'),
    sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='Timestamp de creación (deprecado - usar asignado_en)'),
    sa.ForeignKeyConstraint(['grupo_id'], ['grupos.id'], name='fk_responsable_grupo_grupo'),
    sa.ForeignKeyConstraint(['responsable_id'], ['usuarios.id'], name='fk_responsable_grupo_usuario'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('responsable_id', 'grupo_id', name='uq_responsable_grupo')
    )
    op.create_index('idx_responsable_grupo_grupo', 'responsable_grupo', ['grupo_id'], unique=False)
    op.create_index('idx_responsable_grupo_responsable', 'responsable_grupo', ['responsable_id'], unique=False)
    op.create_index(op.f('ix_responsable_grupo_grupo_id'), 'responsable_grupo', ['grupo_id'], unique=False)
    op.create_index(op.f('ix_responsable_grupo_responsable_id'), 'responsable_grupo', ['responsable_id'], unique=False)
    op.create_table('factura_items',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False, comment='ID único del item'),
    sa.Column('factura_id', sa.BigInteger(), nullable=False, comment='FK a la factura padre'),
    sa.Column('numero_linea', sa.Integer(), nullable=False, comment='Número de línea en el XML (orden)'),
    sa.Column('descripcion', sa.String(length=2000), nullable=False, comment='Descripción completa del item (del XML)'),
    sa.Column('codigo_producto', sa.String(length=100), nullable=True, comment='Código del producto del proveedor'),
    sa.Column('cantidad', sa.Numeric(precision=15, scale=4), nullable=False, comment='Cantidad facturada'),
    sa.Column('unidad_medida', sa.String(length=50), server_default='unidad', nullable=True, comment='Unidad de medida: unidad, kg, litro, hora, etc.'),
    sa.Column('precio_unitario', sa.Numeric(precision=15, scale=4), nullable=False, comment='Precio unitario del item'),
    sa.Column('subtotal', sa.Numeric(precision=15, scale=2), nullable=False, comment='Subtotal del item (cantidad × precio_unitario - descuentos)'),
    sa.Column('total_impuestos', sa.Numeric(precision=15, scale=2), server_default='0', nullable=False, comment='Total de impuestos aplicados al item (IVA, etc.)'),
    sa.Column('total', sa.Numeric(precision=15, scale=2), nullable=False, comment='Total del item (subtotal + impuestos)'),
    sa.Column('descuento_valor', sa.Numeric(precision=15, scale=2), nullable=True, comment='Valor del descuento aplicado'),
    sa.Column('descripcion_normalizada', sa.String(length=500), nullable=True, comment='Descripción normalizada para matching (lowercase, sin acentos, etc.)'),
    sa.Column('item_hash', sa.String(length=32), nullable=True, comment='Hash MD5 de descripcion_normalizada para comparación rápida'),
    sa.Column('categoria', sa.String(length=100), nullable=True, comment='Categoría del item: software, hardware, servicio, consumible, etc.'),
    sa.Column('es_recurrente', sa.Numeric(precision=1, scale=0), server_default=sa.text('0'), nullable=True, comment='1 si el item aparece mensualmente, 0 si es esporádico'),
    sa.Column('creado_en', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='Timestamp de creación'),
    sa.ForeignKeyConstraint(['factura_id'], ['facturas.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_factura_item_linea', 'factura_items', ['factura_id', 'numero_linea'], unique=True)
    op.create_index('idx_item_codigo_producto', 'factura_items', ['codigo_producto', 'factura_id'], unique=False)
    op.create_index('idx_item_descripcion_norm', 'factura_items', ['descripcion_normalizada'], unique=False)
    op.create_index('idx_item_hash_factura', 'factura_items', ['item_hash', 'factura_id'], unique=False)
    op.create_index('idx_item_recurrente_categoria', 'factura_items', ['es_recurrente', 'categoria'], unique=False)
    op.create_index(op.f('ix_factura_items_categoria'), 'factura_items', ['categoria'], unique=False)
    op.create_index(op.f('ix_factura_items_codigo_producto'), 'factura_items', ['codigo_producto'], unique=False)
    op.create_index(op.f('ix_factura_items_descripcion_normalizada'), 'factura_items', ['descripcion_normalizada'], unique=False)
    op.create_index(op.f('ix_factura_items_factura_id'), 'factura_items', ['factura_id'], unique=False)
    op.create_index(op.f('ix_factura_items_item_hash'), 'factura_items', ['item_hash'], unique=False)
    op.create_table('workflow_aprobacion_facturas',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('factura_id', sa.BigInteger(), nullable=False),
    sa.Column('email_id', sa.String(length=255), nullable=True, comment='ID del correo en el servidor'),
    sa.Column('email_asunto', sa.String(length=500), nullable=True, comment='Asunto del correo'),
    sa.Column('email_remitente', sa.String(length=255), nullable=True, comment='Email del remitente'),
    sa.Column('email_fecha_recepcion', sa.DateTime(), nullable=True, comment='Fecha de recepción del correo'),
    sa.Column('email_body_preview', sa.Text(), nullable=True, comment='Preview del cuerpo del correo'),
    sa.Column('estado', sa.Enum('RECIBIDA', 'EN_ANALISIS', 'APROBADA_AUTO', 'PENDIENTE_REVISION', 'EN_REVISION', 'APROBADA_MANUAL', 'RECHAZADA', 'OBSERVADA', 'ENVIADA_CONTABILIDAD', 'PROCESADA', name='estadofacturaworkflow'), nullable=False, comment='Estado actual en el workflow'),
    sa.Column('estado_anterior', sa.Enum('RECIBIDA', 'EN_ANALISIS', 'APROBADA_AUTO', 'PENDIENTE_REVISION', 'EN_REVISION', 'APROBADA_MANUAL', 'RECHAZADA', 'OBSERVADA', 'ENVIADA_CONTABILIDAD', 'PROCESADA', name='estadofacturaworkflow'), nullable=True, comment='Estado previo (para trazabilidad)'),
    sa.Column('fecha_cambio_estado', sa.DateTime(), nullable=True, comment='Última vez que cambió de estado'),
    sa.Column('nit_proveedor', sa.String(length=20), nullable=True, comment='NIT identificado automáticamente'),
    sa.Column('responsable_id', sa.BigInteger(), nullable=True),
    sa.Column('area_responsable', sa.String(length=100), nullable=True, comment='Área del usuario'),
    sa.Column('fecha_asignacion', sa.DateTime(), nullable=True, comment='Cuándo se asignó al usuario'),
    sa.Column('factura_mes_anterior_id', sa.BigInteger(), nullable=True, comment='ID factura del mes anterior'),
    sa.Column('es_identica_mes_anterior', sa.Boolean(), nullable=True, comment='¿Es idéntica a la del mes anterior?'),
    sa.Column('porcentaje_similitud', sa.Numeric(precision=5, scale=2), nullable=True, comment='% de similitud (0-100)'),
    sa.Column('diferencias_detectadas', sa.JSON(), nullable=True, comment='Lista de diferencias encontradas'),
    sa.Column('criterios_comparacion', sa.JSON(), nullable=True, comment="\n    {\n        'monto_igual': true/false,\n        'proveedor_igual': true/false,\n        'concepto_igual': true/false,\n        'fecha_similar': true/false\n    }\n    "),
    sa.Column('tipo_aprobacion', sa.Enum('AUTOMATICA', 'MANUAL', 'MASIVA', 'FORZADA', name='tipoaprobacion'), nullable=True, comment='Tipo de aprobación realizada'),
    sa.Column('aprobada', sa.Boolean(), nullable=True, comment='¿Fue aprobada?'),
    sa.Column('aprobada_por', sa.String(length=255), nullable=True, comment='Usuario que aprobó'),
    sa.Column('fecha_aprobacion', sa.DateTime(), nullable=True, comment='Fecha de aprobación'),
    sa.Column('observaciones_aprobacion', sa.Text(), nullable=True, comment='Observaciones del aprobador'),
    sa.Column('rechazada', sa.Boolean(), nullable=True, comment='¿Fue rechazada?'),
    sa.Column('rechazada_por', sa.String(length=255), nullable=True, comment='Usuario que rechazó'),
    sa.Column('fecha_rechazo', sa.DateTime(), nullable=True, comment='Fecha de rechazo'),
    sa.Column('motivo_rechazo', sa.Enum('MONTO_INCORRECTO', 'SERVICIO_NO_PRESTADO', 'PROVEEDOR_INCORRECTO', 'DUPLICADA', 'SIN_PRESUPUESTO', 'OTRO', name='motivorechazo'), nullable=True),
    sa.Column('detalle_rechazo', sa.Text(), nullable=True, comment='Detalle del rechazo'),
    sa.Column('tiempo_en_analisis', sa.BigInteger(), nullable=True, comment='Segundos en análisis'),
    sa.Column('tiempo_en_revision', sa.BigInteger(), nullable=True, comment='Segundos en revisión'),
    sa.Column('tiempo_total_aprobacion', sa.BigInteger(), nullable=True, comment='Segundos totales hasta aprobación'),
    sa.Column('notificaciones_enviadas', sa.JSON(), nullable=True, comment="\n    [\n        {'tipo': 'factura_recibida', 'fecha': '...', 'destinatarios': [...]}\n    ]\n    "),
    sa.Column('recordatorios_enviados', sa.BigInteger(), nullable=True, comment='Cantidad de recordatorios enviados'),
    sa.Column('metadata_workflow', sa.JSON(), nullable=True, comment='Información adicional del workflow'),
    sa.Column('creado_en', sa.DateTime(), nullable=False),
    sa.Column('actualizado_en', sa.DateTime(), nullable=True),
    sa.Column('creado_por', sa.String(length=255), nullable=True),
    sa.Column('actualizado_por', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['factura_id'], ['facturas.id'], ),
    sa.ForeignKeyConstraint(['factura_mes_anterior_id'], ['facturas.id'], ),
    sa.ForeignKeyConstraint(['responsable_id'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_workflow_estado_fecha', 'workflow_aprobacion_facturas', ['estado', 'fecha_cambio_estado'], unique=False)
    op.create_index('idx_workflow_estado_responsable', 'workflow_aprobacion_facturas', ['estado', 'responsable_id'], unique=False)
    op.create_index('idx_workflow_nit_fecha', 'workflow_aprobacion_facturas', ['nit_proveedor', 'email_fecha_recepcion'], unique=False)
    op.create_index(op.f('ix_workflow_aprobacion_facturas_estado'), 'workflow_aprobacion_facturas', ['estado'], unique=False)
    op.create_index(op.f('ix_workflow_aprobacion_facturas_factura_id'), 'workflow_aprobacion_facturas', ['factura_id'], unique=False)
    op.create_index(op.f('ix_workflow_aprobacion_facturas_nit_proveedor'), 'workflow_aprobacion_facturas', ['nit_proveedor'], unique=False)
    op.create_index(op.f('ix_workflow_aprobacion_facturas_responsable_id'), 'workflow_aprobacion_facturas', ['responsable_id'], unique=False)
    op.create_table('alertas_aprobacion_automatica',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('workflow_id', sa.BigInteger(), nullable=True),
    sa.Column('factura_id', sa.BigInteger(), nullable=False),
    sa.Column('tipo_alerta', sa.String(length=50), nullable=False, comment='Tipo de alerta detectada'),
    sa.Column('severidad', sa.String(length=50), nullable=False, comment='Severidad: BAJA (informativa), MEDIA (revisar diario), ALTA (inmediata), CRITICA (bloquea)'),
    sa.Column('confianza_calculada', sa.Numeric(precision=5, scale=2), nullable=True, comment='Confianza calculada en la decisión'),
    sa.Column('umbral_requerido', sa.Numeric(precision=5, scale=2), nullable=True, comment='Umbral requerido para aprobación'),
    sa.Column('diferencia', sa.Numeric(precision=5, scale=2), nullable=True, comment='Diferencia entre calculada y requerida'),
    sa.Column('valor_detectado', sa.String(length=255), nullable=True, comment='Valor que generó la alerta'),
    sa.Column('valor_esperado', sa.String(length=255), nullable=True, comment='Valor esperado según patrón'),
    sa.Column('requiere_revision_urgente', sa.Boolean(), server_default=sa.text('false'), nullable=False, comment='Si TRUE, requiere revisión inmediata por auditor'),
    sa.Column('revisada', sa.Boolean(), server_default=sa.text('false'), nullable=False, comment='Si TRUE, la alerta ya fue revisada por un humano'),
    sa.Column('revisada_por', sa.String(length=255), nullable=True, comment='Usuario que revisó la alerta'),
    sa.Column('fecha_revision', sa.DateTime(), nullable=True, comment='Cuándo se revisó'),
    sa.Column('accion_tomada', sa.Text(), nullable=True, comment='Descripción de acción tomada tras revisar'),
    sa.Column('metadata_alerta', sa.JSON(), nullable=True, comment='Información adicional: contexto, métricas, recomendaciones'),
    sa.Column('creado_en', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('actualizado_en', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['factura_id'], ['facturas.id'], ),
    sa.ForeignKeyConstraint(['workflow_id'], ['workflow_aprobacion_facturas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_alertas_pendientes', 'alertas_aprobacion_automatica', ['revisada', 'severidad', 'creado_en'], unique=False)
    op.create_index('idx_alertas_tipo_severidad', 'alertas_aprobacion_automatica', ['tipo_alerta', 'severidad'], unique=False)
    op.create_index('idx_alertas_workflow_factura', 'alertas_aprobacion_automatica', ['workflow_id', 'factura_id'], unique=False)
    op.create_index(op.f('ix_alertas_aprobacion_automatica_factura_id'), 'alertas_aprobacion_automatica', ['factura_id'], unique=False)
    op.create_index(op.f('ix_alertas_aprobacion_automatica_revisada'), 'alertas_aprobacion_automatica', ['revisada'], unique=False)
    op.create_index(op.f('ix_alertas_aprobacion_automatica_severidad'), 'alertas_aprobacion_automatica', ['severidad'], unique=False)
    op.create_index(op.f('ix_alertas_aprobacion_automatica_tipo_alerta'), 'alertas_aprobacion_automatica', ['tipo_alerta'], unique=False)
    op.create_index(op.f('ix_alertas_aprobacion_automatica_workflow_id'), 'alertas_aprobacion_automatica', ['workflow_id'], unique=False)
    op.create_table('notificaciones_workflow',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('workflow_id', sa.BigInteger(), nullable=False),
    sa.Column('tipo', sa.Enum('FACTURA_RECIBIDA', 'PENDIENTE_REVISION', 'FACTURA_APROBADA', 'APROBACION_AUTOMATICA', 'FACTURA_RECHAZADA', 'RECORDATORIO', 'ALERTA', name='tiponotificacion'), nullable=False),
    sa.Column('destinatarios', sa.JSON(), nullable=False, comment='Lista de emails destinatarios'),
    sa.Column('asunto', sa.String(length=500), nullable=True),
    sa.Column('cuerpo', sa.Text(), nullable=True),
    sa.Column('enviada', sa.Boolean(), nullable=True),
    sa.Column('fecha_envio', sa.DateTime(), nullable=True),
    sa.Column('proveedor_email', sa.String(length=100), nullable=True, comment='Gmail, Outlook, SendGrid, etc.'),
    sa.Column('abierta', sa.Boolean(), nullable=True),
    sa.Column('fecha_apertura', sa.DateTime(), nullable=True),
    sa.Column('respondida', sa.Boolean(), nullable=True),
    sa.Column('fecha_respuesta', sa.DateTime(), nullable=True),
    sa.Column('error', sa.Text(), nullable=True),
    sa.Column('intentos_envio', sa.BigInteger(), nullable=True),
    sa.Column('creado_en', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['workflow_id'], ['workflow_aprobacion_facturas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_notif_workflow_tipo', 'notificaciones_workflow', ['workflow_id', 'tipo'], unique=False)
    op.create_index(op.f('ix_notificaciones_workflow_enviada'), 'notificaciones_workflow', ['enviada'], unique=False)
    op.create_index(op.f('ix_notificaciones_workflow_tipo'), 'notificaciones_workflow', ['tipo'], unique=False)
    op.create_index(op.f('ix_notificaciones_workflow_workflow_id'), 'notificaciones_workflow', ['workflow_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_notificaciones_workflow_workflow_id'), table_name='notificaciones_workflow')
    op.drop_index(op.f('ix_notificaciones_workflow_tipo'), table_name='notificaciones_workflow')
    op.drop_index(op.f('ix_notificaciones_workflow_enviada'), table_name='notificaciones_workflow')
    op.drop_index('idx_notif_workflow_tipo', table_name='notificaciones_workflow')
    op.drop_table('notificaciones_workflow')
    op.drop_index(op.f('ix_alertas_aprobacion_automatica_workflow_id'), table_name='alertas_aprobacion_automatica')
    op.drop_index(op.f('ix_alertas_aprobacion_automatica_tipo_alerta'), table_name='alertas_aprobacion_automatica')
    op.drop_index(op.f('ix_alertas_aprobacion_automatica_severidad'), table_name='alertas_aprobacion_automatica')
    op.drop_index(op.f('ix_alertas_aprobacion_automatica_revisada'), table_name='alertas_aprobacion_automatica')
    op.drop_index(op.f('ix_alertas_aprobacion_automatica_factura_id'), table_name='alertas_aprobacion_automatica')
    op.drop_index('idx_alertas_workflow_factura', table_name='alertas_aprobacion_automatica')
    op.drop_index('idx_alertas_tipo_severidad', table_name='alertas_aprobacion_automatica')
    op.drop_index('idx_alertas_pendientes', table_name='alertas_aprobacion_automatica')
    op.drop_table('alertas_aprobacion_automatica')
    op.drop_index(op.f('ix_workflow_aprobacion_facturas_responsable_id'), table_name='workflow_aprobacion_facturas')
    op.drop_index(op.f('ix_workflow_aprobacion_facturas_nit_proveedor'), table_name='workflow_aprobacion_facturas')
    op.drop_index(op.f('ix_workflow_aprobacion_facturas_factura_id'), table_name='workflow_aprobacion_facturas')
    op.drop_index(op.f('ix_workflow_aprobacion_facturas_estado'), table_name='workflow_aprobacion_facturas')
    op.drop_index('idx_workflow_nit_fecha', table_name='workflow_aprobacion_facturas')
    op.drop_index('idx_workflow_estado_responsable', table_name='workflow_aprobacion_facturas')
    op.drop_index('idx_workflow_estado_fecha', table_name='workflow_aprobacion_facturas')
    op.drop_table('workflow_aprobacion_facturas')
    op.drop_index(op.f('ix_factura_items_item_hash'), table_name='factura_items')
    op.drop_index(op.f('ix_factura_items_factura_id'), table_name='factura_items')
    op.drop_index(op.f('ix_factura_items_descripcion_normalizada'), table_name='factura_items')
    op.drop_index(op.f('ix_factura_items_codigo_producto'), table_name='factura_items')
    op.drop_index(op.f('ix_factura_items_categoria'), table_name='factura_items')
    op.drop_index('idx_item_recurrente_categoria', table_name='factura_items')
    op.drop_index('idx_item_hash_factura', table_name='factura_items')
    op.drop_index('idx_item_descripcion_norm', table_name='factura_items')
    op.drop_index('idx_item_codigo_producto', table_name='factura_items')
    op.drop_index('idx_factura_item_linea', table_name='factura_items')
    op.drop_table('factura_items')
    op.drop_index(op.f('ix_responsable_grupo_responsable_id'), table_name='responsable_grupo')
    op.drop_index(op.f('ix_responsable_grupo_grupo_id'), table_name='responsable_grupo')
    op.drop_index('idx_responsable_grupo_responsable', table_name='responsable_grupo')
    op.drop_index('idx_responsable_grupo_grupo', table_name='responsable_grupo')
    op.drop_table('responsable_grupo')
    op.drop_index(op.f('ix_nit_configuracion_nit'), table_name='nit_configuracion')
    op.drop_index(op.f('ix_nit_configuracion_id'), table_name='nit_configuracion')
    op.drop_index(op.f('ix_nit_configuracion_cuenta_correo_id'), table_name='nit_configuracion')
    op.drop_index('idx_nit_activo', table_name='nit_configuracion')
    op.drop_table('nit_configuracion')
    op.drop_index(op.f('ix_historial_extracciones_id'), table_name='historial_extracciones')
    op.drop_index(op.f('ix_historial_extracciones_fecha_ejecucion'), table_name='historial_extracciones')
    op.drop_index(op.f('ix_historial_extracciones_cuenta_correo_id'), table_name='historial_extracciones')
    op.drop_index('idx_historial_fecha_exito', table_name='historial_extracciones')
    op.drop_index('idx_historial_cuenta_fecha', table_name='historial_extracciones')
    op.drop_table('historial_extracciones')
    op.drop_index(op.f('ix_facturas_pdf_filename'), table_name='facturas')
    op.drop_index(op.f('ix_facturas_orden_compra_numero'), table_name='facturas')
    op.drop_index(op.f('ix_facturas_grupo_id'), table_name='facturas')
    op.drop_index(op.f('ix_facturas_estado_asignacion'), table_name='facturas')
    op.drop_index(op.f('ix_facturas_concepto_hash'), table_name='facturas')
    op.drop_index(op.f('ix_facturas_accion_por'), table_name='facturas')
    op.drop_table('facturas')
    op.drop_index(op.f('ix_asignacion_nit_responsable_tipo_servicio_proveedor'), table_name='asignacion_nit_responsable')
    op.drop_index(op.f('ix_asignacion_nit_responsable_responsable_id'), table_name='asignacion_nit_responsable')
    op.drop_index(op.f('ix_asignacion_nit_responsable_nivel_confianza_proveedor'), table_name='asignacion_nit_responsable')
    op.drop_index(op.f('ix_asignacion_nit_responsable_nit'), table_name='asignacion_nit_responsable')
    op.drop_index(op.f('ix_asignacion_nit_responsable_grupo_id'), table_name='asignacion_nit_responsable')
    op.drop_index(op.f('ix_asignacion_nit_responsable_activo'), table_name='asignacion_nit_responsable')
    op.drop_index('idx_asignacion_responsable', table_name='asignacion_nit_responsable')
    op.drop_index('idx_asignacion_nit', table_name='asignacion_nit_responsable')
    op.drop_index('idx_asignacion_grupo', table_name='asignacion_nit_responsable')
    op.drop_table('asignacion_nit_responsable')
    op.drop_table('usuarios')
    op.drop_index(op.f('ix_patrones_facturas_tipo_patron'), table_name='patrones_facturas')
    op.drop_index(op.f('ix_patrones_facturas_proveedor_id'), table_name='patrones_facturas')
    op.drop_index(op.f('ix_patrones_facturas_concepto_normalizado'), table_name='patrones_facturas')
    op.drop_index(op.f('ix_patrones_facturas_concepto_hash'), table_name='patrones_facturas')
    op.drop_table('patrones_facturas')
    op.drop_index(op.f('ix_cuentas_correo_organizacion'), table_name='cuentas_correo')
    op.drop_index(op.f('ix_cuentas_correo_id'), table_name='cuentas_correo')
    op.drop_index(op.f('ix_cuentas_correo_grupo_id'), table_name='cuentas_correo')
    op.drop_index(op.f('ix_cuentas_correo_email'), table_name='cuentas_correo')
    op.drop_index(op.f('ix_cuentas_correo_activa'), table_name='cuentas_correo')
    op.drop_index('idx_cuenta_correo_activa_org', table_name='cuentas_correo')
    op.drop_table('cuentas_correo')
    op.drop_table('roles')
    op.drop_index(op.f('ix_proveedores_nit'), table_name='proveedores')
    op.drop_index(op.f('ix_proveedores_es_auto_creado'), table_name='proveedores')
    op.drop_index(op.f('ix_proveedores_creado_automaticamente_en'), table_name='proveedores')
    op.drop_index('idx_proveedor_auto_creado_fecha', table_name='proveedores')
    op.drop_table('proveedores')
    op.drop_index(op.f('ix_grupos_ruta_jerarquica'), table_name='grupos')
    op.drop_index(op.f('ix_grupos_nombre'), table_name='grupos')
    op.drop_index(op.f('ix_grupos_grupo_padre_id'), table_name='grupos')
    op.drop_index(op.f('ix_grupos_eliminado'), table_name='grupos')
    op.drop_index(op.f('ix_grupos_codigo_corto'), table_name='grupos')
    op.drop_index(op.f('ix_grupos_activo'), table_name='grupos')
    op.drop_index('idx_grupo_ruta', table_name='grupos')
    op.drop_index('idx_grupo_padre', table_name='grupos')
    op.drop_index('idx_grupo_codigo', table_name='grupos')
    op.drop_index('idx_grupo_activo_eliminado', table_name='grupos')
    op.drop_table('grupos')
    op.drop_table('audit_log')
    # ### end Alembic commands ###
