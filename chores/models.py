from django.db import models


class Household(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=100)
    household = models.ForeignKey(
        Household, on_delete=models.CASCADE, related_name="people"
    )

    def __str__(self):
        return self.name


class Chore(models.Model):
    name = models.CharField(max_length=100)
    household = models.ForeignKey(
        Household, on_delete=models.CASCADE, related_name="chores"
    )
    people = models.ManyToManyField(
        Person, through="ChoreRotation", related_name="chores"
    )

    def __str__(self):
        return self.name


class ChoreRotation(models.Model):
    """Defines the rotation order of people through a chore."""

    chore = models.ForeignKey(
        Chore, on_delete=models.CASCADE, related_name="rotations"
    )
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]
        unique_together = ("chore", "order")

    def __str__(self):
        return f"{self.chore} -> {self.person} (#{self.order})"


class ChoreAssignment(models.Model):
    STATUS_PENDING = "pending"
    STATUS_DONE = "done"
    STATUS_INCOMPLETE = "incomplete"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_DONE, "Done"),
        (STATUS_INCOMPLETE, "Incomplete"),
    ]

    chore = models.ForeignKey(
        Chore, on_delete=models.CASCADE, related_name="assignments"
    )
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="assignments"
    )
    period_start = models.DateField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-period_start"]
        unique_together = ("chore", "period_start")

    def __str__(self):
        return f"{self.chore} - {self.person} ({self.period_start})"
