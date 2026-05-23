from pydantic import BaseModel, Field


class PackageCreateDTO(BaseModel):
    id: str = Field(..., description="ID único del paquete")
    descripcion: str
    peso: float
    destinatario_id: str
    direccion_entrega: str


class PackageUpdateDTO(BaseModel):
    descripcion: str
    peso: float
    direccion_entrega: str
    estado: str


class PackageResponseDTO(BaseModel):
    id: str
    descripcion: str
    peso: float
    destinatario_id: str
    direccion_entrega: str
    estado: str

    class Config:
        from_attributes = True