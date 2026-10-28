# ============================================================
# Imports
# ============================================================

import math
import sys
import numpy as np

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QLabel,
    QComboBox,
)


# ============================================================
# GalaxyDynamics Theme
# ============================================================

BG_COLOR = "#050814"
SURFACE_COLOR = "#0B1024"
CARD_COLOR = "#111735"
HOVER_COLOR = "#17204A"
BORDER_COLOR = "#252B59"

ACCENT_BLUE = "#3155D8"
ACCENT_INDIGO = "#4A3FA3"
ACCENT_PURPLE = "#6A3FA0"

TEXT_COLOR = "#E5E9FF"
SECONDARY_TEXT = "#7882A8"

HEADER_FONT = "Space Grotesk"
SUBHEADER_FONT = "Inter"
TECH_NUM_FONT = "JetBrains Mono"


# ============================================================
# Celestial Body Library
# μ in km³/s²
# ============================================================

MU_LIBRARY = {
    "Sun": 1.327e11,
    "Earth": 3.986004418e5,
    "Moon": 4.902807e3,
    "Mars": 4.282837e4,
}


# ============================================================
# Application Setup
# ============================================================

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Signal Calculator v0.1")
window.showMaximized()


# ============================================================
# Main Layout
# ============================================================


# ============================================================
# Calculator Layout
# ============================================================

main_layout = QHBoxLayout(window)

main_layout.setContentsMargins(30, 30, 30, 30)
main_layout.setSpacing(30)


# ============================================================
# Input / Output Columns
# ============================================================

input_layout = QVBoxLayout()
input_layout.setSpacing(14)

output_layout = QVBoxLayout()
output_layout.setSpacing(14)

main_layout.addLayout(input_layout, 1)
main_layout.addLayout(output_layout, 1)


# ============================================================
# Reusable Styles
# ============================================================

label_style = f"""
QLabel {{
    color: {SECONDARY_TEXT};
    font-size: 13px;
    font-family: {SUBHEADER_FONT};
}}
"""


input_style = f"""
QLineEdit {{
    background-color: {CARD_COLOR};
    color: {TEXT_COLOR};
    font-size: 17px;
    font-family: {TECH_NUM_FONT};
    border: 1px solid {BORDER_COLOR};
    border-radius: 8px;
    padding: 8px 10px;
}}

QLineEdit:focus {{
    border: 1px solid {ACCENT_BLUE};
}}
"""


dropdown_style = f"""
QComboBox {{
    background-color: {CARD_COLOR};
    color: {TEXT_COLOR};
    font-size: 16px;
    font-family: {SUBHEADER_FONT};
    border: 1px solid {BORDER_COLOR};
    border-radius: 8px;
    padding: 8px 10px;
}}
"""

button_style = f""""

QPushButton {{
    background-color: {CARD_COLOR};
    color: {TEXT_COLOR};
    font-size: 16px;
    font-family: {SUBHEADER_FONT};
    border: 1px solid {BORDER_COLOR};
    border-radius: 8px;
    padding: 8px 10px;
}}

QComboBox:hover {{
    border: 1px solid {ACCENT_BLUE};
}}
"""


result_label_style = f"""
QLabel {{
    color: {TEXT_COLOR};
    font-size: 22px;
    font-family: {TECH_NUM_FONT};
    font-weight: bold;
}}
"""


# ============================================================
# INPUTS
# ============================================================

input_header = QLabel("INPUTS")
input_header.setStyleSheet(f"""
QLabel {{
    color: {TEXT_COLOR};
    font-size: 15px;
    font-family: {SUBHEADER_FONT};
    font-weight: bold;
}}
""")

input_layout.addWidget(input_header)


# ============================================================
# RESULTS
# ============================================================

output_header = QLabel("RESULTS")
output_header.setStyleSheet(f"""
QLabel {{
    color: {TEXT_COLOR};
    font-size: 15px;
    font-family: {SUBHEADER_FONT};
    font-weight: bold;
}}
""")

output_layout.addWidget(output_header)

# ----------------------------
# Distance + Unit
# ----------------------------

distance_row = QHBoxLayout()
distance_row.setSpacing(8)

distance = QLineEdit()
distance.setPlaceholderText("Distance")
distance.setFixedHeight(50)
distance.setStyleSheet(input_style)

Dropdown = QComboBox()
Dropdown.addItems(["km", "AU"])
Dropdown.setFixedHeight(50)
Dropdown.setMinimumWidth(100)
Dropdown.setStyleSheet(dropdown_style)


distance_row.addWidget(distance)
distance_row.addWidget(Dropdown)

input_layout.addLayout(distance_row)


# ----------------------------
# Signal Speed
# ----------------------------

signal_speed = QLineEdit()
signal_speed.setPlaceholderText("Signal Speed (km/s)")
signal_speed.setFixedHeight(50)
signal_speed.setStyleSheet(input_style)

c = "299792.458"  # Speed of light in km/s
signal_speed.setText(c)

input_layout.addWidget(signal_speed)


# Calculate Button
CalculateButton = QPushButton("Calculate")
CalculateButton.setFixedHeight(50)
CalculateButton.setMinimumWidth(150)

input_layout.addWidget(CalculateButton)

# ============================================================
# OUTPUTS
# ============================================================

output_title = QLabel("RESULTS")
output_title.setStyleSheet(label_style)

output_layout.addWidget(output_title)


# ----------------------------
# One-Way Time
# ----------------------------

OneWayTime = QLabel("One-Way Time: --")
OneWayTime.setFixedHeight(70)
OneWayTime.setStyleSheet(label_style)

output_layout.addWidget(OneWayTime)


# ----------------------------
# Both-Ways Time
# ----------------------------

BothWaysTime = QLabel("Round-Trip Time: --")
BothWaysTime.setFixedHeight(70)
BothWaysTime.setStyleSheet(label_style)

output_layout.addWidget(BothWaysTime)

#Caluclations

def calculate_times():

    if CalculateButton.clicked:
        OnewayTime = (float(distance.text()) / float(signal_speed.text()))
        BothWaysTime = (float(distance.text()) / float(signal_speed.text())) * 2

        OneWayTime = QLabel(f"One-Way Time: {OnewayTime:.2f} seconds")
        BothWaysTime = QLabel(f"Round-Trip Time: {BothWaysTime:.2f} seconds")

CalculateButton.clicked.connect(calculate_times)







# ============================================================
# Run
# ============================================================

window.show()
window.adjustSize()
sys.exit(app.exec())