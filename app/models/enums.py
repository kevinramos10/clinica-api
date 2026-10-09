from enum import Enum

class SexoPersona(Enum):
    M = 'M'
    F = 'F'

class EstadoMedico(Enum):
    Activo = "Activo"
    Inactivo = "Inactivo"
    De_Vacaciones = "De Vacaciones"

class EstadoCita(Enum):
    Confirmada = "Confirmada"
    Atendida = "Atendida"
    Cancelada = "Cancelada"

class RolUsuario(Enum):
    Admin = "Admin"
    Recepcionista = "Recepcionista"
    Medico = "Medico"

class EstadoUsuario(Enum):
    Activo = "Activo"
    Inactivo = "Inactivo"