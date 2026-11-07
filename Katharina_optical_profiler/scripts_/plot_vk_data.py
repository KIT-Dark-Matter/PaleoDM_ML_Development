import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import FuncNorm, LinearSegmentedColormap
from matplotlib.ticker import MaxNLocator




def plot_reflected_light(img_array, img_width, img_height, calibration, colormap='gray', scale='absolute'): #271217
    '''
    function for plotting the reflected light image of a VK4 file
    the function uses the plot_reflected_light function to plot the image

    Parameters:
    img_array: np.array, the image data
    img_width: int, the width of the image
    img_height: int, the height of the image
    calibration: int, the calibration value of the image, can be found in the metadata of the VK4 file
    colormap: str, the colormap to use for the plot
    scale: str, the scale of the plot, must be 'absolute' or 'pixels'

    Returns:
    ax: matplotlib axis object, the axis object of the plot
    '''
    assert scale in ['absolute', 'pixels'], 'scale must be either "absolute" or "pixels"'
    fig, ax = plt.subplots(figsize=(8, 8))

    if scale == 'absolute':

        # set axis scale
        width_µm = img_width*calibration[0]/1e6
        height_µm = img_height*calibration[1]/1e6
        if width_µm >= 1000:
            width_µm = width_µm/1e3
            height_µm = height_µm/1e3
            x_label = 'X (mm)'
            y_label = 'Y (mm)'
        else:
            x_label = 'X (µm)'
            y_label = 'Y (µm)'

        ax.imshow(
            img_array, 
            cmap=colormap, 
            extent=[0, width_μm, 
                    0, height_μm]
        )
        #ax.set_xticks(np.linspace(0, img_width-1, 5))
        #ax.set_yticks(np.linspace(0, img_height-1, 5))
        #ax.set_xticklabels(np.round(np.linspace(0, (img_width-1)*calibration/1e6, 5), 2))
        #ax.set_yticklabels(np.round(np.linspace(0, (img_height-1)*calibration/1e6, 5), 2))
        ax.tick_params(axis='both', labelsize=18)
        ax.set_xlabel(x_label, fontsize=20)
        ax.set_ylabel(y_label, fontsize=20)

    else:
        ax.imshow(img_array, cmap=colormap)
        ax.tick_params(axis='both', labelsize=18)
        ax.set_xlabel('X (pixels)', fontsize=20)
        ax.set_ylabel('Y (pixels)', fontsize=20)
    #ax.set_title('Reflected Light Image')

    return ax




def plot_vk4_reflected_light(Vk4File, colormap ='gray', scale='absolute'):
    '''
    function for plotting the reflected light image of a VK4 file
    the function uses the plot_reflected_light function to plot the image

    Parameters:
    Vk4File: dict, a dictionary containing the data of a VK4 file
    colormap: str, the colormap to use for the plot
    scale: str, the scale of the plot, must be 'absolute' or 'pixels'

    Returns:
    ax: matplotlib axis object, the axis object of the plot
    '''

    img_data = Vk4File['img_light_data']
    img_width = img_data['width']
    img_height = img_data['height']
    img_array = img_data['data']

    calibration_x = Vk4File['measurement_conditions']['x_length_per_pixel']
    calibration_y = Vk4File['measurement_conditions']['y_length_per_pixel']
    calibration = [calibration_x, calibration_y]
    img_array = img_array.reshape(img_height, img_width)

    return plot_reflected_light(img_array, img_width, img_height, calibration, colormap, scale)




