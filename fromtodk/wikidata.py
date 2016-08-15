"""Wikidata."""

import re

from geopy.distance import vincenty

import requests

import sparql


USER_AGENT = 'fromtodk, https://github.com/fnielsen/fromtodk'

SPARQL_COORDINATES_PATTERN = """
select ?latitude ?longitude where {{
  wd:{} p:P625 ?coordinate_statement .
  ?coordinate_statement psv:P625 ?coordinate_node .
  ?coordinate_node wikibase:geoLatitude ?latitude .
  ?coordinate_node wikibase:geoLongitude ?longitude .
}}  
"""


def search_wikidata_entities(query, language='da', return_type='qids'):
    """Search with the Wikidata API for entities.

    This function will query the Wikidata API and a such require Internet
    access.

    Parameters
    ----------
    query : str
        Query string

    Returns
    -------
    qids : list of str
        List of strings with Q identifiers

    """
    url = 'https://www.wikidata.org/w/api.php'
    params = {
        'action': 'wbsearchentities',
        'language': language,
        'format': 'json',
        'search': query
    }
    headers = {'User-agent': USER_AGENT}
    response = requests.get(url=url, params=params, headers=headers)
    data = response.json()
    if 'search' in data:
        qids = [item['id'] for item in data['search']]
    else:
        qids = []
    return qids


def is_wikidata_qid(qid):
    """Check if well-formed Q identifier.

    Parameters
    ----------
    qid : str
        String with Q-identifier

    Returns
    -------
    answer : bool
        Boolean with true if it fits the pattern

    Examples
    --------
    >>> is_wikidata_qid('Q1748')
    True

    >>> is_wikidata_qid('q1748')
    False

    >>> is_wikidata_qid('1748')
    False

    >>> is_wikidata_qid('Q')
    False

    """
    if re.match('Q\d+', qid):
        return True
    return False


def get_wdqs_coordinates(qid):
    query = SPARQL_COORDINATES_PATTERN.format(qid)
    service = sparql.Service('https://query.wikidata.org/sparql',
                             method='GET')
    response = service.query(query)
    coordinate_list = response.fetchall()
    try:
        latitude, longitude = (
            coordinate_list[0][0].value, coordinate_list[0][1].value)
        return float(latitude), float(longitude)
    except:
        return None, None


def get_coordinates_from_qid(qid):
    """Get coordinates from a Wikidata item.
    
    None is returned if a coordinate is not found.

    Parameters
    ----------
    qid : str
        String it Q-identifier

    Returns
    -------
    lat : float or None
        Latitude.
    long : float or None
        Longitude.

    Examples
    --------
    >>> lat, long = get_coordinates('Q1748')   # Kongens Lyngby
    >>> round(lat), round(long)
    (56.0, 13.0)

    """
    return get_wdqs_coordinates(qid)


def get_distance_from_qids(from_qid, to_qid):
    """Get distance between to Wikidata items.

    Parameters
    ----------
    from_qid : str
        String with Q-identifier
    to_qid : str
        String with Q-identifier

    Returns
    -------
    distance : float or None
        Distance in kilometer. None is returned if 

    Examples
    --------
    >>> distance = get_distance('Q1748', 'Q2239')
    >>>

    """
    from_lat, from_long = get_coordinates_from_qid(from_qid)
    to_lat, to_long = get_coordinates_from_qid(to_qid)
    if (from_lat is None or from_long is None or to_lat is None or
        to_long is None):
        return None
    distance = vincenty((from_lat, from_long), (to_lat, to_long))
    distance_in_km = distance.km
    return distance_in_km
