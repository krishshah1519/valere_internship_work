import unittest
from Day2 import check_prime


class Test_Prime(unittest.TestCase):

    def test_isprime(self):
        self.assertTrue(check_prime.checkPrime(11), True)
        self.assertFalse(check_prime.checkPrime(-11), False)
        self.assertFalse(check_prime.checkPrime(0), False)
        self.assertFalse(check_prime.checkPrime(1), False)
        self.assertFalse(check_prime.checkPrime(123), False)


if __name__ == "__main__":
    unittest.main()