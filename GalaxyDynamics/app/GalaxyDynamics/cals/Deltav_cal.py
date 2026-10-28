import math 
import sys as sys

# Fuctions

isp = 0
g0 = 0
m0 = 0
m1 = 0

def calculate_DeltaV(isp, g0, m0, m1):
    deltav = isp * g0 * math.log(m0/m1)
    print(f"Delta V: {deltav/1000:.3f} km/s")
    return deltav



# Input fuctions
Inputs = [
    {
        "id": "isp",
        "label": "Specific impulse",
        "unit": "s",
        "type": "Editable",
    },

    {
        "id": "g0",
        "label": "Gravity (mu)",
        "unit": "m3/s2",
        "type": "Editable",
    },

    {
        "id": "m0",
        "label": "Inital Mass (kg)",
        "unit": "kg",
        "type": "Editable",
    },

    {
        "id": "m1",
        "label": "Final Mass (kg)",
        "unit": "kg",
        "type": "Editable",
    }
]

# output fuctions

# Cal runner
