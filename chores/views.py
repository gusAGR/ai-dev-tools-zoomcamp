from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Chore, ChoreAssignment, ChoreRotation, Household, Person


def dashboard(request):
    all_assignments = (
        ChoreAssignment.objects.select_related("chore", "person", "chore__household")
        .order_by("chore_id", "-period_start")
    )

    current_by_chore = {}
    for assignment in all_assignments:
        current_by_chore.setdefault(assignment.chore_id, assignment)

    assignments = sorted(
        current_by_chore.values(),
        key=lambda a: (a.chore.household.name, a.chore.name),
    )
    return render(request, "chores/dashboard.html", {"assignments": assignments})


def mark_done(request, assignment_id):
    assignment = get_object_or_404(ChoreAssignment, pk=assignment_id)
    if request.method == "POST":
        assignment.status = ChoreAssignment.STATUS_DONE
        assignment.completed_at = timezone.now()
        assignment.save()
        messages.success(request, f'Marked "{assignment.chore.name}" as done.')
    return redirect("dashboard")


def household_list(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        if name:
            Household.objects.create(name=name)
            messages.success(request, f'Household "{name}" created.')
        return redirect("household_list")

    households = Household.objects.all().order_by("name")
    return render(request, "chores/household_list.html", {"households": households})


def household_detail(request, household_id):
    household = get_object_or_404(Household, pk=household_id)

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        if name:
            Person.objects.create(name=name, household=household)
            messages.success(request, f'Added "{name}" to {household.name}.')
        return redirect("household_detail", household_id=household.id)

    people = household.people.order_by("name")
    return render(
        request,
        "chores/household_detail.html",
        {"household": household, "people": people},
    )


def person_delete(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    household_id = person.household_id
    if request.method == "POST":
        person.delete()
        messages.success(request, f'Removed "{person.name}".')
    return redirect("household_detail", household_id=household_id)


def chore_list(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        household_id = request.POST.get("household")
        household = get_object_or_404(Household, pk=household_id) if household_id else None
        if name and household:
            Chore.objects.create(name=name, household=household)
            messages.success(request, f'Chore "{name}" created.')
        return redirect("chore_list")

    chores = Chore.objects.select_related("household").order_by(
        "household__name", "name"
    )
    households = Household.objects.order_by("name")
    return render(
        request,
        "chores/chore_list.html",
        {"chores": chores, "households": households},
    )


def chore_detail(request, chore_id):
    chore = get_object_or_404(Chore, pk=chore_id)

    if request.method == "POST":
        person_id = request.POST.get("person")
        person = get_object_or_404(Person, pk=person_id, household=chore.household)
        next_order = (
            chore.rotations.order_by("-order").values_list("order", flat=True).first()
            or 0
        ) + 1
        ChoreRotation.objects.create(chore=chore, person=person, order=next_order)
        messages.success(request, f'Added "{person.name}" to the rotation.')
        return redirect("chore_detail", chore_id=chore.id)

    rotations = chore.rotations.select_related("person").order_by("order")
    eligible_people = chore.household.people.exclude(
        id__in=rotations.values_list("person_id", flat=True)
    ).order_by("name")
    return render(
        request,
        "chores/chore_detail.html",
        {"chore": chore, "rotations": rotations, "eligible_people": eligible_people},
    )


def chore_delete(request, chore_id):
    chore = get_object_or_404(Chore, pk=chore_id)
    if request.method == "POST":
        chore.delete()
        messages.success(request, f'Deleted chore "{chore.name}".')
    return redirect("chore_list")


def rotation_delete(request, rotation_id):
    rotation = get_object_or_404(ChoreRotation, pk=rotation_id)
    chore_id = rotation.chore_id
    if request.method == "POST":
        rotation.delete()
        messages.success(request, "Removed from rotation.")
    return redirect("chore_detail", chore_id=chore_id)
