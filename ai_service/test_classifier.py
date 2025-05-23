import os
import sys
import django

sys.path.append("/app")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "asphalt_aid.settings")
django.setup()

from ai_service.pothole_classifier import classifier


def test_classifier():
    print("Testing Pothole Classifier...")
    print(f"Model loaded: {classifier.model is not None}")
    print(f"Model path: {classifier.model_path}")
    print(f"Model file exists: {os.path.exists(classifier.model_path)}")

    if classifier.model is not None:
        print("✓ AI Classifier is ready!")
    else:
        print("✗ AI Classifier failed to load")


if __name__ == "__main__":
    test_classifier()
