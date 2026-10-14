
import re


def is_valid_email(email):
    """Vérifie qu'une adresse email possède un format valide."""
    if not isinstance(email, str) or not email:
        return False

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return bool(re.fullmatch(pattern, email))


def is_valid_password(password):
    """Vérifie les règles de sécurité d'un mot de passe."""
    errors = []

    if not isinstance(password, str):
        password = ""

    if len(password) < 8:
        errors.append("Minimum 8 caractères")

    if not re.search(r"[A-Z]", password):
        errors.append("Majuscule manquante")

    if not re.search(r"[a-z]", password):
        errors.append("Minuscule manquante")

    if not re.search(r"[0-9]", password):
        errors.append("Chiffre manquant")

    if not re.search(r"[!@#$%^&*]", password):
        errors.append("Caractère spécial manquant")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
    }


def is_valid_age(age):
    """Vérifie que l'âge est un entier compris entre 0 et 150."""
    return type(age) is int and 0 <= age <= 150
