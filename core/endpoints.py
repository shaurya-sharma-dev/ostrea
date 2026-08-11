"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from . import schemas, models
from ninja import Router

oyster_router = Router(tags=["Oysters"])
lessons_router = Router(tags=["Lessons"])

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

@lessons_router.get("/get-all-units", response=
    {
        200: list[schemas.UnitOut],
    }
)
def get_all_units(request):
    return 200, models.Unit.objects.all()

@lessons_router.get("/get-lessons-in-unit", response=
    {
        200: list[schemas.LessonOut],
    }
)
def get_lessons_in_unit(request, unit_id: int):
    return 200, models.Lesson.objects.filter(unit__id=unit_id)

core_router = Router()
core_router.add_router("/lessons", lessons_router)
core_router.add_router("/oyster", oyster_router)