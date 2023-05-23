import flask
import firebase_admin
# from firebase_admin import db
from firebase_admin import firestore
from flask import request, Response
app = flask.Flask(__name__)


@app.route('/')
def extract_name():
    res = "Paxi server is up"
    cred_obj = firebase_admin.credentials.Certificate(r"C:\Users\Hadar\Desktop\paxi\paxi-2926b-firebase-adminsdk-yqehw-fe79636c2c.json")
    firebase_admin.initialize_app(cred_obj, {
	'databaseURL':"https://console.firebase.google.com/u/0/project/paxi-2926b/database"})
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



