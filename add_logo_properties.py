from PIL import Image
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QSlider, QLabel, QMainWindow, QWidget, \
    QPushButton, QGridLayout, QMessageBox, QSizePolicy, QFileDialog
from PyQt5.QtGui import QIcon
from button_styles import BUTTON_BORDER_COLOR, BUTTON_BORDER_COLOR_2, button_style_sheet


class LogoWidget(QMainWindow):
    # Set class variable to keep track of the number of instances. So that user cant create another instance of this
    # class if another one is already in existence
    instance_count = 0

    def __init__(self, original_img, main_window):
        super().__init__()
        # Update class variable upon initialization
        LogoWidget.instance_count += 1
        # Connect the signal that comes from main_window whenever a new image is open
        main_window.image_changed.signal.connect(self.update_original_image)
        # Create lists of buttons, sliders, and clicks for easier management
        self.button_tiles = []
        self.clicks = []
        self.sliders = []
        # Set the path for the original_img
        self.original_img = original_img
        # Make a 'copy' of the path. Since the original_image will change we need this copy when we reset
        self.clear_pic = original_img
        # Set logo_img to None
        self.logo_img = None
        # Set watermarked_img to None
        self.watermarked_img = None
        # Set the main_window. We need this in order to update and display our image in main_window QLabel preview
        self.main_window = main_window
        # Set the self.warning_displayed to False. this is needed since the pyqt5 loops over and over and would show
        # QMessageBox multiple times if we don't restrict it like this
        self.warning_displayed = False

        # Initialize method for creating GUI
        self.initUI()

    def update_original_image(self, file_path):
        self.original_img = file_path

    def closeEvent(self, event):
        """Here I override closeEvent in order to update instance_count when the close event happens"""
        LogoWidget.instance_count = 0

    def initUI(self):
        """Method responsible for creating program's GUI"""
        # Set window title
        self.setWindowTitle("Properties")

        # Set window geometry
        self.setGeometry(600, 300, 400, 400)

        # Set layouts
        self.layout = QGridLayout()
        self.tiles_and_spacing_layout = QGridLayout()
        self.top_buttons_layout = QGridLayout()
        self.buttons_layout = QGridLayout()

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        # CREATE WIDGETS

        # Add logo image button
        self.add_logo_image = QPushButton("Add Logo Image")

        # Size
        self.size_label = QLabel("Size")
        self.size_value = QLabel()
        self.size = QSlider()
        self.sliders.append(self.size)

        # Tile buttons
        self.tile_label = QLabel("Tile")
        self.tile_one = QPushButton()
        self.button_tiles.append(self.tile_one)
        self.tile_four = QPushButton()
        self.button_tiles.append(self.tile_four)
        self.tile_four_ver = QPushButton()
        self.button_tiles.append(self.tile_four_ver)

        # Spacing x and y
        self.spacing_x_label = QLabel("Spacing X-Axis")
        self.spacing_x = QSlider()
        self.sliders.append(self.spacing_x)
        self.spacing_y_label = QLabel("Spacing Y-Axis")
        self.spacing_y = QSlider()
        self.sliders.append(self.spacing_y)
        self.spacing_x_value = QLabel()
        self.spacing_y_value = QLabel()

        # Opacity
        self.opacity_label = QLabel("Opacity")
        self.opacity = QSlider()
        self.sliders.append(self.opacity)
        self.opacity_value = QLabel()

        # Rotation
        self.rotation_label = QLabel("Rotation")
        self.rotation = QSlider()
        self.sliders.append(self.rotation)
        self.rotation_value = QLabel()

        # Reset and save buttons
        self.reset_btn = QPushButton("Reset")
        self.save_image_btn = QPushButton("Save Image")
        self.save_image_btn.setEnabled(False)

        # Create spacers
        self.spacer_widget_1 = QWidget()
        self.spacer_widget_1.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.spacer_widget_2 = QWidget()
        self.spacer_widget_2.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)

        # SLIDERS SETTINGS

        # Opacity slider
        self.opacity.setRange(0, 255)
        self.opacity.setOrientation(Qt.Horizontal)
        self.opacity.setValue(255)
        self.opacity.setEnabled(False)
        self.opacity.setStyleSheet("QSlider::handle:horizontal { background: #DDDDDD; }")

        # Rotation slider
        self.rotation.setRange(0, 180)
        self.rotation.setOrientation(Qt.Horizontal)
        self.rotation.setValue(0)
        self.rotation.setEnabled(False)
        self.rotation.setStyleSheet("QSlider::handle:horizontal { background: #DDDDDD; }")

        # Spacing slider_x
        self.spacing_x.setRange(0, 50)
        self.spacing_x.setOrientation(Qt.Horizontal)
        self.spacing_x.setValue(10)
        self.spacing_x.setSingleStep(1)
        self.spacing_x.setPageStep(1)
        self.spacing_x.setEnabled(False)
        self.spacing_x.setStyleSheet("QSlider::handle:horizontal { background: #DDDDDD; }")

        # Spacing slider_y
        self.spacing_y.setRange(0, 50)
        self.spacing_y.setOrientation(Qt.Horizontal)
        self.spacing_y.setValue(10)
        self.spacing_y.setSingleStep(1)
        self.spacing_y.setPageStep(1)
        self.spacing_y.setEnabled(False)
        self.spacing_y.setStyleSheet("QSlider::handle:horizontal { background: #DDDDDD; }")

        # Size slider
        self.size.setRange(1, 50)
        self.size.setOrientation(Qt.Horizontal)
        self.size.setValue(10)
        self.size.setSingleStep(1)
        self.size.setPageStep(1)
        self.size.setEnabled(False)
        self.size.setStyleSheet("QSlider::handle:horizontal { background: #DDDDDD; }")

        # TILE BUTTONS SETUP, SETTINGS AND LAYOUT

        # Create Icon objects with QIcon
        one_tile_icon = QIcon("Icons/one_tile_icon.png")
        four_tiles_icon = QIcon("Icons/four_tiles_icon.png")
        four_tiles_icon_ver2 = QIcon("Icons/four_tiles_2_icon.png")

        # Set size of the icons
        icon_size = QSize(36, 36)

        # Setting size and styles of button tiles and size of icons
        for button in self.button_tiles:
            button.setFixedSize(40, 40)
            button.setStyleSheet(button_style_sheet)
            button.setIconSize(icon_size)

        # Add icons to the buttons
        self.tile_one.setIcon(one_tile_icon)
        self.tile_four.setIcon(four_tiles_icon)
        self.tile_four_ver.setIcon(four_tiles_icon_ver2)

        # Add tile buttons and spacing sliders to tiles and spacing layout
        self.tiles_and_spacing_layout.addWidget(self.tile_label, 1, 1)
        self.tiles_and_spacing_layout.addWidget(self.tile_one, 1, 2)
        self.tiles_and_spacing_layout.addWidget(self.tile_four, 1, 3)
        self.tiles_and_spacing_layout.addWidget(self.tile_four_ver, 1, 4)
        self.tiles_and_spacing_layout.addWidget(self.spacing_x_label, 2, 1)
        self.tiles_and_spacing_layout.addWidget(self.spacing_x, 2, 2, 1, 3)
        self.tiles_and_spacing_layout.addWidget(self.spacing_x_value, 2, 5)
        self.tiles_and_spacing_layout.addWidget(self.spacing_y_label, 3, 1)
        self.tiles_and_spacing_layout.addWidget(self.spacing_y, 3, 2, 1, 3)
        self.tiles_and_spacing_layout.addWidget(self.spacing_y_value, 3, 5)

        # Set the horizontal and vertical spacing between widgets in tiles_and_spacing_layout
        self.tiles_and_spacing_layout.setVerticalSpacing(15)
        self.tiles_and_spacing_layout.setHorizontalSpacing(15)

        # BUTTONS LAYOUT

        # Add logo image and remove bg buttons to top_buttons_layout
        self.top_buttons_layout.addWidget(self.add_logo_image, 1, 1, 1, 5)

        # Add preview, save and reset button to buttons layout
        self.buttons_layout.addWidget(self.reset_btn, 1, 1, 1, 5)
        self.buttons_layout.addWidget(self.save_image_btn, 2, 1, 1, 5)

        self.buttons_layout.setVerticalSpacing(10)

        # ADD WIDGETS TO MAIN LAYOUT
        self.layout.addLayout(self.top_buttons_layout, 1, 1, 1, 5)
        self.layout.addWidget(self.size_label, 2, 1)
        self.layout.addWidget(self.size, 2, 2, 1, 3)
        self.layout.addWidget(self.size_value, 2, 5)
        self.layout.addLayout(self.tiles_and_spacing_layout, 3, 1, 1, 5)
        self.layout.addWidget(self.opacity_label, 4, 1)
        self.layout.addWidget(self.opacity, 4, 2, 1, 3)
        self.layout.addWidget(self.opacity_value, 4, 5)
        self.layout.addWidget(self.rotation_label, 5, 1)
        self.layout.addWidget(self.rotation, 5, 2, 1, 3)
        self.layout.addWidget(self.rotation_value, 5, 5)
        self.layout.addLayout(self.buttons_layout, 6, 1, 1, 5)

        self.layout.setVerticalSpacing(30)

        # BUTTONS, SLIDERS AND FUNCTIONALITIES CONNECTION

        # Connecting tiles buttons clicks with methods that update clicks list
        self.tile_one.clicked.connect(lambda: self.numb_tiles(self.tile_one))
        self.tile_four.clicked.connect(lambda: self.numb_tiles(self.tile_four))
        self.tile_four_ver.clicked.connect(lambda: self.numb_tiles(self.tile_four_ver))

        # Connecting tiles buttons with methods that change tile buttons appearance when clicked
        self.tile_one.clicked.connect(lambda: self.handle_button_click(self.tile_one))
        self.tile_four.clicked.connect(lambda: self.handle_button_click(self.tile_four))
        self.tile_four_ver.clicked.connect(lambda: self.handle_button_click(self.tile_four_ver))

        # Connecting tile buttons with method that will update image when you click the tile
        self.tile_one.clicked.connect(self.update_image)
        self.tile_four.clicked.connect(self.update_image)
        self.tile_four_ver.clicked.connect(self.update_image)

        # Connecting sliders with methods that display their values
        self.size.valueChanged.connect(self.display_size_value)
        self.opacity.valueChanged.connect(self.display_opacity_value)
        self.rotation.valueChanged.connect(self.display_rotation_value)
        self.spacing_x.valueChanged.connect(self.display_spacing_value_x)
        self.spacing_y.valueChanged.connect(self.display_spacing_value_y)

        # Connecting sliders to the method that will update image if the value of slider changes
        self.size.valueChanged.connect(self.update_image)
        self.opacity.valueChanged.connect(self.update_image)
        self.rotation.valueChanged.connect(self.update_image)
        self.spacing_x.valueChanged.connect(self.update_image)
        self.spacing_y.valueChanged.connect(self.update_image)

        # Connecting add_logo_image button
        self.add_logo_image.clicked.connect(self.open_logo_img)

        # Connecting reset button and reset method
        self.reset_btn.clicked.connect(self.reset)

        # Connecting Save button
        self.save_image_btn.clicked.connect(self.save_image)

    # # # ------------------------------------------- FUNCTIONALITIES -------------------------------------------------# # #
    def numb_tiles(self, tile_button):
        """This method updates the clicks list based on the argument tile_button it receives"""
        if tile_button == self.tile_one:
            self.clicks.clear()
            self.clicks.append(1)
        elif tile_button == self.tile_four:
            self.clicks.clear()
            self.clicks.append(4)
        elif tile_button == self.tile_four_ver:
            self.clicks.clear()
            self.clicks.append(5)

    def handle_button_click(self, button: QPushButton):
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

    def display_size_value(self):
        """Display the current value of size slider"""
        size_multiplier = self.size.value() / 10
        self.size_value.setText(str(size_multiplier) + "x")

    def display_opacity_value(self):
        """Displays current value of the opacity slider"""
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

    def open_logo_img(self):
        """Displays the open dialog for user to choose the image. Activates tile_one so the image can be instantly
        displayed. Enables sliders and save button and sets their style"""
        file_dialog = QFileDialog()
        self.file_path, _ = file_dialog.getOpenFileName(self, "Open Image", "", "Image Files (*.jpg *.jpeg *.png)")
        if self.file_path:
            self.logo_img = Image.open(self.file_path).convert("RGBA")
            self.tile_one.click()
            for slider in self.sliders:
                slider.setEnabled(True)
                slider.setStyleSheet("QSlider::handle:horizontal { background: 1F6E8C; }")
            self.save_image_btn.setEnabled(True)

    def space_between_logos(self, coef_x, coef_y, lg_img):
        """Calculates space between logos on horizontal and vertical axis and returns those values """
        if coef_x == 0:
            space_x = lg_img.width
        else:
            space_x = lg_img.width + round(lg_img.width * coef_x / 10)

        if coef_y == 0:
            space_y = lg_img.height
        else:
            space_y = lg_img.height + round(lg_img.height * coef_y / 10)

        return space_x, space_y

    def number_of_repetitions(self, org_img, lg_image, spacing_x, spacing_y):
        """Calculates number of time logo will be drawn on horizontal and vertical axis"""
        if spacing_x != 0:
            number_horizontal_rep = round(org_img.width / spacing_x)
        else:
            number_horizontal_rep = round(org_img.width / lg_image.width)

        if spacing_y != 0:
            number_vertical_rep = round(org_img.height / spacing_y)
        else:
            number_vertical_rep = round(org_img.height / lg_image.height)

        return number_horizontal_rep, number_vertical_rep

    def logo_patterns(self, logo_img, overlay_img, lg_spacing_x, lg_spacing_y, tile_sig, hr_rep, ver_rep):
        """Draws logo onto the overlay_img based on the patterns chosen by the user"""
        # These are x and y-axis starting points of logo for checker and romb patterns
        starting_point_x = 0
        starting_point_y = 0

        if tile_sig == 1:
            overlay_img.paste(logo_img, (round(overlay_img.width / 2) - round(logo_img.width / 2),
                                         round(overlay_img.height / 2) - round(logo_img.height / 2)), mask=logo_img)

        elif tile_sig == 4:
            # Initial values of spacing between logo. This will be incremented by a value of lg_spacing
            spacing_x = 0
            spacing_y = 0
            for v_numb in range(ver_rep + 1):
                for numb in range(hr_rep + 1):
                    overlay_img.paste(logo_img, (starting_point_x + spacing_x, starting_point_y + spacing_y),
                                      mask=logo_img)
                    spacing_x += lg_spacing_x
                # Increase the y value so that we display the same on the new y column
                spacing_y += lg_spacing_y
                # Reset the value of x for new y column
                spacing_x = 0

        elif tile_sig == 5:
            # Initial values of spacing between logo. This will be incremented by a value of lg_spacing
            spacing_x = 0
            spacing_y = 0
            # This line sets the starting horizontal displacement. If True it shifts the horizontal position
            # of the first logo and consequentially of each following logo by determined value
            displacement = False
            # This determines the starting horizontal point of the logo when displacement = True
            displacement_starting_point = starting_point_x + (round(lg_spacing_x / 2))

            for v_numb in range(ver_rep + 1):
                # We want first line to always be shifted thus displacement = not displacement. By setting it this way
                # the displacement value will change form after each iteration making one line of text shifted and
                # other 'normal', thus creating the romb-like pattern
                displacement = not displacement
                for numb in range(hr_rep + 1):
                    if displacement:
                        overlay_img.paste(logo_img,
                                          (displacement_starting_point + spacing_x, starting_point_y +
                                           spacing_y), mask=logo_img)
                    else:
                        overlay_img.paste(logo_img,
                                          (starting_point_x + spacing_x, starting_point_y + spacing_y),
                                          mask=logo_img)
                    spacing_x += lg_spacing_x
                spacing_y += lg_spacing_y
                spacing_x = 0

    def reset(self):
        """Resets all sliders and buttons to default state. Clears the logo_image and updates the image to the clear
        copy of the original_img"""
        # Set logo_img to None
        self.logo_img = None

        # Take the 'copy' of the original_img
        img = self.clear_pic
        # Create 'copied' image and update main_window preview label
        edited_image = Image.open(img).convert("RGBA")
        self.main_window.update_image(edited_image)

        # Set sliders and buttons states to default
        self.opacity.setValue(255)
        self.opacity.setEnabled(False)
        self.size.setValue(10)
        self.size.setEnabled(False)
        self.rotation.setValue(0)
        self.rotation.setEnabled(False)
        self.spacing_x.setValue(10)
        self.spacing_x.setEnabled(False)
        self.spacing_y.setValue(10)
        self.spacing_y.setEnabled(False)
        self.save_image_btn.setEnabled(False)

    def update_image(self):
        """Updates the image and sends it to main_window to be displayed. If there is no logo_img selected it will
         show warning"""
        if self.logo_img:
            edited_image = self.main()
            self.main_window.update_image(edited_image)
        else:
            if not self.warning_displayed:
                QMessageBox.warning(self, "Warning", "Please open the logo image you want to add.")
                self.warning_displayed = True

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
            rgb_img = self.watermarked_img.convert("RGB")
            rgb_img.save(file_name, "JPEG" if file_name.endswith('.jpg') else "PNG")

    def main(self):
        """Main method that encompasses most of the other methods. Gets all the values, creates image to be combined
        with the original_img, combines them using alpha_composite and returns watermarked image"""
        # Open original img
        original_img = Image.open(self.original_img).convert("RGBA")

        # Set logo img
        logo_image = self.logo_img

        # Create new RGBA image with same dimensions as logo_image
        logo_image_alpha = Image.new("RGBA", logo_image.size)

        # Paste logo_image onto logo_image_alpha
        logo_image_alpha.paste(logo_image, (0, 0), mask=logo_image)

        # Get opacity value from opacity slider
        logo_opacity = int(self.opacity.value())

        # Apply opacity to logo_image_alpha
        logo_image_alpha.putalpha(logo_opacity)

        # Get size value from size slider
        logo_size = self.size.value() / 10

        # Once we get size value we can change the width and the size of logo_image_alpa
        new_width = logo_image_alpha.width * logo_size
        new_height = logo_image_alpha.height * logo_size
        resized_logo_image = logo_image_alpha.resize((int(new_width), int(new_height)))

        # Get horizontal and vertical spacing coefficient between logos from spacing_x and spacing_y sliders
        logo_spacing_x = float(self.spacing_x.value() / 10)
        logo_spacing_y = float(self.spacing_y.value() / 10)

        # Get rotation value from rotation slider
        logo_rotation = int(self.rotation.value())

        # Rotate the resized_logo_image
        rotated_logo_img = resized_logo_image.rotate(logo_rotation, expand=True)

        # Create an overlay image with the same dimensions as the original_img and fully opaque
        overlay_image = Image.new("RGBA", (original_img.width, original_img.height), (255, 255, 255, 0))
        overlay_image = overlay_image.point(lambda p: p * logo_opacity // 255)

        # This tells us which tile button was clicked
        tile_signal = self.clicks[0]

        # Get the values of horizontal and vertical spacing between logos
        gap_x, gap_y = self.space_between_logos(logo_spacing_x, logo_spacing_y, rotated_logo_img)

        # Get the number of horizontal and vertical repetitions of logo
        horizontal_rep, vertical_rep = self.number_of_repetitions(original_img, rotated_logo_img, gap_x, gap_y)

        # Determine the pattern and display the logo in that pattern on original_img
        self.logo_patterns(rotated_logo_img, overlay_image, gap_x, gap_y, tile_signal, horizontal_rep, vertical_rep)

        # Create watermarked image using alpha_composite method
        self.watermarked_img = Image.alpha_composite(original_img, overlay_image)
        return self.watermarked_img
