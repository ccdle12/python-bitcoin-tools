# This class is the basis for performing modulo arithmetic operations on x,y points on the curve

class FieldElement:

    def __init__(self, num, prime):
        self.num = num
        self.prime = prime

        if self.num >= self.prime or self.num < 0:
            raise RuntimeError("Num is not within the field of: {0}".format(self.prime - 1))

    # Checks for equality between self and other
    def __eq__(self, other):
        # if other is None:
        #     return True

        return self.num == other.num and self.prime == other.prime

    def __ne__(self, other):
        if other is None:
            return True
        return self.num != other.num or self.prime != other.prime

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
        num = (self.num * pow(other.num, self.prime - 2, self.prime)) % self.prime

        return self.__class__(num, self.prime)

    def __rmul__(self, scalar):
        num = (scalar * self.num) % self.prime
        return self.__class__(num, self.prime)

    # Function to check if primes are the same number
    def check_primes_the_same(self, other_prime):
        if self.prime != other_prime:
            raise RuntimeError("Primes are different")
