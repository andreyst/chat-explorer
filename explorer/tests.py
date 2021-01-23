from django.test import SimpleTestCase
from .utils import fill_sparse_stats, generate_dates
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class GenerateDates(SimpleTestCase):
    def test_day(self):
      reference_output = [
        (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
        (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
        (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        (datetime.now()).strftime("%Y-%m-%d"),
      ]

      test_output = generate_dates(datetime.now() - timedelta(days=3), group="d")
      self.assertEquals(test_output, reference_output)

    def test_week(self):
      reference_output = [
        (datetime.now() - timedelta(weeks=3)).strftime("%Y-%W"),
        (datetime.now() - timedelta(weeks=2)).strftime("%Y-%W"),
        (datetime.now() - timedelta(weeks=1)).strftime("%Y-%W"),
        (datetime.now()).strftime("%Y-%W"),
      ]

      test_output = generate_dates(datetime.now() - timedelta(weeks=3), group="w")
      print(test_output)
      self.assertEquals(test_output, reference_output)

    def test_month(self):
      reference_output = [
        (datetime.now() - relativedelta(months=3)).strftime("%Y-%m"),
        (datetime.now() - relativedelta(months=2)).strftime("%Y-%m"),
        (datetime.now() - relativedelta(months=1)).strftime("%Y-%m"),
        (datetime.now()).strftime("%Y-%m"),
      ]

      test_output = generate_dates(datetime.now() - relativedelta(months=3), group="m")
      self.assertEquals(test_output, reference_output)

class FillSparseDates(SimpleTestCase):
    def d(self, days_delta):
        return (datetime.now() - timedelta(days=days_delta)).strftime("%Y-%m-%d")

    def test_empty(self):
        test_input = []
        reference_output = []

        test_output = fill_sparse_stats(test_input)
        self.assertEquals(test_output, reference_output)

    def test_fill(self):
        test_input = [
          (0, self.d(1), 1, 1),
          (1, self.d(1), 1, 1),
          (2, self.d(1), 1, 1),
        ]
        reference_output = [
          (0, self.d(1), 1, 1),
          (1, self.d(1), 1, 1),
          (2, self.d(1), 1, 1),
          (0, self.d(0), 0, 0),
          (1, self.d(0), 0, 0),
          (2, self.d(0), 0, 0),
        ]

        test_output = fill_sparse_stats(test_input)
        self.assertEquals(test_output, reference_output)

    def test_fill2(self):
        test_input = [
          (0, self.d(3), 1, 1),
          (1, self.d(2), 1, 1),
          (2, self.d(1), 1, 1),
        ]
        reference_output = [
          (0, self.d(3), 1, 1),
          (1, self.d(3), 0, 0),
          (2, self.d(3), 0, 0),
          (1, self.d(2), 1, 1),
          (0, self.d(2), 0, 0),
          (2, self.d(2), 0, 0),
          (2, self.d(1), 1, 1),
          (0, self.d(1), 0, 0),
          (1, self.d(1), 0, 0),
          (0, self.d(0), 0, 0),
          (1, self.d(0), 0, 0),
          (2, self.d(0), 0, 0),
        ]

        test_output = fill_sparse_stats(test_input)
        self.assertEquals(test_output, reference_output)

    def test_fill3(self):
        test_input = [
          (2, self.d(6), 1, 1),
          (1, self.d(4), 1, 1),
          (0, self.d(2), 1, 1),
        ]
        reference_output = [
          (2, self.d(6), 1, 1),
          (0, self.d(6), 0, 0),
          (1, self.d(6), 0, 0),
          (0, self.d(5), 0, 0),
          (1, self.d(5), 0, 0),
          (2, self.d(5), 0, 0),
          (1, self.d(4), 1, 1),
          (0, self.d(4), 0, 0),
          (2, self.d(4), 0, 0),
          (0, self.d(3), 0, 0),
          (1, self.d(3), 0, 0),
          (2, self.d(3), 0, 0),
          (0, self.d(2), 1, 1),
          (1, self.d(2), 0, 0),
          (2, self.d(2), 0, 0),
          (0, self.d(1), 0, 0),
          (1, self.d(1), 0, 0),
          (2, self.d(1), 0, 0),
          (0, self.d(0), 0, 0),
          (1, self.d(0), 0, 0),
          (2, self.d(0), 0, 0),
        ]

        test_output = fill_sparse_stats(test_input)
        self.assertEquals(test_output, reference_output)