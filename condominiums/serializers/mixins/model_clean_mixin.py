from copy import copy


class ModelCleanMixin:
    def validate(self, attrs):
        attrs = super().validate(attrs)
        model = self.Meta.model

        if self.instace is None:
            instance = model(**attrs)
        else:
            instance = copy(self.instance)
            for name, value in attrs.items():
                setattr(instance, name, value)

        writable = {name for name, f in self.fields.items() if not f.read_only}
