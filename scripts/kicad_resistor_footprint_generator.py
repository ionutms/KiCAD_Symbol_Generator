"""
KiCad Footprint Generator for Panasonic ERJ Series Resistors

Generates standardized KiCad footprint files (.kicad_mod) for Panasonic ERJ
series SMD resistors. Uses manufacturer specifications to create accurate
footprints with appropriate pad dimensions and clearances.
"""

from typing import Dict, NamedTuple
from uuid import uuid4
from series_specs_resistors import SERIES_SPECS, SeriesSpec


class PadDimensions(NamedTuple):
    """
    Defines SMD pad dimensions and positioning.

    All measurements are in millimeters.
    """
    width: float      # Width of each pad
    height: float     # Height of each pad
    center_x: float   # Distance from origin to pad center
    roundrect_ratio: float  # Corner radius ratio for roundrect pads


class ResistorSpecs(NamedTuple):
    """
    Complete specifications for generating a resistor footprint.

    Combines physical dimensions with series-specific properties for
    generating accurate KiCad footprints.
    """
    series_spec: SeriesSpec    # Original series specifications
    body_width: float         # Width of resistor body
    body_height: float        # Height of resistor body
    pad_dims: PadDimensions   # Pad specifications
    silk_inset: float        # Distance silk extends from body
    courtyard_margin: float  # Courtyard margin beyond pads
    ref_y: float            # Y position for reference designator
    value_y: float          # Y position for value text
    fab_reference_y: float  # Y position for fab layer reference


# Mapping of case codes to physical dimensions
CASE_DIMENSIONS: Dict[str, Dict[str, float]] = {
    "0402": {
        "body_width": 1.0,
        "body_height": 0.5,
        "pad_width": 0.54,
        "pad_height": 0.64,
        "pad_center_x": 0.51,
        "silk_inset": 0.15,
        "courtyard_margin": 0.91,
        "ref_y": -1.27,
        "value_y": 1.27,
        "fab_reference_y": 2.54
    },
    "0603": {
        "body_width": 1.6,
        "body_height": 0.8,
        "pad_width": 0.8,
        "pad_height": 0.95,
        "pad_center_x": 0.825,
        "silk_inset": 0.24,
        "courtyard_margin": 1.48,
        "ref_y": -1.524,
        "value_y": 1.524,
        "fab_reference_y": 2.794
    },
    "0805": {
        "body_width": 2.0,
        "body_height": 1.25,
        "pad_width": 1.025,
        "pad_height": 1.4,
        "pad_center_x": 0.9125,
        "silk_inset": 0.23,
        "courtyard_margin": 1.68,
        "ref_y": -1.778,
        "value_y": 1.778,
        "fab_reference_y": 3.048
    },
    "1206": {
        "body_width": 3.2,
        "body_height": 1.6,
        "pad_width": 1.125,
        "pad_height": 1.75,
        "pad_center_x": 1.4625,
        "silk_inset": 0.25,
        "courtyard_margin": 2.28,
        "ref_y": -2.032,
        "value_y": 2.032,
        "fab_reference_y": 3.302
    }
}


def create_resistor_specs(series_spec: SeriesSpec) -> ResistorSpecs:
    """
    Create complete resistor specifications from series specifications.

    Args:
        series_spec: SeriesSpec object containing basic specifications

    Returns:
        ResistorSpecs object with complete physical dimensions

    Raises:
        KeyError: If case code is not found in CASE_DIMENSIONS
    """
    case_dims = CASE_DIMENSIONS[series_spec.case_code_in]

    # Scale text positions based on body size
    size_factor = float(series_spec.case_code_in[:2]) / 4.0
    base_text_offset = 1.27

    return ResistorSpecs(
        series_spec=series_spec,
        body_width=case_dims["body_width"],
        body_height=case_dims["body_height"],
        pad_dims=PadDimensions(
            width=case_dims["pad_width"],
            height=case_dims["pad_height"],
            center_x=case_dims["pad_center_x"],
            roundrect_ratio=0.25
        ),
        silk_inset=case_dims["silk_inset"],
        courtyard_margin=case_dims["courtyard_margin"],
        ref_y=-base_text_offset * size_factor,
        value_y=base_text_offset * size_factor,
        fab_reference_y=2.0 * base_text_offset * size_factor
    )


