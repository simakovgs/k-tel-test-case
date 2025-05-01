import re
from rest_framework.exceptions import ValidationError

def validate_sn(sn: str, snm: str) -> None:
    if len(sn) != len(snm):
        raise ValidationError({
            'serial_number': f'Длина серийного номера должна быть {len(snm)} символов'
        })

    regex_pattern = []
    for i, char in enumerate(snm):
        if char == 'N':
            regex_pattern.append('[0-9]')
        elif char == 'A':
            regex_pattern.append('[A-Z]')
        elif char == 'a':
            regex_pattern.append('[a-z]')
        elif char == 'X':
            regex_pattern.append('[A-Z0-9]')
        elif char == 'Z':
            regex_pattern.append('[-_@]')
        else:
            raise ValidationError({
                'serial_number_mask': f'Недопустимый {i} символ в маске {snm}: {char}'
            })

    full_pattern = '^' + ''.join(regex_pattern) + '$'

    if not re.match(full_pattern, sn):
        raise ValidationError({
            'serial_number': 'Серийный номер не соответствует заданной маске'
        })