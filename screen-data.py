from pynput import mouse
import time
import os
import subprocess
import platform
from PIL import Image, ImageDraw

screenshot_dir = "labeled_images"
annotation_dir = "annotations"

os.makedirs(screenshot_dir, exist_ok=True)
os.makedirs(annotation_dir, exist_ok=True)

box_size = 100


def draw_box_and_save_annotation(image, x, y, filename):
    # scale
    x = x * 2
    y = y * 2
    draw = ImageDraw.Draw(image)
    left = x - box_size // 2
    top = y - box_size // 2
    right = x + box_size // 2
    bottom = y + box_size // 2
    text_position = (
        left,
        bottom + 5,
    )

    draw.rectangle([left, top, right, bottom], outline="red", width=5)
    draw.text(text_position, "button", fill="red")

    image.save(filename)

    # YOLO annotation
    img_width, img_height = image.size
    x_center = (left + right) / 2 / img_width
    y_center = (top + bottom) / 2 / img_height
    width = box_size / img_width
    height = box_size / img_height
    annotation = f"0 {x_center} {y_center} {width} {height}\n"
    print(annotation)
    annotation_filename = os.path.join(
        annotation_dir, os.path.basename(filename).replace(".png", ".txt")
    )
    with open(annotation_filename, "w") as file:
        file.write(annotation)


def on_click(x, y, button, pressed):
    if pressed:
        filename = os.path.join(
            screenshot_dir, f"screenshot_{time.strftime('%Y%m%d_%H%M%S')}.png"
        )
        subprocess.run(["screencapture", "-C", filename])
        screenshot_with_box = Image.open(filename)
        draw_box_and_save_annotation(screenshot_with_box, x, y, filename)
        print(f"Screenshot and annotation saved for click at ({x}, {y})")

with mouse.Listener(on_click=on_click) as listener:
    listener.join()
