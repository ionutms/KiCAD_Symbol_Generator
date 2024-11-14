"""
KiCad Footprint Generator for Surface Mount Capacitors

Generates standardized KiCad footprint files (.kicad_mod) for surface mount
capacitors. Uses manufacturer specifications to create accurate footprints
with appropriate pad dimensions and clearances.
"""

from typing import Dict, NamedTuple
from uuid import uuid4
from series_specs_capacitors import SERIES_SPECS, SeriesSpec


class PadDimensions(NamedTuple):
    """
    Defines SMD pad dimensions and positioning.

    All measurements are in millimeters.
    """
    width: float      # Width of each pad
    height: float     # Height of each pad
    center_x: float   # Distance from origin to pad center
    roundrect_ratio: float  # Corner radius ratio for roundrect pads


class CapacitorSpecs(NamedTuple):
    """
    Complete specifications for generating a capacitor footprint.

    Combines physical dimensions with series-specific properties for
    generating accurate KiCad footprints.
    """
    series_spec: SeriesSpec     # Original series specifications
    body_width: float           # Width of capacitor body
    body_height: float          # Height of capacitor body
    pad_dims: PadDimensions     # Pad specifications
    silk_y: float               # Y-coordinate of silkscreen lines
    silk_extension: float       # X-extension of silkscreen lines from center
    silk_inset: float          # Distance silk extends from body
    courtyard_margin: float     # Courtyard margin beyond pads
    ref_y: float               # Y position for reference designator
    value_y: float             # Y position for value text
    fab_reference_y: float     # Y position for fab layer reference


# Mapping of case codes to physical dimensions
CASE_DIMENSIONS: Dict[str, Dict[str, float]] = {
    "0402": {
        "body_width": 1.0,
        "body_height": 0.5,
        "pad_width": 0.6,
        "pad_height": 0.7,
        "pad_center_x": 0.54,
        "silk_y": 0.38,
        "silk_extension": 0.153641,
        "silk_inset": 0.15,
        "courtyard_margin": 0.91,
        "ref_y": -1.27,
        "value_y": 1.27,
        "fab_reference_y": 2.54
    },
    "0603": {
        "body_width": 1.6,
        "body_height": 0.8,
        "pad_width": 0.9,
        "pad_height": 1.0,
        "pad_center_x": 0.875,
        "silk_y": 0.5225,
        "silk_extension": 0.237258,
        "silk_inset": 0.24,
        "courtyard_margin": 1.48,
        "ref_y": -1.524,
        "value_y": 1.524,
        "fab_reference_y": 2.794
    },
    "0805": {
        "body_width": 2.0,
        "body_height": 1.25,
        "pad_width": 1.15,
        "pad_height": 1.45,
        "pad_center_x": 0.95,
        "silk_y": 0.735,
        "silk_extension": 0.227064,
        "silk_inset": 0.23,
        "courtyard_margin": 1.68,
        "ref_y": -1.778,
        "value_y": 1.778,
        "fab_reference_y": 3.048
    },
    "1206": {
        "body_width": 3.2,
        "body_height": 1.6,
        "pad_width": 1.25,
        "pad_height": 1.8,
        "pad_center_x": 1.5,
        "silk_y": 0.91,
        "silk_extension": 0.727064,
        "silk_inset": 0.25,
        "courtyard_margin": 2.28,
        "ref_y": -2.032,
        "value_y": 2.032,
        "fab_reference_y": 3.302
    }
}


def create_capacitor_specs(series_spec: SeriesSpec) -> CapacitorSpecs:
    """
    Create complete capacitor specifications from series specifications.

    Args:
        series_spec: SeriesSpec object containing basic specifications

    Returns:
        CapacitorSpecs object with complete physical dimensions

    Raises:
        KeyError: If case code is not found in CASE_DIMENSIONS
    """
    case_dims = CASE_DIMENSIONS[series_spec.case_code_in]

    return CapacitorSpecs(
        series_spec=series_spec,
        body_width=case_dims["body_width"],
        body_height=case_dims["body_height"],
        pad_dims=PadDimensions(
            width=case_dims["pad_width"],
            height=case_dims["pad_height"],
            center_x=case_dims["pad_center_x"],
            roundrect_ratio=0.25
        ),
        silk_y=case_dims["silk_y"],
        silk_extension=case_dims["silk_extension"],
        silk_inset=case_dims["silk_inset"],
        courtyard_margin=case_dims["courtyard_margin"],
        ref_y=case_dims["ref_y"],
        value_y=case_dims["value_y"],
        fab_reference_y=case_dims["fab_reference_y"],
    )


