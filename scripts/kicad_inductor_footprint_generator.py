"""
KiCad Footprint Generator Module for Inductors

Generates standardized KiCad footprint files (.kicad_mod) for various inductor
series. Handles pad placement, silkscreen generation, and 3D model alignment
based on manufacturer specifications.
"""

from typing import NamedTuple
from uuid import uuid4
import series_specs_inductors as ssi


class PadSpecs(NamedTuple):
    """Pad dimensions and spacing for surface mount components."""
    width: float      # Pad width
    length: float     # Pad length
    spacing: float    # Center-to-center distance between pads


class OutlineSpecs(NamedTuple):
    """Component body outline dimensions."""
    width: float      # Total width of component body
    length: float     # Total length of component body


class InductorSpecs(NamedTuple):
    """Complete specifications for generating an inductor footprint."""
    pads: PadSpecs           # Pad dimensions and spacing
    outline: OutlineSpecs    # Component body dimensions
    model_offset: tuple[float, float, float]  # 3D model offset
    model_rotation: tuple[float, float, float]  # 3D model rotation angles


# Dictionary mapping series codes to their specifications
INDUCTOR_SPECS = {
    "XFL4020": InductorSpecs(
        pads=PadSpecs(
            width=0.9652,
            length=3.4036,
            spacing=2.3622
        ),
        outline=OutlineSpecs(
            width=4.4704,
            length=4.4704
        ),
        model_offset=(0.0, 0.0, 0.1016),
        model_rotation=(-90, 0, 0)
    ),
    "XFL4015": InductorSpecs(
        pads=PadSpecs(
            width=0.9652,
            length=3.4036,
            spacing=2.3622
        ),
        outline=OutlineSpecs(
            width=4.4704,
            length=4.4704
        ),
        model_offset=(0.0, 0.0, 0.1016),
        model_rotation=(-90, 0, 0)
    ),
}


def generate_footprint(part_info: ssi.PartInfo, specs: InductorSpecs) -> str:
    """Generate complete KiCad footprint file content for an inductor."""
    sections = [
        generate_header(part_info.series),
        generate_properties(part_info),
        generate_lines_and_shapes(),
        generate_pads(specs),
        generate_3d_model(part_info, specs),
        ")"  # Close the footprint
    ]
    return "\n".join(sections)


def generate_header(model_name: str) -> str:
    """Generate the footprint header section."""
    return (
        f'(footprint "{model_name}"\n'
        f'    (version 20240108)\n'
        f'    (generator "pcbnew")\n'
        f'    (generator_version "8.0")\n'
        f'    (layer "F.Cu")'
    )


def generate_properties(part_info: ssi.PartInfo) -> str:
    """Generate the properties section of the footprint."""
    properties = []

    # Common font effects for visible text
    visible_font = (
        '            (font\n'
        '                (size 0.762 0.762)\n'
        '                (thickness 0.1524)\n'
        '            )\n'
        '            (justify left)'
    )

    # Common font effects for hidden properties
    hidden_font = (
        '            (font\n'
        '                (size 1.27 1.27)\n'
        '                (thickness 0.15)\n'
        '            )'
    )

    # Reference property
    properties.append(
        f'    (property "Reference" "REF**"\n'
        f'        (at 0 -3.048 0)\n'
        f'        (unlocked yes)\n'
        f'        (layer "F.SilkS")\n'
        f'        (uuid "{uuid4()}")\n'
        f'        (effects\n'
        f'{visible_font}\n'
        f'        )\n'
        f'    )'
    )

    # Value property
    properties.append(
        f'    (property "Value" "{part_info.series}"\n'
        f'        (at 0 4.318 0)\n'
        f'        (unlocked yes)\n'
        f'        (layer "F.Fab")\n'
        f'        (uuid "{uuid4()}")\n'
        f'        (effects\n'
        f'{visible_font}\n'
        f'        )\n'
        f'    )'
    )

    # Hidden properties
    for prop_name in ["Footprint", "Datasheet", "Description"]:
        properties.append(
            f'    (property "{prop_name}" ""\n'
            f'        (at 0 0 0)\n'
            f'        (layer "F.Fab")\n'
            f'        (hide yes)\n'
            f'        (uuid "{uuid4()}")\n'
            f'        (effects\n'
            f'{hidden_font}\n'
            f'        )\n'
            f'    )'
        )

    return "\n".join(properties)


