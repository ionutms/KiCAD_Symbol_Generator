"""
KiCad Footprint Generator for Power Inductors

Generates standardized KiCad footprint files (.kicad_mod) for power inductors.
Uses manufacturer specifications to create accurate footprints with appropriate
pad dimensions and clearances.
"""

from typing import Dict, NamedTuple
from uuid import uuid4


class PadDimensions(NamedTuple):
    """
    Defines SMD pad dimensions and positioning.

    All measurements in millimeters.
    """
    width: float      # Width of each pad
    height: float     # Height of each pad
    center_x: float   # Distance from origin to pad center


class BodyDimensions(NamedTuple):
    "TODO"
    width: float
    height: float


class InductorSpecs(NamedTuple):
    """
    Complete specifications for generating an inductor footprint.

    Combines physical dimensions with series-specific properties for
    generating accurate KiCad footprints.
    """
    series_name: str          # Inductor series name
    body_dims: BodyDimensions
    pad_dims: PadDimensions  # Pad specifications
    silk_y: float            # Y-coordinate of silkscreen lines
    ref_y: float             # Y position for reference designator
    value_y: float           # Y position for value text
    fab_reference_y: float   # Y position for fab layer reference


# Mapping of inductor series to physical dimensions
INDUCTOR_DIMENSIONS: Dict[str, Dict[str, float]] = {
    "XAL1010": {
        "body": {"width": 10.922, "height": 12.192},
        "pad": {"width": 2.3876, "height": 8.9916, "center_x": 3.3274},
        # "pad_width": 2.3876,
        # "pad_height": 8.9916,
        # "pad_center_x": 3.3274,
        "silk_y": 6.096,
        "ref_y": -6.858,
        "value_y": 8.128,
        "fab_reference_y": 6.858,
    },
}


def create_inductor_specs(series_name: str) -> InductorSpecs:
    """
    Create complete inductor specifications from series name.

    Args:
        series_name: Name of the inductor series (e.g., "XAL1010")

    Returns:
        InductorSpecs object with complete physical dimensions

    Raises:
        KeyError: If series name is not found in INDUCTOR_DIMENSIONS
    """
    dims = INDUCTOR_DIMENSIONS[series_name]

    return InductorSpecs(
        series_name=series_name,
        body_dims=dims["body"],
        pad_dims=dims["pad"],
        silk_y=dims["silk_y"],
        ref_y=dims["ref_y"],
        value_y=dims["value_y"],
        fab_reference_y=dims["fab_reference_y"],
    )


