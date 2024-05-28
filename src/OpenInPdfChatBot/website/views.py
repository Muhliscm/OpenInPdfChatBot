from flask import Blueprint, render_template, request, flash, send_from_directory
from src.OpenInPdfChatBot.components.user_input_reader import user_input_handler
from src.OpenInPdfChatBot.constants import PDF_FILE_DIR
import os
from src.OpenInPdfChatBot import logger

views = Blueprint('views', __name__)


@views.route('/', methods=["GET", "POST"])
@views.route('/home', methods=["GET", "POST"])
def home():
    result = ""
    if request.method == "POST":
        question = request.form.get('question')
        if not question:
            flash("Field is empty", category='error')
        else:
            flash("Question submitted", category='success')
            result = user_input_handler(question)

    return render_template('home.html', result=result)


@views.route('/<filename>')
def serve_pdf(filename):

    logger.info(f"Requested file: {filename}")
    directory = os.path.abspath(PDF_FILE_DIR)
    return send_from_directory(directory, filename)
