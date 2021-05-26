import string
import random


def random_string_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def generate_unique_reference_per_model(model, size=5):
    reference_number = random_string_generator(size=size)

    Klass = model

    qs_exists = Klass.objects.filter(
        order_reference=reference_number).exists()
    if qs_exists:
        return generate_unique_reference_per_model(model, size=size)
    return reference_number
