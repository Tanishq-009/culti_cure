# How to Deploy CultiKure on Streamlit

## Prerequisites
- Python 3.7 or higher
- All dependencies installed
- GitHub account (for Streamlit Cloud deployment)

## Method 1: Run Locally

### Step 1: Install Streamlit
```powershell
pip install streamlit
```

Or install all requirements:
```powershell
pip install -r requirements_streamlit.txt
```

### Step 2: Run the Streamlit App
Navigate to the App directory and run:
```powershell
cd "c:\Users\Tanishq j amin\OneDrive\Documents\CultiKure-Disease-Prediction-main\CultiKure-Disease-Prediction-main\App"
streamlit run streamlit_app.py
```

The app will automatically open in your browser at `http://localhost:8501`

### Step 3: Stop the App
Press `Ctrl + C` in the terminal

---

## Method 2: Deploy to Streamlit Cloud (Free)

### Step 1: Create a GitHub Repository
1. Go to [GitHub](https://github.com) and create a new repository
2. Name it something like `cultikure-streamlit`
3. Make it public (required for free Streamlit Cloud)

### Step 2: Prepare Your Files
Make sure you have these files in your repository:
- `streamlit_app.py` (main app file)
- `requirements_streamlit.txt` (or `requirements.txt` with streamlit added)
- `trained_model.pth` (your trained model)
- `disease_info.csv`
- `supplement_info.csv`
- `CNN.py` (if needed)

### Step 3: Create requirements.txt for Streamlit Cloud
Create a `requirements.txt` file in the root of your repository:

```txt
streamlit>=1.28.0
Pillow
pandas
numpy
torch>=2.9.0
torchvision>=0.24.0
```

**Note:** For Streamlit Cloud, you may need to use CPU-only versions:
```txt
streamlit>=1.28.0
Pillow
pandas
numpy
torch==2.9.0+cpu
torchvision==0.24.0+cpu
--extra-index-url https://download.pytorch.org/whl/cpu
```

### Step 4: Push to GitHub
```powershell
git init
git add .
git commit -m "Initial commit - Streamlit app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### Step 5: Deploy to Streamlit Cloud
1. Go to [Streamlit Cloud](https://streamlit.io/cloud)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository
5. Set the main file path to: `App/streamlit_app.py` (or just `streamlit_app.py` if it's in root)
6. Click "Deploy"

### Step 6: Wait for Deployment
Streamlit Cloud will:
- Install dependencies from `requirements.txt`
- Deploy your app
- Provide you with a public URL (e.g., `https://your-app.streamlit.app`)

---

## Method 3: Deploy to Streamlit Community Cloud (Easiest)

### Quick Steps:
1. **Push to GitHub** (as in Method 2, Step 4)
2. **Go to**: https://share.streamlit.io/
3. **Sign in** with GitHub
4. **Click "New app"**
5. **Select repository** and branch
6. **Set main file**: `App/streamlit_app.py`
7. **Click "Deploy"**

---

## File Structure for Deployment

Your repository should look like this:
```
your-repo/
├── App/
│   ├── streamlit_app.py
│   ├── trained_model.pth
│   ├── disease_info.csv
│   ├── supplement_info.csv
│   └── requirements.txt (or requirements_streamlit.txt)
└── README.md
```

Or if files are in root:
```
your-repo/
├── streamlit_app.py
├── trained_model.pth
├── disease_info.csv
├── supplement_info.csv
├── requirements.txt
└── README.md
```

---

## Important Notes for Streamlit Cloud

### 1. File Size Limits
- Free tier: 1GB total
- Your `trained_model.pth` file should be under 1GB
- If larger, consider using Git LFS or hosting the model elsewhere

### 2. Model Loading
- The app uses `@st.cache_resource` to cache the model
- This ensures the model loads only once per session

### 3. CSV Files
- Make sure CSV files are in the same directory as `streamlit_app.py`
- Or update paths in the code

### 4. Environment Variables
If you need API keys or secrets:
1. Go to your app settings in Streamlit Cloud
2. Add secrets in the "Secrets" section
3. Access them in code: `st.secrets["your_key"]`

---

## Troubleshooting

### Issue: App won't deploy
- Check that `requirements.txt` is in the correct location
- Verify all file paths are correct
- Check Streamlit Cloud logs for errors

### Issue: Model not loading
- Ensure `trained_model.pth` is in the repository
- Check file paths in `streamlit_app.py`
- Verify model file size is within limits

### Issue: CSV files not found
- Check CSV file paths match your repository structure
- Ensure CSV files are committed to GitHub

### Issue: Dependencies not installing
- Verify `requirements.txt` syntax is correct
- Check PyTorch installation (may need CPU-only version for cloud)

---

## Local Development Tips

### Run with auto-reload
```powershell
streamlit run streamlit_app.py --server.runOnSave true
```

### Run on different port
```powershell
streamlit run streamlit_app.py --server.port 8502
```

### View app in browser automatically
```powershell
streamlit run streamlit_app.py --server.headless false
```

---

## Comparison: Flask vs Streamlit

| Feature | Flask | Streamlit |
|---------|-------|-----------|
| Setup | More complex | Simple |
| UI | HTML/CSS/JS | Python widgets |
| Deployment | More options | Streamlit Cloud (easiest) |
| Learning Curve | Steeper | Easier |
| Customization | Full control | Limited but faster |

---

## Next Steps

1. ✅ Test locally first
2. ✅ Push to GitHub
3. ✅ Deploy to Streamlit Cloud
4. ✅ Share your public URL!

Your app will be live at: `https://your-username-your-app-name.streamlit.app`

