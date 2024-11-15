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
    courtyard_margin: float  # Additional space around component for courtyard
    silkscreen_margin: float  # Gap between body and silkscreen


class TextSpecs(NamedTuple):
    """Text placement and size specifications."""
    reference_pos: tuple[float, float]  # Position of reference designator
    value_pos: tuple[float, float]      # Position of value text
    font_size: tuple[float, float]      # Text size (width, height)
    font_thickness: float               # Text line thickness


class InductorSpecs(NamedTuple):
    """Complete specifications for generating an inductor footprint."""
    pads: PadSpecs           # Pad dimensions and spacing
    outline: OutlineSpecs    # Component body dimensions
    text: TextSpecs          # Text placement and sizing
    model_offset: tuple[float, float, float]  # 3D model offset
    model_rotation: tuple[float, float, float]  # 3D model rotation angles
    model_path: str          # Path to 3D model file


# Default text specifications
DEFAULT_TEXT_SPECS = TextSpecs(
    reference_pos=(0, -3.048),
    value_pos=(0, 4.318),
    font_size=(0.762, 0.762),
    font_thickness=0.1524
)


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
            length=4.4704,
            courtyard_margin=0.0,  # No additional margin needed
            silkscreen_margin=1.6256  # Distance from center to silkscreen
        ),
        text=DEFAULT_TEXT_SPECS,
        model_offset=(0.0, 0.0, 0.1016),
        model_rotation=(-90, 0, 0),
        model_path="KiCAD_Symbol_Generator/3D_models/XFL4020.step"
    ),
    "XFL4015": InductorSpecs(
        pads=PadSpecs(
            width=0.9652,
            length=3.4036,
            spacing=2.3622
        ),
        outline=OutlineSpecs(
            width=4.4704,
            length=4.4704,
            courtyard_margin=0.0,
            silkscreen_margin=1.6256
        ),
        text=DEFAULT_TEXT_SPECS,
        model_offset=(0.0, 0.0, 0.1016),
        model_rotation=(-90, 0, 0),
        model_path="KiCAD_Symbol_Generator/3D_models/XFL4015.step"
    ),
}


def generate_header(model_name: str) -> str:
    """Generate the footprint header section."""
    return (
        f'(footprint "{model_name}"\n'
        f'    (version 20240108)\n'
        f'    (generator "pcbnew")\n'
        f'    (generator_version "8.0")\n'
        f'    (layer "F.Cu")'
    )


def generate_properties(part_info: ssi.PartInfo, specs: InductorSpecs) -> str:
    """Generate the properties section of the footprint."""
    properties = []
    ref_x, ref_y = specs.text.reference_pos
    val_x, val_y = specs.text.value_pos
    font_w, font_h = specs.text.font_size

    # Common font effects for visible text
    visible_font = (
        f'            (font\n'
        f'                (size {font_w} {font_h})\n'
        f'                (thickness {specs.text.font_thickness})\n'
        f'            )\n'
        f'            (justify left)'
    )

    # Reference property
    properties.append(
        f'    (property "Reference" "REF**"\n'
        f'        (at {ref_x} {ref_y} 0)\n'
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
        f'        (at {val_x} {val_y} 0)\n'
        f'        (unlocked yes)\n'
        f'        (layer "F.Fab")\n'
        f'        (uuid "{uuid4()}")\n'
        f'        (effects\n'
        f'{visible_font}\n'
        f'        )\n'
        f'    )'
    )

    # Hidden properties with their standard font
    hidden_props = ["Footprint", "Datasheet", "Description"]
    for prop in hidden_props:
        properties.append(generate_hidden_property(prop))

    return "\n".join(properties)


def generate_hidden_property(name: str) -> str:
    """Generate a hidden property entry."""
    return (
        f'    (property "{name}" ""\n'
        f'        (at 0 0 0)\n'
        f'        (layer "F.Fab")\n'
        f'        (hide yes)\n'
        f'        (uuid "{uuid4()}")\n'
        f'        (effects\n'
        f'            (font\n'
        f'                (size 1.27 1.27)\n'
        f'                (thickness 0.15)\n'
        f'            )\n'
        f'        )\n'
        f'    )'
    )


