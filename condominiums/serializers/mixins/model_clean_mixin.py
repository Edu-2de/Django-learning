from copy import copy

from setup.validators.model_clean import full_clean_all


class ModelCleanMixin:
    def validate(self, attrs):
        attrs = super().validate(attrs)
        model = self.Meta.model

        if self.instance is None:
            instance = model(**attrs)
        else:
            instance = copy(self.instance)
            for name, value in attrs.items():
                setattr(instance, name, value)

        writable = {name for name, f in self.fields.items() if not f.read_only}
        exclude = [f.name for f in model._meta.fields if f.name not in writable]

        full_clean_all({"": instance}, exclude={"": exclude})

        return attrs
