import cv2
import numpy as np


def convert_to_gray_scale(image):
    R, G, B = 0.21, 0.72, 0.07

    r_channel = image[:, :, 0]
    g_channel = image[:, :, 1]
    b_channel = image[:, :, 2]

    gray_scale_image = R * r_channel + G * g_channel + B * b_channel

    gray_scale_image = gray_scale_image.reshape((image.shape[:2]) + (1,)).astype("uint8")

    return gray_scale_image


def sample_image(sampling_factor, image):
    height, width, _ = image.shape
    new_height, new_width = round(height * sampling_factor), round(width * sampling_factor)

    w, h = np.meshgrid(np.arange(new_width), np.arange(new_height))

    H = h / sampling_factor
    W = w / sampling_factor

    x1 = np.floor(H).astype(int)
    y1 = np.floor(W).astype(int)

    x2 = np.minimum(x1 + 1, height - 1)
    y2 = np.minimum(y1 + 1, width - 1)

    dx = H - x1
    dy = W - y1

    interpolated_value = (1 - dx) * (1 - dy) * image[x1, y1, 0] + \
        dx * (1 - dy) * image[x2, y1, 0] + \
        (1 - dx) * dy * image[x1, y2, 0] + \
        dx * dy * image[x2, y2, 0]

    return interpolated_value.reshape((new_height, new_width, 1)).astype("uint8")


'''1.Load an image from the disk'''
image = cv2.imread("dog.jpg")
print("Original image: " + str(image.shape))


'''2.Convert the image to gray-scale (8bpp format)'''
gray_scale_image = convert_to_gray_scale(image)
cv2.imwrite("gray_scale_dog.jpg", gray_scale_image)


'''3.Re-sample the image such that the size is 0.7 times it original dimensions using 
linear interpolation method and save the image.'''
down_sampled_image = sample_image(0.7, gray_scale_image)
print("Down sampled gray scale image: " + str(down_sampled_image.shape))
cv2.imwrite("down_sampled_gs_dog.jpg", down_sampled_image)


'''4.Re-sample the image created in (step 3) back to its 
original size and save the image.'''
reconstructed_image = sample_image(1 / 0.7, down_sampled_image)
print("Reconstructed gray scale image: " + str(reconstructed_image.shape))
cv2.imwrite("reconstructed_gs_dog.jpg", reconstructed_image)


'''5.Compute the sum of the average of the squared difference between pixels in the 
original image (in step 2) and the re-samples image in (step 4).'''
sum_square_error = np.sum(np.square(gray_scale_image - reconstructed_image))
mean_square_error = np.mean(np.square(gray_scale_image - reconstructed_image))
print("Sum of Square Error: " + str(sum_square_error))
print("Mean Square Error: " + str(mean_square_error))
