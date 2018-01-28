# This class is the basis for performing modulo arithmetic operations on x,y points on the curve
from unittest import TestCase


class FieldElement:

    def __init__(self, num, prime):
        self.num = num
        self.prime = prime

        if self.num >= self.prime or self.num < 0:
            raise RuntimeError("Num is not within the field of: {0}".format(self.prime - 1))

    # Checks for equality between self and other
    def __eq__(self, other):
        return self.num == other.num and self.prime == other.prime

    # The operations performed when self and other are added together
    def __add__(self, other):
        self.check_primes_the_same(other.prime)

        num = (self.num + other.num) % self.prime

        # Returns an instance of the FieldElement class
        return self.__class__(num, self.prime)

    def __sub__(self, other):
        self.check_primes_the_same(other.prime)

        num = (self.num - other.num) % self.prime

        return self.__class__(num, self.prime)

    def __mul__(self, other):
        self.check_primes_the_same(other.prime)

        num = (self.num * other.num) % self.prime

        return self.__class__(num, self.prime)

    def __pow__(self, power):
        num = pow(self.num, power % (self.prime - 1), self.prime)
        return self.__class__(num, self.prime)

    def __truediv__(self, other):
        self.check_primes_the_same(other.prime)
        exponent = pow(other.num, self.prime-2, self.prime)
        print("Exponent: {0}".format(exponent))
        num = (self.num * pow(other.num, self.prime-2, self.prime)) % self.prime

        return self.__class__(num, self.prime)

    def __rmul__(self, scalar):
        num = (scalar * self.num) % self.prime

        return self.__class__(num, self.prime)

    # Function to check if primes are the same number
    def check_primes_the_same(self, other_prime):
        if self.prime != other_prime:
            raise RuntimeError("Primes are different")


