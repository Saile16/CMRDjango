from django.test import TestCase
from django.shortcuts import reverse

# Create your tests here.


class LadingPageTest(TestCase):

    def test_get(self):
        # Todo some sort of test
        response = self.client.get(reverse("landing-page"))
        # print(response.status_code)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "landing.html")
