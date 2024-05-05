from django.contrib import admin
from QlChungCu.models import Box, Acount, AcountAdmin, People, Car_card
from QlChungCu.views import PeopleViewSet
from django.utils.html import mark_safe

class AcountSet(admin.ModelAdmin):
    # list_display = ['id','name_acount',  'updated_date']
    search_fields = ['id', 'name']
    list_filter = ['id', 'name_acount', 'updated_date']

    # readonly_fields = ['avatar_acount']
    def my_acount(self, acount):
        if acount.avatar_acount:
            return mark_safe(f"< img width='200' src='/static/{acount.avatar_acount.name}' />")


admin.site.register(AcountAdmin)
admin.site.register(Acount, AcountSet)
admin.site.register(Box)
admin.site.register(People)
admin.site.register(Car_card)
