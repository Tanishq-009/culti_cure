# 🌱 Culti Cure

**Culti Cure** is an intelligent website designed for farmers and agriculturists to diagnose plant diseases using deep learning. Easily upload an image of a diseased plant and receive instant, AI-powered predictions along with remedies and supplement recommendations.

---

## ✨ Features

- **AI Disease Detection:** Diagnose plant diseases instantly with a trained deep learning model (CNN).
- **Vast Disease Information:** Get details about plant diseases, symptoms, and preventive care steps.
- **Personalized Supplement Recommendations:** Discover supplements and products to boost crop health.
- **Modern Website UI:** Simple, fast, and user-friendly web interface.
- **Python & Flask Powered:** Built using widely-used Python frameworks for easy development and deployment.

---

## 🚀 Demo

<!-- Add a live demo URL or screenshots if available -->
To try locally, follow the instructions below!

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Machine Learning:** PyTorch, Custom CNN Model (`trained_model.pth`)
- **Frontend:** HTML5, CSS3 (Jinja2 Templates)
- **Database:** CSV (`disease_info.csv`, `supplement_info.csv`)
- **Other:** pandas, numpy, Pillow

---

## 📁 Project Structure

```
.
├── app.py                 # Main Flask app
├── CNN.py                 # Deep learning model
├── trained_model.pth      # Pre-trained model weights
├── disease_info.csv       # Database of diseases
├── supplement_info.csv    # Supplement info
├── requirements.txt       # Python dependencies
├── static/                # Website assets
├── templates/             # HTML templates
└── test.py                # Testing module
```

---

## ⚡ Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Tanishq-009/culti_cure.git
   cd culti_cure
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the website:**
   ```bash
   python app.py
   ```

4. **Open in your browser:**
   - Visit `http://localhost:5000/`

---

## 🧑‍💻 How It Works

- Upload a photo of a plant showing symptoms.
- The website processes your image through a deep learning model.
- Instantly receive a prediction, disease information, and suggested supplements.

---

## 🤝 Contributors

- **Tanishq**
- **Tanay Huddar**

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for details.

---

> **Culti Cure — Empowering agriculture with AI!**
