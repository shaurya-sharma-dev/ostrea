"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from ninja import NinjaAPI
from . import __version__
from core.endpoints import core_router

api = NinjaAPI(
    title="Ostrea API", 
    version=__version__, 
    description="The API for the Ostrea web application.",
    urls_namespace="api",
)

api.add_router("/", core_router)