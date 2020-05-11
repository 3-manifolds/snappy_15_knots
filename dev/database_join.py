from __future__ import print_function
import sys, sqlite3, re, os, random
import snappy_manifolds

# This module uses sqlite3 databases with multiple tables.
# The path to the database file is specified at the module level.
from .sqlite_files import __path__ as manifolds_paths
manifolds_path = manifolds_paths[0]
database_path = os.path.join(manifolds_path, '15_knots.sqlite')

split_filling_info = re.compile('(.*?)((?:\([0-9 .+-]+,[0-9 .+-]+\))*$)')

original_manifolds_path = snappy_manifolds.manifolds_path
original_database_path = os.path.join(original_manifolds_path, 'more_manifolds.sqlite')

def extend_HT_db_with_15_crossing_knots(connection, base_table):
    extra_tables = ['alternating_knots_15', 'nonalternating_knots_15']
    db_name = 'fifteen_knots'
    extra_tables = ['{}.{}'.format(db_name, table) for table in extra_tables]
    cursor = connection.cursor()
    cursor.execute("ATTACH DATABASE '{}' AS {}".format(database_path, db_name))
    create_temp_view_statement = "CREATE TEMP VIEW all_links_view AS SELECT * FROM  {}".format(base_table)
    for extra_table in extra_tables:
        create_temp_view_statement += ' UNION ALL SELECT * FROM '
        create_temp_view_statement += extra_table
    cursor.execute(create_temp_view_statement)
    connection.commit()
    return "temp.all_links_view"

def get_tables(ManifoldTable):
    """
    Functions such as this one are meant to be called in the
    __init__.py module in snappy proper.  To avoid circular imports,
    it takes as argument the class ManifoldTable from database.py in
    snappy. From there, it builds all of the Manifold tables from the
    sqlite databases manifolds.sqlite and more_manifolds.sqlite in
    manifolds_src, and returns them all as a list.
    """

    class LinkExteriorsTable(ManifoldTable):
        """
        Link exteriors usually know a DT code describing the assocated link.
        """
        # Adding id here speeds up the query by a factor of
        # 20. Unfortunately, still 10 times slower than with a
        # nonjoined table.
        _select = 'select name, triangulation, DT, id from %s '

        def _finalize(self, M, row):
            M.set_name(row[0])
            M._set_DTcode(row[2])


    class HTLinkExteriors(LinkExteriorsTable):
        """
        Iterator for all knots up to 15 crossings and links up to 14
        crossings as tabulated by Jim Hoste and Morwen Thistlethwaite.
        In addition to the filter arguments supported by all
        ManifoldTables, this iterator provides
        alternating=<True/False>; knots_vs_links=<'knots'/'links'>;
        and crossings=N. These allow iterations only through
        alternating or non-alternating links with 1 or more than 1
        component and a specified crossing number.


        >>> HTLinkExteriors.identify(LinkExteriors['8_20'])
        K8n1(0,0)
        >>> some_links = HTLinkExteriors(alternating=False,knots_vs_links='links')[8.5:8.7]
        >>> len(some_links)
        8
        >>> for L in some_links:
        ...   print( L.name(), L.num_cusps(), L.volume() )
        ... 
        L11n138 2 8.66421454
        L12n1097 2 8.51918360
        L14n13364 2 8.69338342
        L14n13513 2 8.58439465
        L14n15042 2 8.66421454
        L14n24425 2 8.60676092
        L14n24777 2 8.53123093
        L14n26042 2 8.64333782
        >>> for L in some_links:
        ...   print( L.name(), L.DT_code() )
        ... 
        L11n138 [(8, -10, -12), (6, -16, -18, -22, -20, -2, -4, -14)]
        L12n1097 [(10, 12, -14, -18), (22, 2, -20, 24, -6, -8, 4, 16)]
        L14n13364 [(8, -10, 12), (6, -18, 20, -22, -26, -24, 2, -4, -28, -16, -14)]
        L14n13513 [(8, -10, 12), (6, -20, 18, -26, -24, -4, 2, -28, -16, -14, -22)]
        L14n15042 [(8, -10, 14), (12, -16, 18, -22, 24, 2, 26, 28, 6, -4, 20)]
        L14n24425 [(10, -12, 14, -16), (-18, 26, -24, 22, -20, -28, -6, 4, -2, 8)]
        L14n24777 [(10, 12, -14, -18), (2, 28, -22, 24, -6, 26, -8, 4, 16, 20)]
        L14n26042 [(10, 12, 14, -20), (8, 2, 28, -22, -24, -26, -6, -16, -18, 4)]

        This table extends the HTLinkExteriors table from
        snappy_manifolds with 15 crossing knots (no links with
        multiple components).  They are ordered so that the
        HTLinkExteriors come first, then the alternating 15 acrossing
        knots, then the nonalternating 15 crossing knots.

        >>> isosig = 'sLLLvzLLwQQQQcefjnilmlpnrrqqpprqiitcifaudnbsvrbccnn_bBEd'
        >>> HTLinkExteriors.identify(Manifold(isosig))
        K15n82491(0,0)
        >>> big_links = HTLinkExteriors[32.75:33.0]
        >>> [L.name() for L in big_links]
        ['K15a81381', 'K15a82192']
        """

        _regex = re.compile('[KL][0-9]+[an]([0-9]+)$')
        
        def __init__(self, **kwargs):
            LinkExteriorsTable.__init__(self,
                                        table='HT_links_view',
                                        db_path=original_database_path,
                                        **kwargs)
            self._table = extend_HT_db_with_15_crossing_knots(self._connection, self._table)
            self._get_length()
            self._get_max_volume()
            self._select = LinkExteriorsTable._select % self._table

        def _configure(self, **kwargs):
            """
            Process the ManifoldTable filter arguments and then add
            the ones which are specific to links.
            """
            ManifoldTable._configure(self, **kwargs)
            conditions = []

            alt = kwargs.get('alternating', None)
            if alt == True:
                conditions.append("name like '%a%'")
            elif alt == False:
                conditions.append("name like '%n%'")
            flavor = kwargs.get('knots_vs_links', None)
            if flavor == 'knots':
                conditions.append('cusps=1')
            elif flavor == 'links':
                conditions.append('cusps>1')
            if 'crossings' in kwargs:
                N = int(kwargs['crossings'])
                conditions.append(
                    "(name like '_%da%%' or name like '_%dn%%')"%(N,N))
            if self._filter:
                if len(conditions) > 0:
                    self._filter += (' and ' + ' and '.join(conditions))
            else:
                self._filter = ' and '.join(conditions)

    return [HTLinkExteriors()]


