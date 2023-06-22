from PIL import Image, ImageFont, ImageDraw
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QSlider, QLineEdit, QLabel, QComboBox, QMainWindow, QVBoxLayout, QWidget, \
    QPushButton, QGridLayout, QFileDialog
from PyQt5.QtGui import QIcon
from color_palette import colors
from font_families import available_fonts, fonts_dictionary
from button_styles import BUTTON_BORDER_COLOR, BUTTON_BORDER_COLOR_2, button_style_sheet


class TextWidget(QMainWindow):
    # This class variable helps to keep track of how many instances this clas has. For example, we don't want another
    # instance of the TextWidget class if one already exists
    instance_count = 0

    def __init__(self, original_img, main_window):
        super().__init__()

        # Here we change the instance_count variable as soon as the class is instantiated
        TextWidget.instance_count += 1

        # Connect the signal that comes from main_window whenever a new image is open
        main_window.image_changed.signal.connect(self.update_original_image)

        # Creating variable for image
        self.img = original_img

        # Creating the lists of tiles and buttons and clicks so that it's easier to work with them
        self.button_tiles = []
        self.clicks = []

        # Creating variable for main window
        self.main_window = main_window

        # Instantiating our method for creating GUI
        self.initUI()

        # Creating watermarked_image variable and setting it to None
        self.watermarked_image = None

