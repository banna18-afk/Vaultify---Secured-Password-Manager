# 🔐 Vaultify — Secure Password Vault

Vaultify is a full-stack, multi-user password manager web application built with Python and Flask. It lets users securely store, search, update, and delete their website credentials behind an encrypted, per-vault key.

**🌐 Live Demo:** [harshbanna2008.pythonanywhere.com](https://harshbanna2008.pythonanywhere.com)
**📦 Repository:** [github.com/banna18-afk/Vaultify--Secured-Password-Manager](https://github.com/banna18-afk/Vaultify--Secured-Password-Manager)

> Built entirely on a mobile phone (Pydroid 3), without a laptop, as a 1st-semester BCA (AI & Data Science) project.

---

## ✨ Features

- **Multi-user accounts** — email-based signup/login, each user's data fully isolated
- **Strong password hashing** — PBKDF2-HMAC-SHA256 with 100,000 iterations and a unique salt per user, compared using constant-time (`hmac.compare_digest`) checks to resist timing attacks
- **Encrypted vault storage** — stored passwords are encrypted with Fernet (AES-based symmetric encryption)
- **Full password vault CRUD** — Add, View All, Search, Update, and Delete saved credentials
- **Built-in password strength checker** — enforces length, uppercase, digit, and special-character rules at signup
- **Session-based access control** — protected pages are inaccessible without an active login session
- **Custom frontend** — hand-written HTML/CSS for every page (login, signup, home, add/search/update/delete password)
- **Secrets kept out of source control** — the Flask session key and the vault's encryption key are both loaded from environment variables at deploy time, never hardcoded in the committed code

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLite |
| Security | `hashlib` (PBKDF2), `hmac`, `cryptography` (Fernet) |
| Frontend | HTML5, CSS3, Jinja2 templating |
| Deployment | PythonAnywhere |

## 📂 Project Structure

```
Vaultify--Secured-Password-Manager/
├── app.py                              # Flask routes — connects everything together
├── Auth_Module.py                      # Authorization class — signup, login, salting & hashing
├── Password_Manager_Final_Version.py   # Vault class — password CRUD operations
├── Pass_Checker.py                     # Password strength validator
├── templates/                          # HTML pages (Jinja2)
│   ├── login.html
│   ├── signup.html
│   ├── Home_Page.html
│   ├── add_password.html
│   ├── search_password.html
│   ├── update_password.html
│   ├── view_all_passwords.html
│   └── delete_password.html
└── static/                             # CSS for each page
```

## 🔒 Security Design

- Passwords are never stored in plain text — only PBKDF2 hashes (for login) and Fernet ciphertext (for vault entries) ever touch the database.
- A stolen copy of the database alone is not enough to read anyone's vault — decryption also requires the encryption key, which is injected via an environment variable and never committed to this repository.
- Login failures return a generic error for both "user not found" and "wrong password" cases, to avoid leaking which emails are registered (prevents username enumeration).

## 🚀 Running Locally

```bash
pip install flask cryptography
python app.py
```
Then open `http://127.0.0.1:5000` in your browser.

## 🧭 Roadmap

- [ ] Email OTP verification on signup
- [ ] Forgot-password recovery flow
- [ ] Encrypted file vault (store documents/photos alongside passwords)

## 📄 License

Released under the [MIT License](LICENSE) — free to use, modify, and learn from, with attribution.

## 👤 Author

**Harshvardhan Chauhan**
BCA (AI & Data Science), 1st Semester
GitHub: [@banna18-afk](https://github.com/banna18-afk)
