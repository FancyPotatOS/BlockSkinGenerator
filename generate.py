
import re
import os
import shutil
from PIL import Image, ImageColor, ImageOps



if not (os.path.exists("generated") and os.path.isdir("generated")):
    os.mkdir("generated")
    
if not (os.path.exists("options.config") and os.path.isfile("options.config")):
    with open("options.config", "w") as file:
        file.write("defaultLocation=%appdata%/.minecraft/")


skin_size = (64, 64)
base_mask_specs = [
    (8, 0, 16, 8),
    (0, 8, 32, 8),
    (4, 16, 8, 4),
    (20, 16, 16, 4),
    (44, 16, 8, 4),
    (0, 20, 56, 12),
    (20, 48, 8, 4),
    (36, 48, 8, 4),
    (16, 52, 32, 12)
]
thin_mask_specs = [
    (8, 0, 16, 8),
    (0, 8, 32, 8),
    (4, 16, 8, 4),
    (20, 16, 16, 4),
    (44, 16, 6, 4),
    (0, 20, 54, 12),
    (20, 48, 8, 4),
    (36, 48, 6, 4),
    (16, 52, 30, 12)
]
def gen_mask(is_thin = False):
    image = Image.new("RGBA", skin_size)
    specs = base_mask_specs
    if is_thin:
        specs = thin_mask_specs
    for box in specs:
        mask = Image.new("RGBA", skin_size)
        mask.paste(ImageColor.getrgb("#FFFFFFFF"), (box[0], box[1], box[0]+box[2], box[1]+box[3]))
        image.paste(mask, None, mask)
    return image

print("\n")

options = {
}
if os.path.exists("options.config"):
    print("Config file found.\n\n")
    with open("options.config", "r") as file:
        for line in file.readlines():
            if line == "" or line == "\n":
                continue
            splt = line.split("=")
            options[splt[0]] = "".join(splt[1:])

print("\t\t-= Minecraft Block Skin Creator =-\nBy FancyPotatOS\n\nUsage: Modify the file called options.config if you want to change the default directory. \nOtherwise, continue with the command line and direct it to the location of the block textures (such as in a resource pack folder)\n\n")


base_mask = gen_mask()
base_image = base_mask.copy()
initial_directory = os.getcwd()

print("Generate a normal or thin skin > ", end="")
inp = str.lower(input())
if inp == "":
    inp = "normal"
while not re.match(r"normal|thin", inp):
    print("That is not a valid option. Please input 'normal' or 'thin' > ", end="")
    inp = str.lower(input())
skin_type = inp
if skin_type == "thin":
    base_mask.close()
    base_image.close()

    base_mask = gen_mask(True)
    base_image = base_mask.copy()

print("Background colour for blocks with transparent parts (hexcode) > ", end="")
inp = input()
if inp == "":
    inp = "000000"
while not re.match(r"[A-Fa-f0-9]{6}", inp):
    print("That is not a valid hex code. Please limit it to exactly 6 hexadecimal digits. > ", end="")
    inp = input()
hexcode = inp

#ImageOps.colorize(img, black ="red", white ="yellow")
print("Colourize? (Good for leaves and grass that are grey) > ", end="")
inp = str.lower(input())
if inp == "":
    inp = "false"
while not re.match(r"true|false", inp):
    print("That is not a valid option. Please input 'true' or 'false' > ", end="")
    inp = str.lower(input())
colourize = inp == "true"

if colourize:
    print("Colourization colour (hexcode) - I recommend 42b80f > ", end="")
    inp = input()
    while not re.match(r"[A-Fa-f0-9]{6}", inp):
        print("That is not a valid hex code. Please limit it to exactly 6 hexadecimal digits. > ", end="")
        inp = input()
    colourize_hexcode = inp

print("Directory to find block texture > ", end="")
inp = input()
if inp == "":
    inp = options["defaultLocation"]
while not os.path.isdir(inp):
    print("That is not a valid directory. Please input a directory > ", end="")
    inp = input()
directory = inp

os.chdir(directory)

print("Block to use > ", end="")
inp = str.lower(input()).replace(" ", "_")
while not inp + ".png" in [x for x in os.listdir() if str.endswith(x, ".png") and os.path.isfile(x)]:
    print("That is not a valid block. Please input a block > ", end="")
    inp = str.lower(input()).replace(" ", "_")

block_chosen = Image.open(inp + ".png").convert("RGBA")
repeating = (max(1, int(base_image.size[0] / block_chosen.size[0])), max(1, int(base_image.size[1] / block_chosen.size[1])))
for x in range(repeating[0]):
    for y in range(repeating[1]):
        pos = (x * block_chosen.size[0], y * block_chosen.size[1])
        base_image.paste(block_chosen, pos)
final_image = base_mask.copy()

final_image.paste(base_image, None, base_mask)

transp_mask = final_image.copy()
final_image.paste(ImageColor.getrgb("#" + hexcode), (0, 0, final_image.size[0], final_image.size[1]), base_mask)
final_image.paste(transp_mask, None, transp_mask)

if colourize:
    final_image = final_image.convert("L")
    final_image = ImageOps.colorize(final_image, black="black", white=ImageColor.getrgb("#" + colourize_hexcode))
    final_image = final_image.convert("RGBA")


os.chdir(initial_directory)
os.chdir("generated")
final_image.save(inp + ("_thin" if skin_type == "thin" else "") + ".png")
os.chdir("..")

print("\n\nDone! Press enter to exit.")
input()
