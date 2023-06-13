import heapq

import flask
from datetime import date, datetime
import firebase_admin
# from firebase_admin import db
from firebase_admin import firestore
from flask import request, Response
from jinja2.nodes import Node

app = flask.Flask(__name__)


def buildGraph():
    print("in build graph")
    currentDate = date.today()
    cred_obj = firebase_admin.credentials.Certificate(
        r"C:\Users\Hadar\Desktop\paxi\paxi-2926b-firebase-adminsdk-yqehw-fe79636c2c.json")
    firebase_admin.initialize_app(cred_obj, {
        'databaseURL': "https://console.firebase.google.com/u/0/project/paxi-2926b/database"})
    db = firestore.client()
    docsPacks = db.collection('packages').get()
    for doc in docsPacks:
        graph = {}
        docsDps = db.collection('deliveryPoints').get()
        for dp in docsDps:
            graph[dp.get('deliveryPointName')] = {}
            # graph.update({dp.get('deliveryPointName') : {}})
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
                        # graph.update({r.get('source'): r.get('destination')} {r.get('futureRouteID'): r.get('cost')}})
        # print(graph)
        nodes= dijkstra(graph, s)
        # nodes = PackMatch(graph, s, d, cost)
        if nodes[d][0]!= float('inf'):
            pass
        print( " this is what we wont to seeeeee")
        print(nodes)


def dijkstra(graph, start):
    distances = {}
    for vertex in graph:
        distances[vertex] = [float('inf'), None]
    distances[start][0] = 0

    priority_queue = [(0, start)]
    heapq.heapify(priority_queue)
    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        # Ignore outdated entries in the priority queue
        # print("1111111" + str(distances))
        if current_distance > distances[current_vertex][0]:
            continue

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight['cost']
            # print(neighbor)
            # print("weight['cost']-----" + str(weight['cost']))
            if distance < distances[neighbor][0]:
                distances[neighbor][0] = distance
                distances[neighbor][1]=current_vertex
                heapq.heappush(priority_queue, (distance, neighbor))
    return distances


# def PackMatch(graph, source, destination, cost):
#   nodes = {}
#   c = 0
#   for node in graph:
#       nodes[node] = Node()
#   nodes[source].d = 0
#   queue = [(0, source)] #priority queue
#   while queue:
#       d, node = heapq.heappop(queue)
#       if nodes[node].finished:
#           continue
#       nodes[node].finished = True
#       for neighbor in graph[node]:
#           if nodes[neighbor].finished:
#               continue
#           new_d = d+graph[node][neighbor]
#           if new_d < nodes[neighbor].d:
#               nodes[neighbor].d = new_d
#               nodes[neighbor].parent = node
#               heapq.heappush(queue, (new_d, neighbor))
#   return nodes


# def PackMatch(Graph, source, destination, dDate, cost):
#     currentDate = date.today()
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

@app.route('/')
def extract_name():
    res = "Paxi server is up"
    buildGraph()
    return {"message": res}

# this commands the script to run in the given port


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)


