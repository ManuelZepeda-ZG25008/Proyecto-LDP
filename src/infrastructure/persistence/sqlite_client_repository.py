from typing import List, Optional
from src.domain.entities.client import Client
from src.domain.repositories.client_repository import ClientRepository
from src.infrastructure.persistence.sqlite_connection import get_db_connection

class SQLiteClientRepository(ClientRepository):
    """Implementación real del repositorio usando SQLite y SQL puro."""

    def save(self, client: Client) -> None:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO clients (id, nombre, apellido, email, telefono, direccion)
            VALUES (?, ?, ?, ?, ?, ?);
        """, (client.id, client.nombre, client.apellido, client.email, client.telefono, client.direccion))
        
        conn.commit()
        conn.close()

    def get_by_id(self, client_id: str) -> Optional[Client]:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM clients WHERE id = ?;", (client_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
            
        return Client(
            id=row["id"],
            nombre=row["nombre"],
            apellido=row["apellido"],
            email=row["email"],
            telefono=row["telefono"],
            direccion=row["direccion"]
        )

    def get_all(self) -> List[Client]:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM clients;")
        rows = cursor.fetchall()
        conn.close()
        
        return [
            Client(
                id=row["id"],
                nombre=row["nombre"],
                apellido=row["apellido"],
                email=row["email"],
                telefono=row["telefono"],
                direccion=row["direccion"]
            ) for row in rows
        ]

    def delete(self, client_id: str) -> None:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM clients WHERE id = ?;", (client_id,))
        
        conn.commit()
        conn.close()