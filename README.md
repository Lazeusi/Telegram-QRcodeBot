<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=180&section=header&text=QR%20Code%20Bot&fontSize=45&fontAlignY=35&animation=twinkling&fontColor=fff" />
</p>

<h3 align="center">🚀 Advanced Telegram QR Code Generator Bot</h3>

<p align="center">
  <b>Built with:</b> Aiogram v3.22.0 • Async • MongoDB  
</p>

---

## 📖 Overview

A fully asynchronous Telegram bot for generating various types of QR Codes.  
The project includes a complete **Admin Panel**, **Force Join System**, and **high-performance async structure** suitable for large-scale user bases.

---

## ⚙️ Features

### 🧠 Admin System
Manage everything directly from Telegram using the built-in admin panel:
- Add new admins  
- Remove admins  
- View admin list and details  
- Manage required join channels & groups  
- Send broadcast messages to all users  
- View system and user statistics  

> 🔹 The admin panel is accessible via the command `/panel` in the bot’s private chat.

---

### 🔐 Activation
- If no admin exists in the database, use `/activate` in private chat.  
- The first user who runs `/activate` will become the **main admin**.  
- After that, `/activate` will be **disabled permanently**.

---

### 💬 Force Join System
Users must join your specified channels/groups before using the bot.  
The system automatically checks membership and prevents access until the requirement is met.

---

## 🧩 QR Code Generator

After sending `/start`, users get the **QR Code Menu**, where they can create QR codes for the following types:

| Type | Description |
|------|--------------|
| 📝 Plain Text | Any normal text message |
| 🔗 Link / URL | Website or app links |
| 👤 Contact Info | vCard or basic contact data |
| 📶 Wi-Fi | Wi-Fi SSID, password, and encryption |
| 💰 Payment | Payment links, wallet addresses, etc. |
| 📍 Location | Geographic coordinates (latitude/longitude) |
| 🧾 JSON / Data | Any structured JSON or encoded data |

> Each QR Code is generated instantly and delivered as an image file.  
> The entire process is **asynchronous**, ensuring no delay even under heavy load.

---

## 💾 Database
- Uses **MongoDB** for persistent and scalable storage.
- Collections include:
  - `users`
  - `admins`
  - `channels`
  - `groups`
  - `logs` (optional)

---

## 🛠️ Tech Stack
| Component | Description |
|------------|-------------|
| 🐍 Python 3.11+ | Core language |
| 🤖 Aiogram 3.22.0 | Telegram Bot framework |
| 🍃 MongoDB | Database |
| ⚡ Async / Await | Full async architecture |
| 🧰 Logging & Error Handling | Custom structured logging system |

---

## 🚀 Installation

```bash
git clone https://github.com/yourusername/qr-bot.git
cd qr-bot
pip install -r requirements.txt

```
---

## 😶‍🌫️ HOW Run?
```bash
python main.py
```
---

🧑‍💻 Author

Shayan
Python Developer — Focused on Aiogram, FastAPI, and automation projects.
🔗 GitHub
 | 🐍 Telegram: @lazeusi

<p align="center"> <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=120&section=footer"/> </p>