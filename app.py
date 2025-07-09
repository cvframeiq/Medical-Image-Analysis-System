from flask import Flask, render_template, request, redirect, url_for
from vqa_api import get_vqa_answer
import os
from werkzeug.utils import secure_filename
import markdown  # To render Markdown as HTML

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    question = request.form.get('question', '').strip()
    image = request.files.get('image')

    if image and question:
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)

        raw_answer = get_vqa_answer(image_path, question)
        answer_html = markdown.markdown(raw_answer)

        image_url = '/' + image_path.replace("\\", "/")
        return render_template('index.html', image_url=image_url, question=question, answer_html=answer_html)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
