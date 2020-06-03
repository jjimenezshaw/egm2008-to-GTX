#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import struct

def main(src, dst):
    with open(dst, 'wb') as gtx:
        with open(src, 'r') as infile:
            header = infile.readline()
            h = header.split()
            
            lat = float(h[0])
            lng = float(h[1])
            dlat = float(h[2]) / 60.0
            dlng = float(h[3]) / 60.0
            nrows = int(h[4])
            ncols = int(h[5])

            lat -= (nrows - 1) * dlat
            if lng > 180:
                lng -= 360.0

            gtx.write(struct.pack('>ddddii', lat, lng, dlat, dlng, nrows, ncols))

            counter = 0
            rows = []
            row = []
            data = infile.readlines()
            for datum in data:
                line = datum.split()
                counter += len(line)
                row += [float(j) for j in line]
                if len(row) >= ncols:
                    rows.append(row[:ncols])
                    row = row[ncols:]

            for row in reversed(rows):
                gtx.write(struct.pack('>'+'f'*len(row), *row))

            if counter != nrows*ncols:
                raise RuntimeError("Expected " + str(nrows*ncols) + " values but found " + str(counter))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Convert txt file to GTX binary.')
    parser.add_argument('src', help='source TXT file')
    parser.add_argument('dst', help='destination GTX file')

    args = parser.parse_args()
    main(args.src, args.dst)
