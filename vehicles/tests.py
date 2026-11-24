
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model


class VehicleAPITests(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        self.client.force_authenticate(user=self.user)

    def test_vehicle_list_api(self):
        response = self.client.get('/api/vehicles/')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_vehicle_registration(self):
        data = {
            'vehicle_number': 'TS09AB1234',
            'vehicle_type': 'CAR',
            'owner_name': 'Test Owner'
        }

        response = self.client.post(
            '/api/vehicles/',
            data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
    
    def test_duplicate_vehicle_registration(self):
        data = {
            'vehicle_number': 'TS09AB1234',
            'vehicle_type': 'CAR',
            'owner_name': 'Test Owner'
        }

        self.client.post(
            '/api/vehicles/',
            data,
            format='json'
        )

        response = self.client.post(
            '/api/vehicles/',
            data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
    
    def test_vehicle_entry(self):
        data = {
            'vehicle_number': 'TS09CD5678',
            'vehicle_type': 'CAR',
            'driver_name': 'Ramesh',
            'driver_mobile': '9876543210',
            'purpose': 'MATERIAL_DELIVERY',
            'vendor_name': 'ABC Suppliers'
        }

        response = self.client.post(
            '/api/entries/',
            data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
    
    def test_duplicate_active_entry(self):
        data = {
            'vehicle_number': 'TS09EF1234',
            'vehicle_type': 'CAR',
            'driver_name': 'Ramesh',
            'driver_mobile': '9876543210',
            'purpose': 'MATERIAL_DELIVERY'
        }

        self.client.post(
            '/api/entries/',
            data,
            format='json'
        )

        response = self.client.post(
            '/api/entries/',
            data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
    
    def test_vehicle_exit(self):
        data = {
            'vehicle_number': 'TS09GH1234',
            'vehicle_type': 'CAR',
            'driver_name': 'Ramesh',
            'driver_mobile': '9876543210',
            'purpose': 'MATERIAL_DELIVERY'
        }

        entry_response = self.client.post(
            '/api/entries/',
            data,
            format='json'
        )

        entry_id = entry_response.data['id']

        exit_response = self.client.post(
            f'/api/entries/{entry_id}/exit/'
        )

        self.assertEqual(
            exit_response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            exit_response.data['status'],
            'EXITED'
        )
    
    def test_duplicate_vehicle_exit(self):
        data = {
            'vehicle_number': 'TS09JK1234',
            'vehicle_type': 'CAR',
            'driver_name': 'Ramesh',
            'driver_mobile': '9876543210',
            'purpose': 'MATERIAL_DELIVERY'
        }

        entry_response = self.client.post(
            '/api/entries/',
            data,
            format='json'
        )

        entry_id = entry_response.data['id']

        self.client.post(
            f'/api/entries/{entry_id}/exit/'
        )

        second_exit_response = self.client.post(
            f'/api/entries/{entry_id}/exit/'
        )

        self.assertEqual(
            second_exit_response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
    
    def test_vehicle_reentry_after_exit(self):
        data = {
            'vehicle_number': 'TS09LM1234',
            'vehicle_type': 'CAR',
            'driver_name': 'Ramesh',
            'driver_mobile': '9876543210',
            'purpose': 'MATERIAL_DELIVERY'
        }

        first_entry = self.client.post(
            '/api/entries/',
            data,
            format='json'
        )

        entry_id = first_entry.data['id']

        self.client.post(
            f'/api/entries/{entry_id}/exit/'
        )

        second_entry = self.client.post(
            '/api/entries/',
            data,
            format='json'
        )

        self.assertEqual(
            second_entry.status_code,
            status.HTTP_201_CREATED
        )

        self.assertNotEqual(
            first_entry.data['id'],
            second_entry.data['id']
        )
    
    def test_vehicles_inside_api(self):
        data = {
            'vehicle_number': 'TS09MN1234',
            'vehicle_type': 'CAR',
            'driver_name': 'Ramesh',
            'driver_mobile': '9876543210',
            'purpose': 'MATERIAL_DELIVERY'
        }

        self.client.post(
            '/api/entries/',
            data,
            format='json'
        )

        response = self.client.get(
            '/api/entries/inside/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data['total_inside'],
            1
        )
    
    def test_daily_report_api(self):
        from django.utils import timezone

        today = timezone.localdate()

        data = {
            'vehicle_number': 'TS09PQ1234',
            'vehicle_type': 'CAR',
            'driver_name': 'Ramesh',
            'driver_mobile': '9876543210',
            'purpose': 'MATERIAL_DELIVERY'
        }

        self.client.post(
            '/api/entries/',
            data,
            format='json'
        )

        response = self.client.get(
            f'/api/reports/daily/?date={today}'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data['total_entries'],
            1
        )

