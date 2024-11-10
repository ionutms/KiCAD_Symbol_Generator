"""
KiCad Footprint Generator Module

Generates standardized KiCad footprint files (.kicad_mod) for various connector
series. Handles pad placement, silkscreen generation, and 3D model alignment
based on manufacturer specifications.

The module supports multiple connector series with different pin counts and
pitches, generating complete footprint definitions including:
- Through-hole pad layouts
- Silkscreen outlines
- Component identifiers
- 3D model references
"""

from typing import Callable, Dict, NamedTuple, Tuple
from uuid import uuid4
import series_specs_connectors as ssc


class RectangleSpecs(NamedTuple):
    """
    Defines rectangular dimensions for component footprint outlines.

    All measurements are in millimeters relative to the origin point (0,0).
    Positive values extend right/up, negative values extend left/down.
    """
    width_left: float     # Distance from origin to left edge
    width_right: float    # Distance from origin to right edge
    height_top: float     # Distance from origin to top edge
    height_bottom: float  # Distance from origin to bottom edge


class ConnectorSpecs(NamedTuple):
    """
    Complete specifications for generating a connector footprint.

    Defines all physical dimensions, pad properties, reference designator
    positions, and 3D model alignment parameters needed to generate a complete
    KiCad footprint file.
    """
    width_per_pin: float   # Additional width needed per pin
    rect_dims: RectangleSpecs  # Basic rectangle dimensions
    pad_size: float       # Diameter/size of through-hole pads
    drill_size: float     # Diameter of drill holes
    silk_margin: float    # Clearance for silkscreen outlines
    mask_margin: float    # Solder mask clearance around pads
    mpn_y: float         # Y position for manufacturer part number
    ref_y: float         # Y position for reference designator
    model_offset_base: tuple[float, float, float]  # Base 3D model offset
    model_rotation: tuple[float, float, float]     # 3D model rotation angles
    step_multiplier: float  # Step value for offset calculations
    model_offset_func: Callable  # Function to calculate model offsets


def offset_add(
        base_offset: Tuple[float, float, float],
        step_value: float
) -> Tuple[float, float, float]:
    """
    Calculate 3D model offset by adding step to base X coordinate.

    Args:
        base_offset: Starting (x, y, z) coordinates
        step_value: Value to add to x coordinate

    Returns:
        Updated (x, y, z) coordinates with modified x value
    """
    return (base_offset[0] + step_value, base_offset[1], base_offset[2])


def offset_sub(
        base_offset: Tuple[float, float, float],
        step_value: float
) -> Tuple[float, float, float]:
    """
    Calculate 3D model offset by subtracting step from base X coordinate.

    Args:
        base_offset: Starting (x, y, z) coordinates
        step_value: Value to subtract from x coordinate

    Returns:
        Updated (x, y, z) coordinates with modified x value
    """
    return (base_offset[0] - step_value, base_offset[1], base_offset[2])


