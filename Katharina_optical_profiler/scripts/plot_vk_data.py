import numpy as np
import matplotlib.pyplot as plt




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
    fig, ax = plt.subplots()
    ax.imshow(img_array, cmap=colormap)
    if scale == 'absolute':
        ax.set_xticks(np.linspace(0, img_width-1, 5))
        ax.set_yticks(np.linspace(0, img_height-1, 5))
        ax.set_xticklabels(np.round(np.linspace(0, (img_width-1)*calibration/1e6, 5), 2))
        ax.set_yticklabels(np.round(np.linspace(0, (img_height-1)*calibration/1e6, 5), 2))
        ax.set_xlabel('X (µm)', fontsize=12)
        ax.set_ylabel('Y (µm)', fontsize=12)
    else:
        ax.set_xlabel('X (pixels)', fontsize=12)
        ax.set_ylabel('Y (pixels)', fontsize=12)
    ax.set_title('Reflected Light image')

    return ax




def plot_vk4_reflected_light(Vk4File, colormap = 'gray', scale='absolute'):
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

    calibration = Vk4File['measurement_conditions']['x_length_per_pixel']
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
    '''
    assert scale in ['absolute', 'pixels'], 'scale must be either "absolute" or "pixels"'
    fig, ax = plt.subplots(figsize=(15, 15))


    if scale == 'absolute':
        im = ax.imshow(
            img_array,
            cmap=colormap,
            extent=[0, img_width*calibration/1e6,
                    0, img_height*calibration/1e6]
        )
        ax.set_xlabel('X (µm)', fontsize=12)
        ax.set_ylabel('Y (µm)', fontsize=12)

        # ax.set_xticks(np.linspace(0, img_width-1, 10))
        # ax.set_yticks(np.linspace(0, img_height-1, 10))
        # ax.set_xticklabels(np.round(np.linspace(0, (img_width-1)*calibration/1e6, 10), 3))
        # ax.set_yticklabels(np.round(np.linspace(0, (img_height-1)*calibration/1e6, 10), 3))
        
    else:
        im = ax.imshow(img_array, cmap=colormap)
        ax.set_xlabel('X (pixels)', fontsize=12)
        ax.set_ylabel('Y (pixels)', fontsize=12)
        

    cbar = fig.colorbar(im, ax=ax, label='Height (µm)', orientation='vertical', shrink=0.5)
    cbar.set_ticks(np.arange(int(np.floor(img_array.min()))+2, int(np.ceil(img_array.max())), 5))
    ax.set_title('Height image')
    
    return ax




def plot_vk4_height(Vk4File, data_type='original', colormap = 'viridis', scale='absolute'):
    '''
    function for plotting the height image of a VK4 file
    the function uses the plot_height_data function to plot the image

    Parameters:
    Vk4File: dict, a dictionary containing the data of a VK4 file
    data_type: str, the type of height data to plot, must be 'original', 'baseplane', 'baseplane_fit', or 'baseplane_subtracted'
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
    else:
        raise ValueError('data_type must be either "original", "baseplane", "baseplane_fit", or "baseplane_subtracted"')
    
    img_width = Vk4File['img_height_data']['width']
    img_height = Vk4File['img_height_data']['height']

    calibration = Vk4File['measurement_conditions']['x_length_per_pixel']
    img_array = img_array.reshape(img_height, img_width)

    return plot_height_data(img_array, img_width, img_height, calibration, colormap, scale)
