import numpy as np

from pathlib import Path

from load_vk_data import parse_vk6_file
from load_vk_data import parse_vk4_file_stitched_tile




def vk_height_to_csv(file_name, output_dir=None):
    '''
    Convert the height data in a single VK4/VK6 file to CSV.

    Parameters:
    file_name : str or path, input VK4 or VK6 file
    output_dir : str or path or None, folder to save CSV; if None, same folder as input file
    
    '''

    file_name = Path(file_name)
    suffix = file_name.suffix.lower()

    if suffix not in [".vk4", ".vk6"]:
        raise ValueError("Only .vk4 or .vk6 files are supported")


    if suffix == ".vk6":
        data_vk6 = parse_vk6_file(str(file_name))
        data_vk4 = parse_vk4_file_stitched_tile(data_vk6["Vk4File"])
    else:
        with open(file_name, "rb") as f:
            data_vk4 = parse_vk4_file_stitched_tile(f)

    img = data_vk4["img_height_data"]

    width = img["width"]
    height = img["height"]
    data = img["data"]

    if data.ndim == 1:
        data = data.reshape((height, width), order="C")

    calib_xy = data_vk4["measurement_conditions"]["x_length_per_pixel"]
    calib_z = data_vk4["measurement_conditions"]["z_length_per_digit"]


    if output_dir is None:
        output_dir = file_name.parent
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{file_name.stem}_csv.csv"


    with open(output_file, "w") as f:
        f.write("Height Data Export\n")
        f.write(f"File,{file_name.name}\n")
        f.write(f"Width,{width}\n")
        f.write(f"Height,{height}\n")
        f.write(f"XY calibration (nm/pixel),{calib_xy}\n")
        f.write(f"Z calibration (nm/digit),{calib_z}\n\n")

        np.savetxt(f, data, delimiter=";", fmt="%.3f")

    return output_file



def convert_vk_folder_to_csv(input_folder, output_folder=None):
    '''
    Convert the height data of all VK4/VK6 files in a folder to CSV.

    Parameters:
    input_folder: str, path to folder with VK4/VK6 files
    output_folder: str, output folder; if None, folder 'csv_output' inside original folder is created
    
    '''

    input_folder = Path(input_folder)

    if output_folder is None:
        output_folder = input_folder / "csv_output"
    else:
        output_folder = Path(output_folder)

    output_folder.mkdir(parents=True, exist_ok=True)

    vk_files = sorted(list(input_folder.glob("*.vk4")) +
                      list(input_folder.glob("*.vk6")))

    if not vk_files:
        raise ValueError("No VK4/VK6 files found in folder")

    for file in vk_files:
        out = vk_height_to_csv(file, output_folder)
        print(f"Saved: {out}")