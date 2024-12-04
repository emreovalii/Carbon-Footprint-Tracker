from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from emissions import models
from unittest.mock import patch
from decimal import Decimal

User = get_user_model()


class HouseholdCreateViewTest(TestCase):

    def setUp(self):
        # Test kullanıcısı oluşturuluyor
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client = Client()

    def test_create_household_view(self):
        # Doğrudan view'a GET isteği gönderiliyor
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("emissions:household_create"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "emissions/household_form.html")

    @patch("decouple.config")
    def test_household_form_valid(self, mock_config):
        # Test verilerini gönderiyoruz
        mock_config.return_value = "0.5"  # Elektrik emisyon değeri
        self.client.login(username="testuser", password="testpassword")

        data = {
            "consumption_type": "electricity",
            "consumption_value": Decimal(100),
            "month_period": "2024-10"
        }

        response = self.client.post(reverse("emissions:household_create"), data)

        # Verinin başarılı şekilde kaydedildiğini kontrol ediyoruz
        self.assertEqual(response.status_code, 302)  # Redirection (success)
        self.assertEqual(models.Household.objects.count(), 1)

        household = models.Household.objects.first()
        self.assertEqual(household.consumption_type, "electricity")
        self.assertEqual(household.consumption_value, Decimal(100))
        self.assertEqual(household.month_period, "2024-10")
        self.assertEqual(household.user, self.user)


class TransportationCreateViewTest(TestCase):

    def setUp(self):
        # Test kullanıcısı oluşturuluyor
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client = Client()

    def test_create_transportation_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("emissions:transportation_create"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "emissions/transportation_form.html")

    @patch("decouple.config")
    def test_transportation_form_valid(self, mock_config):
        # Test verisini gönderiyoruz
        mock_config.return_value = "0.2"  # Araba emisyon değeri
        self.client.login(username="testuser", password="testpassword")

        data = {
            "vehicle_type": "car",
            "distance": 50
        }

        response = self.client.post(reverse("emissions:transportation_create"), data)

        # Verinin başarılı şekilde kaydedildiğini kontrol ediyoruz
        self.assertEqual(response.status_code, 302)  # Redirection (success)
        self.assertEqual(models.Transportation.objects.count(), 1)

        transportation = models.Transportation.objects.first()
        self.assertEqual(transportation.vehicle_type, "car")
        self.assertEqual(transportation.distance, 50)
        self.assertEqual(transportation.user, self.user)


class EmissionReportViewTest(TestCase):

    def setUp(self):
        # Test kullanıcısı oluşturuluyor
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client = Client()

    @patch("decouple.config")
    def test_emission_report_view(self, mock_config):
        # Test verilerini ekliyoruz
        mock_config.return_value = "0.2"

        # Transportation verisi
        models.Transportation.objects.create(
            vehicle_type="car", distance=100, user=self.user
        )

        # Household verisi
        models.Household.objects.create(
            consumption_type="electricity",
            consumption_value=Decimal(100),
            month_period="2024-10",
            user=self.user
        )

        self.client.login(username="testuser", password="testpassword")

        response = self.client.get(reverse("emissions:emission_report"))

        # Rapor sayfasının başarılı şekilde döndüğünü kontrol ediyoruz
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reports/reports.html")

        # Transportation emisyonlarını kontrol et
        transportation_report = response.context["transportation_by_date"]
        self.assertEqual(len(transportation_report), 1)  # Sadece bir kaydımız olmalı
        self.assertEqual(transportation_report[0]["total_emission"], 100 * 0.2)  # 100 * 0.2 = 20

        # Household emisyonlarını kontrol et
        household_report = response.context["household_by_month"]
        self.assertEqual(len(household_report), 1)  # Sadece bir kaydımız olmalı
