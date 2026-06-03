import glob
import numpy as np
import re

from load_vk_data import parse_vk6_file
from load_vk_data import parse_vk4_file_stitched_tile
from plot_vk_data import plot_height_data
from tilt_correction import baseplane_filter





def plot_stitched_height_image_from_vk(file_name, mode, overlap_x_um, overlap_y_um):
    '''
    function for plotting the stitched image consisting of VK4 or VK6 file tiles

    Parameters:
    file_name: str, the path to the VK4/VK6 files, file names must correspond to default name by Keyence: 
               'YearMonthDayHourMinuteSecond_Y*_X*.vk4' or 'YearMonthDayHourMinuteSecond_Y*_X*.vk6'
    mode: str, tiles include either original or tilt corrected data, must be either 'orig' or 'tilt_corr'
    overlap_x_um: float, overlap between tiles in x direction in µm
    overlap_y_um: float, overlap between tiles in y direction in µm
    
    Returns:
    ax: matplotlib axis object, the axis object of the plot

    '''
    
    assert mode in ['orig', 'tilt_corr'], 'mode must be either "orig" or "tilt_corr"'
    
    files = glob.glob(file_name)
    tiles = {}

    for f in files:
        
        m = re.search(r"_Y(\d+)_X(\d+)", f)
        
        if m:
            
            y, x = int(m.group(1)), int(m.group(2))

            if f.lower().endswith('.vk6'):
                data_vk6 = parse_vk6_file(f)
                data_vk4 = parse_vk4_file_stitched_tile(data_vk6['Vk4File'])

            elif f.lower().endswith('.vk4'):
                with open(f, 'rb') as vk4_file:
                    data_vk4 = parse_vk4_file_stitched_tile(vk4_file)

            else:
                raise ValueError('File must be .vk4 or .vk6')
            
            calibration = data_vk4['measurement_conditions']['x_length_per_pixel']
            overlap_x_px = int(round(overlap_x_um / (calibration/1e6)))
            overlap_y_px = int(round(overlap_y_um / (calibration/1e6)))
            
            if mode == 'orig':
                img = data_vk4['img_height_data']
                h = img['height']
                w = img['width']
                data = img['data']

                tile = img['data'].reshape(h,w)
                tile = tile[:h-overlap_y_px, :w-overlap_x_px]
                tiles[(y, x)] = tile
                
            else:
                data_vk4_tilt_corr = baseplane_filter(data_vk4, 10)
                img = data_vk4_tilt_corr['img_height_data']
                h = img['height']
                w = img['width']
                data = img['data']

                tile = data_vk4_tilt_corr['baseplane_subtracted'].reshape(h, w)
                tile = tile[:h-overlap_y_px, :w-overlap_x_px]
                tiles[(y, x)] = tile

    
    # grid size
    max_y = max(y for y, _ in tiles)
    max_x = max(x for _, x in tiles)
    
    # big image
    tile_h, tile_w = next(iter(tiles.values())).shape
    big = np.zeros((max_y * tile_h, max_x * tile_w))
    
    # stitch
    for (y, x), tile in tiles.items():
        y0 = (y - 1) * tile_h
        x0 = (x - 1) * tile_w
        big[y0:y0 + tile_h, x0:x0 + tile_w] = tile
    
    # plot    
    height_px, width_px = big.shape
    
    ax = plot_height_data(
        big,
        width_px,
        height_px,
        calibration=calibration,
        colormap='viridis',
        scale='absolute'
    )
    #plt.savefig('Stitched image')

    return ax