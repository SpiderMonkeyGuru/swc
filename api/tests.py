import uuid

from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import ShortenedURL


class URLExpanderDirectTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.short_code = str(uuid.uuid4()).replace("-", "")[:10]
        self.test_mapping = ShortenedURL.objects.create(
            original_url="https://www.example.com", short_code=self.short_code
        )

    def test_if_expander_redirects_to_the_original_url_for_existing_short_code(self):
        url = reverse("expand_url", kwargs={"short_code": self.short_code})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, "https://www.example.com")

    def test_if_expander_returns_404_for_non_existing_short_code(self):
        url = reverse("expand_url", kwargs={"short_code": "nonexistent"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class URLShortenerViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("shorten-list")
        self.valid_url = "https://www.example.com"

        self.test_mapping = ShortenedURL.objects.create(
            original_url="https://www.test.com"
        )

    def test_creating_shortened_url(self):
        response = self.client.post(
            self.url, {"original_url": self.valid_url}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("shortened_url", response.data)
        self.assertTrue(
            ShortenedURL.objects.filter(original_url=self.valid_url).exists()
        )

    def test_creating_shortened_url_with_invalid_url_format(self):
        invalid_url = "not-a-valid-url"
        response = self.client.post(
            self.url, {"original_url": invalid_url}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(ShortenedURL.objects.filter(original_url=invalid_url).exists())

    def test_creating_shortened_url_with_missing_input_url(self):
        response = self.client.post(self.url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_creating_shortened_url_with_too_long_input_url(self):
        too_long_url = self.valid_url + "a" * 2000
        response = self.client.post(
            self.url, {"original_url": too_long_url}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(
            ShortenedURL.objects.filter(original_url=too_long_url).exists()
        )

    def test_creating_shortened_url_with_custom_short_code(self):
        custom_short_code = "custom123"
        response = self.client.post(
            self.url,
            {"original_url": self.valid_url, "short_code": custom_short_code},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url_mapping = ShortenedURL.objects.get(original_url=self.valid_url)
        self.assertNotEqual(url_mapping.short_code, custom_short_code)

    def test_deleting_shortened_url(self):
        url = reverse("shorten-detail", kwargs={"pk": self.test_mapping.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ShortenedURL.objects.filter(id=self.test_mapping.id).exists())

    def test_deleting_nonexistent_url(self):
        non_existent_id = 9999
        url = reverse("shorten-detail", kwargs={"pk": non_existent_id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
