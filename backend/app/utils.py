import secrets
import string

def generate_giftcard_code() -> str:
    alphabet = string.ascii_uppercase + string.digits
    parts = [
        ''.join(secrets.choice(alphabet) for _ in range(4))
        for _ in range(3)
    ]
    return "GC-" + "-".join(parts)
