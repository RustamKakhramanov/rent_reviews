


class HasAttributes:
    def set_attributes(self, data: dict):
        for key, value in data.items():
            if (hasattr(self, key)):
                setattr(self, key, value)