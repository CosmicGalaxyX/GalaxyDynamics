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
window.setWindowTitle("Cartesian Orbit Calculator v0.1")
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


x = QLineEdit()
x.setPlaceholderText("x Position (km)")
x.setFixedHeight(65)
x.setStyleSheet(input_style)

input_layout.addWidget(x)


y = QLineEdit()
y.setPlaceholderText("y Position (km)")
y.setFixedHeight(65)
y.setStyleSheet(input_style)

input_layout.addWidget(y)


z = QLineEdit()
z.setPlaceholderText("z Position (km)")
z.setFixedHeight(65)
z.setStyleSheet(input_style)

input_layout.addWidget(z)


Vx = QLineEdit()
Vx.setPlaceholderText("X Velocity (km/s)")
Vx.setFixedHeight(65)
Vx.setStyleSheet(input_style)

input_layout.addWidget(Vx)


Vy = QLineEdit()
Vy.setPlaceholderText("Y Velocity (km/s)")
Vy.setFixedHeight(65)
Vy.setStyleSheet(input_style)

input_layout.addWidget(Vy)


Vz = QLineEdit()
Vz.setPlaceholderText("Z Velocity (km/s)")
Vz.setFixedHeight(65)
Vz.setStyleSheet(input_style)

input_layout.addWidget(Vz)


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

apoapsis_radius = QLabel("Apoapsis Radius: —")
apoapsis_radius.setStyleSheet(output_style)
apoapsis_radius.setMinimumHeight(60)

periapsis_radius = QLabel("Periapsis Radius: —")
periapsis_radius.setStyleSheet(output_style)
periapsis_radius.setMinimumHeight(60)

Inclination = QLabel("Inclination: —")
Inclination.setStyleSheet(output_style)
Inclination.setMinimumHeight(60)

Eccentricity = QLabel("Eccentricity: —")
Eccentricity.setStyleSheet(output_style)
Eccentricity.setMinimumHeight(60)

RAAN = QLabel("RAAN: —")
RAAN.setStyleSheet(output_style)
RAAN.setMinimumHeight(60)


output_layout.addWidget(orbital_period)
output_layout.addWidget(velocity)
output_layout.addWidget(apoapsis_radius)
output_layout.addWidget(periapsis_radius)
output_layout.addWidget(Inclination)
output_layout.addWidget(Eccentricity)
output_layout.addWidget(RAAN)

output_layout.addStretch()


# ============================================================
# Calculations
# ============================================================

