# NetMon

A simple, terminal-based network monitor that shows:
**App | PID | Protocol | Local → Remote | Remote Host | Location / ISP | Status**

---

## 🧩 Features
- Lists live connections with process name & PID
- Shows remote IP, reverse DNS, and location (via ip-api.com)
- Works on Windows, macOS, Linux
- CSV export option
- Caches geolocation results for performance

---

## 🧰 Setup
```bash
git clone https://github.com/BernieIsAPhysco/Netmon.git
cd netmon
pip install -r requirements.txt
python main.py