def connect_to_db(db_path):
    """
    Open the given sqlite database, ideally in read-only mode.
    """
    if sys.version_info >= (3,4):
        uri = 'file:' + db_path + '?mode=ro'
        return sqlite3.connect(uri, uri=True)
    elif sys.platform.startswith('win'):
        try:
            import apsw
            return apsw.Connection(db_path, flags=apsw.SQLITE_OPEN_READONLY)
        except ImportError:
            return sqlite3.connect(db_path)
    else:
        return sqlite3.connect(db_path)

def get_DT_tables():
    """
    Returns two barebones databases for looking up DT codes by name. 
    """
    class DTCodeTable(object):
        """
        A barebones database for looking up a DT code by knot/link name.
        """
        def __init__(self, name='', table='', db_path=database_path, **filter_args):
            self._table = table
            self._select = 'select DT from ' + table + ' '
            self.name = name
            self._connection = connect_to_db(db_path)
            self._cursor = self._connection.cursor()

        def __repr__(self):
            return self.name

        def __getitem__(self, link_name):
            select_query = self._select + ' where name="{}"'.format(link_name)
            return self._cursor.execute(select_query).fetchall()[0][0]
        
        def __len__(self):
            length_query = 'select count(*) from ' + self._table
            return self._cursor.execute(length_query).fetchone()[0]

    class ExtendedDTCodeTable(DTCodeTable):
        def __init__(self, **kwargs):
            DTCodeTable.__init__(self, table='HT_links_view',
                                 db_path=original_database_path, **kwargs)
            self._name = 'HTExtendedDTCodeTable'
            self._table = extend_HT_db_with_15_crossing_knots(self._connection, self._table)
            self._select = 'select DT from ' + self._table + ' '

    return [ExtendedDTCodeTable()]
