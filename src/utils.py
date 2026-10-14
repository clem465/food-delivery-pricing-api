
import re
import unicodedata


def capitalize(text):
    if text is None or text == "":
        return ""

    return text[0].upper() + text[1:].lower()


def calculate_average(numbers):
    if not numbers:
        return 0

    return round(sum(numbers) / len(numbers), 2)


def slugify(text):
    if not text:
        return ""

    text = unicodedata.normalize("NFKD", text)
    text = "".join(
        char for char in text
        if not unicodedata.combining(char)
    )

    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s-]+", "-", text)

    return text.strip("-")


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


def sort_students(students, sort_by, order="asc"):
    """
    Trie les étudiants par name, grade ou age.

    Retourne un nouveau tableau sans modifier l'original.
    """
    if not students:
        return []

    if sort_by not in ("name", "grade", "age"):
        raise ValueError("Critère de tri invalide")

    if order not in ("asc", "desc"):
        raise ValueError("Ordre de tri invalide")

    reverse = order == "desc"

    return sorted(
        students,
        key=lambda student: student[sort_by],
        reverse=reverse,
    )

