from flask import Flask, render_template, request, jsonify, send_file
import os
from video_generator import AIVideoGenerator
from werkzeug.utils import secure_filename
import threading
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output_videos'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max

# Create folders
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

generator = AIVideoGenerator()
job_status = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_video():
    try:
        data = request.json
        text = data.get('text', '')
        duration = int(data.get('duration', 30))
        voice_speed = float(data.get('voice_speed', 1.0))
        
        if not text or len(text.strip()) < 5:
            return jsonify({'error': 'Text must be at least 5 characters long'}), 400
        
        job_id = str(uuid.uuid4())
        job_status[job_id] = {'status': 'initializing', 'progress': 0, 'message': 'Starting video generation...'}
        
        # Start video generation in background
        thread = threading.Thread(
            target=_generate_in_background,
            args=(job_id, text, duration, voice_speed)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({'job_id': job_id, 'status': 'started'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status/<job_id>')
def get_status(job_id):
    return jsonify(job_status.get(job_id, {'status': 'unknown', 'progress': 0}))

@app.route('/api/download/<job_id>')
def download_video(job_id):
    try:
        video_path = os.path.join(app.config['OUTPUT_FOLDER'], f'{job_id}.mp4')
        if os.path.exists(video_path):
            return send_file(video_path, mimetype='video/mp4', as_attachment=True, download_name=f'video_{job_id}.mp4')
        return jsonify({'error': 'Video not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def _generate_in_background(job_id, text, duration, voice_speed):
    try:
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], f'{job_id}.mp4')
        
        def progress_callback(step, total):
            progress = int((step / total) * 100)
            job_status[job_id]['progress'] = progress
            messages = {
                0: 'Generating AI images...',
                1: 'Creating voice-over...',
                2: 'Assembling video...',
                3: 'Adding effects...',
                4: 'Finalizing video...'
            }
            job_status[job_id]['message'] = messages.get(step, 'Processing...')
        
        generator.create_from_text(
            text, 
            duration, 
            voice_speed, 
            output_path,
            progress_callback
        )
        
        job_status[job_id]['status'] = 'completed'
        job_status[job_id]['progress'] = 100
        job_status[job_id]['output_path'] = output_path
        job_status[job_id]['message'] = 'Video ready for download!'
    
    except Exception as e:
        job_status[job_id]['status'] = 'error'
        job_status[job_id]['error'] = str(e)
        job_status[job_id]['message'] = f'Error: {str(e)}'

@app.route('/api/stats')
def get_stats():
    videos_count = len([f for f in os.listdir(app.config['OUTPUT_FOLDER']) if f.endswith('.mp4')])
    return jsonify({'total_videos_generated': videos_count})

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)