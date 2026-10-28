#Imports:

#Astropy
import astropy.units as u
from astropy.constants import G, M_sun, R_sun, M_earth, R_earth, M_jup, R_jup
import astropy.constants as const
import astropy.coordinates as coord
from astropy.coordinates import get_body, solar_system_ephemeris, SkyCoord, EarthLocation

#UI
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
    QHBoxLayout,
    QToolButton,
    QMenu,
    QComboBox,
)
from PySide6.QtGui import QIcon

#Math
import math
import sys

#Asset Imports
BASE_DIR = "app/GalaxyDynamics/assets"
ICON_PATH = f"{BASE_DIR}/icon.png"

#Design
BG_COLOR       = "#070711"   # almost-black deep blue
SURFACE_COLOR  = "#0B0B1B"   # dark space blue
CARD_COLOR     = "#101023"   # blue-indigo
HOVER_COLOR    = "#17162F"   # stronger deep blue
BORDER_COLOR   = "#24213F"   # indigo-blue
ACCENT_BLUE    = "#4779D6"   # deep electric blue
ACCENT_INDIGO  = "#44417D"   # dark indigo
ACCENT_PURPLE  = "#6A568C"   # deep purple
TEXT_COLOR     = "#E3E2F0"   # cool blue-white
SECONDARY_TEXT = "#9998B4"   # muted blue-gray

HeaderFont = "Space Grotesk"
SubHeaderFont = "Inter"
TechNumFont = "JetBrains Mono"


#--------------------------------------------------

class GD_Main:
    def __init__(self):

        # --------------------------------------------------
        # MAIN WINDOW
        # --------------------------------------------------

        self.window = QWidget()
        self.window.showMaximized()
        self.window.setWindowIcon(QIcon(ICON_PATH))

        self.window.setStyleSheet(
            f"""
            QWidget {{
                background-color: {BG_COLOR};
                color: {TEXT_COLOR};
            }}
            """
        )
        # --------------------------------------------------
        # WINDOW
        # --------------------------------------------------

        self.window.setWindowTitle("Galaxy Dynamics")

        # --------------------------------------------------
        # INTERFACE LAYOUT
        # --------------------------------------------------
        MainLayout = QHBoxLayout(self.window)

        LeftPanel = QFrame()
        MainPanel = QFrame()
        RightPanel = QFrame()
        LeftLayout = QVBoxLayout(LeftPanel)


        RightPanel.setStyleSheet(
            f"""
            QFrame {{
                background-color: {SURFACE_COLOR};
                color: {TEXT_COLOR};
            }}
            """
        )

        LeftPanel.setStyleSheet(
                    f"""
                    QFrame {{
                        background-color: {SURFACE_COLOR};
                        color: {TEXT_COLOR};
                    }}
                    """
                )

        MainPanel.setStyleSheet(
            f"""
            QFrame {{
                background-color: {BG_COLOR};
                color: {TEXT_COLOR};
            }}
            """
        )

        MainLayout.addWidget(LeftPanel, 1)
        MainLayout.addWidget(MainPanel, 2)
        MainLayout.addWidget(RightPanel, 1.5)

        # --------------------------------------------------
        # Left Panel Layout
        # --------------------------------------------------
       
        TitleLabel = QLabel("Galaxy Dynamics")
        TitleLabel.setStyleSheet(
            f"""
            QLabel {{
                font-family: {HeaderFont};
                font-size: 32px;
                font-weight: bold;
                color: {ACCENT_BLUE};
            }}
            """
        )
        TitleLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        LeftLayout.setContentsMargins(0, 0, 0, 0)
        LeftLayout.setSpacing(0)

        LeftLayout.addWidget(TitleLabel)

        # Cals
        caldropdown = QComboBox()
        caldropdown.addItem("Deltav Calculator")

        caldropdown.setStyleSheet(
            f"""
            QComboBox {{
                font-family: {SubHeaderFont};
                font-size: 20px;
                font-weight: bold;
                color: {ACCENT_INDIGO};
            }}

            QComboBox QAbstractItemView {{
                background-color: {SURFACE_COLOR};
                color: {TEXT_COLOR};
                selection-background-color: {ACCENT_BLUE};
                outline: none;
            }}
            """
        )

        LeftLayout.addWidget(
            caldropdown,
            alignment=Qt.AlignmentFlag.AlignHCenter
        )



#--------------------------------------------------


# --------------------------------------------------
# END OF FILE
# --------------------------------------------------
app = QApplication(sys.argv)
window = GD_Main()
window.window.show()

sys.exit(app.exec())