def generate_footprint(specs: ResistorSpecs) -> str:
    """
    Generate complete KiCad footprint file content for an ERJ series resistor.

    Args:
        specs: Physical specifications for the resistor

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


def generate_header(specs: ResistorSpecs) -> str:
    """Generate the footprint header section with ERJ-specific details."""
    series = specs.series_spec.base_series
    case_in = specs.series_spec.case_code_in
    case_mm = specs.series_spec.case_code_mm
    power = specs.series_spec.power_rating
    voltage = specs.series_spec.voltage_rating

    description = (
        f"Panasonic {series} series resistor, {case_in} ({case_mm} Metric), "
        f"{power}, {voltage}, square end terminal"
    )

    footprint_name = f"R_{case_in}_{case_mm}Metric"

    return (
        f'(footprint "{footprint_name}"\n'
        f'    (version 20240108)\n'
        f'    (generator "pcbnew")\n'
        f'    (generator_version "8.0")\n'
        f'    (layer "F.Cu")\n'
        f'    (descr "{description}")\n'
        f'    (tags "resistor panasonic erj")\n'
        f'    (attr smd)'
    )


def generate_properties(specs: ResistorSpecs) -> str:
    """Generate properties section with ERJ-specific information."""
    footprint_name = \
        "R_" + \
        f"{specs.series_spec.case_code_in}_" + \
        f"{specs.series_spec.case_code_mm}" + \
        "Metric"

    font_props = (
        '        (effects\n'
        '            (font\n'
        '                (size 0.762 0.762)\n'
        '                (thickness 0.1524)\n'
        '                (bold yes)\n'
        '            )\n'
        '            (justify left)\n'
        '        )'
    )

    return (
        f'    (property "Reference" "REF**"\n'
        f'        (at 0 {specs.ref_y} 0)\n'
        f'        (layer "F.SilkS")\n'
        f'        (uuid "{uuid4()}")\n'
        f'{font_props}\n'
        f'    )\n'
        f'    (property "Value" "{footprint_name}"\n'
        f'        (at 0 {specs.value_y} 0)\n'
        f'        (layer "F.Fab")\n'
        f'        (uuid "{uuid4()}")\n'
        f'{font_props}\n'
        f'    )\n'
        f'    (property "Footprint" ""\n'
        f'        (at 0 0 0)\n'
        f'        (layer "F.Fab")\n'
        f'        (hide yes)\n'
        f'        (uuid "{uuid4()}")\n'
        f'{font_props}\n'
        f'    )'
    )


def generate_silkscreen(specs: ResistorSpecs) -> str:
    """Generate silkscreen elements with ERJ-specific clearances."""
    half_height = specs.body_height / 2
    silkscreen = []

    # Top silkscreen line
    silkscreen.append(
        f'    (fp_line\n'
        f'        (start -{specs.silk_inset} -{half_height})\n'
        f'        (end {specs.silk_inset} -{half_height})\n'
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
        f'        (start -{specs.silk_inset} {half_height})\n'
        f'        (end {specs.silk_inset} {half_height})\n'
        f'        (stroke\n'
        f'            (width 0.1524)\n'
        f'            (type solid)\n'
        f'        )\n'
        f'        (layer "F.SilkS")\n'
        f'        (uuid "{uuid4()}")\n'
        f'    )'
    )

    return "\n".join(silkscreen)


def generate_courtyard(specs: ResistorSpecs) -> str:
    """Generate courtyard outline with ERJ-specific clearances."""
    half_height = specs.body_height / 2 + specs.courtyard_margin/4
    return (
        f'    (fp_poly\n'
        f'        (pts\n'
        f'            (xy -{specs.courtyard_margin} -{half_height}) '
        f'(xy {specs.courtyard_margin} -{half_height}) '
        f'(xy {specs.courtyard_margin} {half_height}) '
        f'(xy -{specs.courtyard_margin} {half_height})\n'
        f'        )\n'
        f'        (stroke\n'
        f'            (width 0.00635)\n'
        f'            (type solid)\n'
        f'        )\n'
        f'        (fill none)\n'
        f'        (layer "F.CrtYd")\n'
        f'        (uuid "{uuid4()}")\n'
        f'    )'
    )


def generate_fab_layer(specs: ResistorSpecs) -> str:
    """Generate fabrication layer with ERJ-specific markings."""
    half_width = specs.body_width / 2
    half_height = specs.body_height / 2

    return (
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
        f'    )\n'
        f'    (fp_text user "${{REFERENCE}}"\n'
        f'        (at 0 {specs.fab_reference_y} 0)\n'
        f'        (layer "F.Fab")\n'
        f'        (uuid "{uuid4()}")\n'
        f'        (effects\n'
        f'            (font\n'
        f'                (size 0.762 0.762)\n'
        f'                (thickness 0.1524)\n'
        f'            )\n'
        f'        )\n'
        f'    )'
    )


def generate_pads(specs: ResistorSpecs) -> str:
    """Generate SMD pads with ERJ-specific dimensions."""
    pads = []

    # Left pad (1)
    pads.append(
        f'    (pad "1" smd roundrect\n'
        f'        (at -{specs.pad_dims.center_x} 0)\n'
        f'        (size {specs.pad_dims.width} {specs.pad_dims.height})\n'
        f'        (layers "F.Cu" "F.Paste" "F.Mask")\n'
        f'        (roundrect_rratio {specs.pad_dims.roundrect_ratio})\n'
        f'        (uuid "{uuid4()}")\n'
        f'    )'
    )

    # Right pad (2)
    pads.append(
        f'    (pad "2" smd roundrect\n'
        f'        (at {specs.pad_dims.center_x} 0)\n'
        f'        (size {specs.pad_dims.width} {specs.pad_dims.height})\n'
        f'        (layers "F.Cu" "F.Paste" "F.Mask")\n'
        f'        (roundrect_rratio {specs.pad_dims.roundrect_ratio})\n'
        f'        (uuid "{uuid4()}")\n'
        f'    )'
    )

    return "\n".join(pads)


def generate_3d_model(specs: ResistorSpecs) -> str:
    """Generate 3D model reference for ERJ series."""
    case_code = specs.series_spec.case_code_in
    return (
        f'    (model "${{KIPRJMOD}}/KiCAD_Symbol_Generator/3D_models/'
        f'R_{case_code}.step"\n'
        f'        (offset (xyz 0 0 0))\n'
        f'        (scale (xyz 1 1 1))\n'
        f'        (rotate (xyz 0 0 0))\n'
        f'    )'
    )


def generate_footprint_file(
        series_name: str,
        output_dir: str) -> None:
    """
    Generate and save a complete .kicad_mod file for an ERJ series resistor.

    Args:
        series_name: Name of the ERJ series (e.g., "ERJ-2RK")
        output_dir: Directory to save the generated footprint file

    Raises:
        KeyError: If series_name is not found in SERIES_SPECS
        IOError: If there are problems writing the output file
    """
    series_spec = SERIES_SPECS[series_name]
    resistor_specs = create_resistor_specs(series_spec)
    footprint_content = generate_footprint(resistor_specs)

    filename = \
        f"{output_dir}/" + \
        "R_" + \
        f"{series_spec.case_code_in}_" + \
        f"{series_spec.case_code_mm}" + \
        "Metric.kicad_mod"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(footprint_content)
