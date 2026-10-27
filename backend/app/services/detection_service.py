class DetectionService:
    def __init__(self):
        self.model_loaded = False
        self.model_name = 'mock-detector'
    
    def detect_objects(self, image_path, confidence_threshold=0.5):
        import cv2
        try:
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError('Could not load image')
            height, width = image.shape[:2]
            mock_detections = [
                {'label': 'person', 'confidence': 0.85, 'bbox': {'x1': int(width * 0.3), 'y1': int(height * 0.2), 'x2': int(width * 0.5), 'y2': int(height * 0.8)}},
                {'label': 'car', 'confidence': 0.72, 'bbox': {'x1': int(width * 0.6), 'y1': int(height * 0.5), 'x2': int(width * 0.9), 'y2': int(height * 0.9)}}
            ]
            filtered = [d for d in mock_detections if d['confidence'] >= confidence_threshold]
            return filtered, None
        except Exception as e:
            return [], str(e)
    
    def annotate_image(self, image_path, detections, output_path):
        import cv2
        try:
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError('Could not load image')
            colors = {'person': (0, 255, 0), 'car': (255, 0, 0), 'default': (0, 0, 255)}
            for det in detections:
                bbox = det['bbox']
                label = det['label']
                confidence = det['confidence']
                color = colors.get(label, colors['default'])
                cv2.rectangle(image, (bbox['x1'], bbox['y1']), (bbox['x2'], bbox['y2']), color, 2)
                label_text = label + ': ' + str(round(confidence, 2))
                cv2.putText(image, label_text, (bbox['x1'], bbox['y1'] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            cv2.imwrite(output_path, image)
            return True, None
        except Exception as e:
            return False, str(e)

detection_service = DetectionService()
