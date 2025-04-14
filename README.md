# 💸 Personal Finance Tracker

This is a mobile app built with **Flutter** and powered by a **Python Flask ML backend**.

## 📱 Features

- Add & auto-tag expenses
- View pie chart breakdowns and history
- Smart budget suggestions (ML)
- Real-time anomaly detection
- Budget exceedance alerts via notifications

## 🧠 Structure
finance-tracker/
├── backend/       # ML Flask backend
│   ├── app.py
│   ├── model.tflite
│   └── requirements.txt
├── flutter_app/   # Flutter mobile app
│   ├── lib/
│   ├── android/
│   └── pubspec.yaml
## 🧪 How to Run

### 🔧 Backend (Python)
```bash
cd backend
pip install -r requirements.txt
python app.py
### 🔧 Frontend (Flutter)
cd flutter_app
flutter pub get
flutter run
