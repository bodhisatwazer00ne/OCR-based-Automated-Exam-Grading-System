import os
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename

from utils.ocr import extract_text_from_image
from utils.grader import grade_multiple_answers

app = Flask(__name__) 
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'your_secret_key_here'  # Change to secure random key!
#abcd
# Create uploads folder if not exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'answer_sheet' not in request.files or 'reference_answers' not in request.files:
            flash('Please upload both answer sheet and reference answers files.', 'error')
            return redirect(request.url)

        answer_file = request.files['answer_sheet']
        ref_file = request.files['reference_answers']

        if answer_file.filename == '' or ref_file.filename == '':
            flash('No selected file for either answer sheet or reference answers.', 'error')
            return redirect(request.url)

        # Save files securely
        answer_filename = secure_filename(answer_file.filename)
        ref_filename = secure_filename(ref_file.filename)

        answer_path = os.path.join(app.config['UPLOAD_FOLDER'], answer_filename)
        ref_path = os.path.join(app.config['UPLOAD_FOLDER'], ref_filename)

        answer_file.save(answer_path)
        ref_file.save(ref_path)

        # Read reference answers (one per line)
        with open(ref_path, 'r', encoding='utf-8') as f:
            teacher_answers = [line.strip() for line in f if line.strip()]

        # Extract text from student answer sheet
        extracted_text = extract_text_from_image(answer_path)

        # Grade against reference answers
        scores = grade_multiple_answers(extracted_text, teacher_answers)

        # Render results page, passing required variables
        return render_template(
            'results.html',
            text=extracted_text,
            scores=scores,
            answers=teacher_answers
        )

    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
