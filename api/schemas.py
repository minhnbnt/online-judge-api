from ninja import ModelSchema

from .models import Problem


class ProblemDescSchema(ModelSchema):
    class Meta:
        model = Problem
        fields = ["title", "description"]


class ProblemSchema(ModelSchema):
    class Meta:
        model = Problem
        fields = ["id", "idDisplay", "title"]
