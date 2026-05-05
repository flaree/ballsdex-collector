from typing import Self

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.manager import Manager


class CollectorType(models.Model):
    name = models.CharField(max_length=64, unique=True)
    min = models.IntegerField(
        default=250,
        help_text="Minimum ball count required (applied at rarity_min)",
    )
    max = models.IntegerField(
        default=3500,
        help_text="Maximum ball count required (applied at rarity_max)",
    )
    gap = models.IntegerField(
        default=50,
        help_text="Rounding step applied to the interpolated count requirement",
    )
    rarity_min = models.FloatField(
        default=0.05,
        help_text="Ball rarity value that maps to the minimum count requirement",
    )
    rarity_max = models.FloatField(
        default=0.80,
        help_text="Ball rarity value that maps to the maximum count requirement",
    )
    source_special = models.ForeignKey(
        "bd_models.Special",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="collector_source_types",
        help_text="Only count balls with this special towards the requirement (null = count all balls)",
    )
    enabled = models.BooleanField(default=True)

    objects: Manager[Self] = Manager()

    class Meta:
        managed = True
        db_table = "collectortype"

    def __str__(self) -> str:
        return self.name

    def clean(self) -> None:
        if self.min >= self.max:
            raise ValidationError("min must be less than max")
        if self.gap <= 0:
            raise ValidationError("gap must be a positive integer")
        if self.rarity_min >= self.rarity_max:
            raise ValidationError("rarity_min must be less than rarity_max")

    def required_count(self, rarity: float) -> int:
        """Calculate how many balls the player must own to claim or maintain this type.

        The result is rounded to the nearest ``gap``.
        """
        x1, y1 = self.rarity_min, float(self.min)
        x2, y2 = self.rarity_max, float(self.max)
        raw = y1 + (rarity - x1) * (y2 - y1) / (x2 - x1)
        clamped = min(float(self.max), max(float(self.min), raw))
        return int(round(clamped / self.gap)) * self.gap
