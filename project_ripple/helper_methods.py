#------------------------------------------------------------------------------------------
#   Ripple / helper_methods
#------------------------------------------------------------------------------------------

import pygame
import numpy
from PIL import Image, ImageFilter

def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolate on the scale given by a to b, using t as the point on that scale.
    Examples
    --------
        50 == lerp(0, 100, 0.5)
        4.2 == lerp(1, 5, 0.8)
    """
    return (1 - t) * a + t * b

def create_neon(surf, huge=False):

    k1 = (13, 13)
    k2 = (7, 7)

    if huge:
        k1 = (41, 41)
        k2 = (7, 7)

    # surf_alpha = surf.convert_alpha()
    # surf_alpha = pygame.transform.rotate(surf_alpha, -90)
    # surf_alpha = pygame.transform.flip(surf_alpha, True, False)

    pil_string_image = pygame.image.tostring(surf,"RGBA",False)
    
    # rgb = pygame.surfarray.array3d(surf_alpha)
    # alpha = pygame.surfarray.array_alpha(surf_alpha).reshape((*rgb.shape[:2], 1))
    # image_array = numpy.concatenate((rgb, alpha), 2)
    image = Image.frombytes("RGBA", surf.get_size(), pil_string_image)
    image = image.filter(ImageFilter.BoxBlur(3))
    # cv2.GaussianBlur(image, ksize=k1, sigmaX=10, sigmaY=10, dst=image)
    # cv2.blur(image, ksize=k2, dst=image)
    image = numpy.array(image)
    bloom_surf = pygame.image.frombuffer(image, (len(image), len(image[0])), 'RGB')
    return bloom_surf
