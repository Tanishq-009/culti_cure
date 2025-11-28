import streamlit as st
import os
from PIL import Image
import torchvision.transforms.functional as TF
import numpy as np
import torch
import pandas as pd
import torch.nn as nn
from torchvision import transforms
import torchvision.models as models

# Page configuration
st.set_page_config(
    page_title="CultiKure - Plant Disease Prediction",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSV files
@st.cache_data
def load_data():
    disease_info = pd.read_csv('disease_info.csv', encoding='cp1252')
    supplement_info = pd.read_csv('supplement_info.csv', encoding='cp1252')
    return disease_info, supplement_info

disease_info, supplement_info = load_data()

# Initialize and load model
@st.cache_resource
def load_model():
    num_classes = 39
    model = models.resnet50(pretrained=False)
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    
    try:
        if os.path.exists('trained_model.pth'):
            model.load_state_dict(torch.load('trained_model.pth', map_location=torch.device('cpu')))
        elif os.path.exists('ResNet50.pt'):
            model.load_state_dict(torch.load('ResNet50.pt', map_location=torch.device('cpu')))
        else:
            st.warning("Model file not found. Using untrained model.")
    except Exception as e:
        st.warning(f"Could not load model: {e}. Using untrained model.")
    
    model.eval()
    return model

model = load_model()

# Image transformation
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def predict(image):
    """Predict disease from image"""
    try:
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Preprocess
        img = transform(image)
        img = img.unsqueeze(0)
        
        # Make prediction
        with torch.no_grad():
            output = model(img)
            predicted_class = torch.argmax(output, dim=1).item()
        
        return predicted_class
    except Exception as e:
        st.error(f"Prediction error: {e}")
        return 0

# Sidebar navigation
st.sidebar.title("🌱 CultiKure")
st.sidebar.markdown("### Plant Disease Prediction")

page = st.sidebar.radio(
    "Navigate",
    ["Home", "AI Disease Detection", "Market", "Contact Us"]
)

# Home Page
if page == "Home":
    st.title("🌱 Welcome to CultiKure")
    st.markdown("### AI-Powered Plant Disease Detection System")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **CultiKure** is a web-based tool designed to help users detect and address diseases in plants. 
        By analyzing images of plant leaves, this application employs advanced AI technology to identify 
        potential plant health issues, ensuring healthier crops and better yields.
        
        ### Key Features:
        - 🤖 **AI-Powered Disease Detection:** Upload plant leaf images to get real-time analysis
        - 📊 **Informative Reports:** Receive detailed reports about detected diseases
        - 💊 **Supplement Market:** Explore supplements and fertilizers to support plant health
        - 🎯 **User-Friendly Interface:** Intuitive and easy-to-navigate design
        
        ### How to Use:
        1. Navigate to **AI Disease Detection** from the sidebar
        2. Upload an image of a plant leaf
        3. Receive detailed information about the detected disease, including tips and product recommendations
        """)
    
    with col2:
        st.image("https://via.placeholder.com/300x400?text=CultiKure", use_container_width=True)
    
    st.markdown("---")
    st.markdown("### Why Plant Disease Detection Matters")
    st.info("""
    Plant diseases can significantly impact crop health and yield. Early detection and intervention are crucial. 
    CultiKure helps users identify and address potential issues, ensuring healthier crops and better yields.
    """)

# AI Disease Detection Page
elif page == "AI Disease Detection":
    st.title("🤖 AI Disease Detection Engine")
    st.markdown("Upload an image of a plant leaf to detect potential diseases")
    
    uploaded_file = st.file_uploader(
        "Choose an image...",
        type=['jpg', 'jpeg', 'png'],
        help="Upload a clear image of a plant leaf"
    )
    
    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(image, caption="Uploaded Image", use_container_width=True)
        
        with col2:
            if st.button("🔍 Analyze Image", type="primary", use_container_width=True):
                with st.spinner("Analyzing image... Please wait."):
                    pred = predict(image)
                    
                    # Ensure pred is within valid range
                    if pred >= len(disease_info):
                        pred = 0
                    
                    # Get disease information
                    title = disease_info['disease_name'].iloc[pred]
                    description = disease_info['description'].iloc[pred]
                    prevent = disease_info['Possible Steps'].iloc[pred]
                    image_url = disease_info['image_url'].iloc[pred]
                    supplement_name = supplement_info['supplement name'].iloc[pred]
                    supplement_image_url = supplement_info['supplement image'].iloc[pred]
                    supplement_buy_link = supplement_info['buy link'].iloc[pred]
                    
                    # Display results
                    st.success(f"✅ **Detected Disease:** {title}")
                    
                    st.markdown("### 📋 Disease Information")
                    st.markdown(f"**Description:**\n{description}")
                    
                    st.markdown("### 🛡️ Prevention Steps")
                    st.markdown(prevent)
                    
                    st.markdown("### 💊 Recommended Supplement")
                    col_sup1, col_sup2 = st.columns([1, 2])
                    with col_sup1:
                        try:
                            st.image(supplement_image_url, caption=supplement_name, use_container_width=True)
                        except:
                            st.info("Image not available")
                    with col_sup2:
                        st.markdown(f"**{supplement_name}**")
                        st.link_button("🛒 Buy Now", supplement_buy_link)
    else:
        st.info("👆 Please upload an image to get started")

# Market Page
elif page == "Market":
    st.title("🛒 Supplement Market")
    st.markdown("Browse available supplements and fertilizers for plant health")
    
    # Display supplements in a grid
    num_supplements = len(supplement_info)
    cols_per_row = 3
    
    for i in range(0, num_supplements, cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < num_supplements:
                with col:
                    try:
                        st.image(
                            supplement_info['supplement image'].iloc[idx],
                            use_container_width=True
                        )
                    except:
                        st.info("Image not available")
                    
                    st.markdown(f"**{supplement_info['supplement name'].iloc[idx]}**")
                    st.caption(f"For: {disease_info['disease_name'].iloc[idx]}")
                    
                    buy_link = supplement_info['buy link'].iloc[idx]
                    st.link_button("🛒 Buy", buy_link, use_container_width=True)
                    st.markdown("---")

# Contact Us Page
elif page == "Contact Us":
    st.title("📧 Contact Us")
    st.markdown("Get in touch with us for support or inquiries")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🌱 CultiKure Team
        
        We're here to help you with:
        - Technical support
        - Feature requests
        - General inquiries
        - Feedback and suggestions
        
        ### 📍 Contact Information
        - **Email:** support@cultikure.com
        - **Phone:** +1 (555) 123-4567
        - **Address:** 123 Agriculture Street, Farm City, FC 12345
        """)
    
    with col2:
        st.markdown("### 💬 Send us a Message")
        
        contact_form = st.form("contact_form")
        name = contact_form.text_input("Name")
        email = contact_form.text_input("Email")
        message = contact_form.text_area("Message", height=200)
        submit = contact_form.form_submit_button("Send Message")
        
        if submit:
            if name and email and message:
                st.success("✅ Thank you for your message! We'll get back to you soon.")
            else:
                st.error("Please fill in all fields.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("""
### About
CultiKure uses advanced AI technology to help farmers and gardeners identify plant diseases early.

**Version:** 1.0.0
""")

