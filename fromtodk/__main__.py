"""fromtodk

Usage:
  fromtodk [options] <from> <to>

Options:
  -h --help     Print help message
  -v --verbose  Verbose

Examples:
  $ python -m fromtodk "Lyngby Hovedgade" Aros
  150.135086498

"""

from __future__ import division, print_function

import sys

from docopt import docopt

from .wikidata import search_wikidata_entities, get_distance_from_qids


def main():
    """Handel command-line interface."""

    reload(sys)
    sys.setdefaultencoding("utf-8")

    args = docopt(__doc__)

    verbose = args['--verbose']

    from_qids = search_wikidata_entities(args['<from>'])
    if verbose:
        print(from_qids)
    to_qids = search_wikidata_entities(args['<to>'])
    if verbose:
        print(to_qids)

    distance = get_distance_from_qids(from_qids[0], to_qids[0])
    if distance:
        print(distance)
    elif distance is None:
        print()


if __name__ == '__main__':
    main()
