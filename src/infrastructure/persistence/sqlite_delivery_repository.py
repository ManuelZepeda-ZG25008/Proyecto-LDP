from typing import List, Optional
from src.domain.entities.delivery import Delivery
from src.domain.repositories.delivery_repository import DeliveryRepository
from src.infrastructure.persistence.sqlite_connection import get_db_connection

class SQLiteDeliveryRepository(DeliveryRepository):
    """Implementación real del repositorio de Entregas usando SQLite y SQL puro"""

    def save(self, delivery: Delivery) -> None:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO deliveries
                (id, package_id, client_id, direccion_destino, estado, fecha_entrega_estimada, notas)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (
            delivery.id,
            delivery.package_id,
            delivery.client_id,
            delivery.direccion_destino,
            delivery.estado,
            delivery.fecha_entrega_estimada,
            delivery.notas
        ))
        conn.commit()
        conn.close()

    def get_by_id(self, delivery_id: str) -> Optional[Delivery]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM deliveries WHERE id = ?;", (delivery_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        return Delivery(
            id=row["id"],
            package_id=row["package_id"],
            client_id=row["client_id"],
            direccion_destino=row["direccion_destino"],
            estado=row["estado"],
            fecha_entrega_estimada=row["fecha_entrega_estimada"],
            notas=row["notas"]
        )

    def get_all(self) -> List[Delivery]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM deliveries;")
        rows = cursor.fetchall()
        conn.close()

        return [
            Delivery(
                id=row["id"],
                package_id=row["package_id"],
                client_id=row["client_id"],
                direccion_destino=row["direccion_destino"],
                estado=row["estado"],
                fecha_entrega_estimada=row["fecha_entrega_estimada"],
                notas=row["notas"]
            ) for row in rows
        ]

    def delete(self, delivery_id: str) -> None:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM deliveries WHERE id = ?;", (delivery_id,))
        conn.commit()
        conn.close()
