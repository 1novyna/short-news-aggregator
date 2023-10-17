from django.db.models import TextField
import json


class EmbeddingField(TextField):
    def from_db_value(self, value, expression, connection):
        if value:
            return json.loads(value)

    def get_prep_value(self, value):
        if value:
            return json.dumps(value)
