from ultralytics import SAM

# Load a model
model = SAM('sam_b.pt')

# Display model information (optional)
model.info()

# Run inference
model('screenshot.png', save=False, show=True)
