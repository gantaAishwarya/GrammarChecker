from flask import Flask, request, render_template
from checker import SpellCheckerModule

app = Flask(__name__)
spell_checker_module = SpellCheckerModule()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/spell', methods=['POST', 'GET'])
def spell():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            text = data.get('text')  # Assuming the JSON contains 'text'
            corrected_text = spell_checker_module.correct_spell(text)
            corrected_grammar = spell_checker_module.correct_grammar(text)
            return render_template('index.html', corrected_text=corrected_text, corrected_grammar=corrected_grammar)

    return render_template('index.html')  # Or handle other cases accordingly

@app.route('/grammar', methods=['POST', 'GET'])
def grammar():
    if request.method == 'POST':
        file = request.files['file']
        readable_file = file.read().decode('utf-8', errors='ignore')
        corrected_file_text = spell_checker_module.correct_spell(readable_file)
        corrected_file_grammar = spell_checker_module.correct_grammar(readable_file)
        return render_template('index.html', corrected_file_text=corrected_file_text, corrected_file_grammar=corrected_file_grammar)

    return render_template('index.html')  # Or handle other cases accordingly

# Python main
if __name__ == "__main__":
    app.run(debug=True)
