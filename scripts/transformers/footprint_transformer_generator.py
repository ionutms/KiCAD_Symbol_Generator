"""KiCad Footprint Generator for Power Transformers.

Generates standardized KiCad footprint files (.kicad_mod) for power
transformers based on manufacturer specifications.
Creates accurate footprints with appropriate pad dimensions, clearances, and
silkscreen markings for surface mount power transformers with multiple pins.
"""

from pathlib import Path
from uuid import uuid4

import symbol_transformer_specs as sti
from footprint_transformer_specs import TRANSFORMER_SPECS, TransformerSpecs
from utilities import footprint_utils as fu


def generate_footprint(
        part_info: sti.PartInfo, specs: TransformerSpecs,
) -> str:
    """Generate complete KiCad footprint file content for a transformer."""
    sections = [
        fu.generate_header(part_info.series),
        fu.generate_properties(specs.ref_offset_y, part_info.series),
        fu.generate_courtyard(
            specs.body_dimensions.width,
            specs.body_dimensions.height),
        fu.generate_fab_rectangle(
            specs.body_dimensions.width,
            specs.body_dimensions.height),
        fu.generate_silkscreen_lines(
            specs.body_dimensions.height,
            specs.pad_dimensions.center_x,
            specs.pad_dimensions.width),
        generate_shapes(specs),
        generate_pads(specs),
        fu.associate_3d_model(
            "KiCAD_Symbol_Generator/3D_models", part_info.series),
        ")",  # Close the footprint
    ]
    return "\n".join(sections)


def generate_shapes(specs: TransformerSpecs) -> str:
    """Generate the shapes section of the footprint."""
    shapes = []

    # Pin 1 indicator position
    pins_per_side = specs.pad_dimensions.pin_count // 2
    total_height = specs.pad_dimensions.pitch_y * (pins_per_side - 1)
    circle_x = -(specs.pad_dimensions.center_x + specs.pad_dimensions.width)
    circle_y = -total_height / 2
    radius = specs.pad_dimensions.height / 4

    # Pin 1 indicator on silkscreen
    shapes.append(f"""
        (fp_circle
            (center {circle_x} {circle_y})
            (end {circle_x - radius} {circle_y})
            (stroke (width 0.1524) (type solid))
            (fill solid)
            (layer "F.SilkS")
            (uuid "{uuid4()}")
        )
        """)

    return "\n".join(shapes)


def calculate_pad_positions(
        specs: TransformerSpecs,
) -> list[tuple[float, float]]:
    """Calculate positions for all pads based on pin count."""
    pins_per_side = specs.pad_dimensions.pin_count // 2
    total_height = specs.pad_dimensions.pitch_y * (pins_per_side - 1)
    positions = []

    # Left side pads
    for i in range(pins_per_side):
        y_pos = -total_height/2 + i * specs.pad_dimensions.pitch_y
        positions.append((-specs.pad_dimensions.center_x, y_pos))

    # Right side pads (bottom to top)
    for i in range(pins_per_side):
        y_pos = total_height/2 - i * specs.pad_dimensions.pitch_y
        positions.append((specs.pad_dimensions.center_x, y_pos))

    return positions


def generate_pads(specs: TransformerSpecs) -> str:
    """Generate the pads section of the footprint."""
    pads = []
    pad_positions = calculate_pad_positions(specs)
    pad_width = specs.pad_dimensions.width
    pad_heigh = specs.pad_dimensions.height

    for pad_number, (x_pos, y_pos) in enumerate(pad_positions, 1):
        pads.append(f"""
            (pad "{pad_number}" smd rect
                (at {x_pos} {y_pos})
                (size {pad_width} {pad_heigh})
                (layers "F.Cu" "F.Paste" "F.Mask")
                (uuid "{uuid4()}")
            )
            """)

    return "\n".join(pads)


def generate_footprint_file(part_info: sti.PartInfo, output_dir: str) -> None:
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
