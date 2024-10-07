# src/routes/routes.py
from flask import Blueprint
from controllers.sqlController import sqlCtrl
from controllers.gptController import gptCtrl
route = Blueprint('TEST', __name__)

class Routes:

    route.route('/test', methods=['GET'])(sqlCtrl.test) # http://localhost:5000/test GET
    
    route.route('/testGpt', methods=['POST'])(gptCtrl.testGpt) # http://localhost:5000/testGpt POST
    
    route.route('/querySql', methods=['POST'])(sqlCtrl.querySql) # http://localhost:5000/querySql POST
    
    route.route('/getFilters', methods=['GET'])(sqlCtrl.getFilters) # http://localhost:5000/getFilters GET
    
    route.route('/testRag', methods=['POST'])(sqlCtrl.testRag) # http://localhost:5000/testRag POST
    