# Consolidated connector series specifications using common offset patterns
CONNECTOR_SPECS: Dict[str, ConnectorSpecs] = {
    "TB004-508": ConnectorSpecs(
        width_per_pin=5.08,
        rect_dims=RectangleSpecs(
            width_left=5.8,
            width_right=5.2,
            height_top=5.2,
            height_bottom=-5.2
        ),
        pad_size=2.55,
        drill_size=1.7,
        silk_margin=0.1524,
        mask_margin=0.102,
        mpn_y=6.096,
        ref_y=-6.096,
        model_offset_base=(0.0, 0.0, 0.0),
        model_rotation=(0.0, 0.0, 0.0),
        step_multiplier=0.0,
        model_offset_func=offset_sub
    ),
    "TB006-508": ConnectorSpecs(
        width_per_pin=5.08,
        rect_dims=RectangleSpecs(
            width_left=5.8,
            width_right=5.2,
            height_top=4.2,
            height_bottom=-4.2
        ),
        pad_size=2.55,
        drill_size=1.7,
        silk_margin=0.1524,
        mask_margin=0.102,
        mpn_y=5.334,
        ref_y=-5.334,
        model_offset_base=(0.0, 0.0, 0.0),
        model_rotation=(0.0, 0.0, 0.0),
        step_multiplier=0.0,
        model_offset_func=offset_sub
    ),
    "TBP02R1-381": ConnectorSpecs(
        width_per_pin=3.81,
        rect_dims=RectangleSpecs(
            width_left=4.4,
            width_right=4.4,
            height_top=-7.9,
            height_bottom=1.4
        ),
        pad_size=2.1,
        drill_size=1.4,
        silk_margin=0.1524,
        mask_margin=0.102,
        mpn_y=-8.8,
        ref_y=2.4,
        model_offset_base=(0, 0, 0),
        model_rotation=(0, 0, 0),
        step_multiplier=1.905,
        model_offset_func=offset_add
    ),
    "TBP02R2-381": ConnectorSpecs(
        width_per_pin=3.81,
        rect_dims=RectangleSpecs(
            width_left=4.445,
            width_right=4.445,
            height_top=3.2512,
            height_bottom=-4.445
        ),
        pad_size=2.1,
        drill_size=1.4,
        silk_margin=0.1524,
        mask_margin=0.102,
        mpn_y=-5.4,
        ref_y=4.2,
        model_offset_base=(17.145, -6.477, 18.288),
        model_rotation=(90, 0, -90),
        step_multiplier=1.905,
        model_offset_func=offset_sub
    ),
    "TBP04R1-500": ConnectorSpecs(
        width_per_pin=5.0,
        rect_dims=RectangleSpecs(
            width_left=5.2,
            width_right=5.2,
            height_top=-2.2,
            height_bottom=9.9
        ),
        pad_size=2.55,
        drill_size=1.7,
        silk_margin=0.1524,
        mask_margin=0.102,
        mpn_y=10.8,
        ref_y=-3.0,
        model_offset_base=(0, 0, 0),
        model_rotation=(0, 0, 0),
        step_multiplier=2.5,
        model_offset_func=offset_add
    ),
    "TBP04R2-500": ConnectorSpecs(
        width_per_pin=5.0,
        rect_dims=RectangleSpecs(
            width_left=5.8,
            width_right=5.8,
            height_top=4.8,
            height_bottom=-4.0
        ),
        pad_size=2.55,
        drill_size=1.7,
        silk_margin=0.1524,
        mask_margin=0.102,
        mpn_y=-4.8,
        ref_y=5.8,
        model_offset_base=(0, 0, 0),
        model_rotation=(0, 0, 0),
        step_multiplier=2.5,
        model_offset_func=offset_add
    ),
    "TBP04R3-500": ConnectorSpecs(
        width_per_pin=5.0,
        rect_dims=RectangleSpecs(
            width_left=5.2,
            width_right=5.2,
            height_top=4.8,
            height_bottom=-4.0
        ),
        pad_size=2.55,
        drill_size=1.7,
        silk_margin=0.1524,
        mask_margin=0.102,
        mpn_y=-4.8,
        ref_y=5.8,
        model_offset_base=(0, 0, 0),
        model_rotation=(0, 0, 0),
        step_multiplier=2.5,
        model_offset_func=offset_add
    ),
    "TBP04R12-500": ConnectorSpecs(
        width_per_pin=5.0,
        rect_dims=RectangleSpecs(
            width_left=5.8,
            width_right=5.8,
            height_top=-2.2,
            height_bottom=9.9
        ),
        pad_size=2.55,
        drill_size=1.7,
        silk_margin=0.1524,
        mask_margin=0.102,
        mpn_y=10.8,
        ref_y=-3.0,
        model_offset_base=(-5, -5.6, -3.81),
        model_rotation=(-90, 0, 0),
        step_multiplier=2.5,
        model_offset_func=offset_sub
    ),
}


