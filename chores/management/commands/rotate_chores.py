from django.core.management.base import BaseCommand
from django.utils import timezone

from chores.models import Chore, ChoreAssignment


class Command(BaseCommand):
    help = (
        "Flags any pending assignment from the previous period as incomplete, "
        "then advances every chore to the next person in its rotation for the "
        "current period."
    )

    def handle(self, *args, **options):
        today = timezone.localdate()
        created = 0
        flagged = 0

        for chore in Chore.objects.prefetch_related("rotations__person"):
            rotation = list(chore.rotations.order_by("order"))
            if not rotation:
                self.stdout.write(
                    self.style.WARNING(f'Skipping "{chore}": no one in rotation.')
                )
                continue

            last_assignment = chore.assignments.order_by("-period_start").first()
            next_index = 0

            if last_assignment:
                if last_assignment.period_start == today:
                    self.stdout.write(f'Skipping "{chore}": already assigned today.')
                    continue

                if last_assignment.status == ChoreAssignment.STATUS_PENDING:
                    last_assignment.status = ChoreAssignment.STATUS_INCOMPLETE
                    last_assignment.save(update_fields=["status"])
                    flagged += 1

                order_by_person = {r.person_id: r.order for r in rotation}
                last_order = order_by_person.get(last_assignment.person_id)
                if last_order is not None:
                    orders = [r.order for r in rotation]
                    next_index = (orders.index(last_order) + 1) % len(rotation)

            next_person = rotation[next_index].person
            ChoreAssignment.objects.create(
                chore=chore, person=next_person, period_start=today
            )
            created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {created} assignment(s); flagged {flagged} as incomplete."
            )
        )
