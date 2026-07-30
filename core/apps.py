"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from django.apps import AppConfig
from django.utils.autoreload import autoreload_started
from django.conf import settings

class CoreConfig(AppConfig):
    name = 'core'
    verbose_name = 'Ostrea'

    def ready(self):
        def watch_custom_files(sender, **kwargs):
            sender.extra_files.add(settings.BASE_DIR / '.env')

        autoreload_started.connect(watch_custom_files)