class FieldElementTest(TestCase):

    def test_addition(self):
        p1 = FieldElement(9, 11)
        p2 = FieldElement(6, 11)
        self.assertEqual(p1 + p2, FieldElement(4, 11))

        p1 = FieldElement(10, 11)
        p2 = FieldElement(9, 11)
        self.assertEqual(p1 + p2, FieldElement(8, 11))

        # Since product of both nums are below the prime field, the answer is the normal addition
        print("----------------------------------------------------------------------------------------")
        print("Since product of both nums are below the prime field, the answer is the normal addition")
        print("----------------------------------------------------------------------------------------")
        p1 = FieldElement(2, 11)
        p2 = FieldElement(3, 11)
        self.assertEqual(p1 + p2, FieldElement(5, 11))

        p1 = FieldElement(6, 11)
        p2 = FieldElement(3, 11)
        self.assertEqual(p1 + p2, FieldElement(9, 11))

        # Should throw an error since passing two different primes
        print("Should throw an error since passing two different primes")
        print("----------------------------------------------------------------------------------------")
        with self.assertRaises(RuntimeError):
            p1 = FieldElement(2, 11)
            p2 = FieldElement(3, 7)
            p3 = p1 + p2

        # Should throw an error num is greater than prime number
        print("Should throw an error num is greater than prime number")
        print("----------------------------------------------------------------------------------------")
        with self.assertRaises(RuntimeError):
            p1 = FieldElement(12, 11)
            p2 = FieldElement(3, 11)
            p3 = p1 + p2

        with self.assertRaises(RuntimeError):
            p1 = FieldElement(2, 11)
            p2 = FieldElement(24, 11)
            p3 = p1 + p2

        # Should throw an error since num is less than 0, cannot have a member of the prime field below 0
        print("Should throw an error since num is less than 0")
        print("----------------------------------------------------------------------------------------")
        with self.assertRaises(RuntimeError):
            p1 = FieldElement(-1, 11)
            p2 = FieldElement(3, 11)
            p3 = p1 + p2

        with self.assertRaises(RuntimeError):
            p1 = FieldElement(2, 11)
            p2 = FieldElement(-24, 11)
            p3 = p1 + p2

    def test_subtraction(self):
        # Should throw an error since passing two different primes
        print("Should throw an error since passing two different primes")
        print("----------------------------------------------------------------------------------------")
        with self.assertRaises(RuntimeError):
            p1 = FieldElement(2, 11)
            p2 = FieldElement(3, 7)
            p3 = p1 - p2

        p1 = FieldElement(9, 11)
        p2 = FieldElement(6, 11)
        self.assertEqual(p1 - p2, FieldElement(3, 11))

        p1 = FieldElement(10, 11)
        p2 = FieldElement(1, 11)
        self.assertEqual(p1 - p2, FieldElement(9, 11))

        p1 = FieldElement(5, 11)
        p2 = FieldElement(10, 11)
        self.assertEqual(p1 - p2, FieldElement(6, 11))

        p1 = FieldElement(2, 11)
        p2 = FieldElement(4, 11)
        self.assertEqual(p1 - p2, FieldElement(9, 11))

        p1 = FieldElement(1, 11)
        p2 = FieldElement(10, 11)
        self.assertEqual(p1 - p2, FieldElement(2, 11))

    def test_multiplication(self):
        # Should throw an error since passing two different primes
        print("Should throw an error since passing two different primes")
        print("----------------------------------------------------------------------------------------")
        with self.assertRaises(RuntimeError):
            p1 = FieldElement(2, 11)
            p2 = FieldElement(3, 7)
            p3 = p1 * p2

        p1 = FieldElement(9, 11)
        p2 = FieldElement(6, 11)
        self.assertEqual(p1 * p2, FieldElement(10, 11))

        p1 = FieldElement(2, 11)
        p2 = FieldElement(3, 11)
        self.assertEqual(p1 * p2, FieldElement(6, 11))

        p1 = FieldElement(6, 11)
        p2 = FieldElement(6, 11)
        self.assertEqual(p1 * p2, FieldElement(3, 11))

        p1 = FieldElement(3, 11)
        p2 = FieldElement(5, 11)
        self.assertEqual(p1 * p2, FieldElement(4, 11))

    def test_powers(self):
        p1 = FieldElement(9, 11)
        self.assertEqual(p1**2, FieldElement(4, 11))

        print("Will perform powers with an exponent greater than the prime, it should wrap around and keep the product within the field of the prime number")
        p1 = FieldElement(2, 5)
        self.assertEqual(p1 ** 6, FieldElement(4, 5))

        # Prime: 7
        # Powers: 9
        # Num: 5
        # Power % (prime - 1) = 9 % (7-1) = 9 % 6 = 3
            # exponent = 3
        # result = num ^ exponent = 5**3 = 125
        # final result = 125 % 7
        p1 = FieldElement(5, 7)
        self.assertEqual(p1 ** 9, FieldElement(6, 7))


        # Prime: 5
        # Powers: 12
        # Num: 2
        # Exponent = Power % (prime - 1) = 12 % (5 - 1) = 12 % 4 = 8
        # Result = num ^ exponent = 2 ** 8 = 256
        # Final Result = result % prime = 256 % 5 = 1
        p1 = FieldElement(2, 5)
        self.assertEqual(p1 ** 12, FieldElement(1, 5))

        # Prime: 5
        # Powers: 9
        # Num: 3
        # Exponent = Powers % (prime - 1) = 9 % (5 - 1) = 9 % 4 = 5
        # Result = num ^ exponent = 3 ** 5 = 243
        # Final modulo operation keeps result within the prime field
        # Final Result = result % prime = 243 % 5 = 3
        p1 = FieldElement(3, 5)
        self.assertEqual(p1 ** 9, FieldElement(3, 5))

    def test_division(self):
        print("Should throw an error since passing two different primes")
        print("----------------------------------------------------------------------------------------")
        with self.assertRaises(RuntimeError):
            p1 = FieldElement(2, 11)
            p2 = FieldElement(3, 7)
            p3 = p1/p2

        # Formula: (self.num * pow(other.num, self.prime - 2, self.prime)) % self.prime
            # (2 * pow(3, (11-2), 11)) % 11
            # Calculate the pow equation: 3^9 == 19,683
            # exponent = 19,683 % 11 = 4
            # 2 * 4 = 8
            # 8 % 11 = 8
        p1 = FieldElement(2, 11)
        p2 = FieldElement(3, 11)
        print((p1/p2).num)
        self.assertEqual(p1/p2, FieldElement(8, 11))

        # Formula: (self.num * pow(other.num, self.prime - 2, self.prime)) % self.prime
            # (4 * pow(3, (5-2), 5)) % 5
            # 3^3 == 27
            # exponent = 27 % 5 = 2
            # 4 * 2 = 8
            # 8 % 5 = 1
        p1 = FieldElement(4, 5)
        p2 = FieldElement(3, 5)
        self.assertEqual(p1 / p2, FieldElement(3, 5))

        # Formula: (self.num * pow(other.num, self.prime - 2, self.prime)) % self.prime
            # (6 * pow(4, (7-2), 7)) % 7
            # 4^5 == 1024
            # exponent = 1024 % 7 = 2
            # 6 * 2 = 12
            # 12 % 7 = 5
        p1 = FieldElement(6, 7)
        p2 = FieldElement(4, 7)
        self.assertEqual(p1 / p2, FieldElement(5, 7))

    def test_rmul(self):
        p1 = FieldElement(5, 11)
        expected = p1 + p1
        scalar = 2
        self.assertEqual(scalar*p1, expected)

        p1 = FieldElement(5, 11)
        expected = p1 + p1 + p1
        scalar = 3
        self.assertEqual(scalar * p1, expected)

        p1 = FieldElement(5, 11)
        expected = p1 + p1 + p1 + p1 + p1
        scalar = 5
        self.assertEqual(scalar * p1, expected)
