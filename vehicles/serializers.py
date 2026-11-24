from rest_framework import serializers
from .models import Vehicle, VehicleEntry


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

    def validate_vehicle_number(self, value):
        return value.strip().upper()


class VehicleEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleEntry
        fields = '__all__'


class EntryCreateSerializer(serializers.Serializer):
    vehicle_number = serializers.CharField(max_length=20)
    vehicle_type = serializers.ChoiceField(
        choices=Vehicle.VEHICLE_TYPES
    )
    driver_name = serializers.CharField(max_length=100)
    driver_mobile = serializers.CharField(max_length=10)
    vendor_name = serializers.CharField(
        max_length=100, required=False, allow_blank=True
    )
    purpose = serializers.ChoiceField(
        choices=VehicleEntry.PURPOSE_CHOICES
    )

    def validate_vehicle_number(self, value):
        return value.strip().upper()

    def validate_driver_mobile(self, value):
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError(
                "Mobile number must contain exactly 10 digits."
            )
        return value