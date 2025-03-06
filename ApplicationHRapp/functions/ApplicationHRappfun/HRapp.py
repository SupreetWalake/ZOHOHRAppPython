import logging
from flask import Request, make_response, jsonify, render_template,Flask
import json
import zcatalyst_sdk
import os

tableName = 'Candidates'  # The table created in the Data Store
columnName = 'name'  # The column created in the table
colnm2 = 'email'
#app = Flask(__name__)

'''
Execute below command to install SDK in global for enabling code suggestions
-> python3 -m pip install zcatalyst-sdk
'''
JOBS = [
{'id': 1012,
 'title': "Senior Analyst",
 'location': 'San-Jose',
 'Experience': '3-4 Years'
 },
{'id': 1013,
 'title': "Senior Analyst",
 'location': 'San-Jose',
 'Experience': '3-4 Years'
 },
{'id': 1014,
 'title': "Senior Analyst",
 'Experience': '6 Years'
 },
 ]
def handler(request: Request):
	try:
		app = zcatalyst_sdk.initialize()
		logger = logging.getLogger()
		if request.path == "/":
			response = make_response(jsonify({
            'status': 'success',
            'message': 'Hello from HRapp.py'
        }), 200)
			return response
		elif request.path == "/add" and request.method == 'POST': 
			req_data = request.get_json()
			name = req_data.get("name")
			email = req_data.get("email")
			table = app.datastore().table('Candidates')
			row = table.insert_row({
            columnName: name,
			colnm2:email
            })
			response = make_response(jsonify({
                "message": "Thanks for Applying!"
            }), 200)
			return response
		elif request.path == "/app" and request.method == 'GET':
			response = make_response(jsonify({
				'status': 'success',
				'message': 'Hello from app.py'
			}), 200)

			return response
		else:
			app = zcatalyst_sdk.initialize()
			response = make_response('Unknown path')
			return {
				'status': 302,
				'headers': {
				'Location': '/index.html?status=success'
				}
			}
	except Exception as err:
		logger.error(f"Exception in to_do_list_function :{err}")
		response = make_response(jsonify({
                 "error": "Internal server error occurred. Please try again in some time."
        }), 500)
		return response
#print(name)
#apps = Flask(__name__)

'''@app.route("/jobs")
def Carrers():
    return render_template('candidate_view.html', jobs=JOBS)

if __name__=="__main__":
    app.run()'''