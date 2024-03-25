from flask import Flask, request, send_from_directory, render_template
import os
import re

app = Flask(__name__)
STRIPPED_FOLDER = 'stripped_files'

# Check that folder for stripped files exists and create it if it doesn't
os.makedirs(STRIPPED_FOLDER, exist_ok=True)

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def strip_timestamps():
    if 'file' not in request.files:
        return 'No file included in request payload'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        original_filename = os.path.splitext(file.filename)[0]
        stripped_filename = f"{original_filename}_stripped.txt"
        stripped_filepath = os.path.join(STRIPPED_FOLDER, stripped_filename)
        
        # Read  file
        content = file.stream.read().decode('utf-8')
        lines = content.splitlines()
        
        # Write stripped text to file
        with open(stripped_filepath, 'w', encoding='utf-8') as stripped_file:
            for line in lines:
                if not re.match(r'^\d{2}:\d{2}', line):
                    stripped_file.write(line + '\n')

        # Serve processed file
        return send_from_directory(directory=STRIPPED_FOLDER, path=stripped_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=3000
            )
