import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from skimage.filters import difference_of_gaussians
from skimage import exposure
from skimage.morphology import opening, disk, closing, black_tophat, white_tophat




def gaussian_filter_height(Vk4File, sigma):

    background = gaussian_filter(Vk4File['baseplane_subtracted'], sigma=sigma)
    detail = Vk4File['baseplane_subtracted'] - background

    Vk4File['gaussian_filtered'] = detail

    return Vk4File



def feature_enhancement_proceedings(Vk4File):

    detail = gaussian_filter_height(Vk4File, sigma=5)['gaussian_filtered']

    p_low, p_high = np.percentile(Vk4File['baseplane_subtracted'], (1, 99))

    detail =  np.clip(detail, p_low, p_high)


    Vk4File['feature_enhanced'] = detail

    return Vk4File



def feature_enhancement_1(Vk4File):

    detail = gaussian_filter_height(Vk4File, sigma=5)['gaussian_filtered']

    #p_low, p_high = np.percentile(detail, (1, 99))
    #height_plot = np.ma.masked_outside(Vk4File['baseplane_subtracted'], np.min(Vk4File['baseplane_subtracted']), 1)

    detail = np.clip(detail, a_min=-0.1, a_max=0.1)#a_min=None, a_max=0.14)

    Vk4File['feature_enhanced'] = detail #masked_data #height_plot

    return Vk4File



def feature_enhancement_2(Vk4File):

    detail = gaussian_filter_height(Vk4File, sigma=5)['gaussian_filtered']

    #p_low, p_high = np.percentile(Vk4File['baseplane_subtracted'], (1, 99))
    #height_plot = np.ma.masked_outside(Vk4File['baseplane_subtracted'], np.min(Vk4File['baseplane_subtracted']), 1)

    detail =  np.clip(detail, a_min=-0.15, a_max=0)

    Vk4File['feature_enhanced'] = detail #masked_data #height_plot

    return Vk4File




def feature_enhancement_3(Vk4File):

    detail = gaussian_filter_height(Vk4File, sigma=5)['gaussian_filtered']

    #p_low, p_high = np.percentile(Vk4File['baseplane_subtracted'], (1, 99))
    #height_plot = np.ma.masked_outside(Vk4File['baseplane_subtracted'], np.min(Vk4File['baseplane_subtracted']), 1)

    p_low, p_high = np.percentile(detail, (1, 90))
    detail =  np.clip(detail, p_low, p_high)

    #masked_data = np.where((detail >= -0.005), np.mean(detail), detail) 


    Vk4File['feature_enhanced'] = detail #masked_data #height_plot

    return Vk4File



def feature_enhancement_single_gaussian_clip(Vk4File):

    background = gaussian_filter(Vk4File['baseplane_subtracted'], sigma=5)
    detail = Vk4File['baseplane_subtracted'] - background

    p_low, p_high = np.percentile(detail, (1, 87))
    detail =  np.clip(detail, p_low, p_high)

    Vk4File['feature_enhanced'] = detail

    return Vk4File




def feature_enhancement_double_gaussian_clip(Vk4File):

    background = gaussian_filter(Vk4File['baseplane_subtracted'], sigma=300) # remove large topography
    detail = Vk4File['baseplane_subtracted'] - background

    background2 = gaussian_filter(Vk4File['baseplane_subtracted'], sigma=5) # enhance small features
    detail2 = detail - background2

    p_low, p_high = np.percentile(detail2, (1, 87))
    detail2 = np.clip(detail2, p_low, p_high)


    Vk4File['feature_enhanced'] = detail2

    return Vk4File



def feature_enhancement_triple_gaussian_clip(Vk4File):

    background = gaussian_filter(Vk4File['baseplane_subtracted'], sigma=300)
    detail = Vk4File['baseplane_subtracted'] - background

    background2 = gaussian_filter(Vk4File['baseplane_subtracted'], sigma=20)
    detail2 = detail - background2

    background3 = gaussian_filter(Vk4File['baseplane_subtracted'], sigma=5)
    detail3 = detail2 - background3


    p_low, p_high = np.percentile(detail3, (1, 87))
    detail3 = np.clip(detail3, p_low, p_high)


    Vk4File['feature_enhanced'] = detail3

    return Vk4File



def feature_enhancement_single_gaussian_median_clip(Vk4File):

    background = gaussian_filter(Vk4File['baseplane_subtracted'], sigma=5)
    detail = Vk4File['baseplane_subtracted'] - background

    median = np.median(detail)
    p_low, p_high = np.percentile(detail, (1, 90))

    # Replace values above and below percentiles with the median
    clipped = np.where((detail <= p_low) | (detail >= p_high), median, detail)


    Vk4File['feature_enhanced'] = clipped

    return Vk4File




def feature_enhancement_double_gaussian_median_clip(Vk4File):

    background = gaussian_filter(Vk4File['baseplane_subtracted'], sigma=300)
    detail = Vk4File['baseplane_subtracted'] - background

    background2 = gaussian_filter(Vk4File['baseplane_subtracted'], sigma=5)
    detail2 = detail - background2

    median = np.median(detail2)
    p_low, p_high = np.percentile(detail2, (1, 87))

    # Replace values above and below percentiles with the median
    clipped = np.where((detail2 >= p_low) & (detail2 <= p_high), detail2, median)


    Vk4File['feature_enhanced'] = clipped

    return Vk4File



