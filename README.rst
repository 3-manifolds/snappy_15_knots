The SnapPy manifold database for 15 crossings knots
===================================================

This repository stores the manifold databases for 15 crossing knots,
and includes the source code for the Python module "snappy_15_knots"
which packages them up for use in SnapPy and Spherogram.

The raw source for the tables are in::
  
  manifold_src/original_manifold_sources

stored as plain text CSV files for the potential convenience of other
users. The triangulations themselves are stored in the "isosig" format
of Burton, as described in the appendix to `this paper
<http://arxiv.org/abs/1110.6080>`_ with an added "decoration" suffix
that describes the peripheral framing.

For technical reasons, this database includes a copy of the database
for 14 crossing knots and links.

The original enumeration of these knots was done by Hoste,
Thistlethwaite, and Weeks (The Mathematical Intelligencer 20 (1998)).
This database, including the triangulations, was developed primarily
by Malik Obeidin.
