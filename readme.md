# Fast Simon App 🚀

This is a **Flask-based web application** deployed on **Google App Engine**.  
It supports both **local development** and **production** environments with separate `.env` files.

---

## 🔧 **Setup Instructions**

### *** initialize Google Datastore Emulator ***
```commandline
https://cloud.google.com/datastore/docs/tools/datastore-emulator
```

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/benarush/google-cloud-datastore.git
```

### **2️⃣ Install Dependencies**
Make sure you have **Python 3.8+** installed. Then run:
```sh
pip install -r requirements.txt
```

### **3️⃣ Set Up Environment Variables**
There are **two `.env` files**:  
- **`.env.local`** → For local development  
- **`.env.prod`** → For production  

Copy the correct one:  
```sh
cp .env.local .env  # Use local env
# OR
cp .env.prod .env  # Use production env
```

---

## ▶️ **Run the App Locally**
```sh
python main.py
```
The app should be available at:  
👉 **http://127.0.0.1:8080/**  

---

## 🌍 **Deployed URL**
The production app is running at:  
👉 **[https://fast-simon-app.ew.r.appspot.com/hello_world](https://fast-simon-app.ew.r.appspot.com/hello_world)**  

---

## 🛠 **Testing**
A test script (`test_script.py`) is included to validate functionality **against both local and production**.  

Run tests locally or production, see that script:
```sh
python test_script.py 
```

---

## 🚀 **Deployment to Google App Engine**
