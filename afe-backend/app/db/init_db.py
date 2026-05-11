# app/db/init_db.py
from sqlalchemy.orm import Session
from app.models.role import Role
from app.models.usuario import Usuario
from app.core.security import hash_password
from app.utils.logger import logger


def create_default_roles_and_admin(db: Session):
    # === Verificar roles (deben ser creados por migraciones) ===
    roles_esperados = {"superadmin", "admin", "responsable", "contador", "viewer"}
    roles_existentes = {r.nombre for r in db.query(Role).all()}
    
    missing = roles_esperados - roles_existentes
    if missing:
        logger.warning("FALTAN ROLES CRÍTICOS EN DB (deberían estar en migraciones): %s", missing)
    else:
        logger.info("Verificación de roles: OK")


    # === Crear usuario SUPER ADMIN si no existe ===
    super_admin = db.query(Usuario).filter(Usuario.usuario == "super.admin").first()
    if not super_admin:
        # Verificar si el email ya existe
        email_exists = db.query(Usuario).filter(Usuario.email == "afe.sa01@outlook.es").first()
        if email_exists:
            logger.info("Email afe.sa01@outlook.es ya está asociado a otro usuario, saltando creación de super admin")
        else:
            # buscar el rol admin
            admin_role = db.query(Role).filter(Role.nombre == "admin").first()

            super_admin = Usuario(
                usuario="super.admin",
                nombre="Super Admin",
                email="afe.sa01@outlook.es",
                hashed_password=hash_password("Prueba1234"),
                activo=True,
                role_id=admin_role.id if admin_role else None,
                must_change_password=True  # <-- mejora para seguridad
            )
            db.add(super_admin)
            db.commit()
            db.refresh(super_admin)
            logger.info("Super Admin creado: %s", super_admin.usuario)
    else:
        logger.info("Super Admin ya existe: %s", super_admin.usuario)
