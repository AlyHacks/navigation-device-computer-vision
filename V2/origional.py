
import time
import vl53l5cx_ctypes as vl53l5cx
import ST7789
import numpy
from PIL import Image
from matplotlib import cm
import numpy as np

COLOR_MAP = "plasma"
INVERSE = True

'''
def get_palette(name):
    cmap = cm.get_cmap(name, 256)

    try:
        colors = cmap.colors
    except AttributeError:
        colors = numpy.array([cmap(i) for i in range(256)], dtype=float)

    arr = numpy.array(colors * 255).astype('uint8')
    arr = arr.reshape((16, 16, 4))
    arr = arr[:, :, 0:3]
    return arr.tobytes()


display = ST7789.ST7789(
    width=240,
    height=240,
    rotation=90,
    port=0,
    cs=ST7789.BG_SPI_CS_BACK,  # Otherwise it will block the sensor!
    dc=9,
    backlight=18,
    spi_speed_hz=80 * 1000 * 1000,
    offset_left=0,
    offset_top=0
)

pal = get_palette(COLOR_MAP)

print("Uploading firmware, please wait...")
vl53 = vl53l5cx.VL53L5CX()
print("Done!")
vl53.set_resolution(8 * 8)
'''

vl53 = vl53l5cx.VL53L5CX()
# This is a visual demo, so prefer speed over accuracy
vl53.set_ranging_frequency_hz(15)
vl53.set_integration_time_ms(20)
vl53.start_ranging()


while True:
    true_cnt = 0
    if vl53.data_ready():
        data = vl53.get_data()
        arr = np.flipud(np.array(data.distance_mm).reshape((8, 8))).astype('float64')

        min_distance = arr.min()
        
        min_position = np.argwhere(arr == min_distance)
        row, column = np.where(arr == min_distance)

        if column >= 0 and column <= 3:
            print("Object is on the left side of the sensor")
        elif column >= 4 and column <= 7:
            print("Object is on the right side of the sensor")
        
        if abs(min_position-(arr[row+1, column] or arr[row-1, column] or arr[row, column+1] or arr[row, column-1])) <= 10:
            true_cnt += 1
        if true_cnt >= 3:
            #obtain position of the object since 
            print("Object is centered in front of the sensor")
        # Scale view relative to the furthest distance
        # distance = arr.max()

        # Scale view to a fixed distance
        distance = 512

        # Scale and clip the result to 0-255
        arr *= (255.0 / distance)
        arr = np.clip(arr, 0, 255)

        # Invert the array : 0 - 255 becomes 255 - 0
        if INVERSE:
            arr *= -1
            arr += 255.0

        # Force to int
        arr = arr.astype('uint8')


    time.sleep(0.01)  # Avoid polling *too* fast

'''
        # Convert to a palette type image
        img = Image.frombytes("P", (8, 8), arr)
        img.putpalette(pal)
        img = img.convert("RGB")
        img = img.resize((240, 240), resample=Image.NEAREST)

        # Display the result
        display.display(img)
'''

