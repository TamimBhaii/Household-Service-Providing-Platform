# 🏠 Household Service Providing Platform

A complete **Household Service Providing Platform** built with Django, TailwindCSS, and Cloudinary.  
This platform connects **customers** with **service providers**, allowing booking, rating, and managing household services.

---

## ✨ Features

### 👨‍💻 For Customers:
- 🔐 Secure signup/login system
- 🛠 Browse available household services
- 📅 Book a service provider
- ⏳ Track booking status (Pending / Accepted / Rejected / Completed / Cancelled)
- ⭐ Give review & rating **only after booking is accepted**
- 👀 View provider's profile and average ratings before booking

### 🧑‍🔧 For Service Providers:
- 🔐 Secure signup/login system
- ➕ Add new services (title, description, price, duration, cover image)
- ✏️ Edit and update their services
- ❌ Delete their services
- 📩 Manage hire requests (Accept / Reject / Mark Completed)
- 📊 See reviews given by customers

### 🛡 General Features:
- ☁️ **Cloudinary** integration for profile images and service images
- 📂 Static files served via **Whitenoise**
- 🎨 UI styled with **TailwindCSS**
- 🔑 Role-based authentication (`customer` vs `provider`)
- 🗂 Organized apps: `accounts`, `services`, `bookings`, `reviews`

---

## ⚙️ Tech Stack

- **Backend:** Django 5
- **Frontend:** TailwindCSS
- **Database:** SQLite (default) / can be upgraded to PostgreSQL
- **Media Storage:** Cloudinary
- **Static Management:** Whitenoise
- **Version Control:** Git & GitHub

---