def generate_footprint(part_info: ssc.PartInfo, specs: ConnectorSpecs) -> str:
    """
    Generate complete KiCad footprint file content for a connector.

    Creates all required sections of a .kicad_mod file including component
    outline, pad definitions, text elements, and 3D model references.

    Args:
        part_info: Component specifications (MPN, pin count, pitch)
        specs: Physical specifications for the connector series

    Returns:
        Complete .kicad_mod file content as formatted string
    """
    dimensions = calculate_dimensions(part_info, specs)
    sections = [
        generate_header(part_info.mpn),
        generate_properties(part_info, specs, dimensions),
        generate_shapes(dimensions, specs),
        generate_pads(part_info, specs, dimensions),
        generate_3d_model(part_info, specs),
        ")"  # Close the footprint
    ]
    return "\n".join(sections)


def calculate_dimensions(
        part_info: ssc.PartInfo,
        specs: ConnectorSpecs
) -> dict:
    """
    Calculate key dimensions for footprint generation.

    Determines total width, length, and starting positions based on the
    connector's pin count and physical specifications.

    Args:
        part_info: Component specifications (pin count, pitch)
        specs: Physical specifications for the connector series

    Returns:
        Dictionary containing calculated dimensions and positions
    """
    extra_width_per_side = (part_info.pin_count - 2) * specs.width_per_pin / 2
    total_half_width_left = specs.rect_dims.width_left + extra_width_per_side
    total_half_width_right = specs.rect_dims.width_right + extra_width_per_side
    total_length = (part_info.pin_count - 1) * part_info.pitch
    start_position = -total_length / 2

    return {
        "total_half_width_left": total_half_width_left,
        "total_half_width_right": total_half_width_right,
        "total_length": total_length,
        "start_pos": start_position
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


def generate_properties(
    part_info: ssc.PartInfo,
    specs: ConnectorSpecs,
    dimensions: dict
) -> str:
    """Generate the properties section of the footprint."""
    font_props = (
        '        (effects\n'
        '            (font\n'
        '                (size 0.762 0.762)\n'
        '                (thickness 0.1524)\n'
        '            )\n'
        '        )'
    )

    hidden_font_props = (
        '        (effects\n'
        '            (font\n'
        '                (size 1.27 1.27)\n'
        '                (thickness 0.15)\n'
        '            )\n'
        '        )'
    )

    return (
        f'    (property "Reference" "REF**"\n'
        f'        (at 0 {specs.ref_y} 0)\n'
        f'        (layer "F.SilkS")\n'
        f'        (uuid "{uuid4()}")\n'
        f'{font_props}\n'
        f'    )\n'
        f'    (property "Value" "{part_info.mpn}"\n'
        f'        (at 0 {specs.mpn_y} 0)\n'
        f'        (layer "F.Fab")\n'
        f'        (uuid "{uuid4()}")\n'
        f'{font_props}\n'
        f'    )\n'
        f'    (property "Footprint" ""\n'
        f'        (at {dimensions["start_pos"]} 0 0)\n'
        f'        (layer "F.Fab")\n'
        f'        (hide yes)\n'
        f'        (uuid "{uuid4()}")\n'
        f'{hidden_font_props}\n'
        f'    )\n'
        f'    (property "Datasheet" ""\n'
        f'        (at {dimensions["start_pos"]} 0 0)\n'
        f'        (layer "F.Fab")\n'
        f'        (hide yes)\n'
        f'        (uuid "{uuid4()}")\n'
        f'{hidden_font_props}\n'
        f'    )\n'
        f'    (property "Description" ""\n'
        f'        (at {dimensions["start_pos"]} 0 0)\n'
        f'        (layer "F.Fab")\n'
        f'        (hide yes)\n'
        f'        (uuid "{uuid4()}")\n'
        f'{hidden_font_props}\n'
        f'    )'
    )


def generate_shapes(dimensions: dict, specs: ConnectorSpecs) -> str:
    """Generate the shapes section of the footprint."""
    circle_center = -(
        dimensions["total_half_width_left"] + specs.silk_margin * 6
    )
    circle_end = -(
        dimensions["total_half_width_left"] + specs.silk_margin * 2
    )

    rect_start = -dimensions["total_half_width_left"]
    rect_end = dimensions["total_half_width_right"]

    def generate_rect(layer_name: str, stroke_width: str) -> str:
        return (
            f'    (fp_rect\n'
            f'        (start {rect_start:.3f} '
            f'{specs.rect_dims.height_bottom})\n'
            f'        (end {rect_end:.3f} {specs.rect_dims.height_top})\n'
            f'        (stroke\n'
            f'            (width {stroke_width})\n'
            f'            (type default)\n'
            f'        )\n'
            f'        (fill none)\n'
            f'        (layer "{layer_name}")\n'
            f'        (uuid "{uuid4()}")\n'
            f'    )'
        )

    def generate_circle(layer_name: str, fill_type: str) -> str:
        return (
            f'    (fp_circle\n'
            f'        (center {circle_center:.3f} 0)\n'
            f'        (end {circle_end:.3f} 0)\n'
            f'        (stroke\n'
            f'            (width {specs.silk_margin})\n'
            f'            (type solid)\n'
            f'        )\n'
            f'        (fill {fill_type})\n'
            f'        (layer "{layer_name}")\n'
            f'        (uuid "{uuid4()}")\n'
            f'    )'
        )

    shapes = [
        '    (attr through_hole)',
        generate_rect("F.SilkS", specs.silk_margin),
        generate_circle("F.SilkS", "solid"),
        generate_rect("F.CrtYd", "0.00635"),
        generate_rect("F.Fab", specs.silk_margin),
        generate_circle("F.Fab", "none")
    ]

    return "\n".join(shapes)


def generate_pads(
    part_info: ssc.PartInfo,
    specs: ConnectorSpecs,
    dimensions: dict
) -> str:
    """Generate the pads section of the footprint."""
    pads = []
    for pin_num in range(part_info.pin_count):
        xpos = dimensions["start_pos"] + (pin_num * part_info.pitch)
        pad_type = "rect" if pin_num == 0 else "circle"
        pad = (
            f'    (pad "{pin_num + 1}" thru_hole {pad_type}\n'
            f'        (at {xpos:.3f} 0)\n'
            f'        (size {specs.pad_size} {specs.pad_size})\n'
            f'        (drill {specs.drill_size})\n'
            f'        (layers "*.Cu" "*.Mask")\n'
            f'        (remove_unused_layers no)\n'
            f'        (solder_mask_margin {specs.mask_margin})\n'
            f'        (uuid "{uuid4()}")\n'
            f'    )'
        )
        pads.append(pad)
    return "\n".join(pads)


def generate_3d_model(part_info: ssc.PartInfo, specs: ConnectorSpecs) -> str:
    """Generate the 3D model section of the footprint."""
    step_offset = (part_info.pin_count - 2) * specs.step_multiplier
    model_offset = specs.model_offset_func(
        specs.model_offset_base,
        step_offset
    )

    model_path = (
        f'KiCAD_Symbol_Generator/3D_models/'
        f'CUI_DEVICES_{part_info.mpn}.step'
    )

    return (
        f'    (model "${{KIPRJMOD}}/{model_path}"\n'
        f'        (offset\n'
        f'            (xyz {model_offset[0]:.3f} '
        f'{model_offset[1]} {model_offset[2]})\n'
        f'        )\n'
        f'        (scale\n'
        f'            (xyz 1 1 1)\n'
        f'        )\n'
        f'        (rotate\n'
        f'            (xyz {specs.model_rotation[0]} '
        f'{specs.model_rotation[1]} {specs.model_rotation[2]})\n'
        f'        )\n'
        f'    )'
    )


def generate_footprint_file(part_info: ssc.PartInfo) -> None:
    """
    Generate and save a complete .kicad_mod file for a connector.

    Creates a KiCad footprint file in the connector_footprints.pretty
    directory using the specified part information and
    corresponding series specifications.

    Args:
        part_info: Component specifications including MPN and series

    Raises:
        ValueError: If the specified connector series is not supported
        IOError: If there are problems writing the output file
    """
    if part_info.series not in CONNECTOR_SPECS:
        raise ValueError(f"Unknown series: {part_info.series}")

    specs = CONNECTOR_SPECS[part_info.series]
    footprint_content = generate_footprint(part_info, specs)

    filename = f"connector_footprints.pretty/{part_info.mpn}.kicad_mod"
    with open(filename, 'w', encoding='utf-8') as output_file:
        output_file.write(footprint_content)
