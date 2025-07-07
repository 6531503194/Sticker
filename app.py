from flask import Flask, render_template, request, send_from_directory
from PIL import Image, ImageDraw, ImageFont
from rembg import remove
import os
from datetime import datetime
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip

app = Flask(__name__)

@app.route('/upload_gif', methods=['POST'])
def upload_gif():
    uploaded_file = request.files['photo']
    custom_text = request.form['text']

    if uploaded_file.filename != '':
        img = Image.open(uploaded_file.stream).convert("RGBA")
        sticker = remove(img)
        sticker_path = os.path.join(UPLOAD_FOLDER, "temp_sticker.png")
        sticker.save(sticker_path)

        # Create a base image clip
        base_clip = ImageClip(sticker_path, duration=2)  # 2-second duration

        # Create a simple text animation
        text_clip = (TextClip(custom_text, fontsize=40, color='white', font='Arial-Bold')
                    .set_position(('center', 'bottom'))
                    .set_duration(2)
                    .fadein(0.5)
                    .fadeout(0.5))

        final_clip = CompositeVideoClip([base_clip, text_clip])

        # Export as GIF
        gif_filename = f"animated_{datetime.now().strftime('%Y%m%d%H%M%S')}.gif"
        gif_path = os.path.join(UPLOAD_FOLDER, gif_filename)
        final_clip.write_gif(gif_path, fps=10)

        return f'<h2>Your Animated GIF:</h2><img src="/static/output/{gif_filename}" /><br><a href="/">Make another</a>'

    return 'No file uploaded!'

UPLOAD_FOLDER = 'static/output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['photo']
    custom_text = request.form['text']

    if uploaded_file.filename != '':
        img = Image.open(uploaded_file.stream)
        sticker = remove(img)

        draw = ImageDraw.Draw(sticker)
        font = ImageFont.truetype("arial.ttf", 30)
        draw.text((10, 10), custom_text, font=font, fill="white")

        filename = f"sticker_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        sticker.save(filepath)

        return f'<h2>Here is your sticker:</h2><img src="/static/output/{filename}" /><br><a href="/">Make another</a>'

    return 'No file uploaded!'

if __name__ == '__main__':
    app.run(debug=True)
