"""KiCad Footprint Generator for Diodes.

Generates standardized KiCad footprint files (.kicad_mod) for diodes
based on manufacturer specifications. Creates accurate footprints with
appropriate pad dimensions, clearances, and silkscreen markings for surface
mount diodes.
"""

from pathlib import Path

import symbol_transistor_specs
from footprint_transistor_specs import DIODE_SPECS, DiodeSpecs
from utilities import footprint_utils


def generate_footprint(
        part_info: symbol_transistor_specs.PartInfo,
        specs: DiodeSpecs,
) -> str:
    """Generate complete KiCad footprint file content for a diode.

    Args:
        part_info: Component specifications
        specs: Physical specifications for the diode series from DIODE_SPECS

    Returns:
        Complete .kicad_mod file content as formatted string

    """
    body_width = specs.body_dimensions.width
    body_height = specs.body_dimensions.height
    pad_width = specs.pad_dimensions.width
    pad_height = specs.pad_dimensions.height
    pad_center_x = specs.pad_dimensions.pad_center_x
    pad_pitch_y = specs.pad_dimensions.pad_pitch_y
    pins_per_side = specs.pad_dimensions.pins_per_side
    thermal_pad_width = specs.pad_dimensions.thermal_width
    thermal_pad_height = specs.pad_dimensions.thermal_height
    thermal_pad_center_x = specs.pad_dimensions.thermal_pad_center_x

    sections = [
        footprint_utils.generate_header(part_info.package),
        footprint_utils.generate_properties(
            specs.ref_offset_y, part_info.package),
        footprint_utils.generate_courtyard(body_width, body_height),
        footprint_utils.generate_fab_rectangle(body_width, body_height),
        footprint_utils.generate_pads(
            pad_width, pad_height, pad_center_x, pad_pitch_y, pins_per_side,
            [1, 2, 3, 4, 5, 5, 5, 5]),
        footprint_utils.generate_thermal_pad(
            5, thermal_pad_width, thermal_pad_height, thermal_pad_center_x),
        footprint_utils.associate_3d_model(
            "KiCAD_Symbol_Generator/3D_models", part_info.package),
        ")",  # Close the footprint
    ]
    return "\n".join(sections)


def generate_footprint_file(
        part_info: symbol_transistor_specs.PartInfo,
        output_path: str,
) -> None:
    """Generate and save a complete .kicad_mod file for a diode.

    Args:
        part_info: Component specifications including MPN and package type
        output_path: Directory path where the footprint file will be saved

    """
    specs = DIODE_SPECS[part_info.package]
    footprint_content = generate_footprint(part_info, specs)
    filename = f"{part_info.package}.kicad_mod"
    file_path = f"{output_path}/{filename}"

    with Path.open(file_path, "w", encoding="utf-8") as file_handle:
        file_handle.write(footprint_content)
