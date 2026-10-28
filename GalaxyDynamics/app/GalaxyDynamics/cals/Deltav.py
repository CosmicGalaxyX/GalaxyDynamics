# Imports
print("Importing Libraries")

import math
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QFrame,
    QStackedWidget,
    QScrollArea,
    QLabel,
)

BG_COLOR       = "#050814"   # almost-black deep blue
SURFACE_COLOR  = "#0B1024"   # dark space blue
CARD_COLOR     = "#111735"   # blue-indigo
HOVER_COLOR    = "#17204A"   # stronger deep blue
BORDER_COLOR   = "#252B59"   # indigo-blue
ACCENT_BLUE    = "#3155D8"   # deep electric blue
ACCENT_INDIGO  = "#4A3FA3"   # dark indigo
ACCENT_PURPLE  = "#6A3FA0"   # deep purple
TEXT_COLOR     = "#E5E9FF"   # cool blue-white
SECONDARY_TEXT = "#7882A8"   # muted blue-gray

HeaderFont = "Space Grotesk"
SubHeaderFont = "Inter"
TechNumFont = "JetBrains Mono"


# UI Setup
qapp = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Delta V Calulator v0.1.5")
window.showMaximized()

layout = QVBoxLayout()
# Variables
Mercury = 3.7
Venus = 8.87
Earth = 9.81
Mars = 3.71
Jupiter = 24.79
Saturn = 10.44
Uranus = 8.69
Neptune = 11.15
Moon = 1.62
Pluto = 0.62

# UI Buildout

isp_input = QLineEdit()
isp_input.setPlaceholderText("Enter ISP (s)")
isp_input.setFixedHeight(100)
layout.addWidget(isp_input)
isp_input.setStyleSheet( 
     f"""
    QLineEdit {{
        background-color: {CARD_COLOR};
        color: {TEXT_COLOR};
        font-size: 32px;
        font-family: {SubHeaderFont};
        border: 2px solid {BORDER_COLOR};
        border-radius: 16px;
    }}
    """
)

g0_input = QLineEdit()
g0_input.setPlaceholderText("Enter g0 (m/s²)")
g0_input.setFixedHeight(100)
layout.addWidget(g0_input)
g0_input.setStyleSheet( 
     f"""
    QLineEdit {{
        background-color: {CARD_COLOR};
        color: {TEXT_COLOR};
        font-size: 32px;
        font-family: {SubHeaderFont};
        border: 2px solid {BORDER_COLOR};
        border-radius: 16px;
    }}
    """
)

m0_input = QLineEdit()
m0_input.setPlaceholderText("Enter initial mass (kg)")
m0_input.setFixedHeight(100)
layout.addWidget(m0_input)
m0_input.setStyleSheet( 
     f"""
    QLineEdit {{
        background-color: {CARD_COLOR};
        color: {TEXT_COLOR};
        font-size: 32px;
        font-family: {SubHeaderFont};
        border: 2px solid {BORDER_COLOR};
        border-radius: 16px;
    }}
    """
)

m1_input = QLineEdit() 
m1_input.setPlaceholderText("Enter final mass (kg)")
m1_input.setFixedHeight(100)
layout.addWidget(m1_input)
m1_input.setStyleSheet( 
     f"""
    QLineEdit {{
        background-color: {CARD_COLOR};
        color: {TEXT_COLOR};
        font-size: 32px;
        font-family: {SubHeaderFont};
        border: 2px solid {BORDER_COLOR};
        border-radius: 16px;
    }}
    """
)

submit_button = QPushButton("Calculate ΔV")
layout.addWidget(submit_button)
submit_button.setFixedHeight(100)
submit_button.setStyleSheet(
    f"""
    QPushButton {{
        background-color: {CARD_COLOR};
        color: {TEXT_COLOR};
        font-size: 50px;
        font-family: {HeaderFont};
        border: 2px solid {BORDER_COLOR};
        border-radius: 16px;
    }}

    QPushButton:hover {{
        background-color: {HOVER_COLOR};
        border: 2px solid {ACCENT_INDIGO};
    }}

    QPushButton:pressed {{
        background-color: {ACCENT_PURPLE};
    }}
    """
)
OutputLabel = QLabel("Output/Result")
layout.addWidget(OutputLabel)
OutputLabel.setStyleSheet(
     f"""
    QLabel{{
        color: {TEXT_COLOR};
        font-size: 30px;
        font-family: {HeaderFont};
    }}
    """
)
OutputLog = QLabel()
layout.addWidget(OutputLog)
OutputLog.setStyleSheet(
     f"""
    QLabel{{
        color: white;
        font-size: 50px;
        font-family: {TechNumFont};
    }}
    """
)
OutputLog2 = QLabel()
layout.addWidget(OutputLog2)
OutputLog2.setStyleSheet(
     f"""
    QLabel{{
        color: white;
        font-size: 50px;
        font-family: {TechNumFont};
    }}
    """
)


# wehn clicked, call the calculate_DeltaV function and display the result in a message boxn 
    
def calculate():
    isp = float(isp_input.text())
    g0 = float(g0_input.text())
    m0 = float(m0_input.text())
    m1 = float(m1_input.text())

    deltav = isp * g0 * math.log(m0/m1)
    OutputLog.setText(f"Delta V: {deltav/1000:.3f} km/s")
    OutputLog2.setText(f"Delta V: {deltav:.3f} m/s")
    OutputLog.setStyleSheet(
                    f"""
                  QLabel {{
                    color: green;
                    font-size: 30px;
                    }}
                    """
                )
    OutputLog2.setStyleSheet(
                    f"""
                  QLabel {{
                    color: green;
                    font-size: 30px;
                    }}
                    """
                )
    return calculate
   


submit_button.clicked.connect(calculate)


window.setLayout(layout)
window.show()

sys.exit(qapp.exec())
 