"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from functools import wraps
from django.views.decorators.clickjacking import xframe_options_sameorigin

def no_csrf(view_func):
    """Marks a view as CSRF-exempt and deletes the CSRF token cookie from the user's browser.
    The token is regenerated if they go back to a view without this decorator or the `csrf_exempt` decorator,
    like the admin panel or allauth views.
    
    For security, this decorator CANNOT be applied on views that modify server-side data (like allauth or admin 
    views). However, it can be applied on views like `index` or `dashboard` because those views do not interact 
    with server-side data, and using `request.user` in templates for conditional navbar elements is perfectly 
    safe."""

    exempt_view = csrf_exempt(view_func)
    
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        response = exempt_view(request, *args, **kwargs)
        
        response.delete_cookie(
            settings.CSRF_COOKIE_NAME,
            path=settings.CSRF_COOKIE_PATH,
            domain=settings.CSRF_COOKIE_DOMAIN,
        )
        return response
        
    return _wrapped_view

# Create your views here.
@no_csrf
def index(request):
    return render(request, "core/index.html")

@no_csrf
def dashboard(request):
    return render(request, "core/dashboard.html")

@no_csrf
@xframe_options_sameorigin
def interactive_lifecycle_timeline(request):
    return render(request, "core/games/lifecycle-timeline.html")

@no_csrf
@xframe_options_sameorigin
def anatomy_chatbot(request):
    return render(request, "core/games/anatomy-chatbot.html")

@no_csrf
@xframe_options_sameorigin
def habitat_survival(request):
    return render(request, "core/games/habitat-survival.html")

@no_csrf
@xframe_options_sameorigin
def chesapeake_food_web(request):
    return render(request, "core/games/chesapeake-food-web.html")

@no_csrf
@xframe_options_sameorigin
def bay_game(request):
    return render(request, "core/games/bay-game.html")

@no_csrf
@xframe_options_sameorigin
def history_game(request):
    return render(request, "core/games/history-game.html")

@no_csrf
@xframe_options_sameorigin
def oyster_garden(request):
    return render(request, "core/games/oyster-garden.html")

@no_csrf
@xframe_options_sameorigin
def restoration_game(request):
    return render(request, "core/games/restoration-game.html")

@no_csrf
@xframe_options_sameorigin
def oyster_science_flashcards(request):
    return render(request, "core/games/oyster-sci-flashcards.html")

@no_csrf
@xframe_options_sameorigin
def cause_effect(request):
    return render(request, "core/games/cause-effect.html")