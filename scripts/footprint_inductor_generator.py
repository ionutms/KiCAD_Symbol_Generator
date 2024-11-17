"""
KiCad Footprint Generator for Power Inductors

Generates standardized KiCad footprint files (.kicad_mod) for power inductors
based on manufacturer specifications. Creates accurate footprints with
appropriate pad dimensions, clearances, and silkscreen markings for surface
mount power inductors.

The generator supports multiple inductor series with predefined specifications
and produces KiCad-compatible footprint files that include:
- SMD pads with correct dimensions and spacing
- Silk screen markings for part outline
- Fabrication layer markings including polarity indicators
- Courtyard definitions
- 3D model references
"""

from typing import NamedTuple
from uuid import uuid4
import symbol_inductors_specs as ssi
from footprint_inductor_specs import INDUCTOR_SPECS


class PadDimensions(NamedTuple):
    """
    Defines SMD pad dimensions and positioning for power inductors.

    All measurements are in millimeters and follow the KiCad coordinate
    system where positive X is right and positive Y is up.

    Attributes:
        width: Width of each SMD pad
        height: Height of each pad
        center_x: Distance from origin to pad center on X-axis
    """
    width: float
    height: float
    center_x: float


class BodyDimensions(NamedTuple):
    """
    Defines physical dimensions of the inductor body.

    All measurements are in millimeters and represent the maximum extents
    of the component body.

    Attributes:
        width: Width of inductor body (X dimension)
        height: Height of inductor body (Y dimension)
    """
    width: float
    height: float


class InductorSpecs(NamedTuple):
    """
    Complete specifications for generating an inductor footprint.

    Combines series identification, physical dimensions, and placement
    parameters needed to generate accurate KiCad footprints.

    Attributes:
        series_name: Manufacturer's series identifier
        body_dims: Physical dimensions of the inductor body
        pad_dims: SMD pad specifications
        ref_offset_y: Y-axis offset for reference designator placement
    """
    series_name: str
    body_dims: BodyDimensions
    pad_dims: PadDimensions
    ref_offset_y: float


def create_inductor_specs(series_name: str) -> InductorSpecs:
    """
    Create complete inductor specifications from a series name.

    Looks up physical dimensions and parameters for the specified inductor
    series and returns a complete specification object for footprint
    generation.

    Args:
        series_name: Manufacturer's series identifier

    Returns:
        InductorSpecs object containing complete physical dimensions and
        parameters

    Raises:
        KeyError: If series_name is not found in INDUCTOR_SPECS dictionary
    """
    dims = INDUCTOR_SPECS[series_name]
    return InductorSpecs(
        series_name=series_name,
        body_dims=dims["body"],
        pad_dims=dims["pad"],
        ref_offset_y=dims["ref_offset_y"]
    )


def generate_footprint(specs: InductorSpecs) -> str:
    """
    Generate complete KiCad footprint file content for an inductor.

    Creates a KiCad-compatible footprint file (.kicad_mod) containing all
    necessary elements including pads, silkscreen, fabrication layer, and
    3D model references.

    Args:
        specs: Complete physical specifications for the inductor

    Returns:
        Formatted string containing complete .kicad_mod file content
    """
    sections = [
        generate_header(specs),
        generate_properties(specs),
        generate_silkscreen(specs),
        generate_courtyard(specs),
        generate_fab_layer(specs),
        generate_pads(specs),
        generate_3d_model(specs),
        ")"  # Close the footprint
    ]
    return "\n".join(sections)


def generate_header(specs: InductorSpecs) -> str:
    """
    Generate the footprint header section.

    Args:
        specs: Complete physical specifications for the inductor

    Returns:
        Formatted string containing the footprint header section
    """
    return (
        f'(footprint "{specs.series_name}"\n'
        '    (version 20240108)\n'
        '    (generator "pcbnew")\n'
        '    (generator_version "8.0")\n'
        '    (layer "F.Cu")\n'
        '    (descr "")\n'
        '    (tags "")\n'
        '    (attr smd)'
    )


