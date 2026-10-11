"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('games/lifecycle-timeline/', views.interactive_lifecycle_timeline, name="interactive_lifecycle_timeline"),
    path('games/anatomy-chatbot/', views.anatomy_chatbot, name="anatomy_chatbot"),
    path('games/chesapeake-food-web/', views.chesapeake_food_web, name="chesapeake_food_web"),
    path('games/habitat-survival/', views.habitat_survival, name="habitat_survival"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('', views.index, name="home"),
]