from flask import *
from PIL import Image, ImageDraw
import os
from werkzeug.utils import secure_filename


def gridscaler(p, n, bw, f):
    imageName = p
    step_count = int(n)

    image = Image.open(imageName)
    if bw == "on":
        image = image.convert('L')

    draw = ImageDraw.Draw(image)
    y_start = 0
    y_end = image.height
    step_size = int(image.width / step_count)

    for x in range(0, image.width, step_size):
        line = ((x, y_start), (x, y_end))
        draw.line(line, fill=0)

    x_start = 0
    x_end = image.width

    if f == "on":
        step_size = int(image.height / step_count)

    for y in range(0, image.height, step_size):
        line = ((x_start, y), (x_end, y))
        draw.line(line, fill=0)

    newImageName = "/goels-share/Python/gridscaler/output/" + "new " + imageName[
                                                                       len("/goels-share/Python/gridscaler/files//") - 1:]
    c = 1
    while os.path.exists(newImageName):
        newImageName = '/goels-share/Python/gridscaler/output/' + str(c) + newImageName
        c += 1
    image.save(newImageName)
    final_name = newImageName[len("/goels-share/Python/gridscaler/output/"):]
    return final_name


def gapp():
    app = Flask(__name__)
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_FOLD = '/goels-share/Python/gridscaler/'
    UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_FOLD)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    @app.route('/')
    def upload_file():
        return render_template('index.html')

    @app.route('/', methods=['GET', 'POST'])
    def upload_file_():
        if request.method == 'POST':
            r = dict(request.form)
            number = r['number']
            f = request.files['file']
            if "bw" in r:
                bw = str(r['bw'])
            else:
                bw = "off"
            if "fixed" in r:
                fixed = str(r['fixed'])
            else:
                fixed = "off"
            fName = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            while not os.path.exists(UPLOAD_FOLD + fName):
                print("Loading...")
            newPath = UPLOAD_FOLD + 'files/' + fName
            c = 1
            while os.path.exists(newPath):
                newPath = UPLOAD_FOLD + 'files/' + str(c) + fName
                c += 1
            os.rename(UPLOAD_FOLD + fName, newPath)
            try:
                fName = gridscaler(newPath, number, bw, fixed)
                return send_from_directory(UPLOAD_FOLD + 'output/', fName)
            except Exception:
                return "Error: You Did Not Give a valid image.<br>Image must be a png, jpg, jpeg, webp or gif type to work.<br><a href='https://gridscaler.do-something-about-it.com/'>Try Again Here.</a>"

    return app
