class CPF:
    def __init__(self, value: str):
        if len(value) != 11 or not value.isdigit():
            raise ValueError("CPF must contain exactly 11 digits and be numeric.")
        self.value = value

    def __str__(self):
        return self.value
