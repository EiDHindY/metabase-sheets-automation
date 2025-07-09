# src/ui/gui/main_window.py

import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QTableWidget, QTableWidgetItem, QFileDialog, QProgressBar,
    QComboBox, QSpinBox, QGroupBox, QMessageBox, QHeaderView
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont

# Import your existing services
from src.core.services.team_data_service import process_team_data
from src.data.sheets_client.sheets_client import update_sheet_for_agent

class DataProcessingThread(QThread):
    """Background thread for processing and uploading data"""
    progress_update = Signal(int)
    status_update = Signal(str)
    upload_complete = Signal(bool, str)
    
    def __init__(self, agent_data_list):
        super().__init__()
        self.agent_data_list = agent_data_list
        
    def run(self):
        """Process and upload agent data"""
        try:
            total_agents = len(self.agent_data_list)
            
            for i, agent_data in enumerate(self.agent_data_list):
                self.status_update.emit(f"Uploading {agent_data['agent_name']}...")
                
                # Add current date
                agent_data['date'] = datetime.now().strftime("%d/%m/%Y")
                
                # Upload to Google Sheets
                update_sheet_for_agent(agent_data)
                
                # Update progress
                progress = int((i + 1) / total_agents * 100)
                self.progress_update.emit(progress)
                
                # Small delay to show progress
                self.msleep(500)
            
            self.upload_complete.emit(True, "All data uploaded successfully!")
            
        except Exception as e:
            self.upload_complete.emit(False, f"Upload failed: {str(e)}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.apply_dark_theme()
        
        # Data storage
        self.agent_data = []
        self.file_paths = {
            'team_members': None,
            'talk_time': None,
            'dials_made': None,
            'leads': None
        }
        
    def setup_ui(self):
        """Setup the main user interface"""
        self.setWindowTitle("Team Data Processor")
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Title
        title_label = QLabel("Team Data Processor")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        main_layout.addWidget(title_label)
        
        # File selection section
        file_group = self.create_file_selection_group()
        main_layout.addWidget(file_group)
        
        # Load data button
        self.load_button = QPushButton("Load Team Data")
        self.load_button.clicked.connect(self.load_team_data)
        self.load_button.setMinimumHeight(40)
        main_layout.addWidget(self.load_button)
        
        # Data table
        self.create_data_table()
        main_layout.addWidget(self.data_table)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # Upload button
        self.upload_button = QPushButton("Upload to Google Sheets")
        self.upload_button.clicked.connect(self.upload_data)
        self.upload_button.setEnabled(False)
        self.upload_button.setMinimumHeight(40)
        main_layout.addWidget(self.upload_button)
        
        # Status label
        self.status_label = QLabel("Ready - Select CSV files and load team data")
        main_layout.addWidget(self.status_label)
        
    def create_file_selection_group(self):
        """Create file selection interface"""
        group = QGroupBox("Select CSV Files")
        layout = QVBoxLayout(group)
        
        # File selection buttons
        files = [
            ('team_members', 'Team Members CSV (Required)'),
            ('talk_time', 'Talk Time CSV (Required)'),
            ('dials_made', 'Dials Made CSV (Required)'),
            ('leads', 'Leads CSV (Optional)')
        ]
        
        self.file_labels = {}
        
        for key, description in files:
            file_layout = QHBoxLayout()
            
            # Button
            button = QPushButton(f"Select {description}")
            button.clicked.connect(lambda checked, k=key: self.select_file(k))
            file_layout.addWidget(button)
            
            # Label to show selected file
            label = QLabel("No file selected")
            label.setMinimumWidth(300)
            self.file_labels[key] = label
            file_layout.addWidget(label)
            
            layout.addLayout(file_layout)
        
        return group
    
    def create_data_table(self):
        """Create the main data table"""
        self.data_table = QTableWidget()
        
        # Set up columns
        columns = ["Agent Name", "Attendance", "Leads", "Talk Time", "Dials Made", "Notes"]
        self.data_table.setColumnCount(len(columns))
        self.data_table.setHorizontalHeaderLabels(columns)
        
        # Make table look better
        self.data_table.setAlternatingRowColors(True)
        self.data_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        # Auto-resize columns
        header = self.data_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Agent Name
        header.setSectionResizeMode(1, QHeaderView.Fixed)    # Attendance
        header.setSectionResizeMode(2, QHeaderView.Fixed)    # Leads
        header.setSectionResizeMode(3, QHeaderView.Fixed)    # Talk Time
        header.setSectionResizeMode(4, QHeaderView.Fixed)    # Dials Made
        header.setSectionResizeMode(5, QHeaderView.Stretch)  # Notes
        
        # Set column widths
        self.data_table.setColumnWidth(1, 120)  # Attendance
        self.data_table.setColumnWidth(2, 80)   # Leads
        self.data_table.setColumnWidth(3, 100)  # Talk Time
        self.data_table.setColumnWidth(4, 100)  # Dials Made
        
    def select_file(self, file_type):
        """Open file dialog to select CSV file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            f"Select {file_type.replace('_', ' ').title()} CSV", 
            "", 
            "CSV Files (*.csv)"
        )
        
        if file_path:
            self.file_paths[file_type] = file_path
            filename = Path(file_path).name
            self.file_labels[file_type].setText(filename)
            self.check_ready_to_load()
    
    def check_ready_to_load(self):
        """Check if all required files are selected"""
        required_files = ['team_members', 'talk_time', 'dials_made']
        all_required = all(self.file_paths[key] for key in required_files)
        self.load_button.setEnabled(all_required)
    
    def load_team_data(self):
        """Load team data from CSV files"""
        try:
            self.status_label.setText("Loading team data...")
            
            # Use existing team_data_service to process data
            self.agent_data = process_team_data(
                self.file_paths['team_members'],
                self.file_paths['talk_time'],
                self.file_paths['dials_made'],
                self.file_paths['leads']
            )
            
            # Populate table
            self.populate_table()
            
            self.status_label.setText(f"Loaded {len(self.agent_data)} agents")
            self.upload_button.setEnabled(True)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load data: {str(e)}")
            self.status_label.setText("Error loading data")
    
    def populate_table(self):
        """Populate the table with agent data"""
        self.data_table.setRowCount(len(self.agent_data))
        
        for row, agent in enumerate(self.agent_data):
            # Agent Name (read-only)
            self.data_table.setItem(row, 0, QTableWidgetItem(agent['agent_name']))
            self.data_table.item(row, 0).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            
            # Attendance (dropdown)
            attendance_combo = QComboBox()
            attendance_combo.addItems(['office', 'home', 'UPL'])
            attendance_combo.setCurrentText('office')  # Default
            self.data_table.setCellWidget(row, 1, attendance_combo)
            
            # Leads (editable spinbox)
            leads_spin = QSpinBox()
            leads_spin.setRange(0, 999)
            leads_spin.setValue(agent.get('leads', 0))
            self.data_table.setCellWidget(row, 2, leads_spin)
            
            # Talk Time (read-only, formatted)
            talk_time_minutes = agent.get('talk_time', 0)
            talk_time_str = f"{talk_time_minutes:.1f} min"
            self.data_table.setItem(row, 3, QTableWidgetItem(talk_time_str))
            self.data_table.item(row, 3).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            
            # Dials Made (read-only)
            self.data_table.setItem(row, 4, QTableWidgetItem(str(agent.get('dials', 0))))
            self.data_table.item(row, 4).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            
            # Notes (editable)
            notes_item = QTableWidgetItem("")
            self.data_table.setItem(row, 5, notes_item)
    
    def get_table_data(self):
        """Extract data from table including user edits"""
        table_data = []
        
        for row in range(self.data_table.rowCount()):
            # Get original agent data
            agent_data = self.agent_data[row].copy()
            
            # Update with user edits
            attendance_combo = self.data_table.cellWidget(row, 1)
            leads_spin = self.data_table.cellWidget(row, 2)
            notes_item = self.data_table.item(row, 5)
            
            agent_data['attendance'] = attendance_combo.currentText()
            agent_data['leads'] = leads_spin.value()
            agent_data['notes'] = notes_item.text() if notes_item else ""
            
            table_data.append(agent_data)
        
        return table_data
    
    def upload_data(self):
        """Upload data to Google Sheets"""
        if not self.agent_data:
            QMessageBox.warning(self, "Warning", "No data to upload")
            return
        
        # Get current data from table
        current_data = self.get_table_data()
        
        # Start upload process
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.upload_button.setEnabled(False)
        self.status_label.setText("Starting upload...")
        
        # Create and start processing thread
        self.upload_thread = DataProcessingThread(current_data)
        self.upload_thread.progress_update.connect(self.progress_bar.setValue)
        self.upload_thread.status_update.connect(self.status_label.setText)
        self.upload_thread.upload_complete.connect(self.upload_finished)
        self.upload_thread.start()
    
    def upload_finished(self, success, message):
        """Handle upload completion"""
        self.progress_bar.setVisible(False)
        self.upload_button.setEnabled(True)
        self.status_label.setText(message)
        
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.critical(self, "Error", message)
    
    def apply_dark_theme(self):
        """Apply modern dark theme"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            
            QLabel {
                color: #ffffff;
                font-size: 12px;
            }
            
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #106ebe;
            }
            
            QPushButton:disabled {
                background-color: #555555;
                color: #888888;
            }
            
            QGroupBox {
                font-weight: bold;
                border: 2px solid #555555;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #0078d4;
            }
            
            QTableWidget {
                background-color: #3c3c3c;
                border: 1px solid #555555;
                gridline-color: #555555;
                selection-background-color: #0078d4;
            }
            
            QTableWidget::item {
                padding: 5px;
                border-bottom: 1px solid #555555;
            }
            
            QTableWidget::item:alternate {
                background-color: #404040;
            }
            
            QHeaderView::section {
                background-color: #555555;
                color: white;
                padding: 5px;
                border: 1px solid #666666;
                font-weight: bold;
            }
            
            QComboBox, QSpinBox {
                background-color: #3c3c3c;
                border: 1px solid #555555;
                padding: 5px;
                color: white;
            }
            
            QComboBox::drop-down {
                border: none;
            }
            
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid white;
            }
            
            QProgressBar {
                border: 2px solid #555555;
                border-radius: 5px;
                text-align: center;
                font-weight: bold;
            }
            
            QProgressBar::chunk {
                background-color: #0078d4;
                border-radius: 3px;
            }
        """)