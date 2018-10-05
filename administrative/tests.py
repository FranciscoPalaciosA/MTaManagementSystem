from django.test import TestCase

# Create your tests here.

class ProductionReportTest(TestCase):
    def test_new_report_correct(self):
        """
        Creating a new production report with correct information. Expecting a redirect to /administrative/
        """
