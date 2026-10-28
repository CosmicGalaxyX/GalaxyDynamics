# ============================================================
# Imports
# ============================================================

import math
import sys

from PySide6.QtCore import Qt
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
window.setWindowTitle("Keplerian Orbit Calculator v0.1")
window.showMaximized()

main_layout = QHBoxLayout(window)

input_layout = QVBoxLayout()
output_layout = QVBoxLayout()

main_layout.addLayout(input_layout, 1)
main_layout.addLayout(output_layout, 3)


# ============================================================
# Reusable Styles
# ============================================================

input_style = f"""
QLineEdit {{
    background-color: {CARD_COLOR};
    color: {TEXT_COLOR};
    font-size: 22px;
    font-family: {SUBHEADER_FONT};
    border: 2px solid {BORDER_COLOR};
    border-radius: 12px;
    padding: 10px;
}}

QLineEdit:focus {{
    border: 2px solid {ACCENT_BLUE};
}}
"""

dropdown_style = f"""
QComboBox {{
    background-color: {CARD_COLOR};
    color: {TEXT_COLOR};
    font-size: 22px;
    font-family: {SUBHEADER_FONT};
    border: 2px solid {BORDER_COLOR};
    border-radius: 12px;
    padding: 10px;
}}
"""

output_style = f"""
QLabel {{
    background-color: {CARD_COLOR};
    color: {TEXT_COLOR};
    font-size: 18px;
    font-family: {TECH_NUM_FONT};
    border: 2px solid {BORDER_COLOR};
    border-radius: 12px;
    padding: 15px;
}}
"""

button_style = f"""
QPushButton {{
    background-color: {CARD_COLOR};
    color: {TEXT_COLOR};
    font-size: 22px;
    font-family: {TECH_NUM_FONT};
    border: 2px solid {BORDER_COLOR};
    border-radius: 12px;
    padding: 10px;
}}

QPushButton:hover {{
    background-color: {HOVER_COLOR};
}}

QPushButton:pressed {{
    background-color: {ACCENT_BLUE};
}}
"""


# ============================================================
# Input Widgets
# ============================================================

mu = QComboBox()
mu.addItems([
    "Sun",
    "Earth",
    "Moon",
    "Mars",
    "Custom",
])
mu.setFixedHeight(65)
mu.setStyleSheet(dropdown_style)

input_layout.addWidget(mu)


cmu = QLineEdit()
cmu.setPlaceholderText(
    "Custom μ (km³/s²) — example: 1.0e5"
)
cmu.setFixedHeight(65)
cmu.setStyleSheet(input_style)

input_layout.addWidget(cmu)


Sma = QLineEdit()
Sma.setPlaceholderText("Semi-Major Axis (km)")
Sma.setFixedHeight(65)
Sma.setStyleSheet(input_style)

input_layout.addWidget(Sma)


Ecc = QLineEdit()
Ecc.setPlaceholderText("Eccentricity (0–1)")
Ecc.setFixedHeight(65)
Ecc.setStyleSheet(input_style)

input_layout.addWidget(Ecc)


Inc = QLineEdit()
Inc.setPlaceholderText("Inclination (degrees)")
Inc.setFixedHeight(65)
Inc.setStyleSheet(input_style)

input_layout.addWidget(Inc)


RAAN = QLineEdit()
RAAN.setPlaceholderText(
    "RAAN (degrees)"
)
RAAN.setFixedHeight(65)
RAAN.setStyleSheet(input_style)

input_layout.addWidget(RAAN)


aop = QLineEdit()
aop.setPlaceholderText(
    "Argument of Periapsis (degrees)"
)
aop.setFixedHeight(65)
aop.setStyleSheet(input_style)

input_layout.addWidget(aop)


ta = QLineEdit()
ta.setPlaceholderText(
    "True Anomaly (degrees)"
)
ta.setFixedHeight(65)
ta.setStyleSheet(input_style)

