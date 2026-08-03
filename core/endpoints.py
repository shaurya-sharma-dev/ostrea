"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from . import schemas, models
from ninja import Router

oyster_router = Router(tags=["Oysters"])

@oyster_router.get("/get", response=
    {
        200: schemas.OysterOut,
        404: schemas.ErrorResponse,
    }
)
def get_oyster(request, token: str):
    try:
        return 200, models.Oyster.objects.get(token=token)
    except models.Oyster.DoesNotExist:
        return 404, {
            "message": f"Oyster with token '{token}' not found.", 
            "code": schemas.ErrorCodeEnum.OYSTER_NOT_FOUND
        }

core_router = Router()
core_router.add_router("/oyster", oyster_router)