# CultiKure – Plant Disease Detection

CultiKure is a web app that detects plant diseases from a photo of a leaf. Upload an image and it tells you the disease, how to prevent or treat it, and a recommended supplement or fertilizer to buy.

## Features

- **AI disease detection** – a ResNet50 model classifies a leaf photo into one of 39 classes (diseases and healthy leaves for apple, blueberry, cherry, corn, grape, orange, peach, pepper, potato, raspberry, soybean, squash, strawberry and tomato, plus a "no leaf" background class).
- **Disease report** – description of the disease and steps to prevent it.
- **Supplement market** – browse all supplements and fertilizers, filterable by type, with buy links.

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript, Bootstrap 5, Jinja2 templates |
| Backend | Python, Flask |
| AI model | PyTorch, Torchvision (ResNet50, transfer learning, 39 classes) |
| Data | pandas, CSV files (`disease_info.csv`, `supplement_info.csv`) |
| Image handling | Pillow |

## Project structure

```
app.py                 Flask app: routes, image upload, model prediction
CNN.py                 Custom CNN definition (experimental, not used by app.py)
trained_model.pth      Trained ResNet50 weights (39 classes)
disease_info.csv       Disease name, description, prevention steps, image
supplement_info.csv    Supplement/fertilizer name, image, buy link
templates/             HTML pages (base layout, home, AI engine, result, market, contact)
static/uploads/        Site images and uploaded leaf photos
requirements.txt       Python dependencies
```

## Run locally

Requires Python 3.9 or newer.

```bash
git clone https://github.com/Tanishq-009/culti_cure.git
cd culti_cure
pip install -r requirements.txt
python app.py
```

Then open http://localhost:5000 in your browser. Press `Ctrl + C` in the terminal to stop the server.

## Pages

| URL | Page |
|---|---|
| `/` | Home |
| `/index` | AI Engine – upload a leaf photo |
| `/submit` | Prediction result |
| `/market` | Supplements and fertilizers |
| `/contact` | Contact |

## How the prediction works

1. The uploaded photo is resized to 224×224 and normalized with ImageNet mean and standard deviation.
2. ResNet50 outputs a score for each of the 39 classes; the highest score is the prediction.
3. The predicted class index is looked up in `disease_info.csv` and `supplement_info.csv` to build the result page.
