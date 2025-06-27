class LivreIndisponibleError(Exception):
    def __init__(self, message="Le livre est déjà emprunté !"):
        super().__init__(message)

class QuotaEmpruntDepasseError(Exception):
    def __init__(self, message="Le nombre maximal d'emprunt dépassé !"):
        super().__init__(message)

class MembreInexistantError(Exception):
    def __init__(self, message="Le membre demandé n'existe pas !"):
        super().__init__(message)

class LivreInexistantError(Exception):
    def __init__(self, message="Le livre demandé n'existe pas !"):
        super().__init__(message)

