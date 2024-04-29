from django.contrib import admin
from QlChungCu.models import Box, Acount, AcountAdmin


class AcountAdminSet(admin.ModelAdmin):
    fields = ['name_acount', 'pass_acount', 'avatar_acount', 'role_acount', 'admin']
    ssearch_fields = ['id', 'name']

    #
    # def role_acount(self, Acount):
    #     if Acount.role_acount:
    #         exclude = ['admin']


admin.site.register(AcountAdmin)
admin.site.register(Acount, AcountAdminSet)
admin.site.register(Box)
