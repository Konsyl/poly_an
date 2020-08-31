from django.contrib import admin
from polygon_rest.models import Dot
from polygon_rest.models import Rectangle, FRectangle
# Register your models here.
admin.site.register(Dot)
admin.site.register(Rectangle)
admin.site.register(FRectangle)
