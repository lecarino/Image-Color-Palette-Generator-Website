from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from datetime import datetime
from PIL import Image
import numpy as np
import os
from colorthief import ColorThief

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    current_date = datetime.now().strftime("%Y-%m-%d")
    img_path = None 
    palette = None
    color_count = 6

    if request.method == 'POST':
        #check if a file was provided
        if 'file' in request.files:
            file = request.files['file']

            try:
                color_count = int(request.form['text'])
            except KeyError:
                pass

            if file.filename != '':
                image = Image.open(file)
                img_array = np.array(image)

                color_thief = ColorThief(file)
                print(color_count)
                palette = [(index + 1, color) for index, color in enumerate(color_thief.get_palette(color_count= color_count))]

                # Save the image to a file in the static folder
                img_filename = 'uploaded_image.jpg'
                img_path = os.path.join('static', img_filename)
                Image.fromarray(img_array).save(img_path)

    colors = palette if palette is not None else []
    return render_template('index.html', current_date=current_date, img_path=img_path, colors=colors)

if __name__ == "__main__":
    app.run(debug=True, port=5002)