input_layout.addWidget(ta)


# ============================================================
# Calculate Button
# ============================================================

calculate_button = QPushButton("Calculate")
calculate_button.setFixedHeight(60)
calculate_button.setStyleSheet(button_style)

input_layout.addWidget(calculate_button)

input_layout.addStretch()


# ============================================================
# Output Widgets
# ============================================================

orbital_period = QLabel("Orbital Period: —")
orbital_period.setStyleSheet(output_style)
orbital_period.setMinimumHeight(60)

velocity = QLabel("Velocity: —")
velocity.setStyleSheet(output_style)
velocity.setMinimumHeight(60)

current_velocity = QLabel("Current Velcoity at TA: —")
current_velocity.setStyleSheet(output_style)
current_velocity.setMinimumHeight(60)

apoapsis_radius = QLabel("Apoapsis Radius: —")
apoapsis_radius.setStyleSheet(output_style)
apoapsis_radius.setMinimumHeight(60)

periapsis_radius = QLabel("Periapsis Radius: —")
periapsis_radius.setStyleSheet(output_style)
periapsis_radius.setMinimumHeight(60)


output_layout.addWidget(orbital_period)
output_layout.addWidget(velocity)
output_layout.addWidget(current_velocity)
output_layout.addWidget(apoapsis_radius)
output_layout.addWidget(periapsis_radius)

output_layout.addStretch()


# ============================================================
# Calculations
# ============================================================

def calculate_orbit():

    try:
        sma = float(Sma.text())
        ecc = float(Ecc.text())
        

    except ValueError:
        QMessageBox.warning(
            window,
            "Input Error",
            "Please enter valid numerical values."
        )
        return


    # --------------------------------------------------------
    # Get μ
    # --------------------------------------------------------

    if mu.currentText() == "Custom":

        try:
            float_mu = float(cmu.text())

        except ValueError:
            QMessageBox.warning(
                window,
                "Input Error",
                "Please enter a valid custom μ."
            )
            return

    else:
        float_mu = MU_LIBRARY[mu.currentText()]


    # --------------------------------------------------------
    # Orbital Period
    # --------------------------------------------------------

    T = 2 * math.pi * math.sqrt(
        sma**3 / float_mu
    )


    # --------------------------------------------------------
    # Apoapsis / Periapsis
    # --------------------------------------------------------

    periapsis = sma * (1 - ecc)
    apoapsis = sma * (1 + ecc)

    # --------------------------------------------------------
    # velocity
    # --------------------------------------------------------
    velocity_value = math.sqrt(float_mu * (2/sma - 1/sma**2))
    currentvelocity = sma * (1 - ecc**2) / (1 + ecc * math.cos(math.radians(float(ta.text()))))
    # --------------------------------------------------------
    # Display Results
    # --------------------------------------------------------

    if T < 60:
        orbital_period.setText(
            f"Orbital Period: {T:.2f} s"
        )
    elif T < 3600:
        orbital_period.setText(
            f"Orbital Period: {T/60:.2f} min"
        )
    elif T < 86400:
        orbital_period.setText(
            f"Orbital Period: {T/3600:.2f} hr"
        )
    else:
        orbital_period.setText(
            f"Orbital Period: {T/86400:.2f} days"
        )

    apoapsis_radius.setText(
        f"Apoapsis Radius: {apoapsis:.2f} km"
    )

    periapsis_radius.setText(
        f"Periapsis Radius: {periapsis:.2f} km"
    )

    velocity.setText(
        f"Velocity: {velocity_value:.2f} km/s"
    )
    currentvelocity = QLabel( 
    f"Current Velocity: {currentvelocity:.2f} km/s"
    )
    

# ============================================================
# Signals
# ============================================================

calculate_button.clicked.connect(calculate_orbit)


# ============================================================
# Run
# ============================================================

window.show()

sys.exit(app.exec())