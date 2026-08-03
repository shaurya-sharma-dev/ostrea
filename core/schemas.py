"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from . import models
from ninja import ModelSchema, Schema, Field
from enum import Enum

class ErrorCodeEnum(str, Enum):
    "Enum class for API errors."

    OYSTER_NOT_FOUND = "OYSTER_NOT_FOUND"

class ErrorResponse(Schema):
    "Schema for error messages."

    # The Enum automatically documents all allowed error codes in Swagger
    code: ErrorCodeEnum = Field(..., description="The unique system error identifier.")

    message: str = Field(..., description="Human-readable reason for the failure.")

class OysterLogOut(ModelSchema):
    "Schema for OysterLog output."

    class Meta:
        model = models.OysterLog
        fields = ["date", "ph_level", "field_logs"]

class OysterOut(ModelSchema):
    "Schema for Oyster output to use when the API is outputting an Oyster's data."

    oysterlog_set: list[OysterLogOut]

    class Meta:
        model = models.Oyster
        fields = ["name", "site_name", "site_location", "deployment_date", "notes"]

    @staticmethod
    def resolve_oysterlog_set(oyster: models.Oyster):
        return list(oyster.oysterlog_set.all())