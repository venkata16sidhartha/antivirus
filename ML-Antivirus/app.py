from flask import Flask, render_template, request
from werkzeug import secure_filename
import os
app = Flask(__name__)
#app.config['UPLOAD_FOLDER']="uploads"
@app.route('/')
def upload_file_1():
   return render_template('upload.html')
	
@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      data=os.popen("python3 antivirus.py "+secure_filename(f.filename)).read()
      print(len(data))
      os.system("rm "+secure_filename(f.filename))
      if data=="0\n":
          return render_template("danger.html")
      elif data=="1\n":          
          return render_template("safe.html")
      else:
          return "Not a proper .EXE file"

@app.errorhandler(404)
def page_not_found(error):
	app.logger.error('Page not found: %s', (request.path))
	return render_template('404.html')

@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error('Server Error: %s', (error))
    return render_template('500.html')



if __name__ == '__main__':
   app.run()
