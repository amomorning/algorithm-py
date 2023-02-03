from fractions import Fraction
from decimal import Decimal
import math

Fraction(8, 16)
Fraction(1.333333)
Fraction(7e-5)
Fraction('8/28')
Fraction(1.1)
Fraction(Decimal('1.1'))

Fraction('8/28').as_integer_ratio()

# round
math.floor(Fraction('29/18'))
math.ceil(Fraction('29/18'))
round(Fraction('29/18'))

# limit denominator
Fraction(1.333333).limit_denominator(10) # denominator at most 10
