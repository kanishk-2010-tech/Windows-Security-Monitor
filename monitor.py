import os
import platform
import time
from datetime import datetime

import psutil
import security


# ============================================================
# WINDOWS SECURITY MONITOR - FINAL
# ============================================================

REFRESH_TIME = 10


# ============================================================
# SYSTEM INFORMATION
# ============================================================

def get_system_info():

    cpu = psutil.cpu_percent(interval=1)

    memory = psutil.virtual_memory()

    try:
        disk = psutil.disk_usage("C:\\")
    except OSError:
        disk = None

    print("=" * 75)
    print("                 WINDOWS SECURITY MONITOR")
    print("=" * 75)

    print(
        f"Computer : {platform.node()}"
    )

    print(
        f"Windows  : "
        f"{platform.system()} "
        f"{platform.release()}"
    )

    print(
        f"Time     : "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    print("\n[ SYSTEM STATUS ]")

    print(
        f"CPU Usage     : {cpu}%"
    )

    print(
        f"RAM Usage     : {memory.percent}%"
    )

    print(
        f"RAM Total     : "
        f"{memory.total / (1024 ** 3):.2f} GB"
    )

    print(
        f"RAM Available : "
        f"{memory.available / (1024 ** 3):.2f} GB"
    )

    if disk:

        print(
            f"Disk Usage    : "
            f"{disk.percent}%"
        )

        print(
            f"Disk Free     : "
            f"{disk.free / (1024 ** 3):.2f} GB"
        )

    return cpu, memory.percent


# ============================================================
# RUNNING PROCESSES
# ============================================================

def get_processes():

    print("\n[ RUNNING PROCESSES ]")

    processes = []

    for process in psutil.process_iter(
        ["pid", "name", "username"]
    ):

        try:

            info = process.info

            processes.append({
                "pid": info["pid"],
                "name": info["name"] or "Unknown",
                "username": (
                    info["username"] or "Unknown"
                )
            })

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):

            continue

    print(
        f"Total Running Processes: "
        f"{len(processes)}"
    )

    print("\nPID       PROCESS")
    print("-" * 55)

    for process in processes[:20]:

        print(
            f"{process['pid']:<10}"
            f"{process['name']}"
        )

    return processes


# ============================================================
# NETWORK CONNECTIONS
# ============================================================

def get_network_connections():

    print("\n[ NETWORK CONNECTIONS ]")

    try:

        connections = psutil.net_connections(
            kind="inet"
        )

        print(
            f"Total Connections: "
            f"{len(connections)}"
        )

        print(
            "\nLOCAL ADDRESS             "
            "REMOTE ADDRESS            STATUS"
        )

        print("-" * 80)

        for connection in connections[:20]:

            if connection.laddr:

                local_address = (
                    f"{connection.laddr.ip}:"
                    f"{connection.laddr.port}"
                )

            else:

                local_address = "-"

            if connection.raddr:

                remote_address = (
                    f"{connection.raddr.ip}:"
                    f"{connection.raddr.port}"
                )

            else:

                remote_address = "-"

            print(
                f"{local_address:<25}"
                f"{remote_address:<25}"
                f"{connection.status}"
            )

        return connections

    except psutil.AccessDenied:

        print(
            "[!] Access denied while reading "
            "network connections."
        )

        return []


# ============================================================
# LISTENING PORTS
# ============================================================

def get_listening_ports(connections):

    print("\n[ LISTENING PORTS ]")

    listening = []

    for connection in connections:

        if connection.status != psutil.CONN_LISTEN:
            continue

        if not connection.laddr:
            continue

        listening.append(connection)

    print(
        f"Listening Ports: "
        f"{len(listening)}"
    )

    print(
        "\nPORT      ADDRESS              "
        "PID       PROCESS"
    )

    print("-" * 75)

    listening.sort(
        key=lambda connection:
        connection.laddr.port
    )

    port_details = []

    for connection in listening:

        port = connection.laddr.port

        address = (
            f"{connection.laddr.ip}:"
            f"{port}"
        )

        pid = connection.pid

        if pid is None:

            pid_display = "-"
            process_name = "Unknown"

        else:

            pid_display = str(pid)

            try:

                process = psutil.Process(pid)
                process_name = process.name()

            except psutil.NoSuchProcess:

                process_name = "Process Closed"

            except psutil.AccessDenied:

                process_name = "Access Denied"

            except Exception:

                process_name = "Unknown"

        print(
            f"{port:<10}"
            f"{address:<21}"
            f"{pid_display:<10}"
            f"{process_name}"
        )

        port_details.append({
            "port": port,
            "address": address,
            "pid": pid_display,
            "process": process_name
        })

    return port_details


# ============================================================
# SECURITY ANALYSIS
# ============================================================

def run_security_analysis(
    cpu,
    ram,
    processes,
    port_details
):

    print("\n[ SECURITY ANALYSIS ]")

    # CPU + RAM
    resource_alerts = security.check_resources(
        cpu,
        ram
    )

    # Ports
    port_alerts = security.check_ports(
        port_details
    )

    # Processes
    process_alerts = security.analyze_process_risk(
        processes
    )

    # Combine
    alerts = (
        resource_alerts
        + port_alerts
        + process_alerts
    )

    # Display
    security.display_alerts(
        alerts
    )

    # Threat score
    threat_result = (
        security.display_threat_score(
            alerts
        )
    )

    return alerts, threat_result


# ============================================================
# MAIN MONITORING LOOP
# ============================================================

def main():

    print(
        "[+] Starting Windows Security Monitor..."
    )

    print(
        f"[+] Refresh interval: "
        f"{REFRESH_TIME} seconds"
    )

    print(
        "[+] Press CTRL+C to stop."
    )

    time.sleep(2)

    try:

        while True:

            os.system("cls")

            # ----------------------------------------------
            # SYSTEM
            # ----------------------------------------------

            cpu, ram = get_system_info()

            # ----------------------------------------------
            # PROCESSES
            # ----------------------------------------------

            processes = get_processes()

            # ----------------------------------------------
            # NETWORK
            # ----------------------------------------------

            connections = (
                get_network_connections()
            )

            # ----------------------------------------------
            # LISTENING PORTS
            # ----------------------------------------------

            port_details = (
                get_listening_ports(
                    connections
                )
            )

            # ----------------------------------------------
            # SECURITY ENGINE
            # ----------------------------------------------

            run_security_analysis(
                cpu,
                ram,
                processes,
                port_details
            )

            # ----------------------------------------------
            # REFRESH
            # ----------------------------------------------

            print("\n" + "=" * 75)

            print(
                f"Monitoring refresh: "
                f"{REFRESH_TIME} seconds"
            )

            print(
                "Press CTRL+C to stop."
            )

            print("=" * 75)

            time.sleep(
                REFRESH_TIME
            )

    except KeyboardInterrupt:

        print(
            "\n\n[+] Windows Security Monitor stopped."
        )


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":
    main()