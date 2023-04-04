from django.test import TestCase

# Create your tests here.


def sum_func(a, b):
    # if isinstance(a, str):
    #     return ''
    return a + b


class SomeTest(TestCase):

    # def setUp(self):
    #     print('before')

    # def tearDown(self) -> None:
    #     print('after')

    def test_sum_of_numbers(self):
        self.assertEqual(sum_func(1,2), 3)

    def test_sum_of_str(self):
        self.assertEqual(sum_func('1','2'), '')