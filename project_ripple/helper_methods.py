#------------------------------------------------------------------------------------------
#   Ripple / helper_methods
#------------------------------------------------------------------------------------------

import pygame
import numpy
from PIL import Image, ImageFilter
import importlib
import platformdirs
import os

def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolate on the scale given by a to b, using t as the point on that scale.
    Examples
    --------
        50 == lerp(0, 100, 0.5)
        4.2 == lerp(1, 5, 0.8)
    """
    return (1 - t) * a + t * b

def create_neon(surf, huge=False):
    pil_string_image = pygame.image.tostring(surf,"RGBA",False)
    
    image = Image.frombytes("RGBA", surf.get_size(), pil_string_image)
    image = image.filter(ImageFilter.BoxBlur(5))
    image = numpy.array(image)
    bloom_surf = pygame.image.frombuffer(image, (len(image[0]), len(image)), 'RGBA')
    return bloom_surf

def resource(relative_path):
    path = importlib.resources.files("project_ripple").joinpath(relative_path)
    return path

# Can only run once. Might improve performance
def create_user_dir():
    user_path = platformdirs.user_data_dir("Project-Ripple")
    if not os.path.exists(user_path):
        os.makedirs(user_path)
    create_user_dir.__code__ = (lambda:None).__code__

def user_dir(relative_path):
    create_user_dir()
    user_path = platformdirs.user_data_dir("Project-Ripple")
    path = user_path + "/" + relative_path
    return path
