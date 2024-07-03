from rest_framework.exceptions import ValidationError


class ValidateURLResource:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        url = value.get(self.field)
        if url and not url.startswith("https://www.youtube.com/"):
            raise ValidationError("Cторонние видео запрещены")