# ------------------------------------------ SETTING UP GUI -----------------------------------------------------------

    # This is the method in which we will create GUI, widgets, labels, etc
    def initUI(self):

        # Set window title
        self.setWindowTitle("Properties")

        # Set window geometry
        self.setGeometry(600, 300, 300, 600)

        # Set layouts
        self.layout = QVBoxLayout()
        self.sliders_layout = QGridLayout()
        self.tiles_layout = QGridLayout()

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        # ADD WIDGETS

        # Input text
        self.input_txt_label = QLabel("Your Text")
        self.input_txt = QLineEdit()

        # Font
        self.font_label = QLabel("Font")
        self.font = QComboBox()

        # Color
        self.color_label = QLabel("Color")
        self.color = QComboBox()
        self.color_sample = QLabel()

        # Size
        self.size_label = QLabel("Size")
        self.size = QSlider()
        self.size_value = QLabel()

        # Opacity
        self.opacity_label = QLabel("Opacity")
        self.opacity = QSlider()
        self.opacity_value = QLabel()

        # Rotation
        self.rotation_label = QLabel("Rotation")
        self.rotation = QSlider()
        self.rotation_value = QLabel()

        # Button Tiles
        self.one_tile = QPushButton()
        self.button_tiles.append(self.one_tile)
        self.four_tiles = QPushButton()
        self.button_tiles.append(self.four_tiles)
        self.four_tiles_ver = QPushButton()
        self.button_tiles.append(self.four_tiles_ver)

        # Horizontal spacing
        self.spacing_x_label = QLabel("Spacing X-Axis")
        self.spacing_x = QSlider()
        self.spacing_x_value = QLabel()

        # Vertical spacing
        self.spacing_y_label = QLabel("Spacing Y-Axis")
        self.spacing_y = QSlider()
        self.spacing_y_value = QLabel()

        # Save and reset buttons
        self.reset_btn = QPushButton("Reset")
        self.save_btn = QPushButton("Save")

        # SET UP WIDGETS

        # Add colors to the color combobox
        for key, value in colors.items():
            self.color.addItem(key)

        # Add fonts to font combobox
        self.fonts_dic = fonts_dictionary(av_fonts=available_fonts)
        for key, value in self.fonts_dic.items():
            self.font.addItem(key)

        # Add starting text to input_txt
        self.input_txt.setText("Your Text")

        # Add values to opacity slider
        self.opacity.setRange(0, 255)
        self.opacity.setOrientation(Qt.Horizontal)
        self.opacity.setValue(255)

        # Add values to rotation slider
        self.rotation.setRange(0, 180)
        self.rotation.setOrientation(Qt.Horizontal)
        self.rotation.setValue(0)

        # Add values to spacing slider_x
        self.spacing_x.setRange(0, 50)
        self.spacing_x.setOrientation(Qt.Horizontal)
        self.spacing_x.setValue(10)
        self.spacing_x.setSingleStep(1)
        self.spacing_x.setPageStep(1)

        # Add values to spacing slider_y
        self.spacing_y.setRange(0, 50)
        self.spacing_y.setOrientation(Qt.Horizontal)
        self.spacing_y.setValue(10)
        self.spacing_y.setSingleStep(1)
        self.spacing_y.setPageStep(1)

        # Size slider
        self.size.setRange(1, 50)
        self.size.setOrientation(Qt.Horizontal)
        self.size.setValue(10)
        self.size.setSingleStep(1)
        self.size.setPageStep(1)

        # Set size of the buttons
        for button in self.button_tiles:
            button.setFixedSize(50, 50)

        # Set styles of tile buttons
        for button in self.button_tiles:
            button.setStyleSheet(button_style_sheet)

        # Create Icon objects with QIcon
        one_tile_icon = QIcon("Icons/one_tile_icon.png")
        four_tiles_icon = QIcon("Icons/four_tiles_icon.png")
        four_tiles_icon_ver2 = QIcon("Icons/four_tiles_2_icon.png")

        # Set size of the icons
        icon_size = QSize(46, 46)
        self.one_tile.setIconSize(icon_size)
        self.four_tiles.setIconSize(icon_size)
        self.four_tiles_ver.setIconSize(icon_size)

        # Add icons to the buttons
        self.one_tile.setIcon(one_tile_icon)
        self.four_tiles.setIcon(four_tiles_icon)
        self.four_tiles_ver.setIcon(four_tiles_icon_ver2)

        # POPULATE LAYOUTS

        # Add tiles to tiles_layout
        self.tiles_layout.addWidget(self.one_tile, 1, 2)
        self.tiles_layout.addWidget(self.four_tiles, 1, 3)
        self.tiles_layout.addWidget(self.four_tiles_ver, 1, 4)
        self.tiles_layout.addWidget(self.spacing_x_label, 2, 1)
        self.tiles_layout.addWidget(self.spacing_x, 3, 1, 1, 4)
        self.tiles_layout.addWidget(self.spacing_x_value, 3, 5)
        self.tiles_layout.addWidget(self.spacing_y_label, 4, 1)
        self.tiles_layout.addWidget(self.spacing_y, 5, 1, 1, 4)
        self.tiles_layout.addWidget(self.spacing_y_value, 6, 5)

        # Add sliders to sliders grid layout
        self.sliders_layout.addWidget(self.size_label, 0, 1)
        self.sliders_layout.addWidget(self.size, 1, 1)
        self.sliders_layout.addWidget(self.size_value, 1, 2)
        self.sliders_layout.addWidget(self.opacity_label, 2, 1)
        self.sliders_layout.addWidget(self.opacity, 3, 1)
        self.sliders_layout.addWidget(self.opacity_value, 3, 2)
        self.sliders_layout.addWidget(self.rotation_label, 4, 1)
        self.sliders_layout.addWidget(self.rotation, 5, 1)
        self.sliders_layout.addWidget(self.rotation_value, 5, 2)

        # Add widgets to layout
        self.layout.addWidget(self.input_txt_label)
        self.layout.addWidget(self.input_txt)
        self.layout.addWidget(self.font_label)
        self.layout.addWidget(self.font)
        self.layout.addWidget(self.color_label)
        self.layout.addWidget(self.color)
        self.layout.addLayout(self.sliders_layout) # This is where we add sliders_layout to QVBoxLayout
        self.layout.addLayout(self.tiles_layout) # This is where we add tiles_layout to QVBoxLayout
        self.layout.addWidget(self.reset_btn)
        self.layout.addWidget(self.save_btn)

        # Set margins between widgets
        self.layout.setAlignment(Qt.AlignTop)

        # CONNECT BUTTONS, SLIDERS AND FUNCTIONALITIES

        # Display current values for opacity, rotation and spacing sliders
        self.opacity.valueChanged.connect(self.display_opacity_value)
        self.rotation.valueChanged.connect(self.display_rotation_value)
        self.spacing_x.valueChanged.connect(self.display_spacing_value_x)
        self.spacing_y.valueChanged.connect(self.display_spacing_value_y)
        self.size.valueChanged.connect(self.display_size_value)

        # These connections determine which tile button was clicked
        self.one_tile.clicked.connect(lambda: self.numb_tiles(self.one_tile))
        self.four_tiles.clicked.connect(lambda: self.numb_tiles(self.four_tiles))
        self.four_tiles_ver.clicked.connect(lambda: self.numb_tiles(self.four_tiles_ver))

        # Changing the styles of the tile buttons when clicked
        self.one_tile.clicked.connect(lambda: self.handle_button_click(self.one_tile))
        self.four_tiles.clicked.connect(lambda: self.handle_button_click(self.four_tiles))
        self.four_tiles_ver.clicked.connect(lambda: self.handle_button_click(self.four_tiles_ver))

        # Update image upon click
        self.one_tile.clicked.connect(self.update_image)
        self.four_tiles.clicked.connect(self.update_image)
        self.four_tiles_ver.clicked.connect(self.update_image)

        # Update image upon value change
        self.input_txt.textChanged.connect(self.update_image)
        self.opacity.valueChanged.connect(self.update_image)
        self.rotation.valueChanged.connect(self.update_image)
        self.spacing_x.valueChanged.connect(self.update_image)
        self.spacing_y.valueChanged.connect(self.update_image)
        self.size.valueChanged.connect(self.update_image)
        self.font.currentIndexChanged.connect(self.update_image)
        self.color.currentIndexChanged.connect(self.update_image)

        # Connect save and reset buttons with their functionalities
        self.reset_btn.clicked.connect(self.reset)
        self.save_btn.clicked.connect(self.save_image)

        # This is to set first button tile as clicked when starting program
        self.one_tile.click()