def generate_properties(specs: InductorSpecs) -> str:
    """
    Generate properties section with inductor-specific information.

    Args:
        specs: Complete physical specifications for the inductor

    Returns:
        Formatted string containing the properties section
    """
    font_props = (
        '        (effects\n'
        '            (font\n'
        '                (size 0.762 0.762)\n'
        '                (thickness 0.1524)\n'
        '            )\n'
        '            (justify left)\n'
        '        )'
    )

    return (
        '    (property "Reference" "REF**"\n'
        f'        (at 0 {specs.ref_offset_y} 0)\n'
        '        (unlocked yes)\n'
        '        (layer "F.SilkS")\n'
        f'        (uuid "{uuid4()}")\n'
        f'{font_props}\n'
        '    )\n'
        f'    (property "Value" "{specs.series_name}"\n'
        f'        (at 0 {-1 * specs.ref_offset_y} 0)\n'
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


def generate_silkscreen(specs: InductorSpecs) -> str:
    """
    Generate silkscreen elements with inductor-specific clearances.

    Args:
        specs: Complete physical specifications for the inductor

    Returns:
        Formatted string containing silkscreen elements
    """
    silkscreen_x = specs.pad_dims["center_x"] - specs.pad_dims["width"] / 2

    silkscreen = []

    for symbol in ['-', '']:
        silkscreen.append(
            '    (fp_line\n'
            '        (start '
            f'{silkscreen_x} '
            f'{symbol}{specs.body_dims["height"]/2})\n'
            '        (end '
            f'-{silkscreen_x} '
            f'{symbol}{specs.body_dims["height"]/2})\n'
            '        (stroke\n'
            '            (width 0.1524)\n'
            '            (type solid)\n'
            '        )\n'
            '        (layer "F.SilkS")\n'
            f'        (uuid "{uuid4()}")\n'
            '    )'
        )

    return "\n".join(silkscreen)


def generate_courtyard(specs: InductorSpecs) -> str:
    """
    Generate courtyard outline with inductor-specific clearances.

    Args:
        specs: Complete physical specifications for the inductor

    Returns:
        Formatted string containing courtyard outline elements
    """
    half_width = specs.body_dims["width"] / 2
    half_height = specs.body_dims["height"] / 2

    return (
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
        '    )'
    )


def generate_fab_layer(specs: InductorSpecs) -> str:
    """
    Generate fabrication layer with inductor-specific markings.

    Args:
        specs: Complete physical specifications for the inductor

    Returns:
        Formatted string containing fabrication layer elements
    """
    half_width = specs.body_dims["width"] / 2
    half_height = specs.body_dims["height"] / 2

    fab_elements = []

    # Main body outline
    fab_elements.append(
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
        '    )'
    )

    # Polarity marker
    fab_elements.append(
        '    (fp_circle\n'
        f'        (center -{specs.pad_dims["center_x"]} 0)\n'
        f'        (end -{specs.pad_dims["center_x"] - 0.0762} 0)\n'
        '        (stroke\n'
        '            (width 0.0254)\n'
        '            (type solid)\n'
        '        )\n'
        '        (fill none)\n'
        '        (layer "F.Fab")\n'
        f'        (uuid "{uuid4()}")\n'
        '    )'
    )

    # Reference on fab layer
    fab_elements.append(
        f'    (fp_text user "${{REFERENCE}}"\n'
        f'        (at 0 {-1 * specs.ref_offset_y + 1.27} 0)\n'
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

    return "\n".join(fab_elements)


def generate_pads(specs: InductorSpecs) -> str:
    """
    Generate SMD pads with inductor-specific dimensions.

    Args:
        specs: Complete physical specifications for the inductor

    Returns:
        Formatted string containing pad definitions
    """
    pads = []

    for pad_number, symbol in enumerate(['-', ''], start=1):
        pads.append(
            f'    (pad "{pad_number}" smd rect\n'
            f'        (at {symbol}{specs.pad_dims["center_x"]} 0)\n'
            '        (size '
            f'{specs.pad_dims["width"]} '
            f'{specs.pad_dims["height"]})\n'
            '        (layers "F.Cu" "F.Paste" "F.Mask")\n'
            f'        (uuid "{uuid4()}")\n'
            '    )'
        )

    return "\n".join(pads)


def generate_3d_model(specs: InductorSpecs) -> str:
    """
    Generate 3D model reference for the inductor.

    Args:
        specs: Complete physical specifications for the inductor

    Returns:
        Formatted string containing 3D model reference
    """
    return (
        f'    (model "${{KIPRJMOD}}/KiCAD_Symbol_Generator/3D_models/'
        f'{specs.series_name}.step"\n'
        '        (offset (xyz 0 0 0))\n'
        '        (scale (xyz 1 1 1))\n'
        '        (rotate (xyz 0 0 0))\n'
        '    )'
    )


def generate_footprint_file(
        part_info: ssi.PartInfo,
        output_dir: str) -> None:
    """
    Generate and save a complete .kicad_mod file for an inductor.

    Creates a KiCad footprint file in the specified directory using the
    provided PartInfo object containing series information.

    Args:
        part_info: PartInfo object containing the inductor series name
        output_dir:
            Directory path where the generated footprint file will be saved

    Raises:
        ValueError: If the specified series is not found in INDUCTOR_SPECS
    """
    if part_info.series not in INDUCTOR_SPECS:
        raise ValueError(f"Unknown series: {part_info.series}")

    filename = part_info.series

    inductor_specs = create_inductor_specs(filename)
    footprint_content = generate_footprint(inductor_specs)

    filename = f"{output_dir}/{filename}.kicad_mod"
    with open(filename, 'w', encoding='utf-8') as file_handle:
        file_handle.write(footprint_content)
