
import re
import unicodedata
from decimal import Decimal, InvalidOperation


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

def parse_price(value):
    """Convertit un prix en nombre ou retourne None."""
    if isinstance(value, bool) or value is None:
        return None

    if isinstance(value, (int, float, Decimal)):
        try:
            price = Decimal(str(value))
        except InvalidOperation:
            return None
    elif isinstance(value, str):
        text = value.strip().lower()

        if text == "gratuit":
            return 0

        text = text.replace("€", "").strip()
        text = text.replace(",", ".")

        if not re.fullmatch(r"\d+(\.\d+)?", text):
            return None

        price = Decimal(text)
    else:
        return None

    if not price.is_finite() or price < 0:
        return None

    return float(price)


def group_by(array, key):
    """Regroupe des dictionnaires selon une clé."""
    if array is None:
        return {}

    if not isinstance(array, list):
        raise ValueError("Le paramètre doit être une liste")

    groups = {}

    for item in array:
        if not isinstance(item, dict):
            raise ValueError("Chaque élément doit être un dictionnaire")

        value = item.get(key)

        try:
            groups.setdefault(value, []).append(item)
        except TypeError as exc:
            raise ValueError("Clé de regroupement non hashable") from exc

    return groups


def calculate_discount(price, discount_rules):
    """Applique des réductions cumulatives dans l'ordre."""
    if (
        isinstance(price, bool)
        or not isinstance(price, (int, float))
        or not 0 <= price < float("inf")
    ):
        raise ValueError("Prix invalide")

    if not isinstance(discount_rules, list):
        raise ValueError("Règles invalides")

    total = Decimal(str(price))

    for rule in discount_rules:
        if not isinstance(rule, dict):
            raise ValueError("Règle invalide")

        rule_type = rule.get("type")

        if rule_type in ("percentage", "fixed"):
            value = rule.get("value")

            if (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
                or not 0 <= value < float("inf")
            ):
                raise ValueError("Réduction invalide")

            value = Decimal(str(value))

            if rule_type == "percentage":
                if value > 100:
                    raise ValueError("Pourcentage supérieur à 100")
                total *= 1 - value / 100
            else:
                total -= value

        elif rule_type == "buyXgetY":
            buy = rule.get("buy")
            free = rule.get("free")
            item_price = rule.get("itemPrice")

            if (
                type(buy) is not int
                or type(free) is not int
                or buy <= 0
                or free <= 0
                or isinstance(item_price, bool)
                or not isinstance(item_price, (int, float))
                or not 0 < item_price < float("inf")
            ):
                raise ValueError("Offre buyXgetY invalide")

            unit_price = Decimal(str(item_price))
            quantity = int(total // unit_price)
            groups = quantity // (buy + free)
            total -= groups * free * unit_price

        else:
            raise ValueError("Type de réduction inconnu")

        total = max(Decimal("0"), total)

    return float(round(total, 2))
