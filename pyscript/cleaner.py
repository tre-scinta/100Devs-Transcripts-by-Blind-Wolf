from flask import Flask, request, render_template_string, send_file
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Text Cleaner</title>
</head>
<body>
    <h2>Remove HTML Tags</h2>
    <form method="post" enctype="multipart/form-data">
        <label for="text">Text:</label>
        <textarea name="text" rows="10" cols="30"></textarea>
        <br>
        <label for="file">Or upload a file:</label>
        <input type="file" name="file">
        <br>
        <label><input type="checkbox" name="tags" value="p">p-tag</label>
        <label><input type="checkbox" name="tags" value="h1">h1-tags</label>
        <!-- Extend with more checkboxes for other tags as needed -->
        <br>
        <input type="submit" name="action" value="Clean Text">
        <input type="submit" name="action" value="Strip All HTML">
    </form>
    {% if cleaned_text %}
        <h3>Cleaned Text:</h3>
        <p>{{ cleaned_text }}</p>
    {% endif %}
</body>
</html>
"""

def clean_html(text, tags=None):
    soup = BeautifulSoup(text, 'html.parser')
    
    if tags:
        for tag in tags:
            for element in soup.find_all(tag):
                element.decompose()  # Remove the tag
    else:
        for tag in soup.find_all(True):  # Find all tags
            tag.decompose()  # Remove the tag

    return str(soup)

def process_file(file, tags=None):
    content = file.read().decode('utf-8')
    cleaned_content = clean_html(content, tags)
    
    filename = file.filename.rsplit('.', 1)[0] + '_cleaned.txt'
    filepath = os.path.join('processed_files', filename)
    os.makedirs('processed_files', exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    
    return filepath

@app.route('/', methods=['GET', 'POST'])
def clean_text():
    cleaned_text = None
    if request.method == 'POST':
        action = request.form['action']
        tags = request.form.getlist('tags') if action == "Clean Text" else None
        
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            cleaned_file_path = process_file(file, tags)
            return send_file(cleaned_file_path, as_attachment=True)
        else:
            text = request.form['text']
            cleaned_text = clean_html(text, tags)
    return render_template_string(HTML_FORM, cleaned_text=cleaned_text)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
