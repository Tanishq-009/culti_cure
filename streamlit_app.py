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

# Custom CSS to match Flask app exactly
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@100;400;600;700&display=swap');
    
    .main {
        font-family: 'Poppins', sans-serif;
        background-color: #f5f5f5;
    }
    
    .stApp {
        background-color: #f5f5f5;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Header styling */
    .navbar {
        background-color: #f8f9fa;
        padding: 1rem 2rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    .navbar-brand {
        font-size: 20px;
        font-weight: 600;
        color: #ff914d;
        text-decoration: none;
    }
    
    .nav-link {
        color: #333;
        text-decoration: none;
        margin: 0 1rem;
        font-weight: 500;
    }
    
    .nav-link:hover {
        color: #ff914d;
    }
    
    /* Button styling - only for Start button */
    button[kind="primary"] {
        background-image: linear-gradient(270deg, #ff914d, #ff3131) !important;
        color: white !important;
        border: none !important;
        border-radius: 100px !important;
        padding: 1% 6% !important;
        font-size: 20px !important;
        font-weight: 600 !important;
    }
    
    /* Submit button styling - green button */
    button[data-testid="baseButton-secondary"] {
        background-color: #28a745 !important;
        color: white !important;
        border: none !important;
        border-radius: 5px !important;
    }
    
    button[data-testid="baseButton-secondary"]:hover {
        background-color: #218838 !important;
    }
    
    .red-btn {
        background-image: linear-gradient(300deg, #ff5c4d, #ff4d4d);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        cursor: pointer;
        text-decoration: none;
        display: inline-block;
    }
    
    .green-btn {
        background-color: #05380b;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1.5rem;
        cursor: pointer;
        text-decoration: none;
        display: inline-block;
    }
    
    /* Navigation button styling */
    div[data-testid="column"]:nth-of-type(2) button,
    div[data-testid="column"]:nth-of-type(3) button,
    div[data-testid="column"]:nth-of-type(4) button,
    div[data-testid="column"]:nth-of-type(5) button {
        background: transparent;
        color: #333;
        border: none;
        font-weight: 500;
        box-shadow: none;
    }
    
    div[data-testid="column"]:nth-of-type(2) button:hover,
    div[data-testid="column"]:nth-of-type(3) button:hover,
    div[data-testid="column"]:nth-of-type(4) button:hover,
    div[data-testid="column"]:nth-of-type(5) button:hover {
        color: #ff914d;
        background: transparent;
    }
    
    /* Card styling */
    .card {
        background: white;
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
        height: 100%;
    }
    
    .card-sm {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem;
        width: 90%;
        height: 100%;
    }
    
    /* Title styling */
    .main-title {
        font-size: 3rem;
        font-weight: 400;
        color: black;
        text-align: center;
        padding-top: 10%;
        margin-bottom: 1rem;
    }
    
    .subtitle {
        font-weight: 500;
        color: black;
        font-size: 17px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .page-title {
        font-size: 2.5rem;
        font-weight: 400;
        color: rgb(4, 54, 4);
        text-align: center;
        padding-top: 2%;
        margin-bottom: 1rem;
    }
    
    .disease-title {
        font-size: 1.8rem;
        font-weight: 400;
        color: rgb(33, 32, 35);
        text-align: center;
        padding-top: 10%;
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

# Navigation Header
def render_header():
    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
    with col1:
        st.markdown("""
        <div style="font-size: 20px; font-weight: 600; color: #ff914d; margin-top: 10px;">
            <span style="color: #ff914d; font-size: 24px;">क</span> CultiKure
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
    st.markdown("---")

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
    <div class="main-title"><b>PLANT DISEASE DETECTION</b></div>
    <p class="subtitle">This AI Engine Will Help To Detect Disease From Following Fruites And Veggies</p>
    """, unsafe_allow_html=True)
    
    # Center the Start button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Start", use_container_width=True, key="start_btn"):
            st.session_state.page = "AI Disease Detection"
            st.rerun()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Four process cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="card-sm" style="text-align: center;">
            <p style="font-size: 0.9rem; color: #666;">Upload plant leaf image</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card-sm" style="text-align: center;">
            <p style="font-size: 0.9rem; color: #666;">AI analyzes the image</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card-sm" style="text-align: center;">
            <p style="font-size: 0.9rem; color: #666;">Get treatment recommendations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="card-sm" style="text-align: center;">
            <p style="color: #ff914d; font-weight: 600; font-size: 1.1rem;">HAPPY CROPS</p>
            <p style="font-size: 0.9rem; color: #666;">Healthy plants and better yields</p>
        </div>
        """, unsafe_allow_html=True)

# AI Disease Detection Page
elif st.session_state.page == "AI Disease Detection":
    st.markdown("""
    <h1 class="page-title"><b>Detect Disease</b></h1>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h5><b>Why is it necessary to detect disease in plant ?</b></h5>
            <p style="line-height: 1.8;">
            Plant diseases affect the growth of their respective species. In addition, some research gaps are
            identified from which to obtain greater transparency for detecting diseases in plants, even
            before their symptoms appear clearly. Diagnosis is one of the most important aspects of a plant 
            pathologist's training. Without proper identification of the disease and the disease-causing agent, 
            disease control measures can be a waste of time and money and can lead to further plant losses. 
            Proper disease diagnosis is necessary.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h6 style="text-align: center; color: #666; margin-bottom: 2rem;">
                Simply upload your plant's leaf image and then see the magic of AI.
            </h6>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose an image...",
            type=['jpg', 'jpeg', 'png'],
            help="Upload a clear image of a plant leaf",
            key="file_uploader"
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Reset analyzed state if new file uploaded
    if uploaded_file is not None:
        if st.session_state.last_file != uploaded_file:
            st.session_state.analyzed = False
        st.session_state.last_file = uploaded_file
        
        # Show uploaded image and analyze button
        st.markdown("---")
        col1, col2 = st.columns([1, 1])
        
        with col1:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
        
        with col2:
            if st.button("Submit", use_container_width=True, key="analyze_btn"):
                with st.spinner("Analyzing image... Please wait."):
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
            
            st.markdown("---")
            
            # Disease title and image
            st.markdown(f"""
            <h3 class="disease-title"><b>{title}</b></h3>
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
            st.markdown("""
            <div class="card">
                <h5><b>Brief Descritpion :</b></h5>
                <p id="content">{}</p>
            </div>
            """.format(description.replace('\n', '<br>')), unsafe_allow_html=True)
            
            # Prevention and Supplements cards
            col1, col2 = st.columns(2)
            
            with col1:
                prevent_title = "Tips to Grow Healthy Plants :" if is_healthy else "Prevent This Plant Disease By follow below steps :"
                st.markdown(f"""
                <div class="card">
                    <h5><b>{prevent_title}</b></h5>
                    <p>{prevent.replace(chr(10), '<br>')}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if pred != 4:  # Skip background without leaves
                    supplement_title = "Fertilizer :" if is_healthy else "Supplements :"
                    st.markdown(f"""
                    <div class="card">
                        <center>
                            <h5><b>{supplement_title}</b></h5>
                            <br>
                    """, unsafe_allow_html=True)
                    
                    try:
                        if is_valid_url(supplement_image_url):
                            st.image(supplement_image_url, width=200, use_container_width=False)
                    except:
                        pass
                    
                    st.markdown(f"""
                            <br>
                            <h6 id="content">{supplement_name}</h6>
                            <br>
                    """, unsafe_allow_html=True)
                    
                    if is_valid_url(supplement_buy_link):
                        st.markdown(f"""
                        <a target="_blank" href="{supplement_buy_link}">
                            <button class="green-btn">Buy Product</button>
                        </a>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</center></div>", unsafe_allow_html=True)

# Market Page
elif st.session_state.page == "Market":
    st.markdown("""
    <h1 class="page-title"><b>Supplements</b></h1>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 1])
    with col1:
        st.markdown("""
        <p style="font-weight: 500; color: black; font-size: 1.1rem;">Buy Supplements & Fertilizer at one place</p>
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
                    st.markdown(f"""
                    <div class="card-sm">
                        <center>
                    """, unsafe_allow_html=True)
                    
                    if is_healthy:
                        st.markdown("""
                        <h5>Fertilizer<b style="color: green;"> (Healthy):</b></h5>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <h5>Supplements<b style="color: red;"> (Diseased):</b></h5>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    try:
                        img_url = supplement_info['supplement image'].iloc[idx]
                        if is_valid_url(img_url):
                            st.image(img_url, width=100, use_container_width=False)
                    except:
                        pass
                    
                    st.markdown("<br><br>", unsafe_allow_html=True)
                    st.markdown(f"<h6>For {disease_info['disease_name'].iloc[idx]}</h6>", unsafe_allow_html=True)
                    st.markdown(f"<p>{supplement_info['supplement name'].iloc[idx]}</p>", unsafe_allow_html=True)
                    
                    buy_link = supplement_info['buy link'].iloc[idx]
                    if is_valid_url(buy_link):
                        st.markdown(f"""
                        <a target="_blank" href="{buy_link}">
                            <button class="red-btn">Buy Product</button>
                        </a>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</center></div>", unsafe_allow_html=True)

# Contact Us Page
elif st.session_state.page == "Contact Us":
    st.markdown("""
    <h1 class="page-title"><b>📞Contact-Us📞</b></h1>
    <p style="font-weight: 500; color: black; text-align: center; font-size: 1.1rem;">
        For Any Queries & Suggestions Contact Us. We Are Happy To Help.
    </p>
    """, unsafe_allow_html=True)

