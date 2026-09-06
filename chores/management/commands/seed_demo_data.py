from django.core.management.base import BaseCommand

from chores.models import Chore, ChoreRotation, Household, Person

DEMO_DATA = [
    {
        "household": "Smith Family",
        "people": ["Alice", "Ben", "Cara"],
        "chores": {
            "Dishes": ["Alice", "Ben", "Cara"],
            "Trash": ["Ben", "Cara"],
            "Vacuuming": ["Alice", "Cara"],
        },
    },
    {
        "household": "Elm St Roommates",
        "people": ["Dana", "Eli", "Farah", "Gus"],
        "chores": {
            "Kitchen cleanup": ["Dana", "Eli", "Farah", "Gus"],
            "Bathroom cleaning": ["Eli", "Gus"],
        },
    },
]


class Command(BaseCommand):
    help = "Creates example households, people, and chores for local testing."

    def handle(self, *args, **options):
        for entry in DEMO_DATA:
            household, created = Household.objects.get_or_create(
                name=entry["household"]
            )
            if not created:
                self.stdout.write(
                    f'Skipping "{household.name}": already exists.'
                )
                continue

            people_by_name = {
                name: Person.objects.create(name=name, household=household)
                for name in entry["people"]
            }

            for chore_name, rotation_names in entry["chores"].items():
                chore = Chore.objects.create(name=chore_name, household=household)
                for order, name in enumerate(rotation_names, start=1):
                    ChoreRotation.objects.create(
                        chore=chore, person=people_by_name[name], order=order
                    )

            self.stdout.write(self.style.SUCCESS(f'Created "{household.name}".'))
