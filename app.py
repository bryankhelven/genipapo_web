import urllib.parse
from flask import Flask, request, send_file, render_template, make_response, jsonify
import stanza
from stanza.utils.conll import CoNLL
from conllu import parse_incr
import os
import tempfile
from io import StringIO

app = Flask(__name__)

# Ensure the templates folder is correctly configured
app.template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

# Define the model directory and path
model_dir = os.path.join('models')
model_path = os.path.join(model_dir, 'genipapo.pt')

# Initialize the Stanza pipeline once for reuse
nlp = stanza.Pipeline(
    lang='pt',
    processors='depparse',
    depparse_pretagged=True,
    depparse_model_path=model_path,
    tokenize_pretokenized=True,
    use_gpu=False,
    download_method=None
)

def validate_conllu_file(content):
    """
    Validate the .conllu file format and ensure:
    1. Each token line has 10 columns.
    2. POS tags (UPOS) are present and valid.
    Forms or lemmas that are "_" issue warnings but do not prevent processing.
    """
    errors = []
    warnings = []
    valid_pos_tags = set([
        # Common universal POS tags
        "ADJ", "ADP", "ADV", "AUX", "CCONJ", "DET", "INTJ", "NOUN",
        "NUM", "PART", "PRON", "PROPN", "PUNCT", "SCONJ", "SYM", "VERB", "X"
    ])

    lines = content.strip().split('\n')
    line_iter = iter(enumerate(lines, start=1))
    sentence_num = 0

    try:
        for sentence in parse_incr(StringIO(content)):
            sentence_num += 1
            for token in sentence:
                # Find the line corresponding to the current token
                while True:
                    try:
                        line_num, line = next(line_iter)
                    except StopIteration:
                        raise Exception("Unexpected end of content while parsing tokens.")
                    line = line.strip()
                    if line == '' or line.startswith('#'):
                        continue  # Skip empty lines and comments
                    else:
                        break  # Found the token line
                columns = line.split('\t')
                if len(columns) != 10:
                    errors.append(f"Line {line_num} of the conllu file: Incorrect number of columns ({len(columns)} found, 10 required).")
                    continue  # Skip further checks for this token

                if isinstance(token['id'], int):  # Process only word tokens
                    token_id = token['id']
                    form = token.get('form', '').strip()
                    lemma = token.get('lemma', '').strip()
                    upos = token.get('upos', '').strip().upper()

                    if upos == '_':
                        errors.append(f"Line {line_num}: Missing POS tag (UPOS).")
                    elif upos not in valid_pos_tags:
                        errors.append(f"Error on line {line_num} of the conllu file: Invalid POS tag '{upos}'.")

                    if form == "_":
                        warnings.append(f"Warning on line {line_num} of the conllu file: Form is empty")
                    if lemma == "_":
                        warnings.append(f"Warning on line {line_num} of the conllu file: Lemma is empty")
    except Exception as e:
        errors.append(f"Parsing error: {str(e)}")
        return False, errors, warnings

    if errors:
        return False, errors, warnings
    else:
        return True, [], warnings

# Main route for file upload
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the file is present in the request
        if 'file' not in request.files:
            return 'No file found in the request.', 400
        file = request.files['file']
        if file.filename == '':
            return 'No file selected.', 400
        if file and file.filename.endswith('.conllu'):
            # Read the file content
            content = file.read().decode('utf-8')

            # Validate the .conllu file
            is_valid, errors, warnings = validate_conllu_file(content)
            if not is_valid:
                # Return validation errors and stop processing
                error_message = "Validation failed:<br>" + "<br>".join(errors)
                return error_message, 400, {'Content-Type': 'text/html'}
            else:
                # Optionally, display warnings to the user
                if warnings:
                    warning_message = "Warnings:<br>" + "<br>".join(warnings)
                    # You can choose to display warnings or log them
                    print(warning_message)  # Or handle as needed

            # Save the valid file and process it
            input_temp_path = save_temp_file(content)

            # Process the file after validation
            try:
                output_file_path = process_file(input_temp_path, file.filename)

                # Create a response object to include headers
                response = make_response(send_file(output_file_path, as_attachment=True))

                # Include warnings in the response headers if any
                if warnings:
                    # Join warnings into a single string
                    warnings_str = '\n'.join(warnings)
                    # URL-encode the warnings string to safely include in the header
                    warnings_encoded = urllib.parse.quote(warnings_str)
                    # Include warnings in a custom header
                    response.headers['X-Warnings'] = warnings_encoded
                return response
            except Exception as e:
                # Handle unexpected errors in processing
                return f"Error during processing: {str(e)}", 500
        else:
            return 'Invalid file type. Only .conllu files are allowed.', 400

    # Render the HTML template
    return render_template('upload_conllu.html')

