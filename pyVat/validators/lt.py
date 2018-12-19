# Copyright 2018 Agile Geeks

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software
# is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import (
    unicode_literals,
    print_function,
    division
)
import re
from .generic import GenericValidator


class Validator(GenericValidator):
    """
    For rules see /docs/VIES-VAT Validation Routines-v15.0.doc
    """

    def __init__(self):
        self.regexp = re.compile(r'^((\d{9})|(\d{12}))$')

    def validate(self, vat_number):
        if super(Validator, self).validate(vat_number) is False:
            return False

        vat_number = str(vat_number)

        # Legal entities
        if len(vat_number) == 9:
            checksum = int(vat_number[8])
            if int(vat_number[7]) != 1:
                return False
            r1 = self.sum_weights(list(range(1,9)), vat_number) % 11
            if r1 != 10:
                checkval = r1
            else:
                rng = list(range(3,10)) + [1]
                r2 = self.sum_weights(rng, vat_number) % 11
                if r2 == 10:
                    checkval = 0
                else:
                    checkval = r2
        else:
            # Temporarily registered taxpayers
            checksum = int(vat_number[11])
            if int(vat_number[10]) != 1:
                return False

            rng = list(range(1,10)) + list(range(1,3))
            r1 = self.sum_weights(rng, vat_number) % 11
            if r1 != 10:
                checkval = r1
            else:
                rng = list(range(3, 10)) + list(range(1,5))
                r2 = self.sum_weights(rng, vat_number) % 11
                if r2 == 10:
                    checkval = 0
                else:
                    checkval = r2
        return checksum == checkval