def generate_footprint(specs: CapacitorSpecs) -> str:
    """
    Generate complete KiCad footprint file content for a capacitor.

    Args:
        specs: Physical specifications for the capacitor

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


def generate_header(specs: CapacitorSpecs) -> str:
    """
    Generate the footprint header section with capacitor-specific details.
    """
    case_in = specs.series_spec.case_code_in
    case_mm = specs.series_spec.case_code_mm

    footprint_name = f"C_{case_in}_{case_mm}Metric"

    return (
        f'(footprint "{footprint_name}"\n'
        f'    (version 20240108)\n'
        f'    (generator "pcbnew")\n'
        f'    (generator_version "8.0")\n'
        f'    (layer "F.Cu")\n'
        f'    (descr "")\n'
        f'    (tags "")\n'
        f'    (attr smd)'
    )


def generate_properties(specs: CapacitorSpecs) -> str:
    """Generate properties section with capacitor-specific information."""
    footprint_name = \
        "C_" + \
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
        f'    (property "Reference" "C**"\n'
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


def generate_silkscreen(specs: CapacitorSpecs) -> str:
    """Generate silkscreen elements with capacitor-specific markings."""
    silkscreen = []

    # Top silkscreen line
    silkscreen.append(
        f'    (fp_line\n'
        f'        (start -{specs.silk_extension} -{specs.silk_y})\n'
        f'        (end {specs.silk_extension} -{specs.silk_y})\n'
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
        f'        (start -{specs.silk_extension} {specs.silk_y})\n'
        f'        (end {specs.silk_extension} {specs.silk_y})\n'
        f'        (stroke\n'
        f'            (width 0.1524)\n'
        f'            (type solid)\n'
        f'        )\n'
        f'        (layer "F.SilkS")\n'
        f'        (uuid "{uuid4()}")\n'
        f'    )'
    )

    return "\n".join(silkscreen)


def generate_courtyard(specs: CapacitorSpecs) -> str:
    """Generate courtyard outline with capacitor-specific clearances."""
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


def generate_fab_layer(specs: CapacitorSpecs) -> str:
    """Generate fabrication layer with capacitor-specific markings."""
    half_width = specs.body_width / 2
    half_height = specs.body_height / 2

    fab_layer = []

    # Main body outline
    fab_layer.append(
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

    # Polarity marking on negative side (left)
    fab_layer.append(
        f'    (fp_line\n'
        f'        (start -{half_width + 0.1} -{half_height})\n'
        f'        (end -{half_width + 0.1} {half_height})\n'
        f'        (stroke\n'
        f'            (width 0.0254)\n'
        f'            (type default)\n'
        f'        )\n'
        f'        (layer "F.Fab")\n'
        f'        (uuid "{uuid4()}")\n'
        f'    )'
    )

    # Reference designator
    fab_layer.append(
        f'    (fp_text user "${{REFERENCE}}"\n'
        f'        (at 0 {specs.fab_reference_y} 0)\n'
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

    return "\n".join(fab_layer)


def generate_pads(specs: CapacitorSpecs) -> str:
    """Generate SMD pads with capacitor-specific dimensions."""
    pads = []

    # Negative pad (1) - Left pad
    pads.append(
        f'    (pad "1" smd roundrect\n'
        f'        (at -{specs.pad_dims.center_x} 0)\n'
        f'        (size {specs.pad_dims.width} {specs.pad_dims.height})\n'
        f'        (layers "F.Cu" "F.Paste" "F.Mask")\n'
        f'        (roundrect_rratio {specs.pad_dims.roundrect_ratio})\n'
        f'        (uuid "{uuid4()}")\n'
        f'    )'
    )

    # Positive pad (2) - Right pad
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


def generate_3d_model(specs: CapacitorSpecs) -> str:
    """Generate 3D model reference for the capacitor."""
    case_code = specs.series_spec.case_code_in
    return (
        f'    (model "${{KIPRJMOD}}/KiCAD_Symbol_Generator/3D_models/'
        f'C_{case_code}.step"\n'
        f'        (offset (xyz 0 0 0))\n'
        f'        (scale (xyz 1 1 1))\n'
        f'        (rotate (xyz 0 0 0))\n'
        f'    )'
    )


def generate_footprint_file(
        series_name: str,
        output_dir: str) -> None:
    """
    Generate and save a complete .kicad_mod file for a capacitor.

    Args:
        series_name: Name of the capacitor series (e.g., "C0402")
        output_dir: Directory to save the generated footprint file

    Raises:
        KeyError: If series_name is not found in SERIES_SPECS
        IOError: If there are problems writing the output file
    """
    series_spec = SERIES_SPECS[series_name]
    capacitor_specs = create_capacitor_specs(series_spec)
    footprint_content = generate_footprint(capacitor_specs)

    filename = \
        f"{output_dir}/" + \
        "C_" + \
        f"{series_spec.case_code_in}_" + \
        f"{series_spec.case_code_mm}" + \
        "Metric.kicad_mod"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(footprint_content)
