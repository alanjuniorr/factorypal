import pytest
import time
from rest_framework.test import APIClient
from django.urls import reverse
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "factorypal.settings")
django.setup()

@pytest.mark.django_db
class TestMetricsAPI:
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test client and initial known line IDs"""
        self.client = APIClient()
        self.valid_line_id = 11
        self.unknown_line_id = 999  # Not initialized in service

    def test_post_linespeed_success(self):
        """Test posting a valid speed measurement"""
        response = self.client.post(
            reverse("line-speed"),
            data={"line_id": self.valid_line_id, "speed": 150.5, "timestamp": int(time.time() * 1000)},
            format="json"
        )
        assert response.status_code == 201  # Successfully stored the data

    def test_post_linespeed_old_data(self):
        """Test posting an old measurement (older than 60 minutes)"""
        old_timestamp = int((time.time() - 4000) * 1000)  # More than 60 minutes old
        response = self.client.post(
            reverse("line-speed"),
            data={"line_id": self.valid_line_id, "speed": 100.0, "timestamp": old_timestamp},
            format="json"
        )
        assert response.status_code == 204  # Old data should be rejected

    def test_post_linespeed_unknown_line(self):
        """Test posting data to an unknown line"""
        response = self.client.post(
            reverse("line-speed"),
            data={"line_id": self.unknown_line_id, "speed": 120.0, "timestamp": int(time.time() * 1000)},
            format="json"
        )
        assert response.status_code == 404  # Unknown line should return 404

    def test_get_metrics_success(self):
        """Test retrieving metrics after posting speed data"""
        timestamp = int(time.time() * 1000)

        # Post some speed data first
        self.client.post(reverse("line-speed"), data={"line_id": self.valid_line_id, "speed": 100, "timestamp": timestamp}, format="json")
        self.client.post(reverse("line-speed"), data={"line_id": self.valid_line_id, "speed": 200, "timestamp": timestamp}, format="json")
        self.client.post(reverse("line-speed"), data={"line_id": self.valid_line_id, "speed": 150, "timestamp": timestamp}, format="json")

        # Get metrics
        response = self.client.get(reverse("metrics", kwargs={"lineid": self.valid_line_id}))
        assert response.status_code == 200  # Successful response
        data = response.json()
        assert data["avg"] == pytest.approx(150, rel=1e-2)  # Average of 100, 200, 150
        assert data["max"] == 200
        assert data["min"] == 100

    def test_get_metrics_unknown_line(self):
        """Test retrieving metrics for an unknown line"""
        response = self.client.get(reverse("metrics", kwargs={"lineid": self.unknown_line_id}))
        assert response.status_code == 404  # Unknown line should return 404

    def test_get_all_metrics(self):
        """Test retrieving metrics for all known lines"""
        timestamp = int(time.time() * 1000)

        # Post data for multiple lines
        self.client.post(reverse("line-speed"), data={"line_id": 11, "speed": 180, "timestamp": timestamp}, format="json")
        self.client.post(reverse("line-speed"), data={"line_id": 20, "speed": 220, "timestamp": timestamp}, format="json")

        # Get metrics for all lines
        response = self.client.get(reverse("metrics-all"))
        assert response.status_code == 200
        data = response.json()

        assert any(d["line_id"] == 11 for d in data)
        assert any(d["line_id"] == 20 for d in data)
