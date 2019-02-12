import os
import json
import requests
import base64


from flask import Flask, request, send_from_directory, redirect, url_for, send_file, flash
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'docx', 'doc'}
URL = "https://192.168.1.60/UserCheck/TPAPI"

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if not os.path.exists(os.getcwd()+'/uploads'):
                os.mkdir(os.getcwd()+'/uploads')
            file.save(os.getcwd()+'/uploads/'+filename)
            return redirect(url_for('return_cleaned_file',filename=filename)) 
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload file to clean</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/return-files/<filename>')
def return_cleaned_file(filename):
    with open(os.getcwd()+'/uploads/'+filename, 'rb') as file_to_send:
        encoded_file = base64.b64encode(file_to_send.read()).decode('ascii')
    #Check if file isn't empty
    if encoded_file == "":
        flash('File is empty! Please, try again!')
        return redirect(url_for('upload_file'))

    data = {"request":[{
            "protocol_version": "1.1",
            "request_name": "UploadFile",
            "file_enc_data": encoded_file,
            "file_orig_name": filename,
            "scrub_options": {"scrub_method": 2},
            "te_options": {
                "file_name": filename,
                "features": ["te"],
                "te": {"rule_id": 1}
                }
           }]
           }
    
    #Serialize data to json
    request_json = json.dumps(data)
    #Generate API request
    res = requests.post(url=URL,data=request_json,headers={'Content-Type':'application/octet-stream'},verify=False) 
    #Get application/json data
    resp = res.json()
    #Encode into json
    json_data = json.dumps(resp)
    #Decode from json
    parsed_json = json.loads(json_data)
    
    cleaned_file_enc = parsed_json["response"][0]["scrub"]["file_enc_data"]
    cleaned_file_dec = base64.b64decode(cleaned_file_enc)
    if not os.path.exists(os.getcwd()+'/cleaned_files/'):
        os.mkdir(os.getcwd()+'/cleaned_files/')
    #Save cleaned file into dir
    output = open(os.getcwd()+'/cleaned_files/'+filename+".cleaned.pdf", "wb")
    output.write(cleaned_file_dec)
    output.close()
    return send_file(os.getcwd()+'/cleaned_files/'+filename+".cleaned.pdf", mimetype='application/pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4447)
