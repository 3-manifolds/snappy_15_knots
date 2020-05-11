import snappy_15_knots
import snappy

MT = snappy.database.ManifoldTable
HTE = snappy_15_knots.get_tables(MT)[0]

horrible_select = 'select name, triangulation, DT from temp.all_links_view '
bad_select = 'select name, triangulation, DT, id from temp.all_links_view '
good_select = 'select name, triangulation, DT, id from HT_links_view '

def get_index_test(table):
    """
    horrible: 69s
    bad:  4.75 s
    good: 0.615s
    """
    for i in range(1, 100):
        d = 13**i % 100000
        table[d]


def get_index_test_raw(table):
    """
    horrible: 69s
    bad:  4.87s
    good: 0.56s
    """
    for i in range(1, 100):
        d = 13**i % 100000
        query = table._select
        query += 'order by id limit 1 offset %d' % d
        #query += 'order by id limit 1' #offset %d' % d
        list(table._cursor.execute(query).fetchall())


        
def get_index_idea(table):
    """
    """
    for i in range(1, 100):
        d = 13**i % 100000
        query1 = good_select
        query2 = 'select name, triangulation, DT, id from fifteen_knots.alternating_knots_15 '
        query3 = 'select name, triangulation, DT, id from fifteen_knots.nonalternating_knots_15 '
        ans = []
        for query in [query1, query2, query3]:
            query += 'order by id limit 1 offset %d' % d
            ans += list(table._cursor.execute(query).fetchall())
        #print(i, d, d-min(ans, key=lambda x:x[3])[-1])


        
def get_index_idea2(table):
    """
    """
    for i in range(1, 100):
        d = 13**i % 100000
        query1 = 'select min(id) from temp.all_links_view '
        ans = []
        for query in [query1]:
            #query += 'offset %d' % d
            ans += list(table._cursor.execute(query).fetchall())
        print(i, d, ans)
        #print(i, d, d-min(ans, key=lambda x:x[3])[-1])
