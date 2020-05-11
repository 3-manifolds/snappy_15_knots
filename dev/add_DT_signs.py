""" 
Originally, HTLinkExteriors had DT codes which didn't include the
signs
"""

import snappy, spherogram
import csv, os

def add_signs(dt):
    codec = spherogram.DTcodec(dt)
    return codec.encode(header=False)

infile = open('../manifold_src/original_manifold_sources/nonalternating_knots_15.csv',
              newline='')
outfile = open('nonalternating_knots_15.csv', 'w', newline='')
out = csv.writer(outfile, lineterminator=os.linesep)
for row in csv.reader(infile):
    if row[0] != 'id':
        row[3] = add_signs(row[3])
    out.writerow(row)
outfile.close()
    
