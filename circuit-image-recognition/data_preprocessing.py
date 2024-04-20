
import os
import matplotlib.pyplot as plt
from shapely.geometry import LineString
import geojson
import random
import cv2

def plot_line_string(coordinates):
	# Path to the folder containing GeoJSON files
	folder_path = "f1-circuits/circuits"

	# Loop through each file in the folder
	for filename in os.listdir(folder_path):
		if filename.endswith(".geojson"):
			file_path = os.path.join(folder_path, filename)
			
			# Load GeoJSON file
			with open(file_path, 'r') as f:
				data = geojson.load(f)

			# Extract LineString coordinates
			coordinates = data['features'][0]['geometry']['coordinates']

			# Create LineString object
			line = LineString(coordinates)

			# Plot LineString
			fig, ax = plt.subplots(figsize=(8, 8))
			ax.plot(*line.xy, color='white')  # Plot LineString
			ax.set_facecolor('black')  # Set background color to black
			ax.axis('off')  # Turn off axis

			# Save image with filename as the image name
			image_name = os.path.splitext(filename)[0] + ".png"
			image_path = os.path.join("output_images", image_name)
			plt.savefig(image_path, bbox_inches='tight', pad_inches=0, dpi=300, facecolor='black', transparent=True)
			plt.close()



def create_folders_using_images():
	# Path to the folder containing images
	image_folder_path = "output_images"

	# List of image files
	image_files = os.listdir(image_folder_path)

	# Loop through each image file
	for image_file in image_files:
		if image_file.endswith(".png"):  # Process only PNG files
			# Load the image
			image_path = os.path.join(image_folder_path, image_file)
			image = cv2.imread(image_path)

			# Create a folder using the filename without extension
			folder_name = os.path.splitext(image_file)[0]
			folder_path = os.path.join(image_folder_path, folder_name)
			os.makedirs(folder_path, exist_ok=True)

			# Move the image file to the newly created folder
			new_image_path = os.path.join(folder_path, image_file)
			os.rename(image_path, new_image_path)

			print(f"Moved {image_file} to {folder_name}/")


def create_synthetic_images():
	# Path to the folder containing image folders
	base_folder_path = "output_images"

	# List of subfolders (circuit folders) in the base folder
	subfolders = [folder for folder in os.listdir(
		base_folder_path) if os.path.isdir(os.path.join(base_folder_path, folder))]

	# Define the number of synthetic images to generate for each subfolder
	num_synthetic_images_per_folder = 50

	# Loop through each subfolder (circuit folder)
	for subfolder in subfolders:
		# Path to the current subfolder
		subfolder_path = os.path.join(base_folder_path, subfolder)

		# List of image files in the current subfolder
		image_files = [file for file in os.listdir(
			subfolder_path) if file.endswith(".png")]

		# Create synthetic images for the current subfolder
		for i in range(num_synthetic_images_per_folder):
			# Select a random image file from the current subfolder
			image_file = random.choice(image_files)

			# Define random parameters for image transformation, make the between a range
			rand_rotation_neg = random.uniform(-2.0, 0)
			rand_rotation_pos = random.uniform(0, 2.0)
			rand_scaled_x = random.uniform(0.5, 1.5)
			rand_scaled_y = random.uniform(0.5, 1.5)

			# Load the image
			image_path = os.path.join(subfolder_path, image_file)
			image = cv2.imread(image_path)

			# Rotate the image
			rows, cols, _ = image.shape
			rotation_matrix = cv2.getRotationMatrix2D((cols/2, rows/2), random.uniform(rand_rotation_neg, rand_rotation_pos), 1)
			rotated_image = cv2.warpAffine(image, rotation_matrix, (cols, rows))

			# Scale the image
			scaled_image = cv2.resize(rotated_image, None, fx=rand_scaled_x, fy=rand_scaled_y)

			# Adjust brightness
			adjusted_image = cv2.convertScaleAbs(scaled_image, alpha=1.2, beta=10)

			# Save the synthetic image in the same folder as the original file
			synthetic_image_path = os.path.join(subfolder_path, f"{i}_{image_file}")
			cv2.imwrite(synthetic_image_path, adjusted_image)

			# keep track of the progress
			print(f"Generated synthetic image {i+1}/{num_synthetic_images_per_folder} for {subfolder}", end="\r")

	print("Synthetic images generated successfully.")
