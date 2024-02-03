import matplotlib.pyplot as plt
from PIL import Image

# Load the image from the specified path
image_path = "screenshot.png"  # Replace with your image path
img = Image.open(image_path)

# Create a figure and axis for displaying the image
fig, ax = plt.subplots()
ax.imshow(img)  # Display the image

# Set up the grid
n_columns = 8
n_rows = 10

# Set the grid lines
ax.set_xticks([i * img.width / n_columns for i in range(n_columns + 1)])
ax.set_yticks([i * img.height / n_rows for i in range(n_rows + 1)])

# Hide the default tick labels as we will add custom labels
ax.set_xticklabels([""] * (n_columns + 1))
ax.set_yticklabels([""] * (n_rows + 1))

# Calculate the position for each label (at the center of each grid cell)
x_positions = [
    i * img.width / n_columns + img.width / (2 * n_columns) for i in range(n_columns)
]
y_positions = [
    i * img.height / n_rows + img.height / (2 * n_rows) for i in range(n_rows)
]

# Add the labels at calculated positions
for i, x in enumerate(x_positions):
    ax.text(
        x, -20, chr(65 + i), ha="center", va="bottom", fontsize=12, color="black"
    )  # Using ASCII for A, B, C, ...
for i, y in enumerate(y_positions):
    ax.text(
        -20, y, str(i + 1), ha="right", va="center", fontsize=12, color="black"
    )  # Using numbers for row labels

# Show the grid on the image
ax.grid(color="red", linestyle="-", linewidth=4)

plt.show()
