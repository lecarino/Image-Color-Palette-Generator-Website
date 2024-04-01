from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from PIL import Image
import numpy as np
import os
from colorthief import ColorThief

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FLASK_KEY")
Bootstrap5(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    img_path = None
    palette = None
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            try:
                color_count = int(request.form['text'])
            except ValueError:
                color_count = 6
            if file.filename != '':
                image = Image.open(file)
                img_array = np.array(image)

                # Convert RGBA image to RGB
                rgb_image = Image.fromarray(img_array).convert('RGB')

                # Save the RGB image to a temporary file
                temp_img_path = 'temp_image.jpg'
                rgb_image.save(temp_img_path)

                color_thief = ColorThief(temp_img_path)
                palette = [(index + 1, color) for index, color in enumerate(color_thief.get_palette(color_count=color_count))]

                # Define the directory path
                directory = os.path.join('static', 'assets', 'img')

                # Create the directory if it does not exist
                if not os.path.exists(directory):
                    os.makedirs(directory)

                # Update the file path to include the directory
                img_filename = 'uploaded_image.jpg'
                img_path = os.path.join(directory, img_filename)

                # Move the temporary image to the final location
                os.rename(temp_img_path, img_path)

    colors = palette if palette is not None else []
    return render_template('index.html', img_path=img_path, colors=colors)

if __name__ == "__main__":
    app.run(debug=True)