def calculate_orbit():

    # --------------------------------------------------------
    # Get Cartesian State Vector
    # --------------------------------------------------------

    try:
        float_x = float(x.text())
        float_y = float(y.text())
        float_z = float(z.text())

        float_Vx = float(Vx.text())
        float_Vy = float(Vy.text())
        float_Vz = float(Vz.text())

    except ValueError:
        QMessageBox.warning(
            window,
            "Input Error",
            "Please enter valid numerical values for position and velocity."
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
    # Validate μ
    # --------------------------------------------------------

    if float_mu <= 0:

        QMessageBox.warning(
            window,
            "Input Error",
            "μ must be greater than zero."
        )

        return


    # --------------------------------------------------------
    # Create State Vectors
    # --------------------------------------------------------

    r_forward = np.array([
        float_x,
        float_y,
        float_z
    ])

    v_forward = np.array([
        float_Vx,
        float_Vy,
        float_Vz
    ])


    # --------------------------------------------------------
    # Basic Calculations
    # --------------------------------------------------------

    r = np.linalg.norm(r_forward)
    v = np.linalg.norm(v_forward)


    if r == 0:

        QMessageBox.warning(
            window,
            "Invalid State",
            "Position cannot be zero."
        )

        return


    # Specific orbital energy

    epsilon = (v ** 2 / 2) - (float_mu / r)


    # Specific angular momentum vector

    h = np.cross(r_forward, v_forward)
    h_mag = np.linalg.norm(h)


    if h_mag == 0:

        QMessageBox.warning(
            window,
            "Invalid State",
            "The position and velocity vectors cannot produce zero angular momentum."
        )

        return


    # --------------------------------------------------------
    # Semi-major Axis
    # --------------------------------------------------------

    if abs(epsilon) > 1e-12:

        sma = -float_mu / (2 * epsilon)

    else:

        sma = math.inf


    # --------------------------------------------------------
    # Eccentricity Vector
    # --------------------------------------------------------

    eccentricity_vector = (
        np.cross(v_forward, h) / float_mu
    ) - (
        r_forward / r
    )

    eccentricity = np.linalg.norm(eccentricity_vector)


    # --------------------------------------------------------
    # Inclination
    # --------------------------------------------------------

    inclination = math.degrees(
        math.acos(
            np.clip(h[2] / h_mag, -1.0, 1.0)
        )
    )


    # --------------------------------------------------------
    # Node Vector
    # --------------------------------------------------------

    k = np.array([0.0, 0.0, 1.0])

    node_vector = np.cross(k, h)
    node_mag = np.linalg.norm(node_vector)


    # --------------------------------------------------------
    # RAAN
    # --------------------------------------------------------

    if node_mag > 1e-12:

        raan = math.degrees(
            math.atan2(
                node_vector[1],
                node_vector[0]
            )
        )

        if raan < 0:
            raan += 360

    else:

        raan = 0.0


    # --------------------------------------------------------
    # Orbital Type
    # --------------------------------------------------------

    if eccentricity < 1e-8:

        orbit_type = "Circular"

    elif eccentricity < 1:

        orbit_type = "Elliptical"

    elif abs(eccentricity - 1) < 1e-8:

        orbit_type = "Parabolic"

    else:

        orbit_type = "Hyperbolic"


    # --------------------------------------------------------
    # Periapsis / Apoapsis
    # --------------------------------------------------------

    if orbit_type == "Circular":

        periapsis = sma
        apoapsis = sma

        orbital_period_value = (
            2
            * math.pi
            * math.sqrt(sma ** 3 / float_mu)
        )

    elif orbit_type == "Elliptical":

        periapsis = sma * (1 - eccentricity)

        apoapsis = sma * (1 + eccentricity)

        orbital_period_value = (
            2
            * math.pi
            * math.sqrt(sma ** 3 / float_mu)
        )

    elif orbit_type == "Hyperbolic":

        # For a hyperbolic orbit, sma is negative.
        # Periapsis is still positive.

        periapsis = sma * (1 - eccentricity)

        apoapsis = None

        orbital_period_value = None

    else:

        # Parabolic orbit

        periapsis = (
            h_mag ** 2 / (2 * float_mu)
        )

        apoapsis = None

        orbital_period_value = None


    # --------------------------------------------------------
    # Output
    # --------------------------------------------------------

    velocity.setText(
        f"Velocity: {v:.2f} km/s"
    )

    Inclination.setText(
        f"Inclination: {inclination:.2f}°"
    )

    Eccentricity.setText(
        f"Eccentricity: {eccentricity:.6f}"
    )

    RAAN.setText(
        f"RAAN: {raan:.2f}°"
    )


    if orbital_period_value is not None:

        if orbital_period_value < 60:

            orbital_period.setText(
                f"Orbital Period: {orbital_period_value:.2f} s"
            )

        elif orbital_period_value < 3600:

            orbital_period.setText(
                f"Orbital Period: {orbital_period_value/60:.2f} min"
            )

        elif orbital_period_value < 86400:

            orbital_period.setText(
                f"Orbital Period: {orbital_period_value/3600:.2f} hr"
            )

        else:

            orbital_period.setText(
                f"Orbital Period: {orbital_period_value/86400:.2f} days"
            )

    else:

        orbital_period.setText(
            "Orbital Period: N/A"
        )


    periapsis_radius.setText(
        f"Periapsis Radius: {periapsis:.2f} km"
    )


    if apoapsis is not None:

        apoapsis_radius.setText(
            f"Apoapsis Radius: {apoapsis:.2f} km"
        )

    else:

        apoapsis_radius.setText(
            "Apoapsis Radius: N/A"
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