def generate_lines_and_shapes() -> str:
    """Generate the lines and shapes section of the footprint."""
    shapes = ['    (attr smd)']

    # Silkscreen lines
    shapes.extend([
        '    (fp_line\n'
        '        (start -0.6096 2.2352)\n'
        '        (end 0.6096 2.2352)\n'
        '        (stroke\n'
        '            (width 0.1524)\n'
        '            (type solid)\n'
        '        )\n'
        '        (layer "F.SilkS")\n'
        f'        (uuid "{uuid4()}")\n'
        '    )',
        '    (fp_line\n'
        '        (start 0.6096 -2.2352)\n'
        '        (end -0.6096 -2.2352)\n'
        '        (stroke\n'
        '            (width 0.1524)\n'
        '            (type solid)\n'
        '        )\n'
        '        (layer "F.SilkS")\n'
        f'        (uuid "{uuid4()}")\n'
        '    )'
    ])

    # Courtyard rectangle
    shapes.append(
        '    (fp_rect\n'
        '        (start -2.2352 -2.2352)\n'
        '        (end 2.2352 2.2352)\n'
        '        (stroke\n'
        '            (width 0.00635)\n'
        '            (type default)\n'
        '        )\n'
        '        (fill none)\n'
        '        (layer "F.CrtYd")\n'
        f'        (uuid "{uuid4()}")\n'
        '    )'
    )

    # Fabrication layer rectangle
    shapes.append(
        '    (fp_rect\n'
        '        (start -2.2352 -2.2352)\n'
        '        (end 2.2352 2.2352)\n'
        '        (stroke\n'
        '            (width 0.0254)\n'
        '            (type default)\n'
        '        )\n'
        '        (fill none)\n'
        '        (layer "F.Fab")\n'
        f'        (uuid "{uuid4()}")\n'
        '    )'
    )

    # Pin 1 marker circle
    shapes.append(
        '    (fp_circle\n'
        '        (center -1.1811 0)\n'
        '        (end -1.1049 0)\n'
        '        (stroke\n'
        '            (width 0.0254)\n'
        '            (type solid)\n'
        '        )\n'
        '        (fill none)\n'
        '        (layer "F.Fab")\n'
        f'        (uuid "{uuid4()}")\n'
        '    )'
    )

    # Reference on fabrication layer
    shapes.append(
        '    (fp_text user "${REFERENCE}"\n'
        '        (at 0 3.048 0)\n'
        '        (unlocked yes)\n'
        '        (layer "F.Fab")\n'
        f'        (uuid "{uuid4()}")\n'
        '        (effects\n'
        '            (font\n'
        '                (size 0.762 0.762)\n'
        '                (thickness 0.1524)\n'
        '            )\n'
        '            (justify left)\n'
        '        )\n'
        '    )'
    )

    return "\n".join(shapes)


def generate_pads(specs: InductorSpecs) -> str:
    """Generate the pads section of the footprint."""
    return "\n".join([
        '    (pad "1" smd rect\n'
        '        (at -1.1811 0)\n'
        f'        (size {specs.pads.width} {specs.pads.length})\n'
        '        (layers "F.Cu" "F.Paste" "F.Mask")\n'
        f'        (uuid "{uuid4()}")\n'
        '    )',
        '    (pad "2" smd rect\n'
        '        (at 1.1811 0)\n'
        f'        (size {specs.pads.width} {specs.pads.length})\n'
        '        (layers "F.Cu" "F.Paste" "F.Mask")\n'
        f'        (uuid "{uuid4()}")\n'
        '    )'
    ])


def generate_3d_model(part_info: ssi.PartInfo, specs: InductorSpecs) -> str:
    """Generate the 3D model section of the footprint."""
    model_path = f'KiCAD_Symbol_Generator/3D_models//{part_info.series}.step'

    return (
        f'    (model "${{KIPRJMOD}}/{model_path}"\n'
        '        (offset\n'
        f'            (xyz {specs.model_offset[0]} '
        f'{specs.model_offset[1]} {specs.model_offset[2]})\n'
        '        )\n'
        '        (scale\n'
        '            (xyz 1 1 1)\n'
        '        )\n'
        '        (rotate\n'
        f'            (xyz {specs.model_rotation[0]} '
        f'{specs.model_rotation[1]} {specs.model_rotation[2]})\n'
        '        )\n'
        '    )'
    )


def generate_footprint_file(part_info: ssi.PartInfo) -> None:
    """Generate and save a complete .kicad_mod file for an inductor."""
    if part_info.series not in INDUCTOR_SPECS:
        raise ValueError(f"Unknown series: {part_info.series}")

    specs = INDUCTOR_SPECS[part_info.series]
    footprint_content = generate_footprint(part_info, specs)

    filename = f"{part_info.series}.kicad_mod"
    with open(filename, 'w', encoding='utf-8') as output_file:
        output_file.write(footprint_content)
