from django.contrib import admin
from QlChungCu.models import Box, Acount, AcountAdmin, Car_card, Goods, People, Letters, Bill


class AcountAdminSet(admin.ModelAdmin):
    fields = ['name_acount', 'pass_acount', 'avatar_acount', 'admin']
    search_fields = ['id', 'name']

    #
    # def role_acount(self, Acount):
    #     if Acount.role_acount:
    #         exclude = ['admin']


admin.site.register(AcountAdmin)
admin.site.register(Box)
admin.site.register(Acount)
admin.site.register(Car_card)
admin.site.register(Goods)
admin.site.register(People)
admin.site.register(Letters)
admin.site.register(Bill)
admin.site.register(Acount, AcountAdminSet)