# ---------------------------------------- CREATING METHODS ---------------------------------------------------------- #

    def numb_tiles(self, tile_button):
        """This method updates the clicks list based on the argument tile_button it receives"""
        if tile_button == self.one_tile:
            self.clicks.clear()
            self.clicks.append(1)
        elif tile_button == self.four_tiles:
            self.clicks.clear()
            self.clicks.append(4)
        elif tile_button == self.four_tiles_ver:
            self.clicks.clear()
            self.clicks.append(5)

    def handle_button_click(self, button):
        """This method changes the color of the button that is clicked and resets the styles of all other buttons
         to default"""
        button.setStyleSheet(f"""
                QPushButton {{
                    border: 2px solid {BUTTON_BORDER_COLOR_2};
                    border-radius: 5px;
                }}
                """)
        for btn in self.button_tiles:
            if btn != button:
                btn.setStyleSheet(f"""
                QPushButton {{
                    border: 2px solid {BUTTON_BORDER_COLOR};
                    border-radius: 5px;
                }}
                """)

    def display_opacity_value(self):
        """This method displays current opacity value in the label next to opacity slider"""
        # Since opacity value is from 0 to 255, and we want our opacity slider value to be displayed from 0 to 100,
        # we divide current values with 2.55 and round them since it has to be integer value
        opacity_value = round(self.opacity.value() / 2.55, 1)
        self.opacity_value.setText(str(opacity_value) + "%")

    def display_rotation_value(self):
        """This method displays current rotation value in the label next to rotation slider"""
        rotation_value = self.rotation.value()
        self.rotation_value.setText(str(rotation_value) + "°")

    def display_spacing_value_x(self):
        """This method displays current spacing value x in the label next to spacing slider"""
        spacing_value = self.spacing_x.value() / 10
        self.spacing_x_value.setText(str(spacing_value) + "x")

    def display_spacing_value_y(self):
        """This method displays current spacing value y in the label next to spacing slider"""
        spacing_value = self.spacing_y.value() / 10
        self.spacing_y_value.setText(str(spacing_value) + "x")

    def display_size_value(self):
        """This method displays current size value y in the label next to spacing slider"""
        size_value = self.size.value() / 10
        self.size_value.setText(str(size_value) + "x")

    def filter_coeficient(self, coeficient_x, coeficient_y, txt_mask_width, txt_mask_height):
        """ This method takes four arguments: coeficient_x (spacing_x slider value), coeficient_y
        (spacing_y slider value), txt_mask_width and txt_mask_height. It then determines the space between text on x
        and y-axis and returns those two values"""
        if coeficient_x == 0:
            word_gap_x = txt_mask_width
        else:
            word_gap_x = txt_mask_width + round(txt_mask_width * coeficient_x / 10)
        if coeficient_y == 0:
            word_gap_y = txt_mask_height
        else:
            word_gap_y = txt_mask_height + round(txt_mask_height * coeficient_y / 10)
        return word_gap_x, word_gap_y

    def calculate_numb_text_repetitions(self, word_space_x, word_space_y, canvas_width, canvas_height, mask_width,
                                        mask_height):
        """This method takes six arguments: word_space_x (space between text x-axis),
         word_space_y (space between text y-axis),  canvas_width (width of image), canvas_height (height of image)
         mask_width (width of text) mask_height (height of text). It then calculates how many times should the text
         be repeated across the image on x and y-axis and returns those two values"""

        if word_space_x != 0:
            number_of_horizontal_repetitions = round(canvas_width / word_space_x)
        else:
            number_of_horizontal_repetitions = round(canvas_width / mask_width)
        if word_space_y != 0:
            number_of_vertical_repetitions = round(canvas_height / word_space_y)
        else:
            number_of_vertical_repetitions = round(canvas_height / mask_height)

        return number_of_horizontal_repetitions, number_of_vertical_repetitions

    def text_patterns(self, numb_tiles, canv_overlay, rot_txt_mask, horizontal_rep, vertical_rep, word_gap_x,
                      word_gap_y):
        """ This method takes seven arguments: numb-tiles (which tile the user clicked),
        canv_overlay (overlay image on which we will place our text), rot_txt_mask (rotated text),
        horizontal_rep (numb of times text should be repeated across x-axis),
        vertical_rep (numb of times text should be repeated across y-axis), word_gap_x (space between text x-axis),
        word_gap_y (space between text y-axis)"""

        # These are x and y-axis starting points of text for checker and romb patterns
        starting_point_x = 0
        starting_point_y = 0

        # If user wants only one text displayed on image
        if numb_tiles == 1:
            # Calculate the center position of the rotated_text_mask on overlay
            center_x = round((canv_overlay.width / 2)) - round((rot_txt_mask.width / 2))
            center_y = round((canv_overlay.height / 2)) - round((rot_txt_mask.height / 2))
            # Paste rotated_text_mask to overlay
            canv_overlay.paste(rot_txt_mask, (center_x, center_y), mask=rot_txt_mask)
        # If user wants checker pattern text displayed on image
        elif numb_tiles == 4:
            # Initial values of spacing between text. This will be incremented by a value of word_gap
            spacing_x = 0
            spacing_y = 0
            for v_numb in range(vertical_rep + 1):
                for numb in range(horizontal_rep + 1):
                    canv_overlay.paste(rot_txt_mask, (starting_point_x + spacing_x, starting_point_y + spacing_y),
                                       mask=rot_txt_mask)
                    spacing_x += word_gap_x
                # Increase the y value so that we display the same on the new y column
                spacing_y += word_gap_y
                # Reset the value of x for new y column
                spacing_x = 0
        # If user wants romb pattern text displayed on image
        elif numb_tiles == 5:
            # Initial values of spacing between text. This will be incremented by a value of word_gap
            spacing_x = 0
            spacing_y = 0
            # This line sets the starting horizontal displacement. If True it shifts the horizontal position
            # of the first text and consequentially of each following text by determined value
            displacement = False
            # This determines the starting horizontal point of the text when displacement = True
            displacement_starting_point = starting_point_x + (round(word_gap_x / 2))

            for v_numb in range(vertical_rep + 1):
                # We want first line to always be shifted thus displacement = not displacement. By setting it this way
                # the displacement value will change form after each iteration making one line of text shifted and
                # other 'normal', thus creating the romb-like pattern
                displacement = not displacement
                for numb in range(horizontal_rep + 1):
                    if displacement:
                        canv_overlay.paste(rot_txt_mask,
                                           (displacement_starting_point + spacing_x, starting_point_y +
                                            spacing_y), mask=rot_txt_mask)
                    else:
                        canv_overlay.paste(rot_txt_mask,
                                           (starting_point_x + spacing_x, starting_point_y + spacing_y),
                                           mask=rot_txt_mask)
                    spacing_x += word_gap_x
                spacing_y += word_gap_y
                spacing_x = 0

    def update_original_image(self, file_path):
        """This method is called when the clas receives image_changed.signal, takes file_path of that signal as an
        argument and updates the self.img variable """
        self.img = file_path

    # Here we override the class closeEvent in order to reset the instance_count variable
    def closeEvent(self, event):
        TextWidget.instance_count = 0

    def update_image(self):
        """Updates the image and sends it to main_window to be displayed."""
        edited_image = self.add_text_to_img()
        self.main_window.update_image(edited_image)

    def save_image(self):
        """Displays the save dialog for user to save image. If user doesn't provide image format during the save
        it will assign it .jpg format"""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_filter = "JPEG Files (*.jpg);;PNG Files (*.png)"
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", filter=file_filter,
                                                   options=options)

        if file_name:
            extension = "jpg"
            if not file_name.endswith(extension):
                file_name += "." + extension
            rgb_img = self.watermarked_image.convert("RGB")
            rgb_img.save(file_name, "JPEG" if file_name.endswith('.jpg') else "PNG")

    def reset(self):
        """Resets all sliders and buttons to default state. Clears the current text_image and updates the image to the
        default text image"""

        # Set sliders and buttons states to default
        self.input_txt.setText("Your Text")
        self.color.setCurrentIndex(0)
        self.font.setCurrentIndex(0)
        self.opacity.setValue(255)
        self.size.setValue(10)
        self.rotation.setValue(0)
        self.spacing_x.setValue(10)
        self.spacing_y.setValue(10)
        self.one_tile.click()

