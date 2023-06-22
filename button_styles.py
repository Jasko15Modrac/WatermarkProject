BUTTON_BORDER_COLOR = "#C2DEDC"
BUTTON_BORDER_COLOR_2 = "#116A7B"
button_style_sheet = f"""
QPushButton  {{
    border: 2px solid {BUTTON_BORDER_COLOR};
    border-radius: 5px;
}}
QPushButton:pressed {{
border: 2px solid {BUTTON_BORDER_COLOR_2};
border-radius: 5px
}}
"""