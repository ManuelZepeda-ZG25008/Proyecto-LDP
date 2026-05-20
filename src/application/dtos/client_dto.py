from pydantic import BaseModel, Field

class ClientCreateDTO(BaseModel):
    id: str = Field(..., description="ID único o documento de identidad del cliente")
    nombre: str = Field(..., description="Nombre del cliente")
    apellido: str = Field(..., description="Apellido del cliente")
    email: str = Field(..., description="Correo electrónico de contacto")
    telefono: str = Field(..., description="Número de teléfono (mínimo 8 dígitos)")
    direccion: str = Field(..., description="Dirección de residencia o entrega")

class ClientUpdateDTO(BaseModel):
    nombre: str
    apellido: str
    email: str
    telefono: str
    direccion: str

class ClientResponseDTO(BaseModel):
    id: str
    nombre: str
    apellido: str
    email: str
    telefono: str
    direccion: str

    class Config:
        from_attributes = True