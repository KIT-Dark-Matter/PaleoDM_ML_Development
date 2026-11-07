import glob
import numpy as np
import re

from pathlib import Path

from scripts_.plot_vk_data import plot_height_data



def plot_stitched_height_image_from_csv_old(file_name, mode, overlap_x_um, overlap_y_um):
    '''
    function for plotting the stitched image consisting of CSV file tiles

    Parameters:
    file_name: str, glob pattern for CSV files
               file names must have ending: '_Y*_X*.csv'

    mode: str, tiles include either original or tilt corrected data,
          must be either 'orig' or 'tilt_corr'

    overlap_x_um: float, overlap between tiles in x direction in µm

    overlap_y_um: float, overlap between tiles in y direction in µm

    Returns:
    ax: matplotlib axis object
    
    '''

    assert mode in ['orig', 'tilt_corr'], 'mode must be either "orig" or "tilt_corr"'

    files = glob.glob(str(file_name))
    files = [Path(f) for f in files]

    tiles = {}

    # calibration assumed identical for all files
    with open(files[0], 'r') as file:
        lines = file.readlines()
    #calibration = float(lines[4].split(',')[1])
    calibration_nm = float(lines[4].split(':')[1].strip())
    calibration = calibration_nm / 1000

    for f in files:

        m = re.search(r"_Y(\d+)_X(\d+)", f.name)

        if m: 
            y, x = int(m.group(1)), int(m.group(2))

            with open(f, 'r') as file:
                lines = file.readlines()

            overlap_x_px = int(round(overlap_x_um / (calibration/1e6)))
            overlap_y_px = int(round(overlap_y_um / (calibration/1e6)))

            data = np.loadtxt(f, delimiter=';', skiprows=6)

            h, w = data.shape

            tile = data[:h - overlap_y_px, :w - overlap_x_px]

            if mode == 'orig':
                pass

            else:
                pass

            tiles[(y, x)] = tile

    # grid size
    #max_y = max(y for y, _ in tiles)
    #max_x = max(x for _, x in tiles)

    ys = [y for y, _ in tiles]
    xs = [x for _, x in tiles]

    min_y, max_y = min(ys), max(ys)
    min_x, max_x = min(xs), max(xs)

    # big image
    #tile_h, tile_w = next(iter(tiles.values())).shape
    #big = np.zeros((max_y * tile_h, max_x * tile_w))

    tile_h, tile_w = next(iter(tiles.values())).shape

    big_h = (max_y - min_y + 1) * tile_h
    big_w = (max_x - min_x + 1) * tile_w

    big = np.full((big_h, big_w), np.nan)

    # stitch
    for (y, x), tile in tiles.items():
        #y0 = (y - 1) * tile_h
        #x0 = (x - 1) * tile_w

        y0 = (y - min_y) * tile_h
        x0 = (x - min_x) * tile_w

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

    return ax


# Chat GPT:
def plot_stitched_height_image_from_csv(
    file_name, mode, overlap_x_um, overlap_y_um):
    assert mode in ['orig', 'tilt_corr']

    files = sorted(Path(f) for f in glob.glob(str(file_name)))

    if not files:
        raise FileNotFoundError(f"No CSV files matched: {file_name}")

    # Calibration from first file (nm/pixel)
    with open(files[0], 'r') as file:
        lines = file.readlines()

    calibration_nm = float(lines[4].split(':')[1].strip())
    calibration = (calibration_nm / 1000, calibration_nm / 1000)  # µm/pixel

    overlap_x_px = int(round(overlap_x_um * 1000 / calibration_nm))
    overlap_y_px = int(round(overlap_y_um * 1000 / calibration_nm))

    tiles = {}

    for f in files:
        m = re.search(r"_Y(\d+)_X(\d+)", f.name)

        if not m:
            continue

        y, x = map(int, m.groups())

        data = np.loadtxt(f, delimiter=';', skiprows=6)

        if data.ndim != 2:
            raise ValueError(f"Unexpected CSV shape in {f}: {data.shape}")

        h, w = data.shape

        if overlap_x_px >= w or overlap_y_px >= h:
            raise ValueError(
                f"Overlap exceeds tile dimensions for {f.name}.\n"
                f"Tile shape: {data.shape}\n"
                f"Overlap: {overlap_y_px} rows, {overlap_x_px} columns\n"
                f"Calibration: {calibration_nm} nm/pixel"
            )

        tiles[(y, x)] = data

    if not tiles:
        raise ValueError("No tiles were loaded. Check the filename pattern.")

    ys = sorted(set(y for y, x in tiles))
    xs = sorted(set(x for y, x in tiles))

    tile_h, tile_w = next(iter(tiles.values())).shape

    # Verify all tiles have equal dimensions
    for key, tile in tiles.items():
        if tile.shape != (tile_h, tile_w):
            raise ValueError(
                f"Tile {key} has shape {tile.shape}; "
                f"expected {(tile_h, tile_w)}"
            )

    if overlap_x_px >= tile_w or overlap_y_px >= tile_h:
        raise ValueError("Overlap is larger than the tile.")

    # Distance between tile origins
    stride_x = tile_w - overlap_x_px
    stride_y = tile_h - overlap_y_px

    big_h = len(ys) * tile_h - (len(ys) - 1) * overlap_y_px
    big_w = len(xs) * tile_w - (len(xs) - 1) * overlap_x_px

    big = np.full((big_h, big_w), np.nan)

    for (y, x), tile in tiles.items():

        row = ys.index(y)
        col = xs.index(x)

        y0 = row * stride_y
        x0 = col * stride_x

        # Remove overlap from top/left of tiles except first row/column
        tile_crop = tile[
            overlap_y_px if row > 0 else 0:,
            overlap_x_px if col > 0 else 0:
        ]

        h, w = tile_crop.shape

        big[y0:y0 + h, x0:x0 + w] = tile_crop

    height_px, width_px = big.shape

    return plot_height_data(
        big,
        width_px,
        height_px,
        calibration=calibration,
        colormap='viridis',
        scale='absolute'
    )