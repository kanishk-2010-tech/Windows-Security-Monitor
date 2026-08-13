# 🛡️ Windows Security Monitor

A Python-based Windows Security Monitoring System designed to monitor system resources, running processes, network connections, and listening ports.

---

## 📌 Overview

Windows Security Monitor is a lightweight security monitoring application developed using Python.

The project collects information from a Windows computer and presents useful system and security information through a simple dashboard.

It can help users monitor:

- CPU usage
- Memory usage
- Running processes
- Network connections
- Listening ports
- System activity
- Basic security-related information

---

## ✨ Features

### 🖥️ System Monitoring

- Monitor CPU usage
- Monitor RAM usage
- Monitor system resource utilization

### ⚙️ Process Monitoring

- View currently running processes
- Display process information
- Monitor process activity

### 🌐 Network Monitoring

- View active network connections
- Display connection information
- Identify network activity

### 🔌 Port Monitoring

- Detect listening ports
- Display port information
- Help identify services listening on the system

### 🛡️ Security Monitoring

- Perform basic security checks
- Monitor potentially suspicious system activity
- Generate security alerts
- Threat score assessment
- Detect new listening services
- Monitor high CPU and RAM usage

### 📊 Dashboard

- Simple Python-based graphical interface
- Easy-to-understand monitoring information
- Security event history
- Threat level display
- Network and port information

---

## 🛠️ Technologies Used

- **Python 3**
- **Tkinter** – Graphical User Interface
- **Psutil** – System and process monitoring
- **SQLite** – Local database
- **JSON** – Baseline configuration
- **CSV** – Security event export
- **Windows OS**

---

## 📂 Project Structure

```text
Windows-Security-Monitor/
│
├── dashboard.py
├── database.py
├── monitor.py
├── security.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── screenshots/
    └── dashboard.png
```

---

## 📸 Dashboard Preview

![Windows Security Monitor Dashboard](screenshots/dashboard.png)

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/kanishk-2010-tech/Windows-Security-Monitor.git
```

### 2. Enter the Project Directory

```bash
cd Windows-Security-Monitor
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

---

## ▶️ Running the Project

Start the dashboard using:

```bash
python dashboard.py
```

The Windows Security Monitor dashboard will open and display system and security information.

---

## 📋 Requirements

- Windows 10 or Windows 11
- Python 3.x
- pip
- Required packages listed in `requirements.txt`

---

## 🔍 How It Works

The application uses Python and `psutil` to collect information from the Windows system.

### System Monitoring

The application monitors CPU and RAM usage and checks configured resource thresholds.

### Process Monitoring

The application retrieves currently running processes and displays their basic information.

### Network Monitoring

The application checks active network connections and displays local and remote connection information.

### Port Monitoring

The application detects listening ports and attempts to identify the process associated with each listening service.

### Baseline Monitoring

The security system maintains a baseline of known listening ports and can detect newly appearing listening services.

### Threat Assessment

Detected security events contribute to a threat score and threat level.

Possible threat levels include:

- 🟢 LOW
- 🟡 MEDIUM
- 🟠 HIGH
- 🔴 CRITICAL

---

## 🛡️ Security Purpose

This project is intended for **educational and defensive cybersecurity purposes**.

It should only be used on computers and networks that you own or have permission to monitor.

This project is **not a replacement for professional antivirus, EDR, or endpoint security software**.

---

## 🎯 Learning Objectives

This project demonstrates practical concepts including:

- Python programming
- Windows system monitoring
- Process management
- Network monitoring
- Port monitoring
- Security event detection
- Threat scoring
- SQLite database integration
- Tkinter GUI development
- Basic cybersecurity concepts
- Git and GitHub

---

## 🚀 Future Improvements

Possible future improvements include:

- Windows Event Log integration
- Advanced suspicious-process detection
- IP reputation analysis
- Email and desktop notifications
- Advanced network analysis
- Detailed security reports
- Improved dashboard visualizations
- User authentication
- Automated security reports

---

## 👨‍💻 Author

**Ashu**

GitHub:  
https://github.com/kanishk-2010-tech

---

## 📄 License

This project is intended for educational purposes.

---

⭐ If you find this project useful, consider giving the repository a star.

---

**Windows Security Monitor — Python-based Windows security monitoring for learning and defensive analysis.**
