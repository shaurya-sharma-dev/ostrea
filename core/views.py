"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from django.shortcuts import render
from .models import OysterLog, Oyster

# Create your views here.
def index(request):
    return render(request, "core/index.html")

def dashboard(request):
    return render(
        request, 
        "core/dashboard.html", 
        context={
            "logs": [[oyster.name, *OysterLog.objects.filter(oyster=oyster)] for oyster in Oyster.objects.all()]
        }
    )