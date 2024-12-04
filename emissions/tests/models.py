from django.test import TestCase
from django.contrib.auth import get_user_model
from emissions.models import Household, Transportation
from decimal import Decimal
from unittest.mock import patch

User = get_user_model()


class HouseholdModelTest(TestCase):

    def setUp(self):
        # Kullanıcı oluşturuluyor
        self.user = User.objects.create_user(username="testuser", password="testpassword")

    def test_unique_constraint(self):
        # Aynı user, aynı ay, aynı tüketim türü için sadece bir kayıt olmalı
        Household.objects.create(
            consumption_type="electricity",
            consumption_value=Decimal(100),
            month_period="2024-10",
            user=self.user
        )

        with self.assertRaises(Exception):
            Household.objects.create(
                consumption_type="electricity",
                consumption_value=Decimal(100),
                month_period="2024-10",
                user=self.user
            )


class TransportationModelTest(TestCase):

    def setUp(self):
        # Kullanıcı oluşturuluyor
        self.user = User.objects.create_user(username="testuser", password="testpassword")

    @patch("decouple.config")
    def test_get_sum_emissions_car(self, mock_config):
        # Araba emisyonu için config değeri mock'lanıyor
        mock_config.return_value = "0.2"  # Araba için emisyon değeri
        transportation = Transportation.objects.create(
            vehicle_type="car",
            distance=50,
            user=self.user
        )

        expected_emission = 50 * 0.2  # 50 * 0.2 = 10
        self.assertEqual(transportation.get_sum_emissions, expected_emission)

    def test_get_sum_emissions_walking(self):
        # Yürüyüş emisyonu her zaman 0 olmalı
        transportation = Transportation.objects.create(
            vehicle_type="walking",
            distance=10,
            user=self.user
        )

        self.assertEqual(transportation.get_sum_emissions, 0)

    def test_get_sum_emissions_cycling(self):
        # Bisiklet emisyonu her zaman 0 olmalı
        transportation = Transportation.objects.create(
            vehicle_type="cycling",
            distance=20,
            user=self.user
        )

        self.assertEqual(transportation.get_sum_emissions, 0)

    def test_unique_constraint(self):
        # Aynı kullanıcı, aynı taşıma verisi ile aynı kaydı eklememeliyiz
        Transportation.objects.create(
            vehicle_type="car",
            distance=100,
            user=self.user
        )

        with self.assertRaises(Exception):
            Transportation.objects.create(
                vehicle_type="car",
                distance=100,
                user=self.user
            )
