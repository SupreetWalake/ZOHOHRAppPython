import logging
from flask import Request, make_response, redirect, jsonify, send_file, render_template,Flask, Response
import json
import zcatalyst_sdk
from werkzeug.utils import secure_filename
import os
from io import BufferedReader
import io

tableName = 'Candidates'  # The table created in the Data Store
columnName = 'name'  # The column created in the table
colnm2 = 'email'
#apps = Flask(__name__)

#app = zcatalyst_sdk.initialize()

# Mock database


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
			name = request.form.get('name')
			email = request.form.get('email')
			resume = request.files.get('resume')


			if resume is None:
				return {"error": "No file uploaded or file field is missing."}, 400
			filename = secure_filename(resume.filename)

			

			file_content = resume.read()
			table = app.datastore().table('Candidates')

			if not file_content:
				return {"error": "File content is empty."}, 400

	
			filestore_service = app.filestore()

			folder = filestore_service.folder(9405000000012881)
			
			buffer_reader = io.BytesIO(file_content)
			#print("Request Files:", request.files)

			'''if resume:
				print("File Name:", resume.filename)
				print("File Content (first 100 bytes):", file_content[:100])'''

			row = table.insert_row({
            columnName: name,
			colnm2:email
            })

			response = make_response(jsonify({
                "message": "Thanks for Applying!"
            }), 200)
			try:
				#with open(filename, 'rb') as file:
					#buffered_reader = buffer_reader#BufferedReader(resume)
				#resume.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				buffered_file = io.BufferedReader(buffer_reader)# io.BufferedReader(file.stream)
				folder.upload_file(resume.filename,buffered_file)
				return make_response(jsonify({'message': 'Job Applied Successfully. Thanks for Applying!'}),200)
			except Exception as e:
				return make_response(jsonify({'error': str(e)}), 500)
			
		elif request.path == "/login":
			##
			
			response_body = """<!DOCTYPE html>
<html lang="en">
<head>
<script src="https://static.zohocdn.com/catalyst/sdk/js/4.4.0/catalystWebSDK.js"></script>
	<script src="/__catalyst/sdk/init.js"></script>
<script>
  const config = {
  signin_providers_only : true, 
  };
  /* config is optional/*
  {
    css_url : "/embeddediframe.css", // Provide your custom CSS file path here. If no path is provided default css will be rendered
    service_url : "https://aliencity-60032381908.development.catalystserverless.in/server/ApplicationHRappfun/loginhr", // This value is optional. You can provide your redirect URL here.
   // is_customize_forgot_password : true, // Default value is false. Keep this value as true, if you wish to customize Forgot Password page
    //forgot_password_id : "forgotPasswordDivElementId", // The Element id in which forgot password page should be loaded,If no value is provided, it will be rendered in the "loginDivElementId" by default
    //forgot_password_css_url : "/css/forgotPwd.css" // Provide your custom CSS file path for the Forgot Password page.If no path is provided,then the default CSS will be rendered.
  } 
  catalyst.auth.signIn("loginDivElementId", config);
</script>
<div class="signup" id="signup" >
<form class="modal-content" onsubmit="signupAction(this);return false;">
<div class="center">
<h2 style="margin-top: -40px;">Sign Up</h2>
<p>Please fill this form to sign up for a new account.</p>
</div>
</head>
<body style="background: #c0c0c0">
<div id="loginDivElementId">
<label for="firstname"><b>First Name</b></label>
<inputid="firstname"type="text"placeholder="Enter First Name"name="firstname"required/>
<label for="lastname"><b>Last Name</b></label>
<inputid="lastname"type="text"placeholder="Enter Last Name"name="lastname"required/>
<label for="email"><b>Email</b></label>
<inputid="mailid"type="text"placeholder="Enter Email address"name="email"required/>
</div>
</body>
</html>
"""
			return response_body
		elif request.path == "/loginhr":
			auth = app.authentication()
			resp = auth.generate_custom_token({
				'type':'web',
				'user_details':{
					'email_id': '{email_id}',
					}
					})
		elif request.path == "/hrview":
			app = zcatalyst_sdk.initialize()

			table = app.datastore().table('Candidates')
			zcql_service = app.zcql()
			rows = zcql_service.execute_query('SELECT name,email FROM Candidates order by CREATEDTIME')
			mail_service = app.email()
			
			
			'''for row in rows:
				print(row['Candidates']['name'])
				print(row['Candidates'])'''
			

			response_body = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HR View</title>
    <link rel="stylesheet" href="{{url_for('static', filename='style.css')}}">
	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
	

