import random
import string

def generate_redeem_code():
    """Generate a unique 10-character redeem code."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

if __name__ == "__main__":
    print("Generated Code:", generate_redeem_code())