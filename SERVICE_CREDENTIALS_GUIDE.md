# 🔑 SERVICE CREDENTIALS GUIDE
## Complete Setup Instructions for Driving School Platform

### 📋 **OVERVIEW**
This platform uses several external services to provide full functionality. Here's what each service does and how to get the credentials:

---

## 🔧 **REQUIRED SERVICES (Must Have)**

### 1. **MongoDB Database**
- **What it does**: Stores all platform data (users, schools, courses, etc.)
- **Setup**: 
  - Install MongoDB locally: `brew install mongodb` (Mac) or download from mongodb.com
  - Or use MongoDB Atlas (cloud): https://www.mongodb.com/atlas
- **Configuration**: Already set to `mongodb://localhost:27017`
- **Cost**: Free (local) or Free tier (Atlas)

### 2. **JWT Secret Key**
- **What it does**: Secures user authentication tokens
- **Setup**: Generate a random string (at least 32 characters)
- **Example**: `openssl rand -base64 32` (run this command)
- **Configuration**: Replace `SECRET_KEY` in `/app/backend/.env`
- **Cost**: Free

---

## 📸 **FILE STORAGE SERVICE (Recommended)**

### 3. **Cloudinary**
- **What it does**: Stores profile photos, documents, certificates
- **Why needed**: Platform has document upload functionality
- **Setup Instructions**:
  1. Go to https://cloudinary.com
  2. Create free account
  3. Go to Dashboard
  4. Copy: Cloud Name, API Key, API Secret
- **Configuration**: Update in `/app/backend/.env`:
  ```
  CLOUDINARY_CLOUD_NAME="your-actual-cloud-name"
  CLOUDINARY_API_KEY="your-actual-api-key"  
  CLOUDINARY_API_SECRET="your-actual-api-secret"
  ```
- **Cost**: Free tier (25 credits/month)
- **Alternative**: Platform can work without this, but file uploads won't work

---

## 🎥 **VIDEO CALLING SERVICE (Optional)**

### 4. **Daily.co**
- **What it does**: Enables video calls for theory lessons
- **Setup Instructions**:
  1. Go to https://daily.co
  2. Create free account
  3. Go to Developers section
  4. Create API key
- **Configuration**: Update in `/app/backend/.env`:
  ```
  DAILY_API_KEY="your-actual-daily-api-key"
  ```
- **Cost**: Free tier (10,000 minutes/month)
- **Alternative**: Platform works without this, but no video calls

---

## 📧 **EMAIL SERVICE (Optional)**

### 5. **Email Notifications**
- **What it does**: Sends email notifications to users
- **Setup Instructions (Gmail)**:
  1. Enable 2-factor authentication on Gmail
  2. Generate App Password: Google Account → Security → App passwords
  3. Use app password (not regular password)
- **Configuration**: Update in `/app/backend/.env`:
  ```
  SMTP_USERNAME="your-email@gmail.com"
  SMTP_PASSWORD="your-16-digit-app-password"
  FROM_EMAIL="your-email@gmail.com"
  ```
- **Cost**: Free
- **Alternative**: Platform works without this, but no email notifications

---

## 💳 **PAYMENT SERVICES (Algeria-Specific, Optional)**

### 6. **BaridiMob**
- **What it does**: Algerian mobile payment processing
- **Setup**: Contact BaridiMob directly for merchant account
- **Website**: https://www.baridimob.dz
- **Cost**: Merchant fees apply

### 7. **CCP (Chèques Postaux)**
- **What it does**: Algeria Post payment processing
- **Setup**: Contact Algeria Post for merchant account
- **Cost**: Merchant fees apply

---

## 🚀 **QUICK START GUIDE**

### **Minimum to Get Started (Free)**:
1. **MongoDB**: Install locally or use Atlas free tier
2. **JWT Secret**: Generate random string
3. **Update .env files** with your values

### **For Full Functionality (Recommended)**:
1. All of the above, plus:
2. **Cloudinary**: For file uploads
3. **Daily.co**: For video calls
4. **Gmail**: For email notifications

### **For Production (Algeria)**:
1. All of the above, plus:
2. **BaridiMob**: For payments
3. **CCP**: For additional payment options

---

## 🔧 **HOW TO UPDATE CREDENTIALS**

### **Method 1: Edit .env Files Directly**
1. Open `/app/backend/.env`
2. Replace placeholder values with real credentials
3. Save file
4. Restart backend server

### **Method 2: Environment Variables**
Set environment variables in your system:
```bash
export CLOUDINARY_CLOUD_NAME="your-cloud-name"
export DAILY_API_KEY="your-daily-key"
# etc.
```

---

## ⚠️ **SECURITY NOTES**

1. **Never commit .env files to Git**
2. **Use strong, unique passwords**
3. **Keep API keys secret**
4. **Use different credentials for development/production**
5. **Regularly rotate API keys**

---

## 🧪 **TESTING WITHOUT CREDENTIALS**

The platform will work with basic functionality even without external service credentials:
- ✅ User registration/login
- ✅ School browsing
- ✅ Course management
- ✅ Basic workflows
- ❌ File uploads (needs Cloudinary)
- ❌ Video calls (needs Daily.co)
- ❌ Email notifications (needs SMTP)
- ❌ Payments (needs payment gateways)

---

## 📞 **GETTING HELP**

1. **MongoDB**: Check connection with MongoDB Compass
2. **Cloudinary**: Test in their web interface first
3. **Daily.co**: Test with their API explorer
4. **Email**: Test with a simple email script first

Would you like me to help you set up any specific service?