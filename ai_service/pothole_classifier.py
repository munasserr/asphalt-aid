import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

model = None


def load_model():
    """Load the TensorFlow model once globally"""
    global model
    try:
        logger.info("Attempting to load TensorFlow model...")
        import tensorflow as tf

        model_path = os.path.join(
            settings.BASE_DIR, "Pothole Classification", "pothole_model.h5"
        )
        logger.info(f"Model path: {model_path}")

        if os.path.exists(model_path):
            model = tf.keras.models.load_model(model_path)
            logger.info(
                f"✓ Pothole classification model loaded successfully from {model_path}"
            )
        else:
            logger.error(f"✗ Model file not found at {model_path}")

    except ImportError:
        logger.error("✗ TensorFlow not installed. Please install tensorflow.")
    except Exception as e:
        logger.error(f"✗ Error loading model: {str(e)}")


def preprocess_image(image_path):
    """Preprocess image for model prediction"""
    try:
        logger.info(f"Preprocessing image: {image_path}")
        import numpy as np
        from PIL import Image

        # Load and preprocess image to match training data
        img = Image.open(image_path)
        img = img.convert("RGB")
        img = img.resize((224, 224))  # Match training size
        logger.info(f"Image resized to 224x224")

        # Convert to numpy array and normalize
        img_array = np.array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array.astype("float32") / 255.0
        logger.info(f"Image preprocessed successfully. Shape: {img_array.shape}")

        return img_array

    except Exception as e:
        logger.error(f"✗ Error preprocessing image: {str(e)}")
        return None


def predict_severity(image_path):
    """Predict pothole severity from image (0-3 scale)"""
    global model

    logger.info(f"=== AI PREDICTION START ===")
    logger.info(f"Predicting severity for image: {image_path}")
    logger.info(f"Model loaded: {model is not None}")

    if model is None:
        logger.warning("Model not loaded. Loading now...")
        load_model()

    if model is None:
        logger.error("Model still not available. Returning default severity.")
        return 1

    try:
        processed_image = preprocess_image(image_path)
        if processed_image is None:
            logger.error("Image preprocessing failed")
            return 1

        logger.info("Running model prediction...")
        import numpy as np

        predictions = model.predict(processed_image, verbose=0)
        predicted_class = np.argmax(predictions)
        confidence = np.max(predictions)

        logger.info(f"Raw predictions: {predictions}")
        logger.info(f"Predicted class: {predicted_class}")
        logger.info(f"Confidence: {confidence:.4f}")

        # Map model output to severity (0-3)
        severity_mapping = {
            0: 0,  # Normal road - No severity
            1: 1,  # Minor pothole - Low severity
            2: 3,  # Major pothole - High severity
        }

        severity = severity_mapping.get(predicted_class, 1)
        logger.info(f"✓ Final mapped severity: {severity}")
        logger.info(f"=== AI PREDICTION COMPLETED ===")

        return severity

    except Exception as e:
        logger.error(f"✗ Error during prediction: {str(e)}")
        logger.exception("Full exception details:")
        return 1  # Default severity on error


# Load model when module is imported
logger.info("AI service module imported. Loading model...")
load_model()
