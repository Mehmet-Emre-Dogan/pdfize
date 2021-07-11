from json import load, dump
directory = '.'
dataFolder = "/data"
while True:
    try:
        with open(directory + dataFolder + "/confi.json", "r", encoding="utf-8") as fil:
            settings = load(fil)
    except OSError:
        print("Make sure './data/confi.json' exists if so, close 'confi.json' and try again.")
        continue
    try:
        print("="*75)
        mode = int(input("1- Set Cropping\n2- Page number preferences\n3- Watermark Prefences\n4- Dpi preferences\n0- Exit\n--> "))
    except:
        print("Input must be integer.")
    else:
        if mode == 0:
            break
        elif mode == 1:
            try:
                isCrop = input("1- Enable cropping\n0- Disable cropping\nCRTL C- Skip\n--> ")
                if isCrop == '0':
                    settings["noCrop"] = 1
                elif isCrop == '1':
                    settings["noCrop"] = 0
                else:
                    print("Invalid input")
            except KeyboardInterrupt:
                pass

            if not settings["noCrop"]:
                while True:
                    try:
                        up = int(input(f"Current UP cropping limit is: {settings['up']} \nEnter new value or press CRTL C to cancel.\n--> "))
                        settings["up"] = up
                    except KeyboardInterrupt:
                        break
                    except Exception:
                        print("Value must be integer.")
                    else:
                        break
                while True:    
                    try:
                        settings["down"] = int(input(f"Current DOWN cropping limit is: {settings['down']} \nEnter new value or press CRTL C to cancel.\n--> "))
                    except KeyboardInterrupt:
                        break
                    except Exception:
                        print("Value must be integer.")
                    else:
                        break
                while True:
                    try:
                        settings["left"] = int(input(f"Current LEFT cropping limit is: {settings['left']} \nEnter new value or press CRTL C to cancel.\n--> "))   
                    except KeyboardInterrupt:
                        break
                    except Exception:
                        print("Value must be integer.")
                    else:
                        break
                while True:
                    try:
                        settings["right"] = int(input(f"Current RIGHT cropping limit is: {settings['right']} \nEnter new value or press CRTL C to cancel.\n--> "))
                    except KeyboardInterrupt:
                        break
                    except Exception:
                        print("Value must be integer.")
                    else:
                        break

        elif mode == 2: 
            while True:
                try:
                    print("How the pages will numbered?")
                    pagenumIsFilename = int(input("1- Use file name\n0- Use numbers\nCRTL C- Skip\n--> "))
                    if pagenumIsFilename == 1:
                        settings["pagenumIsFilename"] = 1
                        break
                    elif pagenumIsFilename == 0:
                        settings["pagenumIsFilename"]= 0
                        break
                    else:
                        print("Invalid input")
                except KeyboardInterrupt:
                    pass
                except Exception:
                            print("Value must be integer.")
            try:
                settings['fontSize'] = int(input(f"Current page number font size  is: {settings['fontSize']} \nEnter new value or press CRTL C to cancel.\n--> "))
            except KeyboardInterrupt:
                pass
            except Exception:
                        print("Value must be integer.")
            while True:
                try:
                    print("Page number position:")
                    numpos = int(input("1- Bottom right\n2- Up right\n3- Up left\n4- Bottom left\n--> "))
                    if not (numpos >= 1 and numpos <= 4):
                        print("Invalid input.")
                    else:
                        settings["numpos"] = numpos
                        break
                except Exception:
                    print("Value must be integer.")
        elif mode == 3:
            settings["watermark"] = input("Type watermark text or hit enter to no watermark\n--> ").strip()
        elif mode == 4:
            try:
                newDpi = int(input(f"Current DPI is: {settings['dpi']} \nEnter new DPI value or press CRTL C to cancel.\n--> "))
                settings["dpi"] = newDpi
            except KeyboardInterrupt:
                print("Dpi adjustment cancelled.")
                continue
            except Exception:
                print("DPI must be integer.")
        else:
            print("Invalid input.")
    try:
        with open(directory + dataFolder + "/confi.json", "w", encoding="utf-8") as fil:
            dump(settings, fil)
    except OSError:
        print("Make sure './data/confi.json' exists if so, close 'confi.json' and try again.")
        continue
