import io
import base64
import json
import os
import time
import asyncio
import pkg_resources
from ultralytics import YOLO
from PIL import Image, ImageDraw


def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode("utf-8")
    return img_base64


def get_label_coordinates(label, label_coordinates):
    """
    Retrieves the coordinates for a given label.

    :param label: The label to find coordinates for (e.g., "~1").
    :param label_coordinates: Dictionary containing labels and their coordinates.
    :return: Coordinates of the label or None if the label is not found.
    """
    return label_coordinates.get(label)


def is_overlapping(box1, box2):
    x1_box1, y1_box1, x2_box1, y2_box1 = box1
    x1_box2, y1_box2, x2_box2, y2_box2 = box2

    # Check if there is no overlap
    if x1_box1 > x2_box2 or x1_box2 > x2_box1:
        return False
    if (
        y1_box1 > y2_box2 or y1_box2 > y2_box1
    ):  # Adjusted to check 100px proximity above
        return False

    return True


def add_labels(base64_data):
    image_bytes = base64.b64decode(base64_data)
    image_labeled = Image.open(io.BytesIO(image_bytes))  # Corrected this line
    image_debug = image_labeled.copy()  # Create a copy for the debug image
    image_original = (
        image_labeled.copy()
    )  # Copy of the original image for base64 return

    yolo_weights_path = os.path.join(os.getcwd(), "best.pt")
    yolo_model = YOLO(yolo_weights_path)

    results = yolo_model(image_labeled, show=True)

    draw = ImageDraw.Draw(image_labeled)
    debug_draw = ImageDraw.Draw(
        image_debug
    )  # Create a separate draw object for the debug image
    font_size = 45

    labeled_images_dir = "labeled_images"
    label_coordinates = {}  # Dictionary to store coordinates

    if not os.path.exists(labeled_images_dir):
        os.makedirs(labeled_images_dir)

    counter = 0
    drawn_boxes = []  # List to keep track of boxes already drawn
    for result in results:
        if hasattr(result, "boxes"):
            for det in result.boxes:
                bbox = det.xyxy[0]
                x1, y1, x2, y2 = bbox.tolist()

                debug_label = "D_" + str(counter)
                debug_index_position = (x1, y1 - font_size)
                debug_draw.rectangle([(x1, y1), (x2, y2)], outline="blue", width=1)
                debug_draw.text(
                    debug_index_position,
                    debug_label,
                    fill="blue",
                    font_size=font_size,
                )

                overlap = any(
                    is_overlapping((x1, y1, x2, y2), box) for box in drawn_boxes
                )

                if not overlap:
                    draw.rectangle([(x1, y1), (x2, y2)], outline="red", width=1)
                    label = "~" + str(counter)
                    index_position = (x1, y1 - font_size)
                    draw.text(
                        index_position,
                        label,
                        fill="red",
                        font_size=font_size,
                    )

                    # Add the non-overlapping box to the drawn_boxes list
                    drawn_boxes.append((x1, y1, x2, y2))
                    label_coordinates[label] = (x1, y1, x2, y2)

                    counter += 1
    # Save the image
    timestamp = time.strftime("%Y%m%d-%H%M%S")

    output_path = os.path.join(labeled_images_dir, f"img_{timestamp}_labeled.png")
    output_path_debug = os.path.join(labeled_images_dir, f"img_{timestamp}_debug.png")
    output_path_original = os.path.join(
        labeled_images_dir, f"img_{timestamp}_original.png"
    )

    image_labeled.save(output_path)
    image_debug.save(output_path_debug)
    image_original.save(output_path_original)

    buffered_original = io.BytesIO()
    image_original.save(buffered_original, format="PNG")  # I guess this is needed
    img_base64_original = base64.b64encode(buffered_original.getvalue()).decode("utf-8")

    # Convert image to base64 for return
    buffered_labeled = io.BytesIO()
    image_labeled.save(buffered_labeled, format="PNG")  # I guess this is needed
    img_base64_labeled = base64.b64encode(buffered_labeled.getvalue()).decode("utf-8")

    return img_base64_labeled, label_coordinates


base64_image = image_to_base64("screenshot.png")
(
    labeled_image,
    coordinates,
) = add_labels(base64_image)
print(coordinates)
