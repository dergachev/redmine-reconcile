"""
See http://code.google.com/p/google-refine/wiki/ReconciliationServiceApi.
See https://github.com/mikejs/reconcile-demo
"""
import re

from flask import Flask, request, jsonify, json
app = Flask(__name__)

def search(query):

    try:
      int(query)
    except ValueError:
      return []
  
    matches = []
    matches.append({
        "id": query,
        "name": query,
        "score": 100,
        "match": True,
        "type": [
            {"id": "/evolvingweb/redmine-issues",
             "name": "Evolving Web Redmine Issue"}]})

    return matches


def jsonpify(obj):
    """
    Like jsonify but wraps result in a JSONP callback if a 'callback'
    query param is supplied.
    """
    try:
        callback = request.args['callback']
        response = app.make_response("%s(%s)" % (callback, json.dumps(obj)))
        response.mimetype = "text/javascript"
        return response
    except KeyError:
        return jsonify(obj)


@app.route("/redmine-reconcile", methods=['POST', 'GET'])
def reconcile():
    # If a single 'query' is provided do a straightforward search.
    query = request.form.get('query')
    if query:
        # If the 'query' param starts with a "{" then it is a JSON object
        # with the search string as the 'query' member. Otherwise,
        # the 'query' param is the search string itself.
        if query.startswith("{"):
            query = json.loads(query)['query']
        results = search(query)
        return jsonpify({"result": results})

    # If a 'queries' parameter is supplied then it is a dictionary
    # of (key, query) pairs representing a batch of queries. We
    # should return a dictionary of (key, results) pairs.
    queries = request.form.get('queries')
    if queries:
        queries = json.loads(queries)
        results = {}
        for (key, query) in queries.items():
            results[key] = {"result": search(query['query'])}
        return jsonpify(results)

    # If neither a 'query' nor 'queries' parameter is supplied then
    # we should return the service metadata.
    return jsonpify(metadata)

if __name__ == '__main__':
# TODO allow user to specify a subclass of TestAnalyzer to use
    import sys
    from sys import argv
    import argparse
    parser = argparse.ArgumentParser(description='Reconcile redmine issue IDs into proper linked records')

    parser.add_argument('record_view_url', metavar='record_view_url',
          help='URL to use in generating view links for each record, eg http://redmine-server.com/issues/{{id}}')
    args = parser.parse_args()
    record_view_url = args.record_view_url

    # Basic service metadata. There are a number of other documented options
    # but this is all we need for a simple service.
    metadata = {
        "name": "Redmine Reconciliation Service",
        "defaultTypes": [{"id": "/evolvingweb/redmine-issues", "name": "Evolving Web Redmine Issue"}],
        "view": { "url" : record_view_url }
    }

    app.run(debug=True)
