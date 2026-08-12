import json
import os
from datetime import datetime

# ============================================================
# WINDOWS SECURITY ENGINE - FINAL
# ============================================================

BASELINE_FILE = "baseline.json"
PROCESS_BASELINE_FILE = "process_baseline.json"

CPU_THRESHOLD = 90
RAM_THRESHOLD = 90

cpu_alert_active = False
ram_alert_active = False

alerted_ports = set()
alerted_processes = set()


# ============================================================
# UTILITY
# ============================================================

def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ============================================================
# PORT BASELINE
# ============================================================

def load_baseline():

    if not os.path.exists(BASELINE_FILE):
        return None

    try:
        with open(BASELINE_FILE, "r") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return None


def save_baseline(ports):

    data = {
        "created_at": current_time(),
        "ports": sorted(list(ports))
    }

    try:
        with open(BASELINE_FILE, "w") as file:
            json.dump(data, file, indent=4)

    except OSError as error:
        print(f"[!] Could not save port baseline: {error}")


# ============================================================
# PROCESS BASELINE
# ============================================================

def load_process_baseline():

    if not os.path.exists(PROCESS_BASELINE_FILE):
        return None

    try:
        with open(PROCESS_BASELINE_FILE, "r") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return None


def save_process_baseline(processes):

    data = {
        "created_at": current_time(),
        "processes": [
            {
                "pid": process.get("pid"),
                "name": process.get("name", "Unknown")
            }
            for process in processes
        ]
    }

    try:
        with open(PROCESS_BASELINE_FILE, "w") as file:
            json.dump(data, file, indent=4)

    except OSError as error:
        print(
            f"[!] Could not save process baseline: {error}"
        )


# ============================================================
# CPU + RAM SECURITY CHECK
# ============================================================

def check_resources(cpu, ram):

    global cpu_alert_active
    global ram_alert_active

    alerts = []

    # CPU
    if cpu >= CPU_THRESHOLD:

        if not cpu_alert_active:

            cpu_alert_active = True

            alerts.append({
                "severity": "HIGH",
                "type": "HIGH_CPU",
                "port": None,
                "address": None,
                "pid": None,
                "process": None,
                "time": current_time(),
                "message": f"CPU usage is very high: {cpu}%"
            })

    else:
        cpu_alert_active = False

    # RAM
    if ram >= RAM_THRESHOLD:

        if not ram_alert_active:

            ram_alert_active = True

            alerts.append({
                "severity": "MEDIUM",
                "type": "HIGH_RAM",
                "port": None,
                "address": None,
                "pid": None,
                "process": None,
                "time": current_time(),
                "message": f"RAM usage is very high: {ram}%"
            })

    else:
        ram_alert_active = False

    return alerts


# ============================================================
# LISTENING PORT CHECK
# ============================================================

def check_ports(port_details):

    global alerted_ports

    alerts = []

    current_ports = {
        item["port"]
        for item in port_details
    }

    baseline = load_baseline()

    # First run
    if baseline is None:

        save_baseline(current_ports)

        print("\n[+] SECURITY BASELINE CREATED")
        print(
            f"[+] Monitoring "
            f"{len(current_ports)} listening ports."
        )

        return alerts

    old_ports = set(
        baseline.get("ports", [])
    )

    new_ports = current_ports - old_ports

    for item in port_details:

        port = item["port"]

        if port not in new_ports:
            continue

        if port in alerted_ports:
            continue

        alerted_ports.add(port)

        alerts.append({
            "severity": "MEDIUM",
            "type": "NEW_LISTENING_SERVICE",
            "port": port,
            "address": item.get("address"),
            "pid": item.get("pid"),
            "process": item.get("process"),
            "time": current_time(),
            "message": "A new listening service was detected."
        })

    return alerts


# ============================================================
# PROCESS RISK CHECK
# ============================================================

