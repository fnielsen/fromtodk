"""AWS.dk.

Functions related to addresses in Denmark through aws.dk

References
----------
- http://aws.dk/

"""


from __future__ import division, print_function

from collections import OrderedDict

import csv

from os.path import expanduser


ADRESSER_FILENAME = expanduser('~/data/awsdk/adresser')


class AdresserFile(object):
    """Encapsulate an 'adresser' file."""

    def __init__(self, filename=ADRESSER_FILENAME):
        """Initialize reading of CSV file."""
        self.filename = ADRESSER_FILENAME
        self.fid = open(self.filename)
        line = self.fid.readline().decode('utf-8')
        self.header = line.strip().split(',')
        self.csv_reader = csv.reader(self.fid)

    def __iter__(self):
        """Return iterator."""
        return self

    def __next__(self):
        """Iterate over rows in CSV file."""    
        row = next(self.csv_reader)
        return OrderedDict(zip(self.header,
                               [unicode(cell, 'utf-8') for cell in row]))

    next = __next__

    def make_address_coordinate_map(self):
        """Make map between address and geocoordinates.

        Returns
        -------
        map : dict
            Dictionary with addresses as key and coordinates as values.

        """
        map = {}
        for n, address in enumerate(self):
            key = "{} {} {}".format(address['vejnavn'], address['husnr'],
                                    address['postnr'])
            coordinate = (address[u'wgs84koordinat_bredde'],
                          address[u'wgs84koordinat_l\xe6ngde'])
            map[key] = coordinate
        return map


def main():
    """Handle command-line interface."""
    pass


if __name__ == '__main__':
    main()
