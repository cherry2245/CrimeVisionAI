import os
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from app.extensions import db
from app.models import Evidence, AnalysisRun, Detection
from app.services.detection_service import detection_service

analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/image/<evidence_id>', methods=['POST'])
def analyze_image(evidence_id):
    evidence = Evidence.query.get_or_404(evidence_id)
    
    if evidence.media_type != 'image':
        return jsonify({'error': 'Evidence is not an image'}), 400
    
    analysis = AnalysisRun(
        id=str(uuid.uuid4()),
        evidence_id=evidence_id,
        analysis_type='image_detection',
        model_identifier=detection_service.model_name,
        model_version='1.0',
        processing_status='running'
    )
    
    db.session.add(analysis)
    db.session.commit()
    
    try:
        detections, error = detection_service.detect_objects(
            evidence.storage_path,
            confidence_threshold=0.5
        )
        
        if error:
            analysis.processing_status = 'failed'
            analysis.error_details = error
            db.session.commit()
            return jsonify({'error': error}), 500
        
        for det in detections:
            detection = Detection(
                id=str(uuid.uuid4()),
                analysis_run_id=analysis.id,
                label=det['label'],
                confidence=det['confidence'],
                bbox_x1=det['bbox']['x1'],
                bbox_y1=det['bbox']['y1'],
                bbox_x2=det['bbox']['x2'],
                bbox_y2=det['bbox']['y2']
            )
            db.session.add(detection)
        
        thumbnail_path = os.path.join(
            current_app.config['THUMBNAILS_FOLDER'],
            f'{analysis.id}_annotated.jpg'
        )
        detection_service.annotate_image(
            evidence.storage_path,
            detections,
            thumbnail_path
        )
        
        analysis.processing_status = 'completed'
        analysis.completion_timestamp = datetime.utcnow()
        analysis.result_metadata = '{\"detection_count\": ' + str(len(detections)) + '}'
        
        evidence.processing_status = 'analyzed'
        
        db.session.commit()
        
        return jsonify({
            'analysis_id': analysis.id,
            'evidence_id': evidence_id,
            'status': 'completed',
            'detector': {
                'model': detection_service.model_name,
                'detections': detections
            },
            'thumbnail_path': thumbnail_path
        }), 200
        
    except Exception as e:
        analysis.processing_status = 'failed'
        analysis.error_details = str(e)
        db.session.commit()
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/<analysis_id>', methods=['GET'])
def get_analysis(analysis_id):
    analysis = AnalysisRun.query.get_or_404(analysis_id)
    
    detections = Detection.query.filter_by(analysis_run_id=analysis_id).all()
    
    return jsonify({
        'analysis_id': analysis.id,
        'evidence_id': analysis.evidence_id,
        'analysis_type': analysis.analysis_type,
        'model_identifier': analysis.model_identifier,
        'model_version': analysis.model_version,
        'processing_status': analysis.processing_status,
        'creation_timestamp': analysis.creation_timestamp.isoformat(),
        'completion_timestamp': analysis.completion_timestamp.isoformat() if analysis.completion_timestamp else None,
        'error_details': analysis.error_details,
        'detections': [{
            'id': d.id,
            'label': d.label,
            'confidence': d.confidence,
            'bbox': {
                'x1': d.bbox_x1,
                'y1': d.bbox_y1,
                'x2': d.bbox_x2,
                'y2': d.bbox_y2
            }
        } for d in detections]
    })
