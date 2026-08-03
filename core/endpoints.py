"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from . import schemas, models
from ninja import Router
from ninja.errors import HttpError

oyster_router = Router(tags=["Oysters"])

@oyster_router.get("/get", response=schemas.OysterOut)
def get_oyster(request, token: str):
    try:
        return models.Oyster.objects.get(token=token)
    except models.Oyster.DoesNotExist:
        raise HttpError(404, f"Oyster with token '{token}' not found.")

core_router = Router()
core_router.add_router("/oyster", oyster_router)