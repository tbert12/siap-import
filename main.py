from flask import Flask, flash, Response, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from io import StringIO
import siap_import

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files.get('file')
        if not file or file.filename == '' or not allowed_file(file.filename):
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            result = siap_import.process_raw(file)
            name = file.filename.rsplit('.', 1)[0].replace(' ', '').replace('"', '')
            final_name = f"sirap-{name}.txt"
            headers = {"Content-disposition": f"attachment; filename={final_name}"}
            return Response(result, mimetype="text/plain", headers=headers)
    return '''
    <!doctype html>
    <title>SIAP Import</title>
    <h1>Upload AFIP export</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    print("Init app in port 5000")
    app.run(port=5000, debug=True)