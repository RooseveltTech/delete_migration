import secrets
import string


def generate_game_id():
    from main.models import GameTicket
    alphabet = string.ascii_letters + string.digits
    loop_condition = True
    while loop_condition:
        game_id = "".join(secrets.choice(alphabet) for i in range(8))
        if (
            any(c.isupper() for c in game_id)
            and any(c.isupper() for c in game_id)
            and sum(c.isdigit() for c in game_id) >= 6
        ):
            loop_condition = False
    
    if GameTicket.objects.filter(game_id=game_id).exists():
        generate_game_id()

    return game_id

def generate_slip_id():
    from main.models import GameTicket
    alphabet = string.ascii_letters + string.digits
    loop_condition = True
    while loop_condition:
        slip_id = "".join(secrets.choice(alphabet) for i in range(8))
        if (
            any(c.isupper() for c in slip_id)
            and any(c.isupper() for c in slip_id)
            and sum(c.isdigit() for c in slip_id) >= 6
        ):
            loop_condition = False
    
    if GameTicket.objects.filter(slip_id=slip_id).exists():
        generate_slip_id()

    return slip_id

def generate_game_pin():
    from main.models import GameTicket
    alphabet = string.ascii_letters + string.digits
    loop_condition = True
    while loop_condition:
        game_pin = "".join(secrets.choice(alphabet) for i in range(8))
        if (
            any(c.isupper() for c in game_pin)
            and any(c.isupper() for c in game_pin)
            and sum(c.isdigit() for c in game_pin) >= 6
        ):
            loop_condition = False
    
    if GameTicket.objects.filter(game_pin=game_pin).exists():
        generate_game_pin()

    return game_pin

def generate_password():
    alphabet = string.ascii_letters + string.digits
    loop_condition = True
    while loop_condition:
        password = "".join(secrets.choice(alphabet) for i in range(8))
        if (
            any(c.isupper() for c in password)
            and any(c.isupper() for c in password)
            and sum(c.isdigit() for c in password) >= 6
        ):
            loop_condition = False

    return password

def generate_otp():
    alphabet = string.digits
    loop_condition = True
    while loop_condition:
        otp_code = "".join(secrets.choice(alphabet) for i in range(6))
        if (
            sum(c.isdigit() for c in otp_code) >= 4
        ):
            loop_condition = False

    return otp_code

def get_ip_address(request):
    address = request.META.get('HTTP_X_FORWARDED_FOR')
    if address:
        ip_addr = address.split(',')[-1].strip()
    else:
        ip_addr = request.META.get('REMOTE_ADDR')
    return ip_addr