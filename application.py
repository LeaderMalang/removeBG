import os
from flask import Flask,redirect,render_template,request,send_from_directory,send_file,url_for,current_app,json,jsonify
from flask_cors import CORS,cross_origin
from werkzeug.utils import secure_filename
import requests
import shutil
import shlex
import json
import subprocess
import random
from rembg.bg import remove
import numpy as np
import io
from PIL import Image,ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import pathlib
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
cors = CORS(app, resources={r"/": {"origins": "*"}})
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

@app.route('/test', methods=["GET", "POST"])
@cross_origin()
def upload_Image():
    data={"error":'','nonbackground':'','background':''}
    token=request.form['token']
    if request.method == "POST" and token=='hello':
        # for file in os.listdir(os.getcwd()+"/static/Background-Images"):
        #     os.remove(os.path.join(os.getcwd()+"/static/Background-Images", file))
        # for file in os.listdir(os.getcwd()+"/"+"static/Non-Background-Images"):
        #     os.remove(os.path.join(os.getcwd()+"/"+"static/Non-Background-Images",file))
        image = request.files['image']
        imgfilename = request.form['name']
        #print(image)
        if imgfilename == "":
            # data={"error":"No filename"}
            data['error']="No filename"
            res = app.response_class(response=json.dumps(data),
                                     status=400,
                                     mimetype='application/json')

            print("No filename")
            #return redirect(request.url)
            return res
        if allowed_image(imgfilename):
            filename = secure_filename(imgfilename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(filepath)

            image.save(filepath)


            output_path  = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)

            f = np.fromfile(filepath)
            result = remove(f)
            img = Image.open(io.BytesIO(result)).convert("RGB")
            img.save(output_path)
            data['nonbackground'] = request.url_root + "static/Non-Background-Images/" + filename
            data['nonbackgroundurl'] = output_path
            res = app.response_class(response=json.dumps(data),
                                     status=200,
                                     mimetype='application/json')
            return res
    else:
        data['error']="Token Invalid "
        res = app.response_class(response=json.dumps(data),
                                 status=200,
                                 mimetype='application/json')
        #print("That file extension is not allowed")
        #return redirect(request.url)
        return res


    data['error']="Please send post Request"
    res = app.response_class(response=json.dumps(data),
                             status=403,
                             mimetype='application/json')
    print("That file extension is not allowed")
    return res

@app.route("/", methods=["GET", "POST"])
@cross_origin()
def upload_image():
    data={"error":'','nonbackground':'','background':''}
    token=request.form['token']
    if request.method == "POST" and token=='hello':
        # for file in os.listdir(os.getcwd()+"/static/Background-Images"):
        #     os.remove(os.path.join(os.getcwd()+"/static/Background-Images", file))
        # for file in os.listdir(os.getcwd()+"/"+"static/Non-Background-Images"):
        #     os.remove(os.path.join(os.getcwd()+"/"+"static/Non-Background-Images",file))
        image = request.files['image']
        imgfilename = request.form['name']
        #print(image)
        if imgfilename == "":
            # data={"error":"No filename"}
            data['error']="No filename"
            res = app.response_class(response=json.dumps(data),
                                     status=400,
                                     mimetype='application/json')

            print("No filename")
            #return redirect(request.url)
            return res
        if allowed_image(imgfilename):
            filename = secure_filename(imgfilename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(filepath)

            image.save(filepath)



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

                # data={"nonbackground":filename}
                # data={"background":filepath}
                data['nonbackground'] = filename
                data['background'] = filepath
                res = app.response_class(response=json.dumps(data),
                                         status=200,
                                         mimetype='application/json')
                #return render_template('index.html', con=filename, data=filepath)
                return res
            elif response.status_code==402:
                print("ERROR",response.status_code,response)
                cmd = f'''curl -X POST -F "file=@{filepath}" "https://api.boring-images.ml/v1.0/transparent-net?api_key=ak-broad-haze-7fff750"'''
                args = shlex.split(cmd)
                process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                response = json.loads(stdout.decode('utf-8'))
                print(response['result'])
                if response['result'] == '':
                    data['error']="both servers not working"
                    res = app.response_class(response=json.dumps(data),
                                             status=200,
                                             mimetype='application/json')
                    # return render_template('index.html', uri=img, data=filepath)
                    return res

                img = response['result']

                #data = {"background":filepath}
                filepathnonbackground = os.path.join(app.config['DOWNLOAD_FOLDER'], secure_filename(imgfilename))


                r = requests.get(img, stream = True)
                r.raw.decode_content = True
                with open(filepathnonbackground, 'ab') as f:
                    s=shutil.copyfileobj(r.raw, f)
                f.close()
                #exec(s)
                #imgUrl=pathlib.Path(filepathnonbackground).as_uri()



                data['nonbackground'] = request.base_url+"static/Non-Background-Images/"+filename
                data['nonbackgroundurl'] = img

                res = app.response_class(response=json.dumps(data),
                                         status=200,
                                         mimetype='application/json')
                # return render_template('index.html', uri=img, data=filepath)
                return res


            else:
                print("Error:",'both servers not working')
                data['error']="both servers not working"
                res = app.response_class(response=json.dumps(data),
                                         status=200,
                                         mimetype='application/json')
                return res


        else:
            data['error'] = "That file extension is not allowed"
            res = app.response_class(response=json.dumps(data),
                                     status=200,
                                     mimetype='application/json')
            #print("That file extension is not allowed")
            # return redirect(request.url)
            return res

    else:
        data['error']="Token Invalid "
        res = app.response_class(response=json.dumps(data),
                                 status=200,
                                 mimetype='application/json')
        #print("That file extension is not allowed")
        #return redirect(request.url)
        return res


    data['error']="Please send post Request"
    res = app.response_class(response=json.dumps(data),
                             status=403,
                             mimetype='application/json')
    print("That file extension is not allowed")
    # return redirect(request.url)
    return res
    #return render_template('index.html')

if __name__== '__main__':
    app.run(debug=True)


