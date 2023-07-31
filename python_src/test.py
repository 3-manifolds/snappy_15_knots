"""
We do only a very basic test for this module, since most of the
doctests are run by snappy.

>>> HT = get_DT_tables()[0]
>>> len(HT)
433804
>>> str(HT['L12n345'])
'lbbjceGkjHILFadb.010001100011'
>>> str(HT['K15a1'])
'oaobdegahjckmfniol.010100100001110'
>>> str(HT['K15n168030'])
'oaoeimKLjncbaoDhgf.010110110000100'
"""

from .database import get_DT_tables
import sys
import doctest
this_module = sys.modules[__name__]

def run_tests():
    result = doctest.testmod(this_module)
    print('snappy_manifolds: ' + repr(result))

if __name__ == '__main__':
    run_tests()
