# Akmessage

Akmessage is a modern, real-time chat application that i built for CS50 final project with Flask, Flask-SocketIO, and SQLAlchemy.  
It supports private and group conversations, file sharing, and voice messages—all in a clean, responsive interface.

---

## 🚀 Features

- **User Registration & Login**  
  Secure authentication with password hashing.

- **Private & Group Chats**  
  Start one-on-one or group conversations with other users.

- **Real-Time Messaging**  
  Instant message delivery using Flask-SocketIO.

- **File Sharing**  
  Send images, documents, and more in your chats.

- **Voice Messages**  
  Record and send voice messages directly from your browser.

- **Responsive UI**  
  Works great on desktop and mobile.

---

## 🛠️ Tech Stack

- **Backend:** Flask, Flask-Login, Flask-SocketIO, Flask-Migrate, SQLAlchemy
- **Frontend:** Bootstrap 5, Jinja2 templates, JavaScript (Socket.IO)
- **Database:** SQLite (default, easy to swap)

---

## 📦 Installation

1. **Clone the repository**
   ```sh
   git clone https://github.com/YOUR-AKXtreme/akmessage.git
   cd akmessage
   ```

2. **Create a virtual environment**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up the database**
   ```sh
   flask db upgrade
   ```

5. **Run the app**
   ```sh
   python app.py
   ```
   Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## 📁 Project Structure

```
akmessage/
│
├── app.py
├── models.py
├── requirements.txt
├── static/
│   └── uploads/
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── conversations.html
│   ├── conversation.html
│   └── start_conversation.html
└── README.md
```

---

## ✨ Screenshots
<img width="1414" alt="Screenshot 2025-06-15 at 03 20 35" src="https://github.com/user-attachments/assets/cbf9c4b0-257b-4aee-9124-1394ad266d68" />

<img width="1414" alt="Screenshot 2025-06-15 at 03 20 46" src="https://github.com/user-attachments/assets/c866ab6d-8050-481f-aa22-bde6774ea19b" />

<img width="1414" alt="Screenshot 2025-06-15 at 03 19 48" src="https://github.com/user-attachments/assets/07593a30-8026-49c4-a47b-c6f4a1225706" />

---

## 🤝 Contributing

Pull requests are welcome!  
For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

MIT License

---

**Made with ❤️ using Flask and Socket.IO**
