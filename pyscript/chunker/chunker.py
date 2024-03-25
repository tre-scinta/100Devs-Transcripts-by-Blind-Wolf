from flask import Flask, render_template, request, send_file
import os

app = Flask(__name__)

def clean_and_string (content):
    # Replace double spaces with single spaces and remove all newlines
    content = content.replace('  ', ' ').replace('\n', ' ')    
    content = ' '.join(content.split())
    
    return content

def chunk_by_chars (content, num_chars):
    chunked_content = ""
    for i in range(0, len(content), num_chars):
        chunked_content += content[i:i+num_chars] + "\n\n"

    return chunked_content

def chunk_by_words (content, num_words):
    words = content.split()
    chunks = []

    for i in range(0, len(words), num_words):
        chunk = ' '.join(words[i:i+num_words])
        chunks.append(chunk)

        chunked_content = '\n\n'.join(chunks)

    return chunked_content
    
def process_file(input_file, output_filepath, chunk_type, chunk_size):
    content = input_file.read().decode('utf-8')
    cleaned_content = clean_and_string(content)

    if chunk_type == 'words':
        chunked_content = chunk_by_words(cleaned_content, int(chunk_size))
    elif chunk_type == 'chars':
        chunked_content = chunk_by_chars(cleaned_content, int(chunk_size))
    else:
        chunked_content = cleaned_content  

        
        

    # Write the processed content to the output file
    with open(output_filepath, 'w', encoding='utf-8') as output_file:
        output_file.write(chunked_content)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']

        if file.filename == '':
            return 'No selected file'
        
        desired_type = request.form['chunk_type']
        desired_size = request.form['chunk_size']

        original_filename = os.path.splitext(file.filename)[0]
        output_filename = f"{original_filename}_chunked.txt"
        output_filepath = os.path.join('chunked_files', output_filename)
        
        os.makedirs('chunked_files', exist_ok=True)
        process_file(file, output_filepath, desired_type, desired_size)

        return send_file(output_filepath, as_attachment=True)

    # For GET requests, show the file upload form
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True, port=3001)
