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
    initial_sidebar_state="collapsed"
)

# Professional UI/UX Design - Modern & Aesthetic
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .main {
        font-family: 'Inter', 'Poppins', sans-serif;
        background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Modern Navigation Bar */
    .navbar-modern {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 1.2rem 3rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border-bottom: 1px solid rgba(0, 0, 0, 0.05);
        position: sticky;
        top: 0;
        z-index: 1000;
        margin-bottom: 2rem;
    }
    
    .logo-text {
        font-size: 24px;
        font-weight: 700;
        background: linear-gradient(135deg, #ff914d 0%, #ff6b35 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.5px;
    }
    
    .logo-icon {
        font-size: 28px;
        margin-right: 8px;
    }
    
    /* Modern Buttons */
    .btn-primary-modern {
        background: linear-gradient(135deg, #ff914d 0%, #ff6b35 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 14px 40px;
        font-size: 18px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 145, 77, 0.4);
    }
    
    .btn-primary-modern:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 145, 77, 0.5);
    }
    
    .btn-secondary-modern {
        background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 30px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(46, 204, 113, 0.3);
    }
    
    .btn-secondary-modern:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(46, 204, 113, 0.4);
    }
    
    .btn-buy-modern {
        background: linear-gradient(135deg, #ff5c4d 0%, #ff4d4d 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(255, 92, 77, 0.3);
        text-decoration: none;
        display: inline-block;
    }
    
    .btn-buy-modern:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(255, 92, 77, 0.4);
    }
    
    /* Navigation Buttons */
    .nav-btn-modern {
        background: transparent;
        color: #2c3e50;
        border: none;
        font-weight: 500;
        font-size: 15px;
        padding: 8px 16px;
        cursor: pointer;
        transition: all 0.3s ease;
        border-radius: 8px;
    }
    
    .nav-btn-modern:hover {
        background: rgba(255, 145, 77, 0.1);
        color: #ff914d;
    }
    
    /* Modern Cards */
    .card-modern {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
        margin: 1.5rem 0;
        height: 100%;
        transition: all 0.3s ease;
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    .card-modern:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
    }
    
    .card-feature {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        margin: 1rem;
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid rgba(0, 0, 0, 0.05);
        height: 100%;
    }
    
    .card-feature:hover {
        transform: translateY(-8px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
    }
    
    .card-product {
        background: white;
        padding: 1.8rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        margin: 1rem 0;
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid rgba(0, 0, 0, 0.05);
        height: 100%;
    }
    
    .card-product:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }
    
    /* Typography */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin: 3rem 0 1rem 0;
        letter-spacing: -1px;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        color: #5a6c7d;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 400;
        line-height: 1.6;
    }
    
    .section-title {
        font-size: 2.8rem;
        font-weight: 700;
        color: #2c3e50;
        text-align: center;
        margin: 2rem 0 1rem 0;
        letter-spacing: -0.5px;
    }
    
    .card-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    
    .card-text {
        color: #5a6c7d;
        line-height: 1.8;
        font-size: 1rem;
    }
    
    /* Feature Icons */
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .feature-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        color: #7f8c8d;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Status Badges */
    .badge-healthy {
        background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .badge-diseased {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }
    
    /* Upload Area */
    .upload-area {
        border: 2px dashed #bdc3c7;
        border-radius: 16px;
        padding: 3rem;
        text-align: center;
        background: #f8f9fa;
        transition: all 0.3s ease;
    }
    
    .upload-area:hover {
        border-color: #ff914d;
        background: #fff5f0;
    }
    
    /* Results Section */
    .result-card {
        background: linear-gradient(135deg, #fff 0%, #f8f9fa 100%);
        border-left: 4px solid #ff914d;
        padding: 2rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        .section-title {
            font-size: 2rem;
        }
    }
    
    /* Custom Streamlit Button Overrides */
    button[kind="primary"] {
        background: linear-gradient(135deg, #ff914d 0%, #ff6b35 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 14px 40px !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(255, 145, 77, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 145, 77, 0.5) !important;
    }
    
    button[data-testid="baseButton-secondary"] {
        background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 30px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(46, 204, 113, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    button[data-testid="baseButton-secondary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(46, 204, 113, 0.4) !important;
    }
    
    /* Navigation buttons styling */
    div[data-testid="column"]:nth-of-type(2) button,
    div[data-testid="column"]:nth-of-type(3) button,
    div[data-testid="column"]:nth-of-type(4) button,
    div[data-testid="column"]:nth-of-type(5) button {
        background: transparent !important;
        color: #2c3e50 !important;
        border: none !important;
        font-weight: 500 !important;
        font-size: 15px !important;
        box-shadow: none !important;
        padding: 8px 16px !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="column"]:nth-of-type(2) button:hover,
    div[data-testid="column"]:nth-of-type(3) button:hover,
    div[data-testid="column"]:nth-of-type(4) button:hover,
    div[data-testid="column"]:nth-of-type(5) button:hover {
        background: rgba(255, 145, 77, 0.1) !important;
        color: #ff914d !important;
    }
</style>
""", unsafe_allow_html=True)

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
        if image.mode != 'RGB':
            image = image.convert('RGB')
        img = transform(image)
        img = img.unsqueeze(0)
        with torch.no_grad():
            output = model(img)
            predicted_class = torch.argmax(output, dim=1).item()
        return predicted_class
    except Exception as e:
        st.error(f"Prediction error: {e}")
        return 0

def is_valid_url(url):
    """Check if URL is valid"""
    try:
        if pd.isna(url) or url == '' or not isinstance(url, str):
            return False
        return url.startswith('http://') or url.startswith('https://')
    except:
        return False

# Modern Navigation Header
def render_header():
    col1, col2, col3, col4, col5 = st.columns([2.5, 1, 1, 1, 1])
    with col1:
        st.markdown("""
        <div style="display: flex; align-items: center; margin-top: 10px;">
            <span class="logo-icon">🌱</span>
            <span class="logo-text">CultiKure</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("Home", use_container_width=True, key="nav_home"):
            st.session_state.page = "Home"
            st.rerun()
    with col3:
        if st.button("Supplements", use_container_width=True, key="nav_supplements"):
            st.session_state.page = "Market"
            st.rerun()
    with col4:
        if st.button("AiEngine", use_container_width=True, key="nav_ai"):
            st.session_state.page = "AI Disease Detection"
            st.rerun()
    with col5:
        if st.button("Contact Us", use_container_width=True, key="nav_contact"):
            st.session_state.page = "Contact Us"
            st.rerun()
    st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'Home'
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False
if 'pred' not in st.session_state:
    st.session_state.pred = 0
if 'last_file' not in st.session_state:
    st.session_state.last_file = None

# Render header
render_header()

# Sidebar navigation (hidden)
st.sidebar.markdown("""
<style>
    .sidebar .sidebar-content {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Home Page
if st.session_state.page == "Home":
    st.markdown("""
    <div class="fade-in">
        <h1 class="hero-title">Plant Disease Detection</h1>
        <p class="hero-subtitle">
            Advanced AI-powered system to detect and diagnose plant diseases from leaf images.<br>
            Get instant, accurate results to protect your crops and ensure healthy yields.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Center the Start button
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        if st.button("🚀 Get Started", use_container_width=True, key="start_btn"):
            st.session_state.page = "AI Disease Detection"
            st.rerun()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Four feature cards with icons
    st.markdown("""
    <div style="margin: 3rem 0;">
        <h2 style="text-align: center; font-size: 2rem; font-weight: 700; color: #2c3e50; margin-bottom: 2rem;">
            How It Works
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    features = [
        {"icon": "📸", "title": "Upload Image", "desc": "Simply upload a clear photo of your plant leaf"},
        {"icon": "🤖", "title": "AI Analysis", "desc": "Our advanced AI analyzes the image in seconds"},
        {"icon": "💊", "title": "Get Solutions", "desc": "Receive treatment recommendations and supplements"},
        {"icon": "🌾", "title": "Healthy Crops", "desc": "Enjoy bountiful harvests with healthy plants"}
    ]
    
    for i, feature in enumerate(features):
        with [col1, col2, col3, col4][i]:
            st.markdown(f"""
            <div class="card-feature fade-in">
                <span class="feature-icon">{feature['icon']}</span>
                <h3 class="feature-title">{feature['title']}</h3>
                <p class="feature-desc">{feature['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

# AI Disease Detection Page
elif st.session_state.page == "AI Disease Detection":
    st.markdown("""
    <h1 class="section-title">Detect Disease</h1>
    <p style="text-align: center; color: #5a6c7d; font-size: 1.1rem; margin-bottom: 3rem;">
        Upload your plant leaf image and let our AI analyze it for you
    </p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card-modern fade-in">
            <h3 class="card-title">Why Detect Plant Diseases?</h3>
            <p class="card-text">
                Early detection of plant diseases is crucial for maintaining healthy crops and maximizing yields. 
                Plant diseases can spread rapidly and cause significant damage if not identified and treated promptly. 
                Our AI-powered system helps you identify diseases before they become severe, allowing you to take 
                preventive measures and protect your agricultural investment.
            </p>
            <br>
            <p class="card-text">
                <strong>Benefits:</strong><br>
                ✓ Early intervention saves crops<br>
                ✓ Reduces treatment costs<br>
                ✓ Prevents disease spread<br>
                ✓ Ensures better yields
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card-modern fade-in">
            <h3 class="card-title" style="text-align: center;">Upload Your Image</h3>
            <p class="card-text" style="text-align: center; margin-bottom: 2rem;">
                Simply upload a clear image of your plant's leaf and watch our AI work its magic.
            </p>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['jpg', 'jpeg', 'png'],
            help="Upload a clear, well-lit image of a plant leaf for best results",
            key="file_uploader"
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Reset analyzed state if new file uploaded
    if uploaded_file is not None:
        if st.session_state.last_file != uploaded_file:
            st.session_state.analyzed = False
        st.session_state.last_file = uploaded_file
        
        # Show uploaded image and analyze button
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1])
        
        with col1:
            image = Image.open(uploaded_file)
            st.markdown("""
            <div style="text-align: center; margin-bottom: 1rem;">
                <h4 style="color: #2c3e50; font-weight: 600;">Uploaded Image</h4>
            </div>
            """, unsafe_allow_html=True)
            st.image(image, use_container_width=True)
        
        with col2:
            st.markdown("""
            <div style="text-align: center; margin-bottom: 1rem;">
                <h4 style="color: #2c3e50; font-weight: 600;">Ready to Analyze</h4>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🔍 Analyze Image", use_container_width=True, key="analyze_btn"):
                with st.spinner("🤖 AI is analyzing your image... Please wait."):
                    pred = predict(image)
                    if pred >= len(disease_info):
                        pred = 0
                    st.session_state.pred = pred
                    st.session_state.analyzed = True
                    st.rerun()
        
        # Display results if analyzed
        if st.session_state.get('analyzed', False):
            pred = st.session_state.get('pred', 0)
            
            # Get disease information
            title = disease_info['disease_name'].iloc[pred]
            description = disease_info['description'].iloc[pred]
            prevent = disease_info['Possible Steps'].iloc[pred]
            image_url = disease_info['image_url'].iloc[pred]
            supplement_name = supplement_info['supplement name'].iloc[pred]
            supplement_image_url = supplement_info['supplement image'].iloc[pred]
            supplement_buy_link = supplement_info['buy link'].iloc[pred]
            
            # Check if healthy plant
            healthy_indices = [3, 5, 7, 11, 15, 18, 20, 23, 24, 25, 28, 38]
            is_healthy = pred in healthy_indices
            
            st.markdown("<br><br>", unsafe_allow_html=True)
            
            # Disease title and image
            st.markdown(f"""
            <div class="fade-in">
                <h2 style="text-align: center; font-size: 2.2rem; font-weight: 700; color: #2c3e50; margin-bottom: 2rem;">
                    {title}
                </h2>
            </div>
            """, unsafe_allow_html=True)
            
            col_img, _ = st.columns([1, 2])
            with col_img:
                try:
                    if is_valid_url(image_url):
                        st.image(image_url, use_container_width=True)
                except:
                    pass
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Description card
            st.markdown(f"""
            <div class="card-modern fade-in">
                <h3 class="card-title">📋 Brief Description</h3>
                <p class="card-text">{description.replace(chr(10), '<br>')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Prevention and Supplements cards
            col1, col2 = st.columns(2)
            
            with col1:
                prevent_title = "🌿 Tips to Grow Healthy Plants" if is_healthy else "🛡️ Prevention Steps"
                st.markdown(f"""
                <div class="card-modern fade-in">
                    <h3 class="card-title">{prevent_title}</h3>
                    <p class="card-text">{prevent.replace(chr(10), '<br>')}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if pred != 4:  # Skip background without leaves
                    supplement_title = "🌱 Recommended Fertilizer" if is_healthy else "💊 Recommended Supplement"
                    st.markdown(f"""
                    <div class="card-modern fade-in" style="text-align: center;">
                        <h3 class="card-title">{supplement_title}</h3>
                        <br>
                    """, unsafe_allow_html=True)
                    
                    try:
                        if is_valid_url(supplement_image_url):
                            st.image(supplement_image_url, width=200, use_container_width=False)
                    except:
                        pass
                    
                    st.markdown(f"""
                        <br>
                        <h4 style="color: #2c3e50; font-weight: 600; margin: 1rem 0;">{supplement_name}</h4>
                        <br>
                    """, unsafe_allow_html=True)
                    
                    if is_valid_url(supplement_buy_link):
                        st.markdown(f"""
                        <a target="_blank" href="{supplement_buy_link}" style="text-decoration: none;">
                            <button class="btn-buy-modern">🛒 Buy Product</button>
                        </a>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)

# Market Page
elif st.session_state.page == "Market":
    st.markdown("""
    <h1 class="section-title">Supplements & Fertilizers</h1>
    <p style="text-align: center; color: #5a6c7d; font-size: 1.1rem; margin-bottom: 2rem;">
        Browse our curated selection of supplements and fertilizers for optimal plant health
    </p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("""
        <p style="font-weight: 500; color: #2c3e50; font-size: 1.1rem;">
            Buy Supplements & Fertilizer at one place
        </p>
        """, unsafe_allow_html=True)
    with col2:
        filter_option = st.selectbox(
            "Filter",
            ["All", "Fertilizer", "Supplements"],
            label_visibility="collapsed",
            key="market_filter"
        )
    
    # Display supplements in grid
    healthy_indices = [3, 5, 7, 11, 15, 18, 20, 23, 24, 25, 28, 38]
    
    cols_per_row = 3
    num_items = len(supplement_info)
    
    for i in range(0, num_items, cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < num_items and idx != 4:  # Skip index 4
                is_healthy = idx in healthy_indices
                
                # Apply filter
                if filter_option == "Fertilizer" and not is_healthy:
                    continue
                if filter_option == "Supplements" and is_healthy:
                    continue
                
                with col:
                    badge = '<span class="badge-healthy">Healthy</span>' if is_healthy else '<span class="badge-diseased">Diseased</span>'
                    product_type = "Fertilizer" if is_healthy else "Supplements"
                    
                    st.markdown(f"""
                    <div class="card-product fade-in">
                        <div style="margin-bottom: 1rem;">
                            <h5 style="color: #2c3e50; font-weight: 600; margin-bottom: 0.5rem;">{product_type}</h5>
                            {badge}
                        </div>
                    """, unsafe_allow_html=True)
                    
                    try:
                        img_url = supplement_info['supplement image'].iloc[idx]
                        if is_valid_url(img_url):
                            st.image(img_url, width=120, use_container_width=False)
                    except:
                        pass
                    
                    st.markdown(f"""
                        <br>
                        <h6 style="color: #2c3e50; font-weight: 600; margin: 1rem 0;">
                            For {disease_info['disease_name'].iloc[idx]}
                        </h6>
                        <p style="color: #5a6c7d; font-size: 0.95rem; margin-bottom: 1.5rem;">
                            {supplement_info['supplement name'].iloc[idx]}
                        </p>
                    """, unsafe_allow_html=True)
                    
                    buy_link = supplement_info['buy link'].iloc[idx]
                    if is_valid_url(buy_link):
                        st.markdown(f"""
                        <a target="_blank" href="{buy_link}" style="text-decoration: none;">
                            <button class="btn-buy-modern">🛒 Buy Product</button>
                        </a>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)

# Contact Us Page
elif st.session_state.page == "Contact Us":
    st.markdown("""
    <h1 class="section-title">Contact Us</h1>
    <p style="text-align: center; color: #5a6c7d; font-size: 1.1rem; margin-bottom: 3rem;">
        Have questions or suggestions? We're here to help! Get in touch with our team.
    </p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card-modern fade-in">
            <h3 class="card-title">🌱 Get in Touch</h3>
            <p class="card-text" style="margin-bottom: 2rem;">
                We're here to help you with any questions, technical support, or feedback about CultiKure.
            </p>
            <div style="margin: 1.5rem 0;">
                <h4 style="color: #2c3e50; font-weight: 600; margin-bottom: 1rem;">Contact Information</h4>
                <p class="card-text">
                    <strong>📧 Email:</strong> support@cultikure.com<br><br>
                    <strong>📞 Phone:</strong> +1 (555) 123-4567<br><br>
                    <strong>📍 Address:</strong> 123 Agriculture Street<br>
                    Farm City, FC 12345
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card-modern fade-in">
            <h3 class="card-title">💬 Send us a Message</h3>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("contact_form"):
            name = st.text_input("Your Name *", placeholder="Enter your name")
            email = st.text_input("Your Email *", placeholder="Enter your email")
            message = st.text_area("Your Message *", height=200, placeholder="Type your message here...")
            submit = st.form_submit_button("📤 Send Message", use_container_width=True)
            
            if submit:
                if name and email and message:
                    st.success("✅ Thank you for your message! We'll get back to you soon.")
                else:
                    st.error("⚠️ Please fill in all fields marked with *.")
