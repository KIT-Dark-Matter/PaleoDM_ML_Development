import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter



def feature_enhancement(Vk4File):

    sigma = 5         # pixels, adjust depending on feature size
    background = gaussian_filter(Vk4File['baseplane_subtracted'], sigma=sigma)

    detail = Vk4File['baseplane_subtracted'] - background
    detail = np.clip(detail, -0.1, 0.1)
    Vk4File['feature_enhanced'] = detail

    return Vk4File