# --------------------------------------- CREATING MAIN METHOD --------------------------------------------------------
    def add_text_to_img(self):
        """This is the main method that encompasses all other methods in this class"""

        # Collect data from user's input
        font = self.fonts_dic[self.font.currentText()]
        text_to_write = self.input_txt.text()
        color = colors[self.color.currentText()]
        size_coef = self.size.value() / 10
        default_size = 70
        size = round(default_size * size_coef)
        opacity = int(self.opacity.value())
        rotation = int(self.rotation.value())
        spacing_coeficient_x = float(self.spacing_x.value())
        spacing_coeficient_y = float(self.spacing_y.value())

        # Create font object
        font = ImageFont.truetype(font, size)

        # Get width and length of text
        txt_img = Image.new("RGB", (1, 1))
        txt_draw = ImageDraw.Draw(txt_img)
        text_bbox = txt_draw.textbbox((0, 0), text=text_to_write, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Open the image that we want to watermark and convert it to RGBA so that we can change text transparency
        opened_image = Image.open(self.img).convert("RGBA")

        # Create an overlay image for text transparency
        overlay = Image.new("RGBA", (opened_image.width, opened_image.height), (255, 255, 255, 0))

        # Draw the overlay image
        draw = ImageDraw.Draw(overlay)

        # Create text mask
        text_mask = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))
        text_mask_draw = ImageDraw.Draw(text_mask)
        text_mask_draw.text((0, 0), text=text_to_write, fill=(int(color[0]), int(color[1]),
                                                              int(color[2]), opacity), font=font, anchor='lt')
        rotated_text_mask = text_mask.rotate(rotation, expand=True)

        # Get user's choice for text pattern
        tile_sig = self.clicks[0]

        # Determine the area in which the checker and romb pattern text will be written.We leave 50px free on all sides
        target_width = opened_image.width - 50
        target_height = opened_image.height - 50

        # Determine the width of the text mask. We take this value as the length of the text when we calculate number of
        # text repetitions
        rotated_text_mask_width = text_mask.width
        rotated_text_mask_height = text_mask.height

        # Determine the value of gap between text in checker and romb pattern
        word_spacing_x_axis, word_spacing_y_axis = self.filter_coeficient(spacing_coeficient_x, spacing_coeficient_y,
                                                                          rotated_text_mask_width,
                                                                          rotated_text_mask_height)

        # Determine how many times the text will be written over the image both vertically and horizontally
        horizontal_repetitions, vertical_repetitions = self.calculate_numb_text_repetitions(word_spacing_x_axis,
                                                                                            word_spacing_y_axis,
                                                                                            target_width,
                                                                                            target_height,
                                                                                            rotated_text_mask_width,
                                                                                            rotated_text_mask_height)

        # Determine in which pattern the text will be displayed on the image
        self.text_patterns(tile_sig, overlay, rotated_text_mask, horizontal_repetitions, vertical_repetitions,
                           word_spacing_x_axis, word_spacing_y_axis)

        # Combine overlay and opened_image using alpha_composite
        self.watermarked_image = Image.alpha_composite(opened_image, overlay)

        return self.watermarked_image
