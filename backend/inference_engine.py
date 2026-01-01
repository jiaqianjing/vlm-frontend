import sys
import os
import logging
from pathlib import Path

# Add the project root to sys.path to allow imports from vlm package
# Assuming we are running from vlm-frontend/backend or similar, and vlm is in the parent of vlm-frontend
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from vlm.scripts.inference.inference_cli import setup_model, run_inference, DEFAULT_MODEL_PATH

logger = logging.getLogger(__name__)

class InferenceEngine:
    def __init__(self, model_path=DEFAULT_MODEL_PATH, base_model_id="Qwen/Qwen3-VL-32B-Instruct"):
        self.model_path = model_path
        self.base_model_id = base_model_id
        self.model = None
        self.processor = None

    def load_model(self):
        logger.info(f"Initializing Inference Engine with model at {self.model_path}")
        try:
            self.model, self.processor = setup_model(self.base_model_id, self.model_path)
            logger.info("Model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise e

    def predict(self, image_path: str, prompt: str) -> str:
        if not self.model or not self.processor:
            raise RuntimeError("Model is not loaded. Call load_model() first.")
        
        logger.info(f"Running inference on {image_path} with prompt: {prompt}")
        return run_inference(self.model, self.processor, image_path, prompt)

# Singleton instance
engine = InferenceEngine()
