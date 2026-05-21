from src.domain.exceptions import DomainValidationError

VALID_STATUSES = {"pendiente", "en_transito", "entregado", "cancelado"}

class InvalidDeliveryError(DomainValidationError):
    """Hereda de DomainValidationError."""
    pass

class Delivery:
    def __init__(
        self,
        id: str,
        package_id: str,
        client_id: str,
        direccion_destino: str,
        estado: str,
        fecha_entrega_estimada: str,
        notas: str = ""
    ):
        self.id = id
        self.package_id = package_id
        self.client_id = client_id
        self.direccion_destino = direccion_destino
        self.estado = estado
        self.fecha_entrega_estimada = fecha_entrega_estimada
        self.notas = notas
        self.validar()

    def validar(self):
        """Valida que las reglas del negocio de entregas se cumplan."""
        if not self.id.strip():
            raise InvalidDeliveryError("El ID de la entrega no puede estar vacío.")

        if not self.package_id.strip():
            raise InvalidDeliveryError("El ID del paquete no puede estar vacío.")

        if not self.client_id.strip():
            raise InvalidDeliveryError("El ID del cliente no puede estar vacío.")

        if len(self.direccion_destino.strip()) < 5:
            raise InvalidDeliveryError("La dirección de destino es demasiado corta. Pon una dirección real.")

        if self.estado not in VALID_STATUSES:
            raise InvalidDeliveryError(
                f"El estado '{self.estado}' no es válido. "
                f"Los estados permitidos son: {', '.join(VALID_STATUSES)}."
            )

        if not self.fecha_entrega_estimada.strip():
            raise InvalidDeliveryError("La fecha de entrega estimada no puede estar vacía.")

    def update_info(
        self,
        direccion_destino: str,
        estado: str,
        fecha_entrega_estimada: str,
        notas: str = ""
    ):
        """Método de dominio para actualizar los datos respetando las validaciones."""
        self.direccion_destino = direccion_destino
        self.estado = estado
        self.fecha_entrega_estimada = fecha_entrega_estimada
        self.notas = notas
        self.validar()