def plot_height_data(img_array, img_width, img_height, calibration, colormap='viridis', scale='absolute'):
    '''
    function for plotting the height image of a VK4 file

    Parameters:
    img_array: np.array, the image data
    img_width: int, the width of the image
    img_height: int, the height of the image
    calibration: int, the calibration value of the image, can be found in the metadata of the VK4 file
    colormap: str, the colormap to use for the plot
    scale: str, the scale of the plot, must be 'absolute' or 'pixels'

    Returns:
    ax: matplotlib axis object, the axis object of the plot

    zmin = np.min(img_array)
    zmax = np.max(img_array)

    # Breakpoints in data space
    x = np.array([
        zmin,
        -0.1,
        0,
        0.05,
        zmax
    ])

    # Corresponding positions in color space
    # The central -100 to +100 nm region gets 80% of the colors
    y = np.array([
        0.00,
        0.05,
        0.50,
        0.95,
        1.00
    ])

    def forward(v):
        return np.interp(v, x, y)

    def inverse(v):
        return np.interp(v, y, x)

    norm = FuncNorm(
        (forward, inverse),
        vmin=zmin,
        vmax=zmax
    )

    '''
    assert scale in ['absolute', 'pixels'], 'scale must be either "absolute" or "pixels"'

    fig, ax = plt.subplots(figsize=(10, 10))

    #Chat GPT:
    if img_array is None or img_array.size == 0:
        plt.close(fig)
        raise ValueError(
            "img_array is empty. Check the stitching process before plotting."
        )


    # set colorbar scale
    if np.max(np.abs(img_array)) <= 1:
        img_array = img_array*1e3
        cbar_label = 'Height (nm)'
    else:
        cbar_label = 'Height (µm)'

    cmap_enhanced = LinearSegmentedColormap.from_list(
        "low_emphasis",
        ["black", "darkred", "red", "orangered", "darkorange", "orange", "lightgray", "yellow"]#, "orange" #["darkred", "red", "darkorange", "gainsboro", "lightblue"]
    )

    cmap = LinearSegmentedColormap.from_list(
        "low_emphasis",
        ["red", "lightgray", "yellow"]#["darkred", "red", "darkorange", "gainsboro", "lightblue"]
    )

    if scale == 'absolute':
        # set axis scale
        width_µm = img_width*calibration[0]/1e6
        height_µm = img_height*calibration[1]/1e6
        if width_µm >= 1000:
            width_µm = width_µm/1e3
            height_µm = height_µm/1e3
            x_label = 'X (mm)'
            y_label = 'Y (mm)'
        else:
            x_label = 'X (µm)'
            y_label = 'Y (µm)'


        #im = ax.imshow(
        #    img_array,
        #    #norm=norm,
        #    cmap='viridis',#cmap_enhanced,
        #    extent=[0, width_µm,
        #            0, height_µm]
        #)
        im = ax.imshow(
        img_array,
        cmap=colormap,
        extent=[0, width_µm, 0, height_µm]
        )
        ax.tick_params(axis='both', labelsize=18)
        ax.set_xlabel(x_label, fontsize=20)
        ax.set_ylabel(y_label, fontsize=20)

        #ax.set_xticks(np.linspace(0, img_width-1, 10))
        #ax.set_yticks(np.linspace(0, img_height-1, 10))
        #ax.set_xticklabels(np.round(np.linspace(0, (img_width-1)*calibration/1e6, 10), 3))
        #ax.set_yticklabels(np.round(np.linspace(0, (img_height-1)*calibration/1e6, 10), 3))
        
    else:
        im = ax.imshow(img_array, cmap=cmap_enhanced)
        ax.ticks_params(labelsize=18)
        ax.set_xlabel('X (pixels)', fontsize=20)
        ax.set_ylabel('Y (pixels)', fontsize=20)


    # custom axes ticks
    ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5))

    x_ticks = list(ax.get_xticks())
    y_ticks = list(ax.get_yticks())

    x_margin = 0.10 * width_μm
    y_margin = 0.10 * height_μm 

    x_ticks = [t for t in x_ticks if t > x_margin and (width_μm - t) > x_margin]

    y_ticks = [t for t in y_ticks if t > y_margin and (height_μm - t) > y_margin]

    ax.set_xticks([0] + x_ticks + [width_μm])
    ax.set_yticks([0] + y_ticks + [height_μm])

    ax.set_xlim(0, width_μm)
    ax.set_ylim(0, height_μm)


    # custom colorbar ticks
    cbar = fig.colorbar(im, ax=ax, orientation='vertical', shrink=0.6)
    cbar.locator = MaxNLocator(nbins=5)
    cbar.update_ticks()

    vmin = np.nanmin(img_array)
    vmax = np.nanmax(img_array)
    margin = 0.10 * (vmax - vmin)

    ticks = [t for t in cbar.get_ticks() if (t - vmin) > margin and (vmax - t) > margin]
    cbar.set_ticks([vmin] + ticks + [vmax])

    cbar.ax.tick_params(labelsize=18)
    cbar.set_label(cbar_label, fontsize=20) #, rotation=0, loc='bottom')

    #cbar.set_ticks(np.arange(int(np.floor(vmin)), int(np.ceil(vmax))+1, 1))
    #cbar.set_ticks(np.arange(int(np.floor(img_array.min()))+2, int(np.ceil(img_array.max())), 5))
    #ax.set_title('Height Image', fontsize=18)
    
    return ax




