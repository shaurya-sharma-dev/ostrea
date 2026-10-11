"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from ninja import NinjaAPI
from core.endpoints import core_router
from django.conf import settings

api = NinjaAPI(
    title="Ostrea API",
    description="The API for the Ostrea web application.",
    urls_namespace="api",
    docs_url="/docs" if settings.DEBUG else None,
    openapi_url="/openapi.json" if settings.DEBUG else None,
)

api.add_router("/", core_router)