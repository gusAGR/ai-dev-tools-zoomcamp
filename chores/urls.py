from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("assignments/<int:assignment_id>/done/", views.mark_done, name="mark_done"),
    path("households/", views.household_list, name="household_list"),
    path(
        "households/<int:household_id>/",
        views.household_detail,
        name="household_detail",
    ),
    path("people/<int:person_id>/delete/", views.person_delete, name="person_delete"),
    path("chores/", views.chore_list, name="chore_list"),
    path("chores/<int:chore_id>/", views.chore_detail, name="chore_detail"),
    path("chores/<int:chore_id>/delete/", views.chore_delete, name="chore_delete"),
    path(
        "rotations/<int:rotation_id>/delete/",
        views.rotation_delete,
        name="rotation_delete",
    ),
]
