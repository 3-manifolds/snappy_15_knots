"""
Tests to make sure that adding 140% more manifolds does not slow down
HTLinkExteriors too much.

Timings are on thurston.math.illinois.edu, Python 3.7 on macOS
"""

import snappy

try:
    import snappy_15_knots
    print('Using 15 knots')
except:
    print('Not using 15 knots')
print(len(snappy.HTLinkExteriors))


def get_by_index(n):
    """
    Old:

    %timeit get_by_index(200)
    1.07 s +/- 2.5 ms per loop (mean +/- std. dev. of 7 runs, 1 loop each)

    New:

    %timeit get_by_index(200)
    1.07 s +/- 3.46 ms per loop (mean +/- std. dev. of 7 runs, 1 loop each)
    """
    for i in range(1, n):
        d = 13**i % 100000
        snappy.HTLinkExteriors[d]


def random_sample(n):
    """
    Old and new, with latest version of SnapPy, which sped up random
    massively even in the original case.

    Old:

    %timeit random_sample(100)
    64.7 ms +/- 1.15 ms per loop (mean +/- std. dev. of 7 runs, 10 loops each)

    New:

    %timeit random_sample(100)
    58.7 ms +/- 442 µs per loop (mean +/- std. dev. of 7 runs, 10 loops each)

    """
    #HT = snappy.HTLinkExteriors[100:-100]
    #HT = snappy.HTLinkExteriors[10.0:20.0]
    HT = snappy.HTLinkExteriors
    for _ in range(n):
        M = HT.random()
        M.volume()


def identify(n):
    """
    Old:

    %timeit identify(100)
    681 ms +/- 3.91 ms per loop (mean +/- std. dev. of 7 runs, 1 loop each)

    New:

    %timeit identify(100)
    714 ms +/- 3.16 ms per loop (mean +/- std. dev. of 7 runs, 1 loop each)
    """
    M = snappy.Manifold('K13n1234')
    for _ in range(n):
        M.identify()


def iterate(n):
    """
    Old:

    %timeit iterate(1000)
    589 ms +/- 2.63 ms per loop (mean +/- std. dev. of 7 runs, 1 loop each)

    New:
    %timeit iterate(1000)
    590 ms +/- 2.94 ms per loop (mean +/- std. dev. of 7 runs, 1 loop each)
    """
    list([M.volume() for M in snappy.HTLinkExteriors[100000:100000+n]])


def get_by_name(n):
    """
    Old:

    %timeit get_by_name(1000)
    1.05 s +/- 4 ms per loop (mean +/- std. dev. of 7 runs, 1 loop each)

    New:

    %timeit get_by_name(1000)
    1.06 s +/- 1.54 ms per loop (mean +/- std. dev. of 7 runs, 1 loop each)

    """
    for i in range(1, n):
        d = 13**i % 10000
        snappy.HTLinkExteriors['K14n%d' % d]
        snappy.HTLinkExteriors['L14n%d' % d]
