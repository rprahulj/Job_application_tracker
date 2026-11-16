from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Application

User = get_user_model()

class OwnershipTests(APITestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username="alice", password="StrongPass123")
        self.bob = User.objects.create_user(username="bob", password="StrongPass123")
        self.alice_app = Application.objects.create(user=self.alice, company="A Co", role="Engineer")
        self.bob_app = Application.objects.create(user=self.bob, company="B Co", role="Analyst")
        token = str(RefreshToken.for_user(self.alice).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_list_only_returns_own_records(self):
        response = self.client.get("/api/applications/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["company"], "A Co")

    def test_cannot_retrieve_another_users_record(self):
        response = self.client.get(f"/api/applications/{self.bob_app.id}/")
        self.assertEqual(response.status_code, 404)

    def test_cannot_create_interview_for_another_users_application(self):
        response = self.client.post("/api/interviews/", {
            "application": self.bob_app.id,
            "scheduled_at": "2026-12-01T10:00:00Z",
        }, format="json")
        self.assertIn(response.status_code, (400, 404))
