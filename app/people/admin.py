from django.contrib import admin

from app.people.models import *


class PersonAdmin(admin.ModelAdmin):
    search_fields = ['family_name', 'other_names']


admin.site.register(Person, PersonAdmin)
admin.site.register(Organisation)
admin.site.register(Rank)
admin.site.register(ServiceNumber)
admin.site.register(Birth)
admin.site.register(Death)
admin.site.register(LifeEvent)
admin.site.register(AlternativePersonName)
admin.site.register(EventLocation)
admin.site.register(Repository)
admin.site.register(PersonAssociation)
admin.site.register(SourceAssociation)
admin.site.register(PersonOrgAssociation)
admin.site.register(LifeEventType)
