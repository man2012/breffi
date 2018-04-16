from django.core.exceptions import ValidationError
import re

def validate_file_extension(value):
    if not value.name.endswith('.json'):
        raise ValidationError(u'Error: Json files only.')

def validate_phone(value):
    if re.findall(r"^(\+?\(?[0-9]{3,4}\)?[ .-]?[0-9]{3}[ .-]?[0-9]{4})$", value) == []:
        raise ValidationError(u'Error: Incorrect format phone')

def validate_email(value):
    if re.findall(r"^\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b$", value,  re.IGNORECASE) == []:
        raise ValidationError(u'Error: Incorrect format email')
