from django.contrib import admin
from diagnostic.models import Diagnostic

from disease.models import Disease
from drug.models import Drug
from effect.models import Effect

# Register your models here.
admin.site.register([Disease, Drug, Effect, Diagnostic])
