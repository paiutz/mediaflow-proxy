
# MediaFlow Proxy (Windows EXE Version)

**MediaFlow Proxy** is a high-performance proxy server for streaming media. This version is built for Windows (`mediaflow.exe`) and supports both HTTP and HTTPS using local certificates.

## 🌐 Features

- ✅ Proxy HLS (M3U8) and DASH (MPD) streams
- 🔐 HTTPS support via bundled `cert.pem` and `key.pem`
- 🧠 Smart user-agent and header modifications
- 🎯 Supports both live and VOD streams
- 📦 Self-contained single EXE build (no Python or Docker required)
- 🧪 Built-in test UI at `/` and `/speedtest`

---

## 📁 Folder Structure

Place the following files in the **same folder** (e.g. Desktop):

```
Desktop\
│
├── mediaflow.exe
├── cert\
│   ├── cert.pem
│   └── key.pem
└── .env
```

---

## ⚙️ .env Configuration (Optional)

Create a file named `.env` (next to the EXE) with these variables:

```env
API_PASSWORD=your_secure_password
CERT_PATH=cert/cert.pem
KEY_PATH=cert/key.pem
M3U8_CONTENT_ROUTING=mediaflow
```

> If `.env` is missing, `mediaflow.exe` will use defaults and still run.

---

## 🚀 How to Run

1. Double-click `mediaflow.exe`
2. The app starts on:  
   ```
   https://127.0.0.1:8888
   or
   https://<your-local-ip>:8888
   ```

---

## 🌍 External Access (Optional)

To access from the internet:

1. Forward port `8888` on your router (TCP)
2. Set up a dynamic DNS (e.g., `<your-domain>.duckdns.org`)
3. Test via:
   ```
   https://<your-domain>:8888
   ```

> ⚠️ **NAT Loopback Warning:** If your router doesn’t support NAT Hairpin, access from LAN must use the local IP (e.g., `https://192.168.1.X:8888`).

---

## 🔄 Let's Encrypt / HTTPS Renewal

You can use **Certbot** with DNS challenge to generate and renew `cert.pem` + `key.pem`.

Place renewed certs in the `cert/` folder. You can automate this via Task Scheduler.

---

## 🛡️ Firewall Rule (Optional)

Windows may block port 8888. To allow traffic:

```cmd
netsh advfirewall firewall add rule name="MediaFlow HTTPS" dir=in action=allow protocol=TCP localport=8888
```

---

## ✅ Status

- [x] Windows Portable EXE  
- [x] HTTPS Ready (via local certs)  
- [x] API Key Authentication  
- [x] DuckDNS-compatible  
- [x] Self-contained (no dependencies)

---

## 📬 Contact

Built with ❤️ by [you]  
GitHub Repo: `https://github.com/nzo66/mediaflow-proxy`
