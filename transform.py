from PIL import Image, ImageStat, ImageEnhance, ImageOps, ImageFilter
import numpy as np

class ImageTransformer:
    def __init__(self, target_size=600):
        self.target_size = (target_size, target_size)

    def _auto_brighten(self, img, threshold=100, factor=1.5):
        grayscale = img.convert('L')
        if ImageStat.Stat(grayscale).mean[0] < threshold:
            return ImageEnhance.Brightness(img).enhance(factor)
        return img

    def _remove_noise(self, img):
        return img.filter(ImageFilter.MedianFilter(size=3))

    def _sharpen_if_needed(self, img, blur_threshold=20, sharpen_factor=2.0):
        grayscale = img.convert('L')
        edges = grayscale.filter(ImageFilter.FIND_EDGES)
        if ImageStat.Stat(edges).mean[0] < blur_threshold:
            return ImageEnhance.Sharpness(img).enhance(sharpen_factor)
        return img

    
    def process(self, img):
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        img = ImageOps.pad(img, self.target_size, method=Image.Resampling.LANCZOS, color=(0, 0, 0))
        img = self._auto_brighten(img)
        img = self._remove_noise(img)
        img = self._sharpen_if_needed(img)
        
        return np.array(img)