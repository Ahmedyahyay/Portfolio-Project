# 🚀 Quick Start Guide - Personal Nutrition Assistant

## 🎯 **تشغيل الموقع على منفذ واحد**

### **الطريقة 1: التشغيل التلقائي (الأسهل)**

#### **Windows:**
```bash
# انقر مرتين على الملف
run.bat
```

#### **Linux/Mac:**
```bash
# تشغيل مباشر
./run.sh

# أو
bash run.sh
```

#### **Python مباشر:**
```bash
python start.py
```

### **الطريقة 2: التشغيل اليدوي**

#### **1. تثبيت التبعيات:**
```bash
# تبعيات Python
pip install -r backend/requirements.txt

# تبعيات Node.js
cd src/frontend
npm install
cd ../..
```

#### **2. تشغيل الخادم:**
```bash
python server.py --port 3000
```

## 🌐 **الوصول للموقع**

بعد التشغيل، افتح المتصفح واذهب إلى:
- **الموقع:** http://localhost:3000
- **API:** http://localhost:3000/api/

## ⚙️ **خيارات التشغيل**

### **تغيير المنفذ:**
```bash
python start.py 8080
```

### **بناء الواجهة الأمامية:**
```bash
python server.py --build
```

### **تشغيل في وضع الإنتاج:**
```bash
python server.py --port 80
```

## 🔧 **استكشاف الأخطاء**

### **مشكلة: Python not found**
```bash
# تثبيت Python 3.8+
# Windows: https://python.org/downloads
# Linux: sudo apt install python3 python3-pip
# Mac: brew install python3
```

### **مشكلة: Node.js not found**
```bash
# تثبيت Node.js
# Windows: https://nodejs.org
# Linux: sudo apt install nodejs npm
# Mac: brew install node
```

### **مشكلة: Port already in use**
```bash
# استخدم منفذ مختلف
python start.py 3001
```

### **مشكلة: Database errors**
```bash
# حذف قاعدة البيانات القديمة
rm -f nutrition.db
rm -f backend/instance/nutrition.db
```

## 📁 **هيكل المشروع**

```
Portfolio-Project/
├── server.py          # الخادم المتكامل
├── start.py           # ملف التشغيل المبسط
├── run.bat            # تشغيل Windows
├── run.sh             # تشغيل Linux/Mac
├── backend/           # الخادم الخلفي (Flask)
├── src/frontend/      # الواجهة الأمامية (React)
└── nutrition.db       # قاعدة البيانات
```

## 🎉 **المميزات**

- ✅ **منفذ واحد** - كل شيء على http://localhost:3000
- ✅ **تطوير سريع** - Hot reload للواجهة الأمامية
- ✅ **API متكامل** - Flask backend مع React frontend
- ✅ **قاعدة بيانات** - SQLite مدمجة
- ✅ **سهولة التشغيل** - ملف واحد للتشغيل

## 🆘 **الدعم**

إذا واجهت مشاكل:
1. تأكد من تثبيت Python 3.8+ و Node.js
2. تأكد من تثبيت جميع التبعيات
3. تحقق من أن المنفذ متاح
4. امسح قاعدة البيانات القديمة إذا لزم الأمر

---
