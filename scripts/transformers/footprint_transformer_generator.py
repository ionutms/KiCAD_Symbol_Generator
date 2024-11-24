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


def generate_footprint(
        part_info: sti.PartInfo, specs: TransformerSpecs,
) -> str:
    """Generate complete KiCad footprint file content for a transformer."""
    sections = [
        generate_header(part_info.series),
        generate_properties(part_info, specs),
        generate_shapes(specs),
        generate_pads(specs),
        generate_3d_model(part_info),
        ")",  # Close the footprint
    ]
    return "\n".join(sections)


def generate_header(model_name: str) -> str:
    """Generate the footprint header section."""
    return (
        f'(footprint "{model_name}"\n'
        '    (version 20240108)\n'
        '    (generator "pcbnew")\n'
        '    (generator_version "8.0")\n'
        '    (layer "F.Cu")\n'
        '    (descr "")\n'
        '    (tags "")\n'
        '    (attr smd)'
    )


def generate_properties(
        part_info: sti.PartInfo, specs: TransformerSpecs,
) -> str:
    """Generate the properties section of the footprint."""
    font_props = (
        "        (effects\n"
        "            (font\n"
        "                (size 0.762 0.762)\n"
        "                (thickness 0.1524)\n"
        "            )\n"
        "            (justify left)\n"
        "        )"
    )

    ref_offset_y = specs.ref_offset_y

    return (
        '    (property "Reference" "REF**"\n'
        f'        (at 0 {ref_offset_y} 0)\n'
        '        (unlocked yes)\n'
        '        (layer "F.SilkS")\n'
        f'        (uuid "{uuid4()}")\n'
        f'{font_props}\n'
        '    )\n'
        f'    (property "Value" "{part_info.series}"\n'
        f'        (at 0 {-1 * ref_offset_y} 0)\n'
        '        (unlocked yes)\n'
        '        (layer "F.Fab")\n'
        f'        (uuid "{uuid4()}")\n'
        f'{font_props}\n'
        '    )\n'
        '    (property "Footprint" ""\n'
        '        (at 0 0 0)\n'
        '        (layer "F.Fab")\n'
        '        (hide yes)\n'
        f'        (uuid "{uuid4()}")\n'
        '        (effects\n'
        '            (font\n'
        '                (size 1.27 1.27)\n'
        '                (thickness 0.15)\n'
        '            )\n'
        '        )\n'
        '    )'
    )


def generate_shapes(specs: TransformerSpecs) -> str:
    """Generate the shapes section of the footprint."""
    half_width = specs.body_dimensions.width / 2
    half_height = specs.body_dimensions.height / 2
    silkscreen_x = \
        specs.pad_dimensions.center_x - specs.pad_dimensions.width / 2

    shapes = []

    # Silkscreen lines
    for symbol in ["-", ""]:
        shapes.append(  # noqa: PERF401
            '    (fp_line\n'
            '        (start '
            f'{silkscreen_x} '
            f'{symbol}{half_height})\n'
            '        (end '
            f'-{silkscreen_x} '
            f'{symbol}{half_height})\n'
            '        (stroke\n'
            '            (width 0.1524)\n'
            '            (type solid)\n'
            '        )\n'
            '        (layer "F.SilkS")\n'
            f'        (uuid "{uuid4()}")\n'
            '    )',
        )

    # Pin 1 indicator position
    pins_per_side = specs.pad_dimensions.pin_count // 2
    total_height = specs.pad_dimensions.pitch_y * (pins_per_side - 1)
    circle_x = -(specs.pad_dimensions.center_x + specs.pad_dimensions.width)
    circle_y = -total_height / 2
    radius = specs.pad_dimensions.height / 4

    # Pin 1 indicator on silkscreen
    shapes.append(
        '    (fp_circle\n'
        '        (center '
        f'{circle_x} {circle_y})\n'
        '        (end '
        f'{circle_x - radius} {circle_y})\n'
        '        (stroke\n'
        '            (width 0.1524)\n'
        '            (type solid)\n'
        '        )\n'
        '        (fill solid)\n'
        '        (layer "F.SilkS")\n'
        f'        (uuid "{uuid4()}")\n'
        '    )',
    )

    # Courtyard and fabrication layer shapes
    shapes.extend([
        '    (fp_rect\n'
        f'        (start -{half_width} -{half_height})\n'
        f'        (end {half_width} {half_height})\n'
        '        (stroke\n'
        '            (width 0.00635)\n'
        '            (type default)\n'
        '        )\n'
        '        (fill none)\n'
        '        (layer "F.CrtYd")\n'
        f'        (uuid "{uuid4()}")\n'
        '    )',
        '    (fp_rect\n'
        f'        (start -{half_width} -{half_height})\n'
        f'        (end {half_width} {half_height})\n'
        '        (stroke\n'
        '            (width 0.0254)\n'
        '            (type default)\n'
        '        )\n'
        '        (fill none)\n'
        '        (layer "F.Fab")\n'
        f'        (uuid "{uuid4()}")\n'
        '    )',
    ])

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

    for pad_number, (x_pos, y_pos) in enumerate(pad_positions, 1):
        pads.append(
            f'    (pad "{pad_number}" smd rect\n'
            f'        (at {x_pos} {y_pos})\n'
            '        (size '
            f'{specs.pad_dimensions.width} {specs.pad_dimensions.height})\n'
            '        (layers "F.Cu" "F.Paste" "F.Mask")\n'
            f'        (uuid "{uuid4()}")\n'
            '    )',
        )

    return "\n".join(pads)


def generate_3d_model(part_info: sti.PartInfo) -> str:
    """Generate the 3D model section of the footprint."""
    return (
        f'    (model "${{KIPRJMOD}}/KiCAD_Symbol_Generator/3D_models/'
        f'{part_info.series}.step"\n'
        '        (offset (xyz 0 0 0))\n'
        '        (scale (xyz 1 1 1))\n'
        '        (rotate (xyz 0 0 0))\n'
        '    )'
    )


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
