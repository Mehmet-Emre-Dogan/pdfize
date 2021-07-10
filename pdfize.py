try:
    from PIL import Image, ImageFont, ImageDraw 
    import os
    from json import load
    from msvcrt import getch
    from pkg_resources import parse_version

    directory = '.'
    dataFolder = "/data"

    print("Loading...")
    with open(directory + dataFolder + "/confi.json", "r", encoding="utf-8") as fil:
        settings = load(fil)

    ims = [] #image array, for cropped images
    files = [] 
    font = ImageFont.truetype(directory + dataFolder + settings["fontPath"], settings["fontSize"]) #path, font size
    waterFont = ImageFont.truetype(directory + dataFolder + settings["fontPath"], settings["fontSizeWatermark"]) #path, font size

    def process(path, num):
        im = Image.open(path)  # img is the path of the image 
        im = im.convert("RGB")
        if settings["pagenumIsFilename"]:
            num = path[:-4]

        if settings["noCrop"]:
            settings["right"], settings["down"] = im.size
            settings["left"] = settings["up"] = 0
            im1 = im
        else:    
            im1 = im.crop((settings["left"], settings["up"], settings["right"], settings["down"]))#im.crop((left, top, right, bottom))
        dim = ImageDraw.Draw(im1) #drawn image
        textWidth, textHeight = dim.textsize(str(num), font) #will be drawn string, font size
        
        if settings["numPos"] == 1:
            x = settings["right"] - settings["left"] - textWidth - 10
            y = settings["down"] - settings["up"] - textHeight - 10
        elif settings["numPos"] == 2:
            x = settings["right"] - settings["left"] - textWidth - 10
            y = settings["up"] + 10
        elif settings["numPos"] == 3:
            x = settings["left"] + 10
            y = settings["up"] + 10
        elif settings["numPos"] == 4:
            x = settings["left"] + 10
            y = settings["down"] - settings["up"] - textHeight - 10
        if settings["isBgExists"]:
            dim.rectangle((x, y, x + textWidth, y + textHeight), fill=tuple(settings["bgColor"]))
       
        dim.text( (x, y), str(num), fill=tuple(settings["pgnumColor"]), font=font, align ="left") #add page number

        if settings["watermark"]:
            im1 = im1.convert("RGBA")
            watWidth, watHeight = dim.textsize(str(settings["watermark"]), waterFont) #will be drawn watermark string, watermark font size
            wx = (settings["right"] - settings["left"] - watWidth)/2 
            wy = (settings["down"] - settings["up"] - watHeight)/2
            #add watermark
            watermark = Image.new('RGBA', im1.size, (255,255,255,0))
            watermarkD = ImageDraw.Draw(watermark)
            watermarkD.text( (wx, wy), str(settings["watermark"]), fill=tuple(settings["watermarkColor"]), font=waterFont, align ="center")
            watermark = watermark.rotate(settings["watermarkAngle"], expand = False) #degree, counter clockwise
            im1 = Image.alpha_composite(im1, watermark)
            im1 = im1.convert("RGB")

        ims.append(im1)
    
    for item in os.listdir(directory):
        if item.endswith(".png") or item.endswith(".jpg") or item.endswith(".jpeg") or item.endswith(".JPG") or item.endswith(".JPEG"):
            files.append(item)
    files.sort(key=parse_version)
    print(f"{len(files)} files found, they will be converted to pdf")

    i = 1
    for filename in files:
        print(f"{i}-".rjust(3) + f" Processing: {filename}")
        process(filename, i)
        i += 1

    try:
        ims[0].save("output.pdf",save_all=True, append_images=ims[1:], resolution=settings["dpi"], subsampling=0, quality=100)
        print("Pdf has been created successfully. Press any key to exit...")

    except OSError as exo:
        print(exo)
        print("Please close the 'output.pdf' file and run the application again. Press any key to dismiss this message...")
          
except (Exception, OSError, RuntimeError, ImportError) as ex:
    print(ex)

garbage = getch()