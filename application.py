import os
from flask import Flask,redirect,render_template,request,send_from_directory,send_file,url_for,current_app,json
from werkzeug.utils import secure_filename
import requests
import shutil
import shlex
import json
import subprocess
import random
#/Users/casper.local/Desktop/Dev/remove_BG/static/Background-Images/
#Background = os.path.join('static', 'Background-Images')
Background = '/Users/casper.local/Desktop/Dev/remove_BG/static/Background-Images/'
#/Users/casper.local/Desktop/Dev/remove_BG/static/Non-Background-Images/
#NonBackground = os.path.join('static','Non-Background-Images')
NonBackground = '/Users/casper.local/Desktop/Dev/remove_BG/static/Non-Background-Images/'
keys = ['cR5VuqsG332s9idv336LrFB4','BJckx2EsNiChs7EmXxq5gRkU','Fx7h8ohWhpsZSZ4GWdbt75Pf','QwebGn4QUwrbwtmpR9VX7GgS','gJJfbMfeHi6782ofpjitppB3','8HUvQ1tmMsDzUqdANBAUoewp','bV84X5XMLP9stMjm2ZTpdH9s','wtFEZ6dsQByaoq7bdWmsJFDM','2QTtcJNDa49C712LduU912Dm','sxTn9Sak1uZVB48Wy5kSjE6v','7dkXHUWEhaeMLEYsSUr2E6AJ','Sm2VhtgBp7JdrQKEmdovnMQL','6aRy3y7DrorYKQKQozHD1Xpn','kgsDsedicqEY7MxEw4Uew14X','1qVKUAaceLTjSc2yxbEx4dRb','2i6BwmrQCZbMGDVijcyLo8Vs','tJX6juHhBQgkDQpSozpUwj8S','Te6S2RtkqzqxLqpSrTvbpM5W','iPADopHkRrXvz47n1ZmXj2QU']
app = Flask(__name__)
app.config['SECRET_KEY'] = "073129749013740932ABFG879076543"
app.config['UPLOAD_FOLDER'] = Background
app.config['DOWNLOAD_FOLDER'] = NonBackground
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]

def allowed_image(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

@app.route('/download/<path:filename>')
def downloads(filename):
    uploads = os.path.join(current_app.root_path, app.config['DOWNLOAD_FOLDER'])
    try:
        return send_from_directory(directory=uploads, filename=filename,as_attachment=True)
    except:
        return send_file(filename)


@app.route("/", methods=["GET", "POST"])
def upload_image():
    data=[]
    if request.method == "POST":
        # for file in os.listdir(os.getcwd()+"/static/Background-Images"):
        #     os.remove(os.path.join(os.getcwd()+"/static/Background-Images", file))
        # for file in os.listdir(os.getcwd()+"/"+"static/Non-Background-Images"):
        #     os.remove(os.path.join(os.getcwd()+"/"+"static/Non-Background-Images",file))
        image = request.files["image"]
        print(image)
        if image.filename == "":
            data['error']="No filename"
            res = app.response_class(response=json.dumps(data),
                                          status=400,
                                          mimetype='application/json')

            print("No filename")
            #return redirect(request.url)
            return res
        if allowed_image(image.filename):
            filename = secure_filename(image.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(filepath)
            image.save(filepath)
            while True:
                try:
                    response = requests.post(
                        'https://api.remove.bg/v1.0/removebg',
                        files={'image_file': open(filepath, 'rb')},
                        data={'size': 'auto'},
                        headers={'X-Api-Key': random.choice(keys)},
                    )
                    if response.status_code == requests.codes.ok:
                        with open(filename, 'wb') as out:
                            out.write(response.content)
                        shutil.move(os.getcwd() + "/" + filename, os.getcwd() + "/static/Non-Background-Images")

                        data['nonbackground']=filename
                        data['background']=filepath
                        res = app.response_class(response=json.dumps(data),
                                                     status=200,
                                                     mimetype='application/json')
                        #return render_template('index.html', con=filename, data=filepath)
                        return res
                    else:
                        print("Error:", response.status_code, response.text)
                        cmd = f'''curl -X POST -F "file=@{filepath}" "https://api.boring-images.ml/v1.0/transparent-net?api_key=ak-broad-haze-7fff750"'''
                        args = shlex.split(cmd)
                        process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        stdout, stderr = process.communicate()
                        print(stdout)
                        if (str(stdout).__contains__("error")):
                            pass
                        else:
                            response = json.loads(stdout.decode('utf-8'))
                            img = response['result']
                            data['nonbackground'] = img
                            data['background'] = filepath
                            res = app.response_class(response=json.dumps(data),
                                                         status=200,
                                                         mimetype='application/json')
                            #return render_template('index.html', uri=img, data=filepath)
                            return res
                except:
                    break
        else:
            data['error'] = "That file extension is not allowed"
            res = app.response_class(response=json.dumps(data),
                                          status=200,
                                          mimetype='application/json')
            print("That file extension is not allowed")
            #return redirect(request.url)
            return res


    #data['error']="Please use Token and Image file"
    res = app.response_class(response=json.dumps(data),
                             status=200,
                             mimetype='application/json')
    print("That file extension is not allowed")
    # return redirect(request.url)
    return res
    #return render_template('index.html')

if __name__== '__main__':
    app.run(debug=True)


