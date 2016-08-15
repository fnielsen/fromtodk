"""Flask webapp."""

from __future__ import absolute_import

from flask import Flask, request

from .wikidata import search_wikidata_entities, get_distance_from_qids


HTML_TEMPLATE = """
<html>
  <body>
    <form>
      <input name="f">
      <input name="t">
      <input type=submit>
    </form>
    <div>
      Distance: {} 
    </div>
    <div>
      <a href="https://github.com/fnielsen/fromtodk">https://github.com/fnielsen/fromtodk</a>
    </div>

  </body>
</html>
"""


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
    return HTML_TEMPLATE.format(distance)


