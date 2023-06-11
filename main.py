import flask
from datetime import date, datetime
import firebase_admin
# from firebase_admin import db
from firebase_admin import firestore
from flask import request, Response
app = flask.Flask(__name__)


@app.route('/')
def extract_name():
    res = "Paxi server is up"
    cred_obj = firebase_admin.credentials.Certificate(r"C:\Users\Hadar\Desktop\paxi\paxi-2926b-firebase-adminsdk-yqehw-fe79636c2c.json")
    firebase_admin.initialize_app(cred_obj, {'databaseURL':"https://console.firebase.google.com/u/0/project/paxi-2926b/database"})
    db = firestore.client()
    doc_ref = db.collection('routes').document('NJXWjum9WchLU3N58zad')
    doc = doc_ref.get()
    if doc.exists:
        print(f'Document data: {doc.to_dict()}')
    else:
        print('No such document!')
    # print(ref.get())
    return {"message": res}

# this commands the script to run in the given port


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)


def buildGraph():
    cred_obj = firebase_admin.credentials.Certificate(
        r"C:\Users\Hadar\Desktop\paxi\paxi-2926b-firebase-adminsdk-yqehw-fe79636c2c.json")
    firebase_admin.initialize_app(cred_obj, {
        'databaseURL': "https://console.firebase.google.com/u/0/project/paxi-2926b/database"})
    db = firestore.client()
    docsPacks = db.collection('packages').get()
    for doc in docsPacks:
        graph = {}
        s = doc.get('source')
        d = doc.get('destination')
        dDate = doc.get('date')
        cost = doc.get('cost')
        w = doc.get('weight')
        v = doc.get('volume')
        docsRoutes = db.collection('routes').get()
        for i in docsRoutes:
            if w <= i.get('weight') and v <= i.get('volume'):
                if datetime.strptime(i.get('date'), '%m/%d/%y %H:%M:%S') <= datetime.strptime(dDate, '%m/%d/%y %H:%M:%S'):
                    if cost >= i.get('cost'):
                        graph.update({i.get('futureRouteID'): i.get('cost')})
    PackMatch(graph, s, d, dDate, cost)


def PackMatch(Graph, source, destination, dDate, cost):
    currentDate = date.today()
#     create vertex set Q
#
# # Initialization
#
#     for each vertex v in Graph:
#         dist[v] = INFINITY
#         prev[v] = UNDEFINED
#         add v to Q
#
#     dist[source] = 0 # Distance from source to source
#
#     while Q is not empty:
#         u = vertex in Q
#         with min dist[u]
#         remove u from Q
#
#         for each neighbor v of u in range dates:
#             alt = dist[u] + length(u, v)
#             if alt < dist[v]:
#                 dist[v] = alt
#                 prev[v] = u
#                 cDate = Weight.date
#
#     if dist[destination] > cost:
#         return null
#
#     return dist[], prev[]