</head>
<body>
<div class="container">
    <h1 class="my-4">HR View</h1>
	<h3 class="my-3">List of Candidates</h3>
	<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>

  <div class="card">
            <div class="card-body">
  <table border="1" class="table table-primary table-striped table-bordered">
    <thead>
            <tr>
                <th>Name</th>
                <th>Email</th>
				<th>Resume</th>
                <th>Action</th>
            </tr>
        </thead>
		<tbody>
  """
			rows_html = []

			for index,row in enumerate(rows):
				nm = row.get('Candidates', {}).get('name', 'N/A')
				em = row.get('Candidates', {}).get('email', 'N/A')
				file_id = {index}
				print(file_id)
				rows_html.append(f"""
            <tr>
                <td>{nm}</td>
                <td>{em}</td>
				<td>
                    <a href="https://aliencity-60032381908.development.catalystserverless.in/server/ApplicationHRappfun/resume-download/?index={index}">Resume Download</a>
                </td>
                <td>
                    <a href="#" class="approve-link" data-email="{em}">Approve</a>
                </td>
            </tr>
    """)
			response_body += "\n".join(rows_html)
			response_body += """
			</tbody>
			
			</table>
			 </div>
        </div>
        <div class="alert alert-success" role="alert" id="status-message" style="display:none;"></div>
    </div>
		<script>
        document.addEventListener('DOMContentLoaded', function() {
            const approveLinks = document.querySelectorAll('.approve-link');
            approveLinks.forEach(link => {
                link.addEventListener('click', function(event) {
                    event.preventDefault(); // Prevent the default link behavior
					const email = this.getAttribute('data-email');
                    fetch(`https://aliencity-60032381908.development.catalystserverless.in/server/ApplicationHRappfun/approve?email=${email}`, {
                        method: 'GET'
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            // Change the link text to "Approved"
                    		this.innerText = 'Approved';
                    		this.classList.add('disabled'); // Add a class to style as disabled
                        	this.style.pointerEvents = 'none';
                    		const statusMessage = document.getElementById('status-message');
                    		statusMessage.innerText = data.message; // "Mail sent Successfully"
                    		statusMessage.style.display = 'block';
                        } else {
                            alert('Failed to approve candidate.');
                        }
					});
                });
            });
        });
		</script>
		 <style>
		 .disabled {
		 color: green;
		 pointer-events: none; 
		 text-decoration: none; 
		 }
		</style>
			</body>
			</html>
        	"""
			
			return response_body
		elif request.path == "/approve" and request.method == 'GET':
				app = zcatalyst_sdk.initialize()
				mail_service = app.email()
				def approveEmail():
					email = request.args.get('email')
					mail_obj = {
					'from_email': 'supreetwalake@gmail.com',
					'to_email':[email],
					'subject': 'Greetings from ZOHO!',
					'content': """Hello, 
We're glad to welcome you at ZOHO.We cannot wait to get started!
					
Cheers!
Team ZOHO"""
					}
					response = mail_service.send_mail(mail_obj)
					return jsonify(success=True, message="Mail sent Successfully")
				return approveEmail()
		elif request.path == "/app" and request.method == 'GET':
			response = make_response(jsonify({
				'status': 'success',
				'message': 'Hello from app.py'
			}), 200)

			return '/hr_view.html'
		elif request.path == "/resume-download":
			app = zcatalyst_sdk.initialize()
			filestore_service = app.filestore()
			folder_service=filestore_service.folder(9405000000012881)
			data = filestore_service.get_folder_details(9405000000012881)
			file_ids = [file['id'] for file in data['file_details']]
			index1 = int(request.args.get('index'))
			print(index1) # index value from for loop(name,email)
			print(file_ids) #file - ids from folder details

			
			# Set the filename and content type as needed
			file_info = []
			
			for file in data['file_details']:
				file_id = file['id']
				file_name = file['file_name']
				file_info.append({'id': file_id, 'file_name': file_name})# file_info=[{id:96203402342,file_name:sample.txt}]

			neg_idx= -(index1+1)
			new_file_id=file_info[neg_idx]['id']
			new_file_name=file_info[neg_idx]['file_name']

			def get_file_type(file_name):
				# Split the file name into name and extension
				_, extension = os.path.splitext(file_name)
				return extension.lower()  # Return the extension in lower case


			file_type = get_file_type(new_file_name)

			file_data= folder_service.download_file(new_file_id)
			byte_stream = io.BytesIO(file_data)

			filename = f'file_{new_file_id}{file_type}'
			def download_file_fun(n):
				downloded_file=folder_service.download_file(n)
				return downloded_file
			return send_file(byte_stream, as_attachment=True, download_name=filename)

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
