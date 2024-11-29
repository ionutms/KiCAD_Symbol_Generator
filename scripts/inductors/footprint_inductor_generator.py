"""KiCad Footprint Generator for Power Inductors.

Generates standardized KiCad footprint files (.kicad_mod) for power inductors
based on manufacturer specifications. Creates accurate footprints with
appropriate pad dimensions, clearances, and silkscreen markings for surface
mount power inductors.
"""

from pathlib import Path
from uuid import uuid4

import symbol_inductors_specs
from footprint_inductor_specs import INDUCTOR_SPECS, InductorSpecs
from utilities import footprint_utils


def generate_footprint(
        part_info: symbol_inductors_specs.PartInfo,
        specs: InductorSpecs,
) -> str:
    """Generate complete KiCad footprint file content for an inductor.

    Args:
        part_info: Component specifications
        specs:
            Physical specifications for the inductor series
            from INDUCTOR_SPECS

    Returns:
        Complete .kicad_mod file content as formatted string

    """
    body_width = specs.body_dimensions.width
    body_height = specs.body_dimensions.height

    pad_center_x = specs.pad_dimensions.center_x
    pad_width = specs.pad_dimensions.width
    pad_height = specs.pad_dimensions.height

    sections = [
        footprint_utils.generate_header(part_info.series),
        footprint_utils.generate_properties(
            specs.ref_offset_y, part_info.series),
        footprint_utils.generate_courtyard(body_width, body_height),
        footprint_utils.generate_fab_rectangle(body_width, body_height),
        footprint_utils.generate_silkscreen_lines(
            body_height, pad_center_x, pad_width),
        footprint_utils.generate_pin_1_indicator(pad_center_x, pad_width),
        footprint_utils.generate_pads(pad_width, pad_height, pad_center_x),
        footprint_utils.associate_3d_model(
            "KiCAD_Symbol_Generator/3D_models", part_info.series),
        ")",  # Close the footprint
    ]
    return "\n".join(sections)


def generate_pads(specs: InductorSpecs) -> str:
    """Generate the pads section of the footprint."""
    pads = []
    pad_center_x = specs.pad_dimensions.center_x
    pad_width = specs.pad_dimensions.width
    pad_height = specs.pad_dimensions.height

    for pad_number, symbol in enumerate(["-", ""], start=1):
        pads.append(f"""
            (pad "{pad_number}" smd rect
                (at {symbol}{pad_center_x} 0)
                (size {pad_width} {pad_height})
                (layers "F.Cu" "F.Paste" "F.Mask")
                (uuid "{uuid4()}")
            )
            """)

    return "\n".join(pads)


def generate_footprint_file(
        part_info: symbol_inductors_specs.PartInfo,
        output_path: str,
) -> None:
    """Generate and save a complete .kicad_mod file for an inductor.

    Args:
        part_info: Component specifications including MPN and series
        output_path: Directory path where the footprint file will be saved

    """
    specs = INDUCTOR_SPECS[part_info.series]
    footprint_content = generate_footprint(part_info, specs)
    filename = f"{part_info.series}.kicad_mod"
    file_path = f"{output_path}/{filename}"

    with Path.open(file_path, "w", encoding="utf-8") as file_handle:
        file_handle.write(footprint_content)