def plot_vk4_height(Vk4File, data_type='original', scale='absolute'):

    '''
    function for plotting the height image of a VK4 file
    the function uses the plot_height_data function to plot the image

    Parameters:
    Vk4File: dict, a dictionary containing the data of a VK4 file
    data_type: str, the type of height data to plot, must be 'original', 'baseplane', 'baseplane_fit', 'baseplane_subtracted', 'gaussian_filtered' or 'feature_enhanced'
    colormap: str, the colormap to use for the plot
    scale: str, the scale of the plot, must be 'absolute' or 'pixels'

    Returns:
    ax: matplotlib axis object, the axis object of the plot
    '''

    if data_type == 'original':
        img_array = Vk4File['img_height_data']['data']
    elif data_type == 'baseplane':
        img_array = Vk4File['baseplane']
    elif data_type == 'baseplane_fit':
        img_array = Vk4File['baseplane_fit']
    elif data_type == 'baseplane_subtracted':
        img_array = Vk4File['baseplane_subtracted']
    elif data_type == 'gaussian_filtered':
        img_array = Vk4File['gaussian_filtered']
    elif data_type == 'feature_enhanced':
        img_array = Vk4File['feature_enhanced']
    else:
        raise ValueError('data_type must be either "original", "baseplane", "baseplane_fit", "baseplane_subtracted", "gaussian_filtered" or "feature_enhanced"')
    
    img_width = Vk4File['img_height_data']['width']
    img_height = Vk4File['img_height_data']['height']

    calibration_x = Vk4File['measurement_conditions']['x_length_per_pixel']
    calibration_y = Vk4File['measurement_conditions']['y_length_per_pixel']
    calibration = [calibration_x, calibration_y]

    img_array = img_array.reshape(img_height, img_width)

    return plot_height_data(
    img_array,
    img_width,
    img_height,
    calibration,
    colormap='viridis',
    scale=scale
    )
    #return plot_height_data(img_array, img_width, img_height, calibration, scale)



def reshape_img_data(Vk4File, data_type='original'):

    if data_type == 'original':
        img_array = Vk4File['img_height_data']['data']
    elif data_type == 'baseplane':
        img_array = Vk4File['baseplane']
    elif data_type == 'baseplane_fit':
        img_array = Vk4File['baseplane_fit']
    elif data_type == 'baseplane_subtracted':
        img_array = Vk4File['baseplane_subtracted']
    elif data_type == 'gaussian_filtered':
        img_array = Vk4File['gaussian_filtered']
    elif data_type == 'feature_enhanced':
        img_array = Vk4File['feature_enhanced']
    else:
        raise ValueError('data_type must be either "original", "baseplane", "baseplane_fit", "baseplane_subtracted", "gaussian_filtered" or "feature_enhanced"')

    img_width = Vk4File['img_height_data']['width']
    img_height = Vk4File['img_height_data']['height']

    img_array = img_array.reshape(img_height, img_width)

    return img_array