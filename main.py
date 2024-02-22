from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
# from datetime import datetime
from PIL import Image
import numpy as np
import os
from colorthief import ColorThief
# from memory_profiler import profile

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FLASK_KEY")

@app.route('/', methods=['GET', 'POST'])
# @profile
def home():
    img_path = None 
    palette = None
    if request.method == 'POST':
        #check if a file was provided
        if 'file' in request.files:
            file = request.files['file']
            try:
                color_count = int(request.form['text'])
            except ValueError:
                color_count = 6
            if file.filename != '':
                image = Image.open(file)
                img_array = np.array(image)

                color_thief = ColorThief(file)
                palette = [(index + 1, color) for index, color in enumerate(color_thief.get_palette(color_count= color_count))]

                # Save the image to a file in the static folder
                img_filename = 'uploaded_image.jpg'
                img_path = os.path.join('static', img_filename)
                Image.fromarray(img_array).save(img_path)

    colors = palette if palette is not None else []
    return render_template('index.html', img_path=img_path, colors=colors)

if __name__ == "__main__":
    app.run(debug=True)
