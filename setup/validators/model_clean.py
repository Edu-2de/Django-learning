from django.core.exceptions import ValidationError


def full_clean_all(objects):
    exclude = {}
    errors = {}

    for prefix, object in objects.items():
        try:
            object.full_clean(exclude=exclude.items())
        except ValidationError as exception:
            for field, messages in exception.message_dict.items():
                key = f"{prefix}.{field}" if prefix else field
                errors[key] = messages

    if errors:
        raise ValidationError(errors)
