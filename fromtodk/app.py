"""Flask webapp."""

from __future__ import absolute_import

from flask import Flask, request, render_template

from .wikidata import search_wikidata_entities, get_distance_from_qids


app = Flask(__name__)


@app.route("/")
def index():
    """Index page for webapp."""
    from_ = request.args.get('f')
    to = request.args.get('t')
    from_qids = search_wikidata_entities(from_)
    to_qids = search_wikidata_entities(to)
    if len(from_qids) > 0 and len(to_qids) > 0:
        distance = get_distance_from_qids(from_qids[0], to_qids[0])
    else:
        distance = None
    return render_template("index.html", f=from_, t=to, distance=distance)
