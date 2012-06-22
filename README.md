redmine-reconcile
=================

Google Refine reconciliation service implementation for Redmine issues
This makes Google Refine render each redmine issue ID as a clickable link.

![screenshot](http://dl-web.dropbox.com/u/29440342/screenshots/Screen%20Shot%202012-06-22%20at%204.08.56%20PM.png)

At the moment all it does is blindly verifies any integer to itself, and provides the following metadata:

    metadata = {
      "name": "Redmine Reconciliation Service",
      "defaultTypes": [{"id": "/evolvingweb/redmine-issues", "name": "Redmine ID"}],
      "view": { "url" : "http://your-redmine-server.com/issues/{{id}}" } 
    }```

Note that the metadata.view.url comes from a command line argument to the script

Requirements
------------
Requires python and flask, a python microframework with a built-in server:
    pip install flask

Starting the server
-------------------

To start the service:
    python redmine-reconcile.py 'http://your-redmine-server.com/issues/{{id}}'

To use in Google Refine:
* Select a column containing numeric redmine IDs > Reconcile > Start Reconciling...
* Add the following reconciliation service URL: http://localhost:5000/redmine-reconcile
* Click "Start Reconciling"

TODO
----
* do something interesting (reconcile by title?)

Inspiration
-----------
This was adapted from the following:

See http://code.google.com/p/google-refine/wiki/ReconciliationServiceApi.
See https://github.com/mikejs/reconcile-demo
