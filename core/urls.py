"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('games/oyster-anatomy/', views.oyster_anatomy_memory_game, name="oyster_anatomy_memory_game"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('', views.index, name="home"),
]