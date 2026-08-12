import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import csv
import psutil


DB_NAME = "security_monitor.db"


class SecurityDashboard:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Windows Security Monitor - Dashboard"
        )

        self.root.geometry("1250x750")
        self.root.minsize(1000, 650)

        self.root.configure(
            bg="#0f172a"
        )

        self.create_database()
        self.create_ui()

        self.refresh_dashboard()

    # =========================================================
    # DATABASE
    # =========================================================

    def create_database(self):

        connection = sqlite3.connect(DB_NAME)

        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS security_events (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                timestamp TEXT,

                severity TEXT,

                event_type TEXT,

                port INTEGER,

                address TEXT,

                pid TEXT,

                process TEXT,

                message TEXT

            )
        """)

        connection.commit()
        connection.close()

    # =========================================================
    # USER INTERFACE
    # =========================================================

    def create_ui(self):

        # =====================================================
        # HEADER
        # =====================================================

        header = tk.Frame(
            self.root,
            bg="#111827",
            height=105
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="🛡 WINDOWS SECURITY MONITOR",
            font=("Segoe UI", 25, "bold"),
            fg="white",
            bg="#111827"
        )

        title.pack(
            pady=(18, 2)
        )

        self.status_label = tk.Label(
            header,
            text="● MONITORING ACTIVE",
            font=("Segoe UI", 12, "bold"),
            fg="#22c55e",
            bg="#111827"
        )

        self.status_label.pack()

        # =====================================================
        # STATISTICS CARDS
        # =====================================================

        stats_frame = tk.Frame(
            self.root,
            bg="#0f172a"
        )

        stats_frame.pack(
            fill="x",
            padx=25,
            pady=20
        )

        self.total_label = self.create_stat_card(
            stats_frame,
            "TOTAL EVENTS"
        )

        self.medium_label = self.create_stat_card(
            stats_frame,
            "MEDIUM ALERTS"
        )

        self.high_label = self.create_stat_card(
            stats_frame,
            "HIGH ALERTS"
        )

        self.port_label = self.create_stat_card(
            stats_frame,
            "LISTENING PORTS"
        )

        # =====================================================
        # SYSTEM STATUS
        # =====================================================

        system_frame = tk.Frame(
            self.root,
            bg="#1e293b"
        )

        system_frame.pack(
            fill="x",
            padx=25,
            pady=(0, 15)
        )

        self.cpu_label = tk.Label(
            system_frame,
            text="CPU: --",
            font=("Segoe UI", 12, "bold"),
            fg="white",
            bg="#1e293b"
        )

        self.cpu_label.pack(
            side="left",
            padx=25,
            pady=12
        )

        self.ram_label = tk.Label(
            system_frame,
            text="RAM: --",
            font=("Segoe UI", 12, "bold"),
            fg="white",
            bg="#1e293b"
        )

        self.ram_label.pack(
            side="left",
            padx=25
        )

        self.connection_label = tk.Label(
            system_frame,
            text="Connections: --",
            font=("Segoe UI", 12, "bold"),
            fg="white",
            bg="#1e293b"
        )

        self.connection_label.pack(
            side="left",
            padx=25
        )

        # =====================================================
        # BUTTONS
        # =====================================================

        button_frame = tk.Frame(
            self.root,
            bg="#0f172a"
        )

        button_frame.pack(
            fill="x",
            padx=25
        )

        refresh_button = tk.Button(
            button_frame,
            text="⟳  Refresh",
            command=self.refresh_dashboard,
            font=("Segoe UI", 11, "bold"),
            bg="#2563eb",
            fg="white",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2"
        )

        refresh_button.pack(
            side="left"
        )

        export_button = tk.Button(
            button_frame,
            text="⇩  Export CSV",
            command=self.export_csv,
            font=("Segoe UI", 11, "bold"),
            bg="#16a34a",
            fg="white",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2"
        )

        export_button.pack(
            side="left",
            padx=10
        )

        # =====================================================
        # EVENTS TITLE
        # =====================================================

        events_title = tk.Label(
            self.root,
            text="Recent Security Events",
            font=("Segoe UI", 18, "bold"),
            fg="white",
            bg="#0f172a",
            anchor="w"
        )

        events_title.pack(
            fill="x",
            padx=25,
            pady=(15, 8)
        )

        # =====================================================
        # TABLE
        # =====================================================

        table_frame = tk.Frame(
            self.root,
            bg="#0f172a"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )

        columns = (
            "time",
            "severity",
            "event",
            "port",
            "address",
            "pid",
            "process",
            "message"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "time": "Time",
            "severity": "Severity",
            "event": "Event",
            "port": "Port",
            "address": "Address",
            "pid": "PID",
            "process": "Process",
            "message": "Message"
        }

        widths = {
            "time": 150,
            "severity": 90,
            "event": 190,
            "port": 65,
            "address": 160,
            "pid": 75,
            "process": 120,
            "message": 320
        }

        for column in columns:

            self.table.heading(
                column,
                text=headings[column]
            )

            self.table.column(
                column,
                width=widths[column],
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        self.table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # =====================================================
        # SEVERITY COLORS
        # =====================================================

        self.table.tag_configure(
            "HIGH",
            foreground="#ef4444"
        )

        self.table.tag_configure(
            "MEDIUM",
            foreground="#f59e0b"
        )

        self.table.tag_configure(
            "LOW",
            foreground="#22c55e"
        )

    # =========================================================
    # STAT CARD
    # =========================================================

    def create_stat_card(
        self,
        parent,
        title
    ):

        frame = tk.Frame(
            parent,
            bg="#1e293b",
            height=90
        )

        frame.pack(
            side="left",
            fill="x",
            expand=True,
            padx=6
        )

        title_label = tk.Label(
            frame,
            text=title,
            font=("Segoe UI", 10, "bold"),
            fg="#94a3b8",
            bg="#1e293b"
        )

        title_label.pack(
            pady=(12, 2)
        )

        value_label = tk.Label(
            frame,
            text="0",
            font=("Segoe UI", 25, "bold"),
            fg="white",
            bg="#1e293b"
        )

        value_label.pack()

        return value_label

    # =========================================================
    # GET EVENTS
    # =========================================================

    def get_events(self):

        try:

            connection = sqlite3.connect(
                DB_NAME
            )

            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    timestamp,
                    severity,
                    event_type,
                    port,
                    address,
                    pid,
                    process,
                    message
                FROM security_events
                ORDER BY id DESC
                LIMIT 100
            """)

            events = cursor.fetchall()

            connection.close()

            return events

        except sqlite3.Error as error:

            print(
                f"[DATABASE ERROR] {error}"
            )

            return []

    # =========================================================
    # REFRESH DASHBOARD
    # =========================================================

    def refresh_dashboard(self):

        events = self.get_events()

        # -----------------------------------------------------
        # Clear old table
        # -----------------------------------------------------

        for item in self.table.get_children():

            self.table.delete(item)

        # -----------------------------------------------------
        # Add events
        # -----------------------------------------------------

        for event in events:

            severity = str(
                event[1] or "LOW"
            ).upper()

            if severity not in (
                "HIGH",
                "MEDIUM",
                "LOW"
            ):

                severity = "LOW"

            self.table.insert(
                "",
                "end",
                values=event,
                tags=(severity,)
            )

        # -----------------------------------------------------
        # Statistics
        # -----------------------------------------------------

        total = len(events)

        medium = sum(
            1
            for event in events
            if str(
                event[1] or ""
            ).upper() == "MEDIUM"
        )

        high = sum(
            1
            for event in events
            if str(
                event[1] or ""
            ).upper() == "HIGH"
        )

        # -----------------------------------------------------
        # Update cards
        # -----------------------------------------------------

        self.total_label.config(
            text=str(total)
        )

        self.medium_label.config(
            text=str(medium)
        )

        self.high_label.config(
            text=str(high)
        )

        # =====================================================
        # NETWORK INFORMATION
        # =====================================================

        try:

            connections = psutil.net_connections(
                kind="inet"
            )

            listening = []

            for connection in connections:

                if (
                    connection.status
                    == psutil.CONN_LISTEN
                ):

                    listening.append(
                        connection
                    )

            self.port_label.config(
                text=str(
                    len(listening)
                )
            )

            self.connection_label.config(
                text=f"Connections: {len(connections)}"
            )

        except Exception:

            self.port_label.config(
                text="?"
            )

            self.connection_label.config(
                text="Connections: ?"
            )

        # =====================================================
        # SYSTEM INFORMATION
        # =====================================================

        try:

            cpu = psutil.cpu_percent(
                interval=0.2
            )

            ram = psutil.virtual_memory().percent

            self.cpu_label.config(
                text=f"CPU: {cpu:.1f}%"
            )

            self.ram_label.config(
                text=f"RAM: {ram:.1f}%"
            )

        except Exception:

            self.cpu_label.config(
                text="CPU: ?"
            )

            self.ram_label.config(
                text="RAM: ?"
            )

        # =====================================================
        # SECURITY STATUS
        # =====================================================

        if high > 0:

            self.status_label.config(
                text="● HIGH THREAT DETECTED",
                fg="#ef4444"
            )

        elif medium > 0:

            self.status_label.config(
                text="● SUSPICIOUS ACTIVITY",
                fg="#f59e0b"
            )

        else:

            self.status_label.config(
                text="● MONITORING ACTIVE",
                fg="#22c55e"
            )

        # =====================================================
        # AUTO REFRESH
        # =====================================================

        self.root.after(
            3000,
            self.refresh_dashboard
        )

    # =========================================================
    # EXPORT CSV
    # =========================================================

    def export_csv(self):

        events = self.get_events()

        if not events:

            messagebox.showinfo(
                "Export",
                "No security events available."
            )

            return

        filename = filedialog.asksaveasfilename(
            title="Export Security Events",
            defaultextension=".csv",
            filetypes=[
                (
                    "CSV files",
                    "*.csv"
                )
            ]
        )

        if not filename:

            return

        headers = [
            "Time",
            "Severity",
            "Event",
            "Port",
            "Address",
            "PID",
            "Process",
            "Message"
        ]

        try:

            with open(
                filename,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(
                    file
                )

                writer.writerow(
                    headers
                )

                writer.writerows(
                    events
                )

            messagebox.showinfo(
                "Export Complete",
                "Security events exported successfully."
            )

        except Exception as error:

            messagebox.showerror(
                "Export Error",
                str(error)
            )


# =============================================================
# PROGRAM START
# =============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = SecurityDashboard(
        root
    )

    root.mainloop()