from flask import Flask, render_template, request, jsonify, send_file
import io
import time
from deep_translator import GoogleTranslator

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Cache translators by language
translator_cache = {}
# Track translation progress per session
translation_progress = {}


def get_translator(target_lang):
    """Get or create a translator for the target language"""
    if target_lang not in translator_cache:
        translator_cache[target_lang] = GoogleTranslator(source='auto', target=target_lang)
    return translator_cache[target_lang]


def parse_srt(content):
    """Parse SRT content into list of subtitles"""
    # Normalize line endings to Unix style
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    
    blocks = content.strip().split('\n\n')
    subtitles = []
    
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            try:
                index = int(lines[0].strip())
                timing = lines[1].strip()
                text = '\n'.join(line.strip() for line in lines[2:])
                if text.strip():
                    subtitles.append({
                        'index': index,
                        'timing': timing,
                        'text': text
                    })
            except (ValueError, IndexError):
                continue
    
    return subtitles


def translate_text(text, translator):
    """Translate text using provided translator instance"""
    if not text.strip():
        return text
    
    try:
        translated = translator.translate(text)
        return translated if translated else text
    except Exception:
        return text


def build_srt(subtitles):
    """Build SRT content from subtitles"""
    srt_content = ""
    for sub in subtitles:
        srt_content += f"{sub['index']}\n"
        srt_content += f"{sub['timing']}\n"
        srt_content += f"{sub['text']}\n\n"
    
    return srt_content.strip()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/translate', methods=['POST'])
def translate():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    if 'target_lang' not in request.form:
        return jsonify({'error': 'No target language provided'}), 400
    
    file = request.files['file']
    target_lang = request.form['target_lang']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.endswith('.srt'):
        return jsonify({'error': 'Only .srt files are supported'}), 400
    
    try:
        # Generate a session ID for tracking progress
        session_id = request.remote_addr + str(time.time())
        translation_progress[session_id] = {'current': 0, 'total': 0}
        
        content = file.read().decode('utf-8', errors='ignore')
        subtitles = parse_srt(content)
        
        translation_progress[session_id]['total'] = len(subtitles)
        
        # Get cached translator instance
        translator = get_translator(target_lang)
        
        # Translate each subtitle
        for i, sub in enumerate(subtitles):
            sub['text'] = translate_text(sub['text'], translator)
            translation_progress[session_id]['current'] = i + 1
        
        translated_srt = build_srt(subtitles)
        
        # Clean up progress tracking
        if session_id in translation_progress:
            del translation_progress[session_id]
        
        # Return as downloadable file
        output = io.BytesIO()
        output.write(translated_srt.encode('utf-8'))
        output.seek(0)
        
        filename = f"translated_{target_lang}_{file.filename}"
        
        return send_file(
            output,
            mimetype='text/plain',
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        if session_id in translation_progress:
            del translation_progress[session_id]
        return jsonify({'error': f'Translation failed: {str(e)}'}), 500


@app.route('/api/progress')
def get_progress():
    """Get translation progress for the current session"""
    session_id = request.remote_addr
    
    # Find matching session
    for key in translation_progress:
        if key.startswith(session_id):
            progress = translation_progress[key]
            if progress['total'] > 0:
                percent = int((progress['current'] / progress['total']) * 100)
                return jsonify({
                    'current': progress['current'],
                    'total': progress['total'],
                    'percent': percent
                })
    
    return jsonify({'current': 0, 'total': 0, 'percent': 0})


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
