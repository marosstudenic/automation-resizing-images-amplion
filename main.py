import os
from PIL import Image

#source https://www.thepythoncode.com/article/compress-images-in-python

#exmple usage
# python3 main.py -w 1600 -sw 400 -q 95 --out-folder fotogaleria-festivalu-2022 --in-folder origin


def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"



def compress_img(image_filename, image_dest_filename, quality=90, width=1400, height=None):
    # print(image_filename)
    # load the image to memory
    img = Image.open(image_filename)
    # print the original image shape
    # print("[*] Image shape:", img.size)
    # get the original image size in bytes
    image_size = os.path.getsize(image_filename)
    # print the size before compression/resizing

    if height==None:
        new_size_ratio = width/img.size[0]
    elif width==None:
        new_size_ratio = height/img.size[1]
    else:
        new_size_ratio = min(width/img.size[0], height/img.size[1])

    # print("[+] New size ratio: ",new_size_ratio)
    if new_size_ratio < 1.0:
        img.thumbnail((img.size[0]*new_size_ratio, img.size[1]*new_size_ratio), Image.Resampling.LANCZOS)
        # print new image shape
        # print("[+] New Image shape:", img.size)

    # save the image to disk
    try:
        # save the image with the corresponding quality and optimize set to True
        img.save(image_dest_filename, quality=quality, optimize=True)
    except OSError:
        # convert the image to RGB mode first
        img = img.convert("RGB")
        # save the image with the corresponding quality and optimize set to True
        img.save(image_dest_filename, quality=quality, optimize=True)
    # print("[+] New file saved:", image_dest_filename)
    # get the new image size in bytes
    new_image_size = os.path.getsize(image_dest_filename)
    # print the new size in a good format
    # print("[+] Size after compression:", get_size_format(new_image_size))
    # calculate the saving bytes
    saving_diff = new_image_size - image_size
    # print the saving percentage
    # print(f"[+] Image size change: {saving_diff/image_size*100:.2f}% of the original image size.")
    print("[*] Image shape", '%15s' % str(img.size),  "Size before/ after  compression:", get_size_format(image_size), "/", get_size_format(new_image_size), f"{saving_diff/image_size*100:.2f}% of the original image size.")



def iterate_through_folder(folder, output_folder="fotogaleria-festivalu-XXXX", quality=90, width=1440, height=None):
    counter=0
    for file in os.listdir(folder):
        if file.lower().endswith(".jpg") or file.lower().endswith(".jpeg") or file.lower().endswith(".png"):
            counter+=1
    
    for (index, file) in enumerate(os.listdir(folder)):
        print("processing file: ", file, f"{index}/{counter}", end=" ")
        if file.lower().endswith(".jpg") or file.lower().endswith(".jpeg") or file.lower().endswith(".png"):
            new_filename = file.replace(file.lower().split(".")[-1], "jpg")
            compress_img(os.path.join(folder, file), os.path.join(output_folder, new_filename), quality, width, height)

def print_filenames(folder):
    filenames = []
    list_file = open("list.txt", "w")
    for file in os.listdir(folder):
        if file.endswith(".jpg"):
            filenames.append(file)
    
    filenames.sort()
    for filename in filenames:
        list_file.write(filename+"\n")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Script for compressing archive images for amplion website")
    parser.add_argument("-i", "--in-folder", help="Target image to compress and/or resize", default="./")
    parser.add_argument("-o", "--out-folder", help="Output folder for compressed images", default="fotogaleria-festivalu-XXXX")
    # parser.add_argument("-j", "--to-jpg", action="store_true", help="Whether to convert the image to the JPEG format")
    parser.add_argument("-q", "--quality", type=int, help="Quality ranging from a minimum of 0 (worst) to a maximum of 95 (best). Default is 90", default=90)
    # parser.add_argument("-r", "--resize-ratio", type=float, help="Resizing ratio from 0 to 1, setting to 0.5 will multiply width & height of the image by 0.5. Default is 1.0", default=1.0)
    parser.add_argument("-w", "--width", type=int, help="The new width image, make sure to set it with the `height` parameter", default=None)
    parser.add_argument("-he", "--height", type=int, help="The new height image, make sure to set it with the `width` parameter //on the web the max-height is 1051px", default=1100)
    parser.add_argument("-sw", "--small-width", type=int, help="The new width image, make sure to set it with the `height` parameter", default=400)
    parser.add_argument("-she", "--small-height", type=int, help="The new height image, make sure to set it with the `width` parameter", default=None)
    args = parser.parse_args()
    # print the passed arguments
    print("="*50)
    print("[*] In folder:", args.in_folder)
    print("[*] Out folder:", args.out_folder)
    print("[*] Quality:", args.quality)
    if args.width or args.height:
        print("[*] Width:", args.width)
        print("[*] Height:", args.height)

    if args.small_width or args.small_height:
        print("[*] Width:", args.small_width)
        print("[*] Height:", args.small_height)
    print("="*50)
    # compress the image

    small_folder = os.path.join(args.out_folder, "small")
    os.makedirs(args.out_folder, exist_ok=True)
    os.makedirs(small_folder, exist_ok=True)
    iterate_through_folder(args.in_folder, args.out_folder, args.quality, args.width, args.height)
    iterate_through_folder(args.in_folder, small_folder, args.quality, args.small_width, args.small_height)

    print_filenames(args.in_folder)


    print("[+] Done!")

