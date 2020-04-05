# [START gae_python37_app]
from flask import Flask
from flask import request
from google.cloud import firestore
from google.oauth2 import service_account
import jinja2
import logging

app = Flask(__name__)

def appString(name):
  return db.collection(u'app-string').document(name).get().get('en');

def getCategory(key):
  return db.collection(u'categories').document(key).get().get('name');

def getCategories():
  stream = db.collection(u'categories').stream();
  categories = []
  for category in list(stream):
    categories.append(formatCategory(category))
  return categories

def getNeighborhood(key):
  return db.collection(u'neighborhoods').document(key).get().get('name');

def getBusiness(key):
  return formatBusiness(db.collection(u'businesses').document(key).get());


def getBusinesses(category):
  if category != None and category != '':
    docref = db.collection(u'categories').document(category)
    stream = db.collection(u'businesses').where(u'category', u'array_contains', docref).stream()
  else:
    stream = db.collection(u'businesses').stream()
  businesses = []
  for business in list(stream):
    businesses.append(formatBusiness(business))
  return businesses

def formatCategory(category):
  categoryDict = category.to_dict()
  categoryDict['id'] = category.id
  return categoryDict

def formatBusiness(business):
  businessDict = business.to_dict()
  businessDict['id'] = business.id
  businessDict['displayCategory'] = getCategory(business.get('category')[0].id)
  businessDict['displayNeighborhood'] = getNeighborhood(business.get('neighborhood').id)
  return businessDict


db = firestore.Client(credentials=service_account.Credentials.from_service_account_file(
    'config/shoplocalse.json'))
templateLoader = jinja2.FileSystemLoader(searchpath='./')
templateEnv = jinja2.Environment(loader=templateLoader)
templateEnv.globals.update(s=appString)


@app.route('/')
def homepage():
    filter = request.args.get('filter')
    return templateEnv.get_template('templates/homepage.html').render(businesses=getBusinesses(filter), categories=getCategories(), filter=filter)

@app.route('/connect')
def connect():
    id = request.args.get('id')
    return templateEnv.get_template('templates/connect.html').render(business=getBusiness(id))

@app.route('/transaction')
def transaction():
    id = request.args.get('id')
    return templateEnv.get_template('templates/transaction.html').render(business=getBusiness(id))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]