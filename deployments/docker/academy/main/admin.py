from django.contrib import admin
from .models import (Feature,
                     Questions,
                     Notification,
                    )

# Register your models here.

admin.site.register(Feature)
admin.site.register(Questions)
admin.site.register(Notification)
