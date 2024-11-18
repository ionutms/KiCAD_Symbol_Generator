"""
KiCad Footprint Generator for Surface Mount Capacitors

Generates standardized KiCad footprint files (.kicad_mod) for surface mount
capacitors. Uses manufacturer specifications to create accurate footprints
with appropriate pad dimensions and clearances.
"""

from typing import NamedTuple
from uuid import uuid4
from symbol_capacitors_specs import SERIES_SPECS, SeriesSpec
from footprint_capacitor_specs import CAPACITOR_SPECS, CapacitorSpecs


class FootprintSpecs(NamedTuple):
    """
    Complete specifications for generating a capacitor footprint.

    Combines physical dimensions with series-specific properties for
    generating accurate KiCad footprints.
    """
    series_spec: SeriesSpec     # Original series specifications
    capacitor_specs: CapacitorSpecs  # Physical specifications


def create_footprint_specs(series_spec: SeriesSpec) -> FootprintSpecs:
    """
    Create complete footprint specifications from series specifications.

    Args:
        series_spec: SeriesSpec object containing basic specifications

    Returns:
        FootprintSpecs object with complete physical dimensions

    Raises:
        KeyError: If case code is not found in CAPACITOR_SPECS
    """
    return FootprintSpecs(
        series_spec=series_spec,
        capacitor_specs=CAPACITOR_SPECS[series_spec.case_code_in]
    )


def generate_footprint(specs: FootprintSpecs) -> str:
    """
    Generate complete KiCad footprint file content for a capacitor.

    Args:
        specs: Combined specifications for the capacitor

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


def generate_header(specs: FootprintSpecs) -> str:
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


def generate_properties(specs: FootprintSpecs) -> str:
    """Generate properties section with capacitor-specific information."""
    footprint_name = \
        "C_" + \
        f"{specs.series_spec.case_code_in}_" + \
        f"{specs.series_spec.case_code_mm}" + \
        "Metric"

    cap_specs = specs.capacitor_specs
    text_pos = cap_specs.text_positions

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
        f'        (at 0 {text_pos.reference} 0)\n'
        f'        (layer "F.SilkS")\n'
        f'        (uuid "{uuid4()}")\n'
        f'{font_props}\n'
        f'    )\n'
        f'    (property "Value" "{footprint_name}"\n'
        f'        (at 0 {text_pos.value} 0)\n'
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


def generate_silkscreen(specs: FootprintSpecs) -> str:
    """Generate silkscreen elements with capacitor-specific markings."""
    silkscreen = []
    cap_specs = specs.capacitor_specs
    silk = cap_specs.silkscreen

    for symbol in ['-', '']:
        silkscreen.append(
            f'    (fp_line\n'
            f'        (start -{silk.extension} {symbol}{silk.y_position})\n'
            f'        (end {silk.extension} {symbol}{silk.y_position})\n'
            f'        (stroke\n'
            f'            (width 0.1524)\n'
            f'            (type solid)\n'
            f'        )\n'
            f'        (layer "F.SilkS")\n'
            f'        (uuid "{uuid4()}")\n'
            f'    )'
        )

    return "\n".join(silkscreen)


def generate_courtyard(specs: FootprintSpecs) -> str:
    """Generate courtyard outline with capacitor-specific clearances."""
    cap_specs = specs.capacitor_specs
    half_height = \
        cap_specs.body_dimensions.height / 2 + cap_specs.courtyard_margin/4
    half_width = cap_specs.courtyard_margin

    return (
        f'    (fp_rect\n'
        f'        (start -{half_width} -{half_height})\n'
        f'        (end {half_width} {half_height})\n'
        f'        (stroke\n'
        f'            (width 0.00635)\n'
        f'            (type solid)\n'
        f'        )\n'
        f'        (fill none)\n'
        f'        (layer "F.CrtYd")\n'
        f'        (uuid "{uuid4()}")\n'
        f'    )'
    )


def generate_fab_layer(specs: FootprintSpecs) -> str:
    """Generate fabrication layer with capacitor-specific markings."""
    cap_specs = specs.capacitor_specs
    body = cap_specs.body_dimensions
    half_width = body.width / 2
    half_height = body.height / 2

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

    # Reference designator
    fab_layer.append(
        f'    (fp_text user "${{REFERENCE}}"\n'
        f'        (at 0 {cap_specs.text_positions.fab_reference} 0)\n'
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


def generate_pads(specs: FootprintSpecs) -> str:
    """Generate SMD pads with capacitor-specific dimensions."""
    pads = []
    cap_specs = specs.capacitor_specs
    pad = cap_specs.pad_dimensions

    for pad_number, symbol in enumerate(['-', ''], start=1):
        pads.append(
            f'    (pad "{pad_number}" smd roundrect\n'
            f'        (at {symbol}{pad.center_x} 0)\n'
            f'        (size {pad.width} {pad.height})\n'
            f'        (layers "F.Cu" "F.Paste" "F.Mask")\n'
            f'        (roundrect_rratio {pad.roundrect_ratio})\n'
            f'        (uuid "{uuid4()}")\n'
            f'    )'
        )

    return "\n".join(pads)


def generate_3d_model(specs: FootprintSpecs) -> str:
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
    footprint_specs = create_footprint_specs(series_spec)
    footprint_content = generate_footprint(footprint_specs)

    filename = \
        f"{output_dir}/" + \
        "C_" + \
        f"{series_spec.case_code_in}_" + \
        f"{series_spec.case_code_mm}" + \
        "Metric.kicad_mod"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(footprint_content)