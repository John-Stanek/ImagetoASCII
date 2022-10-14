from tkinter import Tk,Canvas,Button
from PIL import Image
from tkinter import filedialog

def open_img(w,h):
    canvas.delete("text")
    x = openfilename()

    img = Image.open(x)
    img_size_w = w // const_scale
    img_size_h = h // const_scale
    #resize to roughly 300x300
    img = img.resize((img_size_w,img_size_h),Image.NEAREST )

    create_pixelated_image(img)
    
def openfilename():
    filename = filedialog.askopenfilename(title = '"pen')
    return filename

def rgbtohex(r,g,b):
    #convert rgb value to Tkinter color value in hex format
    return f'#{r:02x}{g:02x}{b:02x}'

def map_rgb_to_index(val,list_length):
    #val in range 0 - 255
    #index in range 0 - n
    """
    ex: if len = 10, rgb=0 => index=0
    rgb=255 => index=10

    to do this, divide by ratio of 255/list_length
    """
    
    temp = 255 // (list_length)+1
    if temp == 0:
        return 0
    return val // temp

def create_pixelated_image(img):
    #light to dark ascii chars
    #pad beginning with more spaces to capture less background color
    density = "    _.,-=+:;cba!?0123456789$W#@Ñ"
    
    pixels = list(img.getdata())
    width,height = img.size
    pixels = [pixels[i * width: (i+1) * width] for i in range(height)]

    for j,p in enumerate(pixels):
        for i,pixel in enumerate(pixels[j]):
            r = pixel[0]
            g = pixel[1]
            b = pixel[2]
        
            avg = (r + g + b)//3

            """Create pixelated image with code below"""
            #color = rgbtohex(avg,avg,avg)
            #canvas.create_rectangle(i,j,i+1,j+1, fill=color,width=0)

            """Create pixelated image with char determining color instead of actual color"""
            charindex = map_rgb_to_index(avg,len(density))
            ch = density[charindex]
            canvas.create_text(i*const_scale,j*const_scale,text = ch, fill="white",justify="center",tags=["text"],font=("Courier",const_scale))
    canvas.pack()

def main():
    #set up image window
    h,w = 400,400
    root = Tk()
    root.title("Image Loader")
    root.geometry(f"{w}x{h}")

    #scale to make large letters at offset in canvas
    global const_scale
    const_scale = 10

    global canvas
    canvas = Canvas(root, width=w*const_scale, height = h*const_scale,background="black")

    #allow resizable window
    root.resizable(width=True,height=True)

    #button to open new image
    btn = Button(root,text='open image', command=lambda: (open_img(w,h)))
    btn.pack()
    root.mainloop()

if __name__ == "__main__":
    main()
