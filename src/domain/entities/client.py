from src.domain.exceptions import DomainValidationError

class InvalidClientError(DomainValidationError):
    """Hereda de DomainValidationError."""
    pass

class Client:
    def __init__(self, id: str, nombre: str, apellido: str, email: str, telefono: str, direccion: str):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.direccion = direccion
        self.validar()

    def validar(self):
        """Valida que las reglas del negocio de paquetería se cumplan."""
        if not self.nombre.strip():
            raise InvalidClientError("El nombre del cliente no puede estar vacío.")
            
        if not self.apellido.strip():
            raise InvalidClientError("El apellido del cliente no puede estar vacío.")

        if "@" not in self.email or "." not in self.email:
            raise InvalidClientError(f"El email '{self.email}' no tiene un formato válido.")

        if len(self.telefono.strip().replace("-", "")) < 8:
            raise InvalidClientError("El teléfono debe tener al menos 8 dígitos numéricos.")

        if len(self.direccion.strip()) < 5:
            raise InvalidClientError("La dirección es demasiado corta. Poné una dirección real.")
            
    def update_info(self, nombre: str, apellido: str, email: str, telefono: str, direccion: str):
        """Método de dominio para actualizar los datos respetando las validaciones."""
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.direccion = direccion
        self.validar()