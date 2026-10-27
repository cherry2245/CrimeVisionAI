import os
import uuid
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models import Evidence
from app.utils.file_utils import allowed_file, calculate_file_hash, generate_internal_filename

evidence_bp = Blueprint('evidence', __name__)

@evidence_bp.route('/upload', methods=['POST'])
def upload_evidence():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    # Generate internal filename
    internal_filename = generate_internal_filename(file.filename)
    storage_path = os.path.join(current_app.config['UPLOAD_FOLDER'], internal_filename)
    
    # Save file
    file.save(storage_path)
    
    # Calculate hash
    file_hash = calculate_file_hash(storage_path)
    
    # Check for duplicate
    existing = Evidence.query.filter_by(file_hash=file_hash).first()
    if existing:
        os.remove(storage_path)
        return jsonify({'error': 'File already exists', 'evidence_id': existing.id}), 409
    
    # Create evidence record
    evidence = Evidence(
        id=str(uuid.uuid4()),
        original_filename=secure_filename(file.filename),
        internal_filename=internal_filename,
        storage_path=storage_path,
        media_type='image',
        file_size=os.path.getsize(storage_path),
        file_hash=file_hash,
        processing_status='pending'
    )
    
    db.session.add(evidence)
    db.session.commit()
    
    return jsonify({
        'evidence_id': evidence.id,
        'original_filename': evidence.original_filename,
        'file_size': evidence.file_size,
        'file_hash': evidence.file_hash,
        'upload_timestamp': evidence.upload_timestamp.isoformat(),
        'processing_status': evidence.processing_status
    }), 201

@evidence_bp.route('/', methods=['GET'])
def list_evidence():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    evidence_list = Evidence.query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'evidence': [{
            'id': e.id,
            'original_filename': e.original_filename,
            'media_type': e.media_type,
            'file_size': e.file_size,
            'upload_timestamp': e.upload_timestamp.isoformat(),
            'processing_status': e.processing_status
        } for e in evidence_list.items],
        'total': evidence_list.total,
        'pages': evidence_list.pages,
        'current_page': page
    })

@evidence_bp.route('/<evidence_id>', methods=['GET'])
def get_evidence(evidence_id):
    evidence = Evidence.query.get_or_404(evidence_id)
    
    return jsonify({
        'id': evidence.id,
        'original_filename': evidence.original_filename,
        'internal_filename': evidence.internal_filename,
        'media_type': evidence.media_type,
        'file_size': evidence.file_size,
        'file_hash': evidence.file_hash,
        'upload_timestamp': evidence.upload_timestamp.isoformat(),
        'processing_status': evidence.processing_status
    })
