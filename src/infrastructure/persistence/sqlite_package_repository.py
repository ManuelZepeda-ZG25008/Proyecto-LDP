from typing import List, Optional

from src.domain.entities.package import Package
from src.domain.repositories.package_repository import PackageRepository

from src.infrastructure.persistence.sqlite_connection import get_db_connection


class SQLitePackageRepository(PackageRepository):

    def save(self, package: Package) -> None:

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO packages (
                id,
                descripcion,
                peso,
                destinatario_id,
                direccion_entrega,
                estado
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            package.id,
            package.descripcion,
            package.peso,
            package.destinatario_id,
            package.direccion_entrega,
            package.estado
        ))

        conn.commit()
        conn.close()

    def get_by_id(self, package_id: str) -> Optional[Package]:

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM packages WHERE id = ?",
            (package_id,)
        )

        row = cursor.fetchone()
        conn.close()

        if row:
            return Package(*row)

        return None

    def get_all(self) -> List[Package]:

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM packages")

        rows = cursor.fetchall()
        conn.close()

        return [Package(*row) for row in rows]

    def delete(self, package_id: str) -> None:

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM packages WHERE id = ?",
            (package_id,)
        )

        conn.commit()
        conn.close()