def generate_footprint(specs: InductorSpecs) -> str:
    """
    Generate complete KiCad footprint file content for an inductor.

    Args:
        specs: Physical specifications for the inductor

    Returns:
        Complete .kicad_mod file content as formatted string
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
    """Generate the footprint header section."""
    return (
        f'(footprint "{specs.series_name}"\n'
        f'    (version 20240108)\n'
        f'    (generator "pcbnew")\n'
        f'    (generator_version "8.0")\n'
        f'    (layer "F.Cu")\n'
        f'    (descr "")\n'
        f'    (tags "")\n'
        f'    (attr smd)'
    )


def generate_properties(specs: InductorSpecs) -> str:
    """Generate properties section with inductor-specific information."""
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
        f'    (property "Reference" "REF**"\n'
        f'        (at 0 {specs.ref_y} 0)\n'
        f'        (unlocked yes)\n'
        f'        (layer "F.SilkS")\n'
        f'        (uuid "{uuid4()}")\n'
        f'{font_props}\n'
        f'    )\n'
        f'    (property "Value" "{specs.series_name}"\n'
        f'        (at 0 {specs.value_y} 0)\n'
        f'        (unlocked yes)\n'
        f'        (layer "F.Fab")\n'
        f'        (uuid "{uuid4()}")\n'
        f'{font_props}\n'
        f'    )\n'
        f'    (property "Footprint" ""\n'
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


def generate_silkscreen(specs: InductorSpecs) -> str:
    """Generate silkscreen elements with inductor-specific clearances."""
    half_width = specs.body_dims["width"] / 2
    silkscreen_x = half_width * 0.372  # Adjust silk line length

    silkscreen = []

    # Top silkscreen line
    silkscreen.append(
        f'    (fp_line\n'
        f'        (start {silkscreen_x} -{specs.silk_y})\n'
        f'        (end -{silkscreen_x} -{specs.silk_y})\n'
        f'        (stroke\n'
        f'            (width 0.1524)\n'
        f'            (type solid)\n'
        f'        )\n'
        f'        (layer "F.SilkS")\n'
        f'        (uuid "{uuid4()}")\n'
        f'    )'
    )

    # Bottom silkscreen line
    silkscreen.append(
        f'    (fp_line\n'
        f'        (start {silkscreen_x} {specs.silk_y})\n'
        f'        (end -{silkscreen_x} {specs.silk_y})\n'
        f'        (stroke\n'
        f'            (width 0.1524)\n'
        f'            (type solid)\n'
        f'        )\n'
        f'        (layer "F.SilkS")\n'
        f'        (uuid "{uuid4()}")\n'
        f'    )'
    )

    return "\n".join(silkscreen)


def generate_courtyard(specs: InductorSpecs) -> str:
    """Generate courtyard outline with inductor-specific clearances."""
    half_width = specs.body_dims["width"] / 2
    half_height = specs.body_dims["height"] / 2

    return (
        f'    (fp_rect\n'
        f'        (start -{half_width} -{half_height})\n'
        f'        (end {half_width} {half_height})\n'
        f'        (stroke\n'
        f'            (width 0.00635)\n'
        f'            (type default)\n'
        f'        )\n'
        f'        (fill none)\n'
        f'        (layer "F.CrtYd")\n'
        f'        (uuid "{uuid4()}")\n'
        f'    )'
    )


def generate_fab_layer(specs: InductorSpecs) -> str:
    """Generate fabrication layer with inductor-specific markings."""
    half_width = specs.body_dims["width"] / 2
    half_height = specs.body_dims["height"] / 2

    fab_elements = []

    # Main body outline
    fab_elements.append(
        f'    (fp_rect\n'
        f'        (start -{half_width} -{half_height})\n'
        f'        (end {half_width} {half_height})\n'
        f'        (stroke\n'
        f'            (width 0.0254)\n'
        f'            (type default)\n'
        f'        )\n'
        f'        (fill none)\n'
        f'        (layer "F.Fab")\n'
        f'        (uuid "{uuid4()}")\n'
        f'    )'
    )

    # Polarity marker
    fab_elements.append(
        f'    (fp_circle\n'
        f'        (center -{specs.pad_dims["center_x"]} 0)\n'
        f'        (end -{specs.pad_dims["center_x"] - 0.0762} 0)\n'
        f'        (stroke\n'
        f'            (width 0.0254)\n'
        f'            (type solid)\n'
        f'        )\n'
        f'        (fill none)\n'
        f'        (layer "F.Fab")\n'
        f'        (uuid "{uuid4()}")\n'
        f'    )'
    )

    # Reference on fab layer
    fab_elements.append(
        f'    (fp_text user "${{REFERENCE}}"\n'
        f'        (at 0 {specs.fab_reference_y} 0)\n'
        f'        (unlocked yes)\n'
        f'        (layer "F.Fab")\n'
        f'        (uuid "{uuid4()}")\n'
        f'        (effects\n'
        f'            (font\n'
        f'                (size 0.762 0.762)\n'
        f'                (thickness 0.1524)\n'
        f'            )\n'
        f'            (justify left)\n'
        f'        )\n'
        f'    )'
    )

    return "\n".join(fab_elements)


def generate_pads(specs: InductorSpecs) -> str:
    """Generate SMD pads with inductor-specific dimensions."""
    pads = []

    # Left pad (1)
    pads.append(
        f'    (pad "1" smd rect\n'
        f'        (at -{specs.pad_dims["center_x"]} 0)\n'
        f'        (size '
        f'{specs.pad_dims["width"]} '
        f'{specs.pad_dims["height"]})\n'
        f'        (layers "F.Cu" "F.Paste" "F.Mask")\n'
        f'        (uuid "{uuid4()}")\n'
        f'    )'
    )

    # Right pad (2)
    pads.append(
        f'    (pad "2" smd rect\n'
        f'        (at {specs.pad_dims["center_x"]} 0)\n'
        f'        (size '
        f'{specs.pad_dims["width"]} '
        f'{specs.pad_dims["height"]})\n'
        f'        (layers "F.Cu" "F.Paste" "F.Mask")\n'
        f'        (uuid "{uuid4()}")\n'
        f'    )'
    )

    return "\n".join(pads)


def generate_3d_model(specs: InductorSpecs) -> str:
    """Generate 3D model reference for the inductor."""
    return (
        f'    (model "${{KIPRJMOD}}/KiCAD_Symbol_Generator/3D_models/'
        f'{specs.series_name}.step"\n'
        f'        (offset\n'
        f'            (xyz 0 0 0)\n'
        f'        )\n'
        f'        (scale\n'
        f'            (xyz 1 1 1)\n'
        f'        )\n'
        f'        (rotate\n'
        f'            (xyz 0 0 0)\n'
        f'        )\n'
        f'    )'
    )


def generate_footprint_file(
        part_info,  # Can be str or PartInfo
        output_dir: str) -> None:
    """
    Generate and save a complete .kicad_mod file for an inductor.

    Args:
        part_info:
            Either series name string (e.g., "XAL1010") or PartInfo object
        output_dir: Directory to save the generated footprint file

    Raises:
        KeyError: If series_name is not found in INDUCTOR_DIMENSIONS
        IOError: If there are problems writing the output file
    """

    if part_info.series not in INDUCTOR_DIMENSIONS:
        raise ValueError(f"Unknown series: {part_info.series}")
    # Extract series name if PartInfo object is provided
    series_name = \
        part_info.series if hasattr(part_info, 'series') else part_info

    inductor_specs = create_inductor_specs(series_name)
    footprint_content = generate_footprint(inductor_specs)

    filename = f"{output_dir}/{series_name}.kicad_mod"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(footprint_content)