def feature_enhancement_median_clip_high(Vk4File):

    background = gaussian_filter(Vk4File['baseplane_subtracted'], sigma=5)
    detail = Vk4File['baseplane_subtracted'] - background

    median = np.median(detail)
    threshold = np.percentile(detail, 87)

    # Replace values above threshold percentile with the median
    clipped = np.where((detail >= threshold), detail, median)


    Vk4File['feature_enhanced'] = clipped

    return Vk4File



def feature_enhancement_cut_elevations_and_holes(Vk4File):

    background = gaussian_filter(Vk4File['baseplane_subtracted'], sigma=5)
    detail = Vk4File['baseplane_subtracted'] - background

    # cut away elevations (everything that's still above baseplane)
    detail = np.minimum(detail, 0)

    # cut away very deep holes
    p1 = np.percentile(detail, 0.5)
    detail = np.maximum(detail, p1)


    Vk4File['feature_enhanced'] = detail


    return Vk4File



def feature_enhancement_cut_elevations_and_holes_2(Vk4File):

    background = gaussian_filter(Vk4File['baseplane_subtracted'], sigma=5)
    detail = background - Vk4File['baseplane_subtracted']

    # cut away elevations (everything that's still above baseplane)
    detail = np.clip(detail, 0, None)

    # cut away very deep holes
    p1 = np.percentile(detail, 99.5)
    detail = np.minimum(detail, p1)


    Vk4File['feature_enhanced'] = detail


    return Vk4File




def feature_enhancement_morphological(Vk4File, max_feature_radius=2):
    """Isolates narrow scratches and small holes regardless of underlying multi-scale surface structures.

    Parameters:
        max_feature_radius (int): Approximate radius (in pixels) of the largest scratch or hole you want to detect.
    """
    height_data = feature_enhancement_cut_elevations_and_holes(Vk4File)['feature_enhanced']

    # Create a circular structuring element larger than the widest 
    selem = disk(max_feature_radius)

    # Black top-hat isolates small features
    scratches_and_holes = black_tophat(height_data, selem)

    Vk4File['feature_enhanced'] = scratches_and_holes

    return Vk4File


def feature_enhancement_diff_gaussians(Vk4File):

    detail = difference_of_gaussians(Vk4File['baseplane_subtracted'], low_sigma=1, high_sigma=5)

    #median = np.median(detail)
    p_low, p_high = np.percentile(detail, (1, 87))

    clipped = np.clip(detail, p_low, p_high)


    # Stretch contrast for visualization
    #detail = exposure.equalize_adapthist(detail, clip_limit=0.03)
    clipped = exposure.equalize_adapthist(clipped, clip_limit=0.03)

    Vk4File['feature_enhanced'] = detail #clipped

    return Vk4File


# Chat GPT
def feature_enhancement_stretch_contrast(Vk4File):

    p_1, p_99 = np.percentile(
        Vk4File['baseplane_subtracted'], (1, 99)
    )

    stretched = exposure.rescale_intensity(
        Vk4File['baseplane_subtracted'],
        in_range=(p_1, p_99)
    )

    Vk4File['feature_enhanced'] = stretched

    return Vk4File

def feature_enhancement_stretch_contrast_old(Vk4File):

    p_1, p_99 = np.percentile(Vk4File['baseplane_subtracted'], (1, 99))
    stretched = exposure.rescale_intensity(Vk4File['baseplane_subtracted'], in_range=(p_1, p_99))

    return stretched




    # Only keep local depressions
    #residual = np.minimum(residual, 0)

    # Remove shallow ones
    #residual[residual > -0.5] = 0 

    #sigma = 1        # pixels, adjust depending on feature size

    #background = gaussian_filter(Vk4File['baseplane_subtracted'], sigma=sigma) # ['img_height_data']['data']

    #detail = Vk4File['baseplane_subtracted'] - background

    #filtered = difference_of_gaussians(
    #Vk4File['baseplane_subtracted'],
    #low_sigma=1,
    #high_sigma=5
#)

    #background = opening(Vk4File['baseplane_subtracted'], disk(20))
    #background = closing(Vk4File['baseplane_subtracted'], disk(20))

    #detail = Vk4File['baseplane_subtracted'] - background

    #holes = black_tophat(detail, disk(30))

    # Remove broad background
    #background = gaussian_filter(Vk4File['baseplane_subtracted'], sigma=5)
    #detail = Vk4File['baseplane_subtracted'] - background

    #median = np.mean(detail)

    #lower = np.percentile(detail, 2)     # keep only deepest 2%
    #upper = np.percentile(detail, 99.9)  # remove nearly all peaks

    #filtered = detail.copy()
    #filtered[filtered > upper] = median
    #filtered[filtered < lower] = median

    #median = np.median(Vk4File['baseplane_subtracted'])

    #filtered = Vk4File['baseplane_subtracted'].copy()

    #threshold = np.percentile(Vk4File['baseplane_subtracted'], 99)  # top 1%
    #filtered[filtered > threshold] = median

    # Keep only a desired spatial scale
    #detail = difference_of_gaussians(detail, low_sigma=1, high_sigma=4)

    # Stretch contrast for visualization
    #detail = exposure.equalize_adapthist(detail)

    #limit = np.percentile(np.abs(residual), 99)
    #detail = np.clip(residual, -limit, limit)

    #detail = np.clip(detail, -0.1, 0.1)