from flask import Flask, flash, Response, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from io import StringIO
import siap_import

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
app = Flask(__name__)

def process(request, processor):
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect('/')
    file = request.files.get('file')
    if not file or file.filename == '' or not allowed_file(file.filename):
        flash('No selected file')
        return redirect('/')
    if file and allowed_file(file.filename):
        result, filename = processor(file)
        headers = {"Content-disposition": f"attachment; filename={filename}"}
        return Response(result, mimetype="text/plain", headers=headers)

@app.route('/voucher', methods=["POST"])
def voucer():
    return process(request, siap_import.process_voucher_raw)

@app.route('/aliquot', methods=["POST"])
def aliquot():
    return process(request, siap_import.process_aliquot_raw)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    return '''
    <!doctype html>
    <title>SIAP Import</title>
    <h1>Upload AFIP export</h1>
    <script src="https://code.jquery.com/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>
    <form id="siap" method=post enctype=multipart/form-data>
      <input type=file name=file><br/>
      <input id=download type=button value="Descargar para SIAP">
      <script>
            var $download = $('#download');
            var $form = $('#siap');
            function download(endpoint) {
                $form.attr('action', endpoint).submit();
            }
            $download.on('click', function() {
                download('/voucher');
                setTimeout(function() {
                    download('/aliquot');
                }, 500);
            });
      </script>
    </form>
    '''

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    print("Init app in port 5000")
    app.run(port=5000, debug=True)