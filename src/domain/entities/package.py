from src.domain.exceptions import DomainValidationError

class InvalidPackageError(DomainValidationError):
    pass


class Package:
    def __init__(
        self,
        id: str,
        descripcion: str,
        peso: float,
        destinatario_id: str,
        direccion_entrega: str,
        estado: str = "Pendiente"
    ):
        self.id = id
        self.descripcion = descripcion
        self.peso = peso
        self.destinatario_id = destinatario_id
        self.direccion_entrega = direccion_entrega
        self.estado = estado

        self.validar()

    def validar(self):

        if not self.id.strip():
            raise InvalidPackageError("El ID del paquete no puede venir vacío.")

        if not self.descripcion.strip():
            raise InvalidPackageError("La descripción del paquete es obligatoria.")

        if self.peso <= 0:
            raise InvalidPackageError("El peso del paquete debe ser mayor a cero.")

        if not self.destinatario_id.strip():
            raise InvalidPackageError("El destinatario es obligatorio.")

        if len(self.direccion_entrega.strip()) < 5:
            raise InvalidPackageError("La dirección de entrega es inválida.")

        estados_validos = [
            "Pendiente",
            "En tránsito",
            "Entregado",
            "Cancelado"
        ]

        if self.estado not in estados_validos:
            raise InvalidPackageError(
                f"Estado inválido. Estados válidos: {estados_validos}"
            )

    def update_info(
        self,
        descripcion: str,
        peso: float,
        direccion_entrega: str,
        estado: str
    ):
        self.descripcion = descripcion
        self.peso = peso
        self.direccion_entrega = direccion_entrega
        self.estado = estado

        self.validar()