"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import OysterLog, Oyster

# Create your views here.
guest_only = user_passes_test(lambda u: not u.is_authenticated, login_url="dashboard", redirect_field_name=None)

@guest_only
def index(request):
    return render(request, "core/index.html")

@login_required(login_url="account_login")
def dashboard(request):
    return render(
        request, 
        "core/dashboard.html", 
        context={
            "logs": [[oyster.name, *OysterLog.objects.filter(oyster=oyster)] for oyster in Oyster.objects.all()]
        }
    )