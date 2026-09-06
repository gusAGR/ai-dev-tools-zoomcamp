from django.contrib import admin

from .models import Chore, ChoreAssignment, ChoreRotation, Household, Person


@admin.register(Household)
class HouseholdAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("name", "household")
    list_filter = ("household",)


class ChoreRotationInline(admin.TabularInline):
    model = ChoreRotation
    extra = 1


@admin.register(Chore)
class ChoreAdmin(admin.ModelAdmin):
    list_display = ("name", "household")
    list_filter = ("household",)
    inlines = [ChoreRotationInline]


@admin.register(ChoreAssignment)
class ChoreAssignmentAdmin(admin.ModelAdmin):
    list_display = ("chore", "person", "period_start", "status", "completed_at")
    list_filter = ("status", "chore__household")
