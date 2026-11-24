
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db import transaction, IntegrityError
from django.utils import timezone
from django.utils.dateparse import parse_date

from .models import Vehicle, VehicleEntry
from .serializers import (
    VehicleSerializer,
    VehicleEntrySerializer,
    EntryCreateSerializer
)


# 1. Vehicle Registration and List API
class VehicleListCreateView(generics.ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


# 2. Vehicle Details and Update API
class VehicleDetailView(generics.RetrieveUpdateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


# 3. Vehicle Entry and History API
class VehicleEntryListCreateView(APIView):

    def get(self, request):
        entries = VehicleEntry.objects.all().order_by('-entry_time')

        vehicle_number = request.query_params.get('vehicle_number')
        status_value = request.query_params.get('status')
        date = request.query_params.get('date')

        if vehicle_number:
            entries = entries.filter(
                vehicle__vehicle_number__icontains=vehicle_number.strip().upper()
            )

        if status_value:
            entries = entries.filter(status=status_value.upper())

        if date:
            entries = entries.filter(entry_time__date=date)

        serializer = VehicleEntrySerializer(entries, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = EntryCreateSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            try:
                with transaction.atomic():

                    vehicle = Vehicle.objects.filter(
                        vehicle_number=data['vehicle_number']
                    ).first()

                    if vehicle:
                        if vehicle.vehicle_type != data['vehicle_type']:
                            return Response(
                                {"error": "Vehicle type does not match."},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                    else:
                        vehicle = Vehicle.objects.create(
                            vehicle_number=data['vehicle_number'],
                            vehicle_type=data['vehicle_type']
                        )

                    active_entry = VehicleEntry.objects.filter(
                        vehicle=vehicle,
                        status='INSIDE'
                    ).exists()

                    if active_entry:
                        return Response(
                            {"error": "This vehicle is already inside."},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    entry = VehicleEntry.objects.create(
                        vehicle=vehicle,
                        driver_name=data['driver_name'],
                        driver_mobile=data['driver_mobile'],
                        vendor_name=data.get('vendor_name'),
                        purpose=data['purpose']
                    )

                return Response(
                    VehicleEntrySerializer(entry).data,
                    status=status.HTTP_201_CREATED
                )

            except IntegrityError:
                return Response(
                    {"error": "This vehicle already has an active entry."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# 4. Vehicle Exit API
class VehicleExitView(APIView):

    def post(self, request, pk):
        try:
            entry = VehicleEntry.objects.get(
                id=pk,
                status='INSIDE'
            )

        except VehicleEntry.DoesNotExist:
            return Response(
                {"error": "Active vehicle entry not found."},
                status=status.HTTP_400_BAD_REQUEST
            )

        entry.exit_time = timezone.now()
        entry.status = 'EXITED'
        entry.save()

        duration = entry.exit_time - entry.entry_time
        duration_minutes = int(duration.total_seconds() / 60)

        return Response({
            "message": "Vehicle exited successfully.",
            "vehicle_number": entry.vehicle.vehicle_number,
            "entry_time": entry.entry_time,
            "exit_time": entry.exit_time,
            "status": entry.status,
            "duration_minutes": duration_minutes
        }, status=status.HTTP_200_OK)


# 5. Currently Inside API
class VehicleInsideView(APIView):

    def get(self, request):
        entries = VehicleEntry.objects.filter(
            status='INSIDE'
        ).order_by('-entry_time')

        serializer = VehicleEntrySerializer(
            entries,
            many=True
        )

        return Response({
            "total_inside": entries.count(),
            "vehicles": serializer.data
        }, status=status.HTTP_200_OK)


# 6. Daily Vehicle Report API
class DailyReportView(APIView):

    def get(self, request):
        date_value = request.query_params.get('date')

        if not date_value:
            return Response(
                {"error": "Please provide a date."},
                status=status.HTTP_400_BAD_REQUEST
            )

        report_date = parse_date(date_value)

        if report_date is None:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )

        total_entries = VehicleEntry.objects.filter(
            entry_time__date=report_date
        ).count()

        total_exits = VehicleEntry.objects.filter(
            exit_time__date=report_date
        ).count()

        currently_inside = VehicleEntry.objects.filter(
            status='INSIDE'
        ).count()

        return Response({
            "date": str(report_date),
            "total_entries": total_entries,
            "total_exits": total_exits,
            "currently_inside": currently_inside
        }, status=status.HTTP_200_OK)
