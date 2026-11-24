
from django.db import models


class Vehicle(models.Model):

    VEHICLE_TYPES = [
        ('TWO_WHEELER', 'Two Wheeler'),
        ('CAR', 'Car'),
        ('TRUCK', 'Truck'),
        ('OTHER', 'Other'),
    ]

    vehicle_number = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES)
    owner_name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.vehicle_number


class VehicleEntry(models.Model):

    PURPOSE_CHOICES = [
        ('MATERIAL_DELIVERY', 'Material Delivery'),
        ('PICKUP', 'Pickup'),
        ('VISITOR', 'Visitor'),
        ('OTHER', 'Other'),
    ]

    STATUS_CHOICES = [
        ('INSIDE', 'Inside'),
        ('EXITED', 'Exited'),
    ]

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='entries'
    )

    driver_name = models.CharField(max_length=100)
    driver_mobile = models.CharField(max_length=10)
    vendor_name = models.CharField(max_length=100, blank=True, null=True)

    purpose = models.CharField(max_length=30, choices=PURPOSE_CHOICES)

    entry_time = models.DateTimeField(auto_now_add=True)
    exit_time = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='INSIDE'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vehicle.vehicle_number} - {self.status}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['vehicle'],
                condition=models.Q(status='INSIDE'),
                name='unique_active_entry_per_vehicle'
                )
        ]

# Create your models here.
