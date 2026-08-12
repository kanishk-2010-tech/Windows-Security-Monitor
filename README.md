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
- Provide useful information for defensive security analysis

### 📊 Dashboard
- Simple Python-based graphical interface
- Easy-to-understand monitoring information
- Designed for learning and security analysis

---

## 🛠️ Technologies Used

- **Python 3**
- **Tkinter** – Graphical User Interface
- **Psutil** – System and process monitoring
- **SQLite** – Local database
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
└── .gitignore
