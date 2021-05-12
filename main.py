from PIL import Image
from forms import UploadForm
from werkzeug.utils import secure_filename
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import os
import webcolors
from colorthief import ColorThief

UPLOAD_FOLDER = "static/uploads"
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Bootstrap(app)
app.secret_key = "BlahBlahBlah"

def GetColourPalette(file):
    # with open(file, 'r+b') as f:
    #     with Image.open(f) as image:
    color_thief = ColorThief(file)
    color_palette = color_thief.get_palette(color_count=11, quality=1)
    colour_palette_list = []
    for color in color_palette:
        HexValue = webcolors.rgb_to_hex(color)
        colour_palette_list.append(HexValue)
    return colour_palette_list

@app.route('/', methods=["GET", "POST"])
def home():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.file.data
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
        palette = GetColourPalette(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        return render_template('ImageInfo.html', palette=palette, image=os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
    return render_template('home.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)