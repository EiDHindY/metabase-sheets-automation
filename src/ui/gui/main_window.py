import os
import traceback
from typing import List, Dict, Any
from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QComboBox, QLineEdit, QPushButton, QHBoxLayout, QMessageBox,
    QAbstractItemView
)

from src.data.file_manager.file_manager import process_daily_files
from src.data.sheets_client.sheets_client import update_sheet_for_agent

ATTENDANCE_OPTIONS = ["Office", "Home", "UPL"]

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Metabase→Sheets Automation")
        self.setWindowIcon(QIcon.fromTheme("document-send"))
        self.resize(1000, 700)

        # Central widget and layout
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Data table - 7 columns to match your data structure
        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels([
            "Agent", "Date", "Talk Time (min)", "Dials", "Leads", "Attendance", "Notes"
        ])
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        layout.addWidget(self.table)

        # Buttons
        btn_layout = QHBoxLayout()
        self.load_btn = QPushButton("Load Today's CSVs")
        self.load_btn.clicked.connect(self.load_daily_files)
        btn_layout.addWidget(self.load_btn)

        self.upload_btn = QPushButton("Upload to Google Sheets")
        self.upload_btn.clicked.connect(self.upload_all)
        self.upload_btn.setEnabled(False)
        btn_layout.addWidget(self.upload_btn)
        layout.addLayout(btn_layout)

        # Exit menu
        exit_act = QAction("E&xit", self)
        exit_act.triggered.connect(self.close)
        self.menuBar().addAction(exit_act)

        # Data storage
        self.records: List[Dict[str, Any]] = []

        # Styling
        self.setStyleSheet("""
            QTableWidget { 
                gridline-color: #ccc; 
                font-size: 10pt;
            }
            QHeaderView::section { 
                background: #f0f0f0; 
                padding: 6px; 
                font-weight: bold;
            }
            QPushButton {
                padding: 8px 16px;
                font-size: 10pt;
            }
        """)

    @Slot()
    def load_daily_files(self) -> None:
        """
        Load and merge CSVs using your actual file_manager.process_daily_files function.
        """
        try:
            base_dir = os.getcwd()
            leads_dir = os.path.join(base_dir, "raw-data", "input", "leads")
            talk_time_dir = os.path.join(base_dir, "raw-data", "input", "talk-time")
            dials_made_dir = os.path.join(base_dir, "raw-data", "input", "dials-made")
            team_members_dir = os.path.join(base_dir, "raw-data", "team")

            self.records = process_daily_files(
                leads_dir=leads_dir,
                talk_time_dir=talk_time_dir,
                dials_made_dir=dials_made_dir,
                team_members_dir=team_members_dir
            )

        except Exception as e:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error Loading Files")
            msg.setText("Failed to load and process CSV files.")
            msg.setInformativeText("Click 'Show Details...' for full error trace.")
            msg.setDetailedText(traceback.format_exc())
            msg.setSizeGripEnabled(True)
            msg.setOption(QMessageBox.DontUseNativeDialog, True)
            msg.exec()
            return

        self.populate_table()
        self.upload_btn.setEnabled(True)

    def populate_table(self) -> None:
        """
        Fill QTableWidget with records from your team data processing.
        """
        self.table.setRowCount(len(self.records))

        for row, rec in enumerate(self.records):
            self.table.setItem(row, 0, QTableWidgetItem(str(rec.get("agent_name", ""))))
            self.table.setItem(row, 1, QTableWidgetItem(str(rec.get("date", ""))))
            talk_time = rec.get("talk_time", 0.0)
            self.table.setItem(row, 2, QTableWidgetItem(f"{talk_time:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(str(rec.get("dials", 0))))

            leads_edit = QLineEdit(str(rec.get("leads", 0)))
            leads_edit.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(row, 4, leads_edit)

            att_combo = QComboBox()
            att_combo.addItems(ATTENDANCE_OPTIONS)
            current_att = rec.get("attendance", "")
            if current_att in ATTENDANCE_OPTIONS:
                att_combo.setCurrentText(current_att)
            self.table.setCellWidget(row, 5, att_combo)

            notes_edit = QLineEdit(str(rec.get("notes", "")))
            self.table.setCellWidget(row, 6, notes_edit)

    @Slot()
    def upload_all(self) -> None:
        """
        Read each row's widget values, ensure 'date' is set from the table,
        and call update_sheet_for_agent for each record.
        """
        errors: List[str] = []

        # 1) Force commit of in-progress edits
        for r in range(self.table.rowCount()):
            for c in [4, 5, 6]:  # editable columns
                widget = self.table.cellWidget(r, c)
                if widget:
                    widget.clearFocus()

        # 2) Read current widget values and populate 'date'
        for r in range(self.table.rowCount()):
            rec = self.records[r]

            # Populate date from column 1
            date_item = self.table.item(r, 1)
            rec["date"] = date_item.text() if date_item else ""

            # Read leads
            leads_widget = self.table.cellWidget(r, 4)
            if isinstance(leads_widget, QLineEdit):
                try:
                    rec["leads"] = int(leads_widget.text() or "0")
                except ValueError:
                    rec["leads"] = 0

            # Read attendance
            att_widget = self.table.cellWidget(r, 5)
            if isinstance(att_widget, QComboBox):
                rec["attendance"] = att_widget.currentText()

            # Read notes
            notes_widget = self.table.cellWidget(r, 6)
            if isinstance(notes_widget, QLineEdit):
                rec["notes"] = notes_widget.text()

            # 3) Upload to Google Sheets
            try:
                update_sheet_for_agent(rec)
            except Exception:
                tb = traceback.format_exc()
                agent_name = rec.get("agent_name", "Unknown")
                date = rec.get("date", "")
                errors.append(
                    f"Agent: {agent_name} ({date})\nError: {str(tb)}"
                )

        # 4) Show result dialog
        if errors:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Upload Completed with Errors")
            msg.setText(f"Failed to upload {len(errors)} out of {len(self.records)} agents.")
            msg.setInformativeText("Click 'Show Details...' for full errors.")
            msg.setDetailedText("\n\n".join(errors))
            msg.setSizeGripEnabled(True)
            msg.setOption(QMessageBox.DontUseNativeDialog, True)
            msg.exec()
        else:
            QMessageBox.information(
                self,
                "Success",
                f"All {len(self.records)} agents uploaded successfully!"
            )

        # Disable the upload button after completion
        self.upload_btn.setEnabled(False)
