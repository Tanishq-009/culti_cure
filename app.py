import os
from werkzeug.utils import secure_filename
from flask import Flask, redirect, render_template, request, jsonify
from PIL import Image
import torchvision.transforms.functional as TF
import numpy as np
import torch
import pandas as pd
import torch.nn as nn
from torchvision import transforms
import torchvision.models as models

# Keep CPU/memory use low on small servers (e.g. Render free tier)
torch.set_num_threads(1)

# Load CSV files
disease_info = pd.read_csv('disease_info.csv', encoding='cp1252')
supplement_info = pd.read_csv('supplement_info.csv', encoding='cp1252')

# Initialize ResNet50 model with 39 classes
num_classes = 39
model = models.resnet50(weights=None)
model.fc = nn.Linear(model.fc.in_features, num_classes)

# Load the trained model
try:
    # Try loading the model file
    if os.path.exists('trained_model.pth'):
        model.load_state_dict(torch.load('trained_model.pth', map_location=torch.device('cpu')))
    elif os.path.exists('ResNet50.pt'):
        model.load_state_dict(torch.load('ResNet50.pt', map_location=torch.device('cpu')))
    else:
        print("Warning: Model file not found. Using untrained model.")
except Exception as e:
    print(f"Warning: Could not load model: {e}. Using untrained model.")

model.eval()

# Image transformation
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def predict(file_path):
    try:
        # Open and preprocess the image
        img = Image.open(file_path).convert('RGB')
        img = transform(img)
        img = img.unsqueeze(0)
        
        # Make a prediction
        with torch.no_grad():
            output = model(img)
            predicted_class = torch.argmax(output, dim=1).item()
        
        return predicted_class
    except Exception as e:
        print(f"Prediction error: {e}")
        return 0  # Return default class if prediction fails

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('contact-us.html')

@app.route('/index')
def ai_engine_page():
    return render_template('index.html')

@app.route('/mobile-device')
def mobile_device_detected_page():
    return render_template('mobile-device.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        try:
            if 'image' not in request.files:
                return "No image file provided", 400
            
            image = request.files['image']
            if image.filename == '':
                return "No image selected", 400
            
            filename = secure_filename(image.filename) or 'upload.jpg'
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(file_path)
            print(f"Image saved to: {file_path}")
            
            pred = predict(file_path)
            
            # Ensure pred is within valid range
            if pred >= len(disease_info):
                pred = 0
            
            title = disease_info['disease_name'].iloc[pred]
            description = disease_info['description'].iloc[pred]
            prevent = disease_info['Possible Steps'].iloc[pred]
            image_url = disease_info['image_url'].iloc[pred]
            supplement_name = supplement_info['supplement name'].iloc[pred]
            supplement_image_url = supplement_info['supplement image'].iloc[pred]
            supplement_buy_link = supplement_info['buy link'].iloc[pred]
            
            return render_template('submit.html', title=title, desc=description, prevent=prevent,
                                   image_url=image_url, pred=pred, sname=supplement_name, 
                                   simage=supplement_image_url, buy_link=supplement_buy_link)
        except Exception as e:
            return f"Error processing image: {str(e)}", 500
    
    return render_template('index.html')

@app.route('/market', methods=['GET', 'POST'])
def market():
    return render_template('market.html', 
                         supplement_image=list(supplement_info['supplement image']),
                         supplement_name=list(supplement_info['supplement name']), 
                         disease=list(disease_info['disease_name']), 
                         buy=list(supplement_info['buy link']))

if __name__ == '__main__':
    # Render (and other hosts) set PORT; locally it defaults to 5000.
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', '1') == '1'
    app.run(host='0.0.0.0', port=port, debug=debug)
