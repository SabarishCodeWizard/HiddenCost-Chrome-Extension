from inference_sdk import InferenceHTTPClient
import requests

# Initialize the Inference Client
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="Isfvfx8t9DOFP0WoUNuu"
)

# Specify the image path and model ID
image_path = "D:/GitHub/Team_excalibur_hidden_cost-main/train_classifier/image.jpg"  # Replace with your actual image path
model_id = "dark-pattern-_visual-detection/1"

try:
    # Perform inference on the image
    result = CLIENT.infer(image_path, model_id=model_id)

    # Process and print the results
    if 'predictions' in result:
        for prediction in result['predictions']:
            print(f"Label: {prediction['class']}, Confidence: {prediction['confidence']:.2f}, Bounding Box: {prediction['bounding_box']}")
    else:
        print("No predictions found.")
except Exception as e:
    print(f"An error occurred: {e}")
