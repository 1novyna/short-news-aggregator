from django.contrib import admin
from ast import literal_eval


def bool_filter_factory(parameter_name, **kwargs):
    body = {
        "parameter_name": parameter_name,
    }
    body.update(kwargs)
    list_filter = type("BoolFilter", (GeneralBooleanListFilter,), body)

    return list_filter


class GeneralBooleanListFilter(admin.SimpleListFilter):
    def get_parameter_name(self):
        parameter = self.parameter_name
        if self.filter_lookup:
            parameter += "__" + self.filter_lookup
        return parameter

    def lookups(self, *args, **kwargs):
        return [
            (True, "True"),
            (False, "False"),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(**{self.get_parameter_name(): literal_eval(value)})
        return queryset
