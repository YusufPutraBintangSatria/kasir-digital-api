# 📚 Kasir Digital API - Complete Documentation

**Version:** 2.0.0  
**Last Updated:** November 30, 2025  
**Author:** Yusuf Putra Bintang Satria

---

## 📖 Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture & Design](#architecture--design)
3. [API Endpoints](#api-endpoints)
4. [Authentication](#authentication)
5. [Usage Examples](#usage-examples)
6. [Database Schema](#database-schema)
7. [Deployment Guide](#deployment-guide)

---

## 🎯 Project Overview

**Kasir Digital API** adalah REST API backend service untuk mengelola transaksi top-up digital (Game, Pulsa, dll) dengan fitur-fitur professional-grade:

### Key Features
- ✅ **REST API** - 6 fully functional endpoints
- ✅ **JWT Authentication** - Secure token-based access
- ✅ **Modular Architecture** - Clean separation of concerns
- ✅ **Input Validation** - Comprehensive error handling
- ✅ **JSON Database** - Lightweight & efficient storage
- ✅ **Production Ready** - Proper HTTP status codes

### Technologies
- **Backend:** Flask (Python 3.7+)
- **Authentication:** JWT (PyJWT)
- **Database:** JSON file
- **Architecture:** Modular, scalable design

---

## 🏗️ Architecture & Design

### Project Structure

```
Proyek_Kasir_Digital/
├── app.py              # Main REST API application
├── auth.py             # JWT authentication module
├── config.py           # Configuration & constants
├── database.py         # Database operations
├── menu.py             # CLI menu (optional)
├── transaksi.py        # Transaction business logic
├── utils.py            # Utility functions
├── main.py             # CLI entry point
├── transaksi.json      # Transaction database
├── users.json          # User credentials
└── README.md           # Documentation
```

### Design Patterns Used

1. **Modular Design** - Each module has single responsibility
2. **OOP Principles** - Class-based architecture for auth & database
3. **Decorator Pattern** - `@token_required` for route protection
4. **Singleton Pattern** - Single database instance
5. **Error Handling** - Consistent error responses

### Data Flow

```
Client Request
    ↓
Flask Router (@app.route)
    ↓
@token_required Decorator (if protected)
    ↓
JWT Validation
    ↓
Route Handler Function
    ↓
Business Logic (transaksi.py / database.py)
    ↓
JSON Response with Status Code
    ↓
Client Response
```

---

## 📡 API Endpoints

### 1. Home Endpoint (Public)

```
GET /
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Selamat datang di Kasir Digital API v2.0",
  "features": ["Authentication", "JWT Token", "Protected Endpoints"],
  "info": "Gunakan /auth/register dan /auth/login untuk memulai"
}
```

---

### 2. Register User (Public)

```
POST /auth/register
Content-Type: application/json

{
  "username": "yusuf",
  "password": "password123"
}
```

**Success Response (201 Created):**
```json
{
  "status": "success",
  "message": "User berhasil terdaftar"
}
```

**Error Response (400 Bad Request):**
```json
{
  "status": "error",
  "message": "Username dan password harus disediakan"
}
```

**Error Response (400 Bad Request):**
```json
{
  "status": "error",
  "message": "Username sudah terdaftar"
}
```

---

### 3. Login (Public)

```
POST /auth/login
Content-Type: application/json

{
  "username": "yusuf",
  "password": "password123"
}
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Login berhasil",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Inl1c3VmIiwiaWF0IjoxNjk4NzM0MzY3LCJleHAiOjE2OTg4MjA3Njd9.vhXXVbfqnD_LxKpUVpUe1y5w8zKc2Q3m0fRnT8JvYKk"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "status": "error",
  "message": "Password salah"
}
```

---

### 4. Get Product List (Protected)

```
GET /api/produk
Authorization: Bearer <token>
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "data": [
    {
      "kode": "ML_86",
      "nama": "Mobile Legends 86 Diamond",
      "harga": 20000,
      "kategori": "Game"
    },
    {
      "kode": "FF_140",
      "nama": "Free Fire 140 Diamond",
      "harga": 19000,
      "kategori": "Game"
    },
    {
      "kode": "PULSA_20",
      "nama": "Pulsa All Operator 20rb",
      "harga": 22000,
      "kategori": "Pulsa"
    }
  ],
  "total": 3
}
```

**Error Response (401 Unauthorized):**
```json
{
  "status": "error",
  "message": "Token tidak ditemukan di header Authorization"
}
```

---

### 5. Create Transaction (Protected)

```
POST /api/transaksi
Authorization: Bearer <token>
Content-Type: application/json

{
  "nama": "Yusuf",
  "kode_produk": "ML_86"
}
```

**Success Response (201 Created):**
```json
{
  "status": "success",
  "message": "Transaksi berhasil dibuat",
  "data": {
    "tanggal": "2025-11-30 17:31:07",
    "nama": "Yusuf",
    "produk": "Mobile Legends 86 Diamond",
    "kategori": "Game",
    "harga": 20000,
    "operator": "yusuf"
  }
}
```

**Error Response (404 Not Found):**
```json
{
  "status": "error",
  "message": "Kode produk 'INVALID' tidak ditemukan"
}
```

---

### 6. Get Transaction History (Protected)

```
GET /api/riwayat
Authorization: Bearer <token>

# Optional: Filter by customer name
GET /api/riwayat?nama=Yusuf
Authorization: Bearer <token>
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "data": [
    {
      "tanggal": "2025-11-30 17:31:07",
      "nama": "Yusuf",
      "produk": "Mobile Legends 86 Diamond",
      "kategori": "Game",
      "harga": 20000,
      "operator": "yusuf"
    }
  ],
  "total": 1
}
```

---

### 7. Get Sales Report (Protected)

```
GET /api/laporan
Authorization: Bearer <token>
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "total_transaksi": 5,
    "total_penjualan": 100000,
    "rata_rata_per_transaksi": 20000
  }
}
```

---

## 🔐 Authentication

### JWT Overview

**JWT (JSON Web Token)** adalah standar industry untuk secure API authentication.

### How It Works

1. **User registers** dengan username & password
2. **User logs in** dengan credentials
3. **Server validates** credentials
4. **Server returns JWT token** (valid 24 jam)
5. **Client stores** token
6. **Client includes token** di setiap request: `Authorization: Bearer <token>`
7. **Server validates** token sebelum process request

### Token Structure

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Inl1c3VmIiwiaWF0IjoxNjk4NzM0MzY3LCJleHAiOjE2OTg4MjA3Njd9.vhXXVbfqnD_LxKpUVpUe1y5w8zKc2Q3m0fRnT8JvYKk
        ↓
    Header.Payload.Signature
```

### Token Content

```json
{
  "username": "yusuf",
  "iat": 1698734367,     // Issued at
  "exp": 1698820767      // Expires at (24 hours later)
}
```

### Error Responses

| Scenario | HTTP Code | Response |
|---|---|---|
| Invalid token | 401 | `"Token tidak valid atau sudah expired"` |
| No token | 401 | `"Token tidak ditemukan di header Authorization"` |
| Wrong format | 401 | `"Format token tidak valid. Gunakan: Bearer <token>"` |

---

## 💻 Usage Examples

### Using PowerShell

#### 1. Register User

```powershell
$registerBody = @{
    username = "yusuf"
    password = "password123"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://127.0.0.1:5000/auth/register" `
    -Method POST `
    -Headers @{"Content-Type" = "application/json"} `
    -Body $registerBody

Write-Host $response.Content
```

#### 2. Login & Get Token

```powershell
$loginBody = @{
    username = "yusuf"
    password = "password123"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://127.0.0.1:5000/auth/login" `
    -Method POST `
    -Headers @{"Content-Type" = "application/json"} `
    -Body $loginBody

$token = ($response.Content | ConvertFrom-Json).token
Write-Host "Token: $token"
```

#### 3. Create Transaction

```powershell
$transactionBody = @{
    nama = "Yusuf"
    kode_produk = "ML_86"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/transaksi" `
    -Method POST `
    -Headers @{
        "Authorization" = "Bearer $token"
        "Content-Type" = "application/json"
    } `
    -Body $transactionBody

Write-Host $response.Content
```

#### 4. Get Products

```powershell
$response = Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/produk" `
    -Method GET `
    -Headers @{"Authorization" = "Bearer $token"}

$response.Content | ConvertFrom-Json | Format-Table
```

---

## 💾 Database Schema

### users.json

```json
{
  "yusuf": {
    "password": "password123",
    "created_at": "2025-11-30T17:00:00"
  },
  "admin": {
    "password": "admin123",
    "created_at": "2025-11-30T17:05:00"
  }
}
```

**Note:** Password di-store plain text untuk demo. Use hashing (bcrypt) di production!

### transaksi.json

```json
[
  {
    "tanggal": "2025-11-30 17:31:07",
    "nama": "Yusuf",
    "produk": "Mobile Legends 86 Diamond",
    "kategori": "Game",
    "harga": 20000,
    "operator": "yusuf"
  },
  {
    "tanggal": "2025-11-30 17:35:22",
    "nama": "Bintang",
    "produk": "Free Fire 140 Diamond",
    "kategori": "Game",
    "harga": 19000,
    "operator": "admin"
  }
]
```

---

## 🚀 Deployment Guide

### Local Development

```bash
# Navigate ke project folder
cd Proyek_Kasir_Digital

# Install dependencies
pip install flask PyJWT

# Run development server
python app.py

# API available at http://127.0.0.1:5000
```

### Production Deployment

#### With Gunicorn

```bash
pip install gunicorn

gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### Deploy to Heroku

```bash
# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Create requirements.txt
pip freeze > requirements.txt

# Deploy
git push heroku main
```

#### Deploy to Railway / Render

1. Push code to GitHub
2. Connect repository to platform
3. Set environment variables
4. Deploy!

---

## 🎓 Learning Outcomes

Setelah mempelajari project ini, Anda akan memahami:

- ✅ REST API design & implementation principles
- ✅ JWT authentication & authorization
- ✅ Modular architecture & separation of concerns
- ✅ HTTP methods & status codes
- ✅ Input validation & error handling
- ✅ Database design (JSON-based)
- ✅ Security best practices
- ✅ Clean code principles

---

## 📈 Future Enhancements

- [ ] Migrate ke database (SQLite/PostgreSQL)
- [ ] Add password hashing (bcrypt)
- [ ] Add logging system
- [ ] Add unit & integration tests
- [ ] Add Swagger/OpenAPI documentation
- [ ] Add rate limiting
- [ ] Add caching layer (Redis)
- [ ] Add email notifications
- [ ] Add API analytics

---

## 🤝 Contributing

Contributions welcome! Feel free to fork, improve, dan submit PR.

---

## 📞 Support & Questions

For questions atau issues, silakan buat GitHub issue.

---

**Happy Coding! 🚀**
