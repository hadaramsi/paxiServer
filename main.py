import heapq

import flask
from datetime import date, datetime
import firebase_admin
# from firebase_admin import db
from firebase_admin import firestore
from flask import request, Response

app = flask.Flask(__name__)
cred_obj = firebase_admin.credentials.Certificate(
        r"C:\Users\Hadar\Desktop\paxi\paxi-2926b-firebase-adminsdk-yqehw-fe79636c2c.json")
firebase_admin.initialize_app(cred_obj, {
        'databaseURL': "https://console.firebase.google.com/u/0/project/paxi-2926b/database"})
db = firestore.client()

def buildGraph():
    print("in build graph")
    currentDate = date.today()

    docsPacks = db.collection('packages').get()
    for doc in docsPacks:
        if doc.get('driver') == "no":
            graph = {}
            docsDps = db.collection('deliveryPoints').get()
            for dp in docsDps:
                graph[dp.get('deliveryPointName')] = {}
            s = doc.get('source')
            d = doc.get('destination')
            dDate = doc.get('date')
            cost = doc.get('cost')
            w = doc.get('weight')
            v = doc.get('volume')
            docsRoutes = db.collection('routes').get()
            for r in docsRoutes:
                if w <= r.get('weight') and v <= r.get('volume') and datetime.strptime(r.get('date'), '%d/%m/%Y').date() > currentDate:
                    if datetime.strptime(r.get('date'), '%d/%m/%Y').date() <= datetime.strptime(dDate, '%d/%m/%Y').date():
                        if cost >= r.get('cost'):
                            graph[r.get('source')][r.get('destination')] = {'futureRouteID': r.get('futureRouteID'),
                                                                        'date': r.get('date'),
                                                                        'cost': r.get('cost')}
            distances = improvedDijkstra(graph, s)
            print("distances: \n")
            print(distances)
            if distances[d][0] != float('inf') and distances[d][0] <= cost:
                routes = checkMatch(distances, graph, s,  d)
                if routes is not []:
                    doc_driv = db.collection('drivers').document(r.get('driver'))
                    data = {
                        'cost': doc.get('cost'),
                        'date': doc.get('date'),
                        'destination': doc.get('destination'),
                        'driver': doc_driv.get().to_dict()['fullName'],
                        'ifRate': doc.get('ifRate'),
                        'note': doc.get('note'),
                        'packageID': doc.get('packageID'),
                        'pay': doc.get('pay'),
                        'rate': doc_driv.get().to_dict()['rate'],
                        'sender': doc.get('sender'),
                        'source': doc.get('source'),
                        'volume': doc.get('volume'),
                        'weight': doc.get('weight')
                    }
                    doc_pac = db.collection('packages').document(doc.get('packageID'))
                    doc_pac.set(data)
                    for i in routes:
                        doc_ref = db.collection('routes').document(i)
                        pacsList = doc_ref.get().to_dict()['packagesList'] + ", " + doc.get('packageID')
                        roteData = {
                            'cost': doc_ref.get().to_dict()['cost'],
                            'date': doc_ref.get().to_dict()['date'],
                            'destination': doc_ref.get().to_dict()['destination'],
                            'driver': doc_ref.get().to_dict()['driver'],
                            'futureRouteID': doc_ref.get().to_dict()['futureRouteID'],
                            'source': doc_ref.get().to_dict()['source'],
                            'volume': doc_ref.get().to_dict()['volume']-v,
                            'weight':  doc_ref.get().to_dict()['weight']-w,
                            'packagesList': pacsList
                        }
                        doc_ref.set(roteData)
                    print("Match !!!!!")


def checkMatch(distances, graph, s, d):
    routes = []
    tempDate = graph[distances[d][1]][d]
    current_vertex = distances[d][1]
    before = d
    while current_vertex is not None:
        if current_vertex == s:
            routes.append(graph[current_vertex][before]['futureRouteID'])
            return routes
        before = distances[current_vertex][1]
        temp = graph[before][current_vertex]
        if datetime.strptime(temp['date'], '%d/%m/%Y').date() < datetime.strptime(tempDate['date'], '%d/%m/%Y').date():
            routes.insert(tempDate['futureRouteID'])
            tempDate = graph[before][current_vertex]['date']
            current_vertex = before
        else:
            return []
    return routes


def improvedDijkstra(graph, start):
    distances = {}
    for vertex in graph:
        distances[vertex] = [float('inf'), None]
    distances[start][0] = 0
    priority_queue = [(0, start)]
    heapq.heapify(priority_queue)
    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        if current_distance > distances[current_vertex][0]:
            continue

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight['cost']
            if distance < distances[neighbor][0]:
                distances[neighbor][0] = distance
                distances[neighbor][1]=current_vertex
                heapq.heappush(priority_queue, (distance, neighbor))
    return distances


@app.route('/')
def extract_name():
    res = "Paxi server is up"
    buildGraph()
    return {"message": res}

# this commands the script to run in the given port


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

