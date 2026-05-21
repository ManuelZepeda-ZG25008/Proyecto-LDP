from pydantic import BaseModel, Field

class DeliveryCreateDTO(BaseModel):
    id: str = Field(..., description="ID único de la entrega")
    package_id: str = Field(..., description="ID del paquete asociado a esta entrega")
    client_id: str = Field(..., description="ID del cliente destinatario")
    direccion_destino: str = Field(..., description="Dirección física de destino de la entrega")
    estado: str = Field(..., description="Estado actual: pendiente, en_transito, entregado, cancelado")
    fecha_entrega_estimada: str = Field(..., description="Fecha estimada de entrega (ej: 2025-12-31)")
    notas: str = Field(default="", description="Notas adicionales opcionales para el repartidor")

class DeliveryUpdateDTO(BaseModel):
    direccion_destino: str
    estado: str
    fecha_entrega_estimada: str
    notas: str = ""

class DeliveryResponseDTO(BaseModel):
    id: str
    package_id: str
    client_id: str
    direccion_destino: str
    estado: str
    fecha_entrega_estimada: str
    notas: str

    class Config:
        from_attributes = True
