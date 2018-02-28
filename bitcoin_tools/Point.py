from bitcoin_tools.FieldElement import FieldElement

class Point:
    def __init__(self, x, y, a, b):
        self.x = x
        self.y = y
        self.a = a
        self.b = b

        if self.x is None and self.y is None:
            return

        if self.y ** 2 != self.x ** 3 + self.a * self.x + self.b:
            raise RuntimeError("Points not on the curve")

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and \
               self.a == other.a and self.b == other.b

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y or \
               self.a != other.a or self.b != other.b

    def __repr__(self):
        if self.x is None:
            return 'Point(infinity)'
        else:
            return 'Point({},{})'.format(self.x, self.y)

    def __add__(self, other):
        if self.a != other.a or self.b != other.b:
            raise RuntimeError("Points are using different curves")

        if self.x is None:
            return other

        if other.x is None:
            return self

        # Check for reaching point at infinity
        # X are the same point but y is not, this would be a perfectly horizontal line on the curve
        if self.x == other.x and self.y != other.y:
            return self.__class__(None, None, self.a, self.b)

        # Calculate if self.x != other.x
        if self.x != other.x:
            slope = (self.y - other.y) / (self.x - other.x)

            # x3 = s**2 -x1 -x2
            x3 = slope ** 2 - self.x - other.x

            # y3 = slope * (x1 - x3) - y1
            y3 = slope * (self.x - x3) - self.y

            return self.__class__(x3, y3, self.a, self.b)
        else:
            # Point Doubling because x is the same value
            # Slope = (3* x1 ** 2 +a) / (2 * y1)
            slope = (3 * self.x ** 2 + self.a) / (2 * self.y)

            # x3 = slope**2 - 2*x1
            x3 = slope ** 2 - 2 * self.x

            # y3 = slope * (x1 - x3) - y1
            y3 = slope * (self.x - x3) - self.y

            return self.__class__(x3, y3, self.a, self.b)

    def __rmul__(self, scalar):
        product = self.__class__(None, None, self.a, self.b)

        for _ in range(scalar):
            product += self

        return product
