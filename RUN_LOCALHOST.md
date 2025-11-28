# How to Run CultiKure on Localhost

## Prerequisites
- Python 3.7 or higher installed
- All dependencies installed

## Step-by-Step Instructions

### Step 1: Open Terminal/Command Prompt
- Press `Win + R`, type `cmd` or `powershell`, and press Enter
- Or right-click in the App folder and select "Open in Terminal"

### Step 2: Navigate to the App Directory
```powershell
cd "c:\Users\Tanishq j amin\OneDrive\Documents\CultiKure-Disease-Prediction-main\CultiKure-Disease-Prediction-main\App"
```

### Step 3: Verify Dependencies (Optional)
Check if required packages are installed:
```powershell
python -m pip list | Select-String "Flask|torch|Pillow|pandas|numpy"
```

If packages are missing, install them:
```powershell
python -m pip install -r requirements.txt
```

### Step 4: Run the Application

#### Option A: Simple Method (Recommended)
Run the Flask app directly:
```powershell
python app.py
```

#### Option B: Using quick_start.py
Run the quick start script (includes ngrok tunnel attempt):
```powershell
python quick_start.py
```

### Step 5: Access the Application
Once you see "Running on..." message:
1. Open your web browser
2. Go to: **http://localhost:5000**
3. You should see the CultiKure homepage

### Step 6: Stop the Application
- Press `Ctrl + C` in the terminal to stop the server

## Troubleshooting

### Port 5000 Already in Use
If you get an error that port 5000 is busy:
1. Find what's using it: `netstat -ano | findstr :5000`
2. Or change the port in `app.py` (last line) to a different port like 5001

### Missing Dependencies
If you see import errors:
```powershell
python -m pip install Flask Pillow pandas numpy torch torchvision pyngrok
```

### Model File Not Found
Make sure `trained_model.pth` exists in the App folder. The app will still run but may not make predictions.

## Available Routes
- Home: http://localhost:5000
- AI Engine: http://localhost:5000/index
- Market: http://localhost:5000/market
- Contact: http://localhost:5000/contact

