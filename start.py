import tesserocr
from PIL import Image

image = Image.open('image2.png')
result = tesserocr.image_to_text(image)
print(result) ### wrong, the correct answer is 7364

import numpy as np
image = image.resize((image.width * 3, image.height * 3), Image.BICUBIC)

# print(np.array(image).shape)
# print(image.mode)

image = image.convert('L')
# threshold = 180
threshold = 100

array = np.array(image)
array = np.where(array > threshold, 255, 0)
# array = 255 - array
# array = np.minimum(array + 60, 255)
image = Image.fromarray(array.astype('uint8'))

image.show()

print(tesserocr.image_to_text(
    image,
    psm=tesserocr.PSM.SINGLE_LINE))


with tesserocr.PyTessBaseAPI(psm=tesserocr.PSM.SINGLE_LINE) as api:
    api.SetVariable('tessedit_char_whitelist', '0123456789')  
    api.SetImage(image)
    result = api.GetUTF8Text()

print(result.strip())


