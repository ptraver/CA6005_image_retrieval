import os
import rank_match_flask


from flask import Flask, redirect, request, render_template, send_from_directory, url_for

__author__ = 'ibininja'

app = Flask(__name__)



APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'images/')
    print(target)
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        print ("Accept incoming file:", filename)
        print ("Save it to:", destination)
        upload.save(destination)

    # return send_from_directory("images", filename, as_attachment=True)
    return render_template("complete.html", image_name=filename)

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)

@app.route('/gallery', methods = ["POST", "GET"])
def get_gallery():

    image_names = rank_match_flask.score_collection('happy')

    if request.method == "POST":
        keyword = request.form["nm"]
        return redirect(url_for("keyword", kyword=keyword))
    #image_names = os.listdir('./images') #output of ranking
    else:
        return render_template("gallery3.html", image_names=image_names)

@app.route("/<kyword>", methods = ["POST", "GET"])
def keyword(kyword):
    image_names = rank_match_flask.score_collection(f'{kyword}')
    #keyword = request.form["nm"]
    #return redirect(url_for("keyword", kyword=keyword))

    if request.method == "POST":
        keyword = request.form["nm"]
        return redirect(url_for("keyword", kyword=keyword))
    #image_names = os.listdir('./images') #output of ranking
    else:
        return render_template("gallery3.html", image_names=image_names)

    #return render_template("gallery3.html", image_names=image_names)

if __name__ == "__main__":
    app.run(port=4555, debug=True)




