def analyze_process_risk(processes):

    global alerted_processes

    alerts = []

    if not processes:
        return alerts

    baseline = load_process_baseline()

    # First run
    if baseline is None:

        save_process_baseline(processes)

        print("\n[+] PROCESS BASELINE CREATED")
        print(
            f"[+] Monitoring "
            f"{len(processes)} processes."
        )

        return alerts

    old_processes = baseline.get(
        "processes",
        []
    )

    old_names = {
        process.get("name", "").lower()
        for process in old_processes
    }

    for process in processes:

        name = process.get(
            "name",
            "Unknown"
        )

        pid = process.get(
            "pid",
            "-"
        )

        key = f"{name.lower()}:{pid}"

        if name.lower() in old_names:
            continue

        if key in alerted_processes:
            continue

        alerted_processes.add(key)

        alerts.append({
            "severity": "LOW",
            "type": "NEW_PROCESS",
            "port": None,
            "address": None,
            "pid": pid,
            "process": name,
            "time": current_time(),
            "message": (
                "A process not present in the "
                "security baseline was detected."
            )
        })

    return alerts


# ============================================================
# THREAT SCORE
# ============================================================

def calculate_threat_score(alerts):

    score = 0
    reasons = []

    for alert in alerts:

        alert_type = alert.get("type")
        severity = alert.get("severity")

        if alert_type == "HIGH_CPU":

            score += 15

            reasons.append(
                "High CPU usage detected"
            )

        elif alert_type == "HIGH_RAM":

            score += 10

            reasons.append(
                "High RAM usage detected"
            )

        elif alert_type == "NEW_LISTENING_SERVICE":

            score += 20

            reasons.append(
                f"New listening port detected: "
                f"{alert.get('port', 'Unknown')}"
            )

        elif alert_type == "NEW_PROCESS":

            score += 5

            reasons.append(
                f"New process detected: "
                f"{alert.get('process', 'Unknown')}"
            )

        if severity == "HIGH":
            score += 10

    score = min(score, 100)

    if score >= 80:
        level = "CRITICAL"

    elif score >= 60:
        level = "HIGH"

    elif score >= 30:
        level = "MEDIUM"

    else:
        level = "LOW"

    return {
        "score": score,
        "level": level,
        "reasons": reasons
    }


# ============================================================
# DISPLAY ALERTS
# ============================================================

def display_alerts(alerts):

    if not alerts:

        print("\n[✓] SECURITY STATUS: NORMAL")

        return

    print("\n" + "=" * 75)
    print("                       SECURITY ALERTS")
    print("=" * 75)

    for alert in alerts:

        print(
            f"\n[{alert.get('severity', 'UNKNOWN')}] "
            f"{alert.get('type', 'UNKNOWN')}"
        )

        if alert.get("port") is not None:

            print(
                f"    Port      : "
                f"{alert.get('port', '-')}"
            )

            print(
                f"    Address   : "
                f"{alert.get('address', '-')}"
            )

        if alert.get("pid") is not None:

            print(
                f"    PID       : "
                f"{alert.get('pid', '-')}"
            )

        if alert.get("process") is not None:

            print(
                f"    Process   : "
                f"{alert.get('process', '-')}"
            )

        print(
            f"    Time      : "
            f"{alert.get('time', '-')}"
        )

        print(
            f"    Reason    : "
            f"{alert.get('message', '-')}"
        )

    print("\n" + "=" * 75)


# ============================================================
# DISPLAY THREAT SCORE
# ============================================================

def display_threat_score(alerts):

    result = calculate_threat_score(alerts)

    print("\n[ THREAT ASSESSMENT ]")
    print("=" * 75)

    print(
        f"Threat Score : "
        f"{result['score']}/100"
    )

    print(
        f"Threat Level : "
        f"{result['level']}"
    )

    print("\nReasons:")

    if result["reasons"]:

        unique_reasons = list(
            dict.fromkeys(result["reasons"])
        )

        for reason in unique_reasons:
            print(f"  - {reason}")

    else:

        print("  - No active security alerts")

    print("=" * 75)

    return result


# ============================================================
# RESET
# ============================================================

def reset_alert_state():

    global alerted_ports
    global alerted_processes

    alerted_ports.clear()
    alerted_processes.clear()

    print("[+] Alert history cleared.")


# ============================================================
# MODULE TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 75)
    print("                 WINDOWS SECURITY ENGINE")
    print("=" * 75)

    print("[+] Security module loaded successfully.")
    print(f"[+] CPU threshold : {CPU_THRESHOLD}%")
    print(f"[+] RAM threshold : {RAM_THRESHOLD}%")

    print("=" * 75)