"""KiCad Footprint Generator for Power Transformers.

Generates standardized KiCad footprint files (.kicad_mod) for power
transformers based on manufacturer specifications.
Creates accurate footprints with appropriate pad dimensions, clearances, and
silkscreen markings for surface mount power transformers with multiple pins.
"""

from pathlib import Path

import symbol_transformer_specs
from footprint_transformer_specs import TRANSFORMER_SPECS, TransformerSpecs
from utilities import footprint_utils


def generate_footprint(
        part_info: symbol_transformer_specs.PartInfo,
        specs: TransformerSpecs,
) -> str:
    """Generate complete KiCad footprint file content for a transformer."""
    body_width = specs.body_dimensions.width
    body_height = specs.body_dimensions.height

    pad_center_x = specs.pad_dimensions.center_x
    pad_width = specs.pad_dimensions.width
    pad_height = specs.pad_dimensions.height
    pad_pitch_y = specs.pad_dimensions.pitch_y
    pins_per_side = specs.pad_dimensions.pin_count//2

    sections = [
        footprint_utils.generate_header(part_info.series),
        footprint_utils.generate_properties(
            specs.ref_offset_y, part_info.series),
        footprint_utils.generate_courtyard(body_width, body_height),
        footprint_utils.generate_fab_rectangle(body_width, body_height),
        footprint_utils.generate_silkscreen_lines(
            body_height, pad_center_x, pad_width),
        footprint_utils.generate_pin_1_indicator(
            pad_center_x, pad_width, pins_per_side, pad_pitch_y),
        footprint_utils.generate_pads(
            pad_width, pad_height, pad_center_x, pad_pitch_y, pins_per_side),
        footprint_utils.associate_3d_model(
            "KiCAD_Symbol_Generator/3D_models", part_info.series),
        ")",  # Close the footprint
    ]
    return "\n".join(sections)


def generate_footprint_file(
        part_info: symbol_transformer_specs.PartInfo,
        output_dir: str,
) -> None:
    """Generate and save a complete .kicad_mod file for a transformer."""
    if part_info.series not in TRANSFORMER_SPECS:
        msg = f"Unknown series: {part_info.series}"
        raise ValueError(msg)

    specs = TRANSFORMER_SPECS[part_info.series]
    if specs.pad_dimensions.pin_count % 2 != 0:
        msg = "Pin count must be even"
        raise ValueError(msg)

    footprint_content = generate_footprint(part_info, specs)

    filename = f"{output_dir}/{part_info.series}.kicad_mod"
    with Path.open(filename, "w", encoding="utf-8") as file_handle:
        file_handle.write(footprint_content)
