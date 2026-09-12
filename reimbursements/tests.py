from django.test import TestCase
from django.urls import reverse

from .models import Reimbursement


class ReimbursementTests(TestCase):
    def test_dashboard_loads(self):
        response = self.client.get(reverse("reimbursements:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Receipt Reimbursements")

    def test_can_submit_reimbursement(self):
        response = self.client.post(
            reverse("reimbursements:dashboard"),
            {
                "title": "Food reimbursement",
                "description": "Snacks for event",
                "amount": "54.25",
                "receipt_url": "https://example.com/receipt",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Reimbursement.objects.count(), 1)
