class MyCustomError(Exception):
    def __init__(self, message):
        super().__init__(message)

def do_something(value):
    if value < 0:
        raise MyCustomError("Der Wert kann nicht negativ sein!")
    print("Wert ist gültig:", value)

try:
    do_something(-1)
except MyCustomError as e:
    print(f"Benutzerdefinierte Ausnahme aufgetreten: {e}")
