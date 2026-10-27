from flask import Blueprint, jsonify
from app.config import settings

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'CrimeVision AI Backend',
        'version': '0.1.0',
        'environment': settings.FLASK_ENV
    }), 200


@health_bp.route('/capabilities', methods=['GET'])
def capabilities():
    """Return system capabilities and configuration status."""
    return jsonify({
        'status': 'operational',
        'modules': {
            'image_analysis': 'available',
            'video_analysis': 'available',
            'audio_transcription': 'available',
            'llm_reasoning': 'configured' if settings.GROQ_API_KEY else 'unconfigured',
            'report_generation': 'available',
            'timeline': 'available'
        },
        'models': {
            'detection': settings.DETECTION_MODEL,
            'whisper': settings.WHISPER_MODEL,
            'captioning': settings.CAPTIONING_MODEL,
            'groq': settings.GROQ_MODEL if settings.GROQ_API_KEY else None
        },
        'supported_formats': {
            'images': ['jpg', 'jpeg', 'png', 'bmp', 'webp'],
            'videos': ['mp4', 'avi', 'mov', 'mkv'],
            'audio': ['wav', 'mp3', 'm4a', 'flac']
        },
        'limits': {
            'max_upload_size_mb': settings.MAX_UPLOAD_SIZE // (1024 * 1024),
            'max_video_duration_seconds': settings.MAX_VIDEO_DURATION,
            'max_concurrent_jobs': settings.MAX_CONCURRENT_JOBS
        }
    }), 200