def save_temp_file(content):
    """
    Save the content to a temporary file and return its path.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix='.conllu', mode='w', encoding='utf-8') as input_temp:
        input_temp.write(content)
        return input_temp.name

def process_file(input_file_path, original_filename):
    """
    Process the .conllu file using the Stanza pipeline.
    """
    doc = CoNLL.conll2doc(input_file=input_file_path)
    parsed_doc = nlp(doc)

    for orig_sentence, parsed_sentence in zip(doc.sentences, parsed_doc.sentences):
        for orig_word, parsed_word in zip(orig_sentence.words, parsed_sentence.words):
            orig_word.head = parsed_word.head
            orig_word.deprel = parsed_word.deprel

    base_name = os.path.splitext(original_filename)[0]
    output_filename = base_name + '_parsed.conllu'
    output_file_path = os.path.join(tempfile.gettempdir(), output_filename)

    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write("{:C}".format(doc))
        f.write('\n\n')

    return output_file_path

@app.route('/api/process', methods=['POST'])
def process_api():
    response_format = request.args.get('response_format', 'file')

    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not file.filename.endswith('.conllu'):
        return jsonify({'error': 'Invalid file type. Only .conllu files are allowed.'}), 400

    content = file.read().decode('utf-8')
    is_valid, errors, warnings = validate_conllu_file(content)
    if not is_valid:
        return jsonify({'status': 'error', 'errors': errors, 'warnings': warnings}), 400

    # Save the valid file and process it
    input_temp_path = save_temp_file(content)

    try:
        output_file_path = process_file(input_temp_path, file.filename)

        if response_format == 'json':
            # Read the processed content from the file
            with open(output_file_path, 'r', encoding='utf-8') as processed_file:
                output_content = processed_file.read()

            return jsonify({
                'status': 'success',
                'warnings': warnings,
                'processed_content': output_content
            }), 200
        else:
            # Return the processed file directly
            response = send_file(output_file_path, as_attachment=True, download_name='processed.conllu')
            if warnings:
                warnings_str = '\n'.join(warnings)
                response.headers['X-Warnings'] = urllib.parse.quote(warnings_str)
            return response
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api/process/json', methods=['POST'])
def process_api_json():
    # Check if the request body contains JSON
    if not request.is_json:
        return jsonify({'error': 'Request body must be JSON'}), 400

    data = request.get_json()
    content = data.get('content')
    if not content:
        return jsonify({'error': 'JSON must include a "content" field with .conllu data'}), 400

    # Validate the .conllu content
    is_valid, errors, warnings = validate_conllu_file(content)
    if not is_valid:
        return jsonify({'status': 'error', 'errors': errors, 'warnings': warnings}), 400

    try:
        # Save the valid content to a temporary file
        input_temp_path = save_temp_file(content)
        output_file_path = process_file(input_temp_path, "input.conllu")

        # Read the processed content from the file
        with open(output_file_path, 'r', encoding='utf-8') as processed_file:
            output_content = processed_file.read()

        return jsonify({
            'status': 'success',
            'warnings': warnings,
            'processed_content': output_content
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/api_guide')
def api_guide():
    return render_template('api_guide.html')

if __name__ == '__main__':
    # Run the app on port 8000
    app.run(host='0.0.0.0', port=8000)
