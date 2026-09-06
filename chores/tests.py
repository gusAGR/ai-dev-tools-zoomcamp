from datetime import timedelta

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Chore, ChoreAssignment, ChoreRotation, Household, Person


class ChoreRotationTests(TestCase):
    def setUp(self):
        self.household = Household.objects.create(name="Test House")
        self.alice = Person.objects.create(name="Alice", household=self.household)
        self.bob = Person.objects.create(name="Bob", household=self.household)
        self.chore = Chore.objects.create(name="Dishes", household=self.household)
        ChoreRotation.objects.create(chore=self.chore, person=self.alice, order=1)
        ChoreRotation.objects.create(chore=self.chore, person=self.bob, order=2)

    def test_rotate_chores_creates_first_assignment(self):
        call_command("rotate_chores")

        self.assertEqual(ChoreAssignment.objects.count(), 1)
        assignment = ChoreAssignment.objects.first()
        self.assertEqual(assignment.person, self.alice)
        self.assertEqual(assignment.status, ChoreAssignment.STATUS_PENDING)

    def test_rotate_chores_advances_to_next_person(self):
        call_command("rotate_chores")
        first = ChoreAssignment.objects.first()
        first.period_start -= timedelta(days=7)
        first.save()

        call_command("rotate_chores")

        self.assertEqual(ChoreAssignment.objects.count(), 2)
        latest = ChoreAssignment.objects.order_by("-period_start").first()
        self.assertEqual(latest.person, self.bob)

    def test_rotate_chores_flags_stale_pending_as_incomplete(self):
        call_command("rotate_chores")
        first = ChoreAssignment.objects.first()
        first.period_start -= timedelta(days=7)
        first.save()

        call_command("rotate_chores")

        first.refresh_from_db()
        self.assertEqual(first.status, ChoreAssignment.STATUS_INCOMPLETE)

    def test_rotate_chores_skips_chore_with_empty_rotation(self):
        empty_chore = Chore.objects.create(name="Laundry", household=self.household)

        call_command("rotate_chores")

        self.assertFalse(
            ChoreAssignment.objects.filter(chore=empty_chore).exists()
        )

    def test_rotate_chores_is_idempotent_within_same_period(self):
        call_command("rotate_chores")
        call_command("rotate_chores")

        self.assertEqual(ChoreAssignment.objects.count(), 1)


class MarkDoneViewTests(TestCase):
    def setUp(self):
        household = Household.objects.create(name="Test House")
        self.alice = Person.objects.create(name="Alice", household=household)
        self.chore = Chore.objects.create(name="Dishes", household=household)
        self.assignment = ChoreAssignment.objects.create(
            chore=self.chore, person=self.alice, period_start=timezone.localdate()
        )

    def test_mark_done_updates_status_and_timestamp(self):
        response = self.client.post(
            reverse("mark_done", args=[self.assignment.id])
        )

        self.assertRedirects(response, reverse("dashboard"))
        self.assignment.refresh_from_db()
        self.assertEqual(self.assignment.status, ChoreAssignment.STATUS_DONE)
        self.assertIsNotNone(self.assignment.completed_at)

    def test_mark_done_requires_post(self):
        response = self.client.get(
            reverse("mark_done", args=[self.assignment.id])
        )

        self.assignment.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.assignment.status, ChoreAssignment.STATUS_PENDING)


class HouseholdManagementViewTests(TestCase):
    def test_create_household(self):
        response = self.client.post(reverse("household_list"), {"name": "New House"})

        self.assertRedirects(response, reverse("household_list"))
        self.assertTrue(Household.objects.filter(name="New House").exists())

    def test_add_and_remove_person(self):
        household = Household.objects.create(name="Test House")

        self.client.post(
            reverse("household_detail", args=[household.id]), {"name": "Alice"}
        )
        person = Person.objects.get(name="Alice", household=household)
        self.assertEqual(household.people.count(), 1)

        self.client.post(reverse("person_delete", args=[person.id]))
        self.assertEqual(household.people.count(), 0)


class ChoreManagementViewTests(TestCase):
    def setUp(self):
        self.household = Household.objects.create(name="Test House")
        self.alice = Person.objects.create(name="Alice", household=self.household)

    def test_create_chore(self):
        response = self.client.post(
            reverse("chore_list"),
            {"name": "Dishes", "household": self.household.id},
        )

        self.assertRedirects(response, reverse("chore_list"))
        self.assertTrue(Chore.objects.filter(name="Dishes").exists())

    def test_add_and_remove_rotation_entry(self):
        chore = Chore.objects.create(name="Dishes", household=self.household)

        self.client.post(
            reverse("chore_detail", args=[chore.id]), {"person": self.alice.id}
        )
        rotation = ChoreRotation.objects.get(chore=chore, person=self.alice)
        self.assertEqual(chore.rotations.count(), 1)

        self.client.post(reverse("rotation_delete", args=[rotation.id]))
        self.assertEqual(chore.rotations.count(), 0)