def generate_lines_and_shapes(specs: InductorSpecs) -> str:
    """Generate the lines and shapes section of the footprint."""
    silk_y = specs.outline.silkscreen_margin
    court_x = specs.outline.width/2 + specs.outline.courtyard_margin
    court_y = specs.outline.length/2 + specs.outline.courtyard_margin

    shapes = ['    (attr smd)']

    # Silkscreen lines
    shapes.extend([
        generate_silkscreen_line(-0.6096, silk_y, 0.6096, silk_y),
        generate_silkscreen_line(0.6096, -silk_y, -0.6096, -silk_y)
    ])

    # Courtyard and fabrication layer rectangles
    shapes.extend([
        generate_rectangle(
            "F.CrtYd", -court_x, -court_y, court_x, court_y, 0.00635),
        generate_rectangle(
            "F.Fab", -court_x, -court_y, court_x, court_y, 0.0254)
    ])

    # Pin 1 marker
    shapes.append(generate_pin1_marker(-1.1811))

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


def generate_silkscreen_line(
        start_x: float, start_y: float,
        end_x: float, end_y: float) -> str:
    """Generate a silkscreen line entry."""
    return (
        '    (fp_line\n'
        f'        (start {start_x} {start_y})\n'
        f'        (end {end_x} {end_y})\n'
        '        (stroke\n'
        '            (width 0.1524)\n'
        '            (type solid)\n'
        '        )\n'
        '        (layer "F.SilkS")\n'
        f'        (uuid "{uuid4()}")\n'
        '    )'
    )


def generate_rectangle(
        layer: str, start_x: float, start_y: float,
        end_x: float, end_y: float, width: float) -> str:
    """Generate a rectangle entry."""
    return (
        '    (fp_rect\n'
        f'        (start {start_x} {start_y})\n'
        f'        (end {end_x} {end_y})\n'
        '        (stroke\n'
        f'            (width {width})\n'
        '            (type default)\n'
        '        )\n'
        '        (fill none)\n'
        f'        (layer "{layer}")\n'
        f'        (uuid "{uuid4()}")\n'
        '    )'
    )


def generate_pin1_marker(center_x: float) -> str:
    """Generate a pin 1 marker circle."""
    return (
        '    (fp_circle\n'
        f'        (center {center_x} 0)\n'
        f'        (end {center_x + 0.0762} 0)\n'
        '        (stroke\n'
        '            (width 0.0254)\n'
        '            (type solid)\n'
        '        )\n'
        '        (fill none)\n'
        '        (layer "F.Fab")\n'
        f'        (uuid "{uuid4()}")\n'
        '    )'
    )


def generate_pads(specs: InductorSpecs) -> str:
    """Generate the pads section of the footprint."""
    pad_x = specs.pads.spacing / 2
    return "\n".join([
        generate_pad("1", -pad_x, specs.pads),
        generate_pad("2", pad_x, specs.pads)
    ])


def generate_pad(number: str, x_pos: float, pad_specs: PadSpecs) -> str:
    """Generate a single pad entry."""
    return (
        f'    (pad "{number}" smd rect\n'
        f'        (at {x_pos} 0)\n'
        f'        (size {pad_specs.width} {pad_specs.length})\n'
        '        (layers "F.Cu" "F.Paste" "F.Mask")\n'
        f'        (uuid "{uuid4()}")\n'
        '    )'
    )


def generate_3d_model(specs: InductorSpecs) -> str:
    """Generate the 3D model section of the footprint."""
    return (
        f'    (model "${{KIPRJMOD}}/{specs.model_path}"\n'
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


def generate_footprint(part_info: ssi.PartInfo, specs: InductorSpecs) -> str:
    """Generate complete KiCad footprint file content for an inductor."""
    sections = [
        generate_header(part_info.series),
        generate_properties(part_info, specs),
        generate_lines_and_shapes(specs),
        generate_pads(specs),
        generate_3d_model(specs),
        ")"  # Close the footprint
    ]
    return "\n".join(sections)


def generate_footprint_file(part_info: ssi.PartInfo) -> None:
    """Generate and save a complete .kicad_mod file for an inductor."""
    if part_info.series not in INDUCTOR_SPECS:
        raise ValueError(f"Unknown series: {part_info.series}")

    specs = INDUCTOR_SPECS[part_info.series]
    footprint_content = generate_footprint(part_info, specs)

    filename = f"{part_info.series}.kicad_mod"
    with open(filename, 'w', encoding='utf-8') as output_file:
        output_file.write(footprint_content)
