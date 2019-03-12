from PIL import Image
import os
import random

large_image_path = input("Enter the path to the large image: ")
small_image_folder = input("Enter the path to the small images folder(folder should contain between 400-1,000 images for best results: ")
final_size = int(input("Enter target height of final image (pixel values between 1,000-20,000 for best results): "))
small_image_size = int(input("Enter the size of small images (pixel values between 50-200 for best results): "))
image_list = []
image_brightness_list = []
new_image = Image.new('RGBA', (final_size, final_size))
large_image = Image.open(large_image_path)
large_image_alpha = Image.open(large_image_path)
large_image_alpha = large_image_alpha.convert('RGBA')
scale = int(final_size/small_image_size)
large_image_pixels = []

def resize_crop(image, size):
    
    crop_size = 0
    if image.size[0] > image.size[1]:
        crop_size = image.size[1]
    else:
        crop_size = image.size[0]
    image = image.crop((0,0,crop_size,crop_size))
    image.thumbnail((size, size), Image.ANTIALIAS)
    return image

def get_target_pixels(image):
    
    width, height = image.size
    
    for x in range(0, width):
        for y in range(0, height):
            r, g, b = image.getpixel((x,y))
            average = int((r+g+b)/3)
            large_image_pixels.append(average)
            
def get_small_averages(path):
    
    for file in os.listdir(path):
        small_image = Image.open("{}/{}".format(path,file))
        resized_small_image = resize_crop(small_image, small_image_size)
        image_list.append(resized_small_image)

    for image in image_list:
        width, height = image.size
        r_total = 0
        g_total = 0
        b_total = 0
        count = 0
        for x in range(0, width):
            for y in range(0, height):
                r, g, b = image.getpixel((x,y))
                r_total += r
                g_total += g
                b_total += b
                count += 1
                average_brightness = int((((r_total + g_total + b_total)/count)/3))
        image_brightness_list.append(average_brightness)

choice_list = []      
def get_choices():
    threshold = 40
    for pixel in large_image_pixels:
        possible_matches = []
        for b in image_brightness_list:
            if abs(b-pixel) <= threshold:
                possible_matches.append(image_list[image_brightness_list.index(b)])
        
        if len(possible_matches) == 0:
                possible_matches.append(image_list[image_brightness_list.index(random.choice(image_brightness_list))])
                print("added random!")
        choice_list.append(random.choice(possible_matches))            

def paste():
    
    w, h = new_image.size
    count = 0
    for x in range(0, w, int(small_image_size)):
        for y in range(0, h, int(small_image_size)):
            new_image.paste(choice_list[count], (x, y, x+int(choice_list[count].size[0]), y+int(choice_list[count].size[1])))
            count += 1

print("Resizing large image...")
large_image = resize_crop(large_image, scale)
large_image_alpha = resize_crop(large_image_alpha, final_size)
large_image_alpha = large_image_alpha.resize((final_size, final_size))
print("Getting pixel values from large image...")
get_target_pixels(large_image)
print("Resizing and gathering pixel data from small images...")
get_small_averages(small_image_folder)
print("Calculating matches for pixels...")
get_choices()
print("pasting images into final image...")
paste()
final_image = Image.blend(large_image_alpha, new_image, .65)
print("Finishing!")
final_image.save("result.png")
