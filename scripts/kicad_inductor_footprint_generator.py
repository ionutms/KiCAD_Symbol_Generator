"""
KiCad Footprint Generator Module for Inductors

Generates standardized KiCad footprint files (.kicad_mod) for various inductor
series. Handles pad placement, silkscreen generation, and 3D model alignment
based on manufacturer specifications.

The module supports multiple inductor series with different package sizes and
pad configurations, generating complete footprint definitions including:
- Surface mount pad layouts
- Silkscreen outlines
- Component identifiers
- 3D model references
"""

from typing import NamedTuple
from uuid import uuid4
import series_specs_inductors as ssi


class PadSpecs(NamedTuple):
    """
    Defines pad dimensions and spacing for surface mount components.

    All measurements are in millimeters.
    """
    width: float      # Pad width
    length: float     # Pad length
    spacing: float    # Center-to-center distance between pads


class OutlineSpecs(NamedTuple):
    """
    Defines component body outline dimensions.

    All measurements are in millimeters.
    """
    width: float      # Total width of component body
    length: float     # Total length of component body
    height: float     # Height of component body (for 3D model)


class InductorSpecs(NamedTuple):
    """
    Complete specifications for generating an inductor footprint.

    Defines all physical dimensions, pad properties, and 3D model parameters
    needed to generate a complete KiCad footprint file.
    """
    pads: PadSpecs           # Pad dimensions and spacing
    outline: OutlineSpecs    # Component body dimensions
    silk_margin: float       # Clearance for silkscreen outlines
    mask_margin: float       # Solder mask clearance around pads
    paste_margin: float      # Solder paste margin adjustment
    paste_ratio: float       # Solder paste ratio adjustment
    fab_ref_y: float        # Y position for fabrication reference
    silk_ref_y: float       # Y position for silkscreen reference
    model_offset: tuple[float, float, float]  # 3D model offset
    model_rotation: tuple[float, float, float]  # 3D model rotation angles


# Dictionary mapping series codes to their specifications
INDUCTOR_SPECS = {
    "XFL4020": InductorSpecs(
        pads=PadSpecs(
            width=1.35,
            length=1.75,
            spacing=3.4
        ),
        outline=OutlineSpecs(
            width=4.0,
            length=4.0,
            height=2.0
        ),
        silk_margin=0.1524,
        mask_margin=0.0762,
        paste_margin=0.0508,
        paste_ratio=0.9,
        fab_ref_y=2.8,
        silk_ref_y=-2.8,
        model_offset=(0.0, 0.0, 0.0),
        model_rotation=(0.0, 0.0, 0.0)
    ),
    "XFL4015": InductorSpecs(
        pads=PadSpecs(
            width=1.2,
            length=1.6,
            spacing=3.0
        ),
        outline=OutlineSpecs(
            width=4.0,
            length=4.0,
            height=1.5
        ),
        silk_margin=0.1524,
        mask_margin=0.0762,
        paste_margin=0.0508,
        paste_ratio=0.9,
        fab_ref_y=2.6,
        silk_ref_y=-2.6,
        model_offset=(0.0, 0.0, 0.0),
        model_rotation=(0.0, 0.0, 0.0)
    ),
    # Add more series specifications as needed
}


def generate_footprint(part_info: ssi.PartInfo, specs: InductorSpecs) -> str:
    """
    Generate complete KiCad footprint file content for an inductor.

    Creates all required sections of a .kicad_mod file including pad layout,
    component outline, text elements, and 3D model references.

    Args:
        part_info: Component specifications from the inductor database
        specs: Physical specifications for the inductor series

    Returns:
        Complete .kicad_mod file content as formatted string
    """
    sections = [
        generate_header(part_info.series),
        generate_properties(part_info, specs),
        generate_shapes(specs),
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


def generate_properties(part_info: ssi.PartInfo, specs: InductorSpecs) -> str:
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
        '            hide\n'
        '        )'
    )

    return (
        f'    (property "Reference" "L"\n'
        f'        (at 0 {specs.silk_ref_y} 0)\n'
        f'        (layer "F.SilkS")\n'
        f'        (uuid "{uuid4()}")\n'
        f'{font_props}\n'
        f'    )\n'
        f'    (property "Value" "{part_info.series}"\n'
        f'        (at 0 {specs.fab_ref_y} 0)\n'
        f'        (layer "F.Fab")\n'
        f'        (uuid "{uuid4()}")\n'
        f'{font_props}\n'
        f'    )\n'
        f'    (property "Footprint" ""\n'
        f'        (at 0 0 0)\n'
        f'        (layer "F.Fab")\n'
        f'        (uuid "{uuid4()}")\n'
        f'{hidden_font_props}\n'
        f'    )'
    )


def generate_shapes(specs: InductorSpecs) -> str:
    """Generate the shapes section of the footprint."""
    half_width = specs.outline.width / 2

    def generate_rect(layer_name: str, margin: float) -> str:
        total_margin = specs.silk_margin + margin
        width = specs.outline.width + total_margin * 2
        length = specs.outline.length + total_margin * 2
        half_w = width / 2
        half_l = length / 2

        return (
            f'    (fp_rect\n'
            f'        (start {-half_w} {-half_l})\n'
            f'        (end {half_w} {half_l})\n'
            f'        (stroke\n'
            f'            (width {specs.silk_margin})\n'
            f'            (type default)\n'
            f'        )\n'
            f'        (fill none)\n'
            f'        (layer "{layer_name}")\n'
            f'        (uuid "{uuid4()}")\n'
            f'    )'
        )

    # Pin 1 marker
    marker_x = -(half_width + specs.silk_margin * 4)
    marker_size = specs.silk_margin * 2
    pin_marker = (
        f'    (fp_circle\n'
        f'        (center {marker_x} 0)\n'
        f'        (end {marker_x + marker_size} 0)\n'
        f'        (stroke\n'
        f'            (width {specs.silk_margin})\n'
        f'            (type default)\n'
        f'        )\n'
        f'        (fill none)\n'
        f'        (layer "F.SilkS")\n'
        f'        (uuid "{uuid4()}")\n'
        f'    )'
    )

    shapes = [
        '    (attr smd)',
        generate_rect("F.SilkS", specs.silk_margin),
        generate_rect("F.CrtYd", specs.silk_margin * 2),
        generate_rect("F.Fab", 0),
        pin_marker
    ]

    return "\n".join(shapes)


def generate_pads(specs: InductorSpecs) -> str:
    """Generate the pads section of the footprint."""
    half_spacing = specs.pads.spacing / 2

    pad_props = (
        f'        (size {specs.pads.width} {specs.pads.length})\n'
        f'        (layers "F.Cu" "F.Paste" "F.Mask")\n'
        f'        (solder_mask_margin {specs.mask_margin})\n'
        f'        (solder_paste_margin {specs.paste_margin})\n'
        f'        (solder_paste_margin_ratio {specs.paste_ratio})\n'
        f'        (uuid "{uuid4()}")'
    )

    pads = [
        f'    (pad "1" smd rect\n'
        f'        (at {-half_spacing} 0)\n'
        f'{pad_props}\n'
        f'    )',
        f'    (pad "2" smd rect\n'
        f'        (at {half_spacing} 0)\n'
        f'{pad_props}\n'
        f'    )'
    ]

    return "\n".join(pads)


def generate_3d_model(part_info: ssi.PartInfo, specs: InductorSpecs) -> str:
    """Generate the 3D model section of the footprint."""
    model_path = (
        f'KiCAD_Symbol_Generator/3D_models/'
        f'{part_info.series}.step'
    )

    return (
        f'    (model "${{KIPRJMOD}}/{model_path}"\n'
        f'        (offset\n'
        f'            (xyz {specs.model_offset[0]} '
        f'{specs.model_offset[1]} {specs.model_offset[2]})\n'
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


def generate_footprint_file(part_info: ssi.PartInfo) -> None:
    """
    Generate and save a complete .kicad_mod file for an inductor.

    Creates a KiCad footprint file in the inductor_footprints.pretty
    directory using the specified part information and series specifications.

    Args:
        part_info: Component specifications including MPN and series

    Raises:
        ValueError: If the specified inductor series is not supported
        IOError: If there are problems writing the output file
    """
    if part_info.series not in INDUCTOR_SPECS:
        raise ValueError(f"Unknown series: {part_info.series}")

    specs = INDUCTOR_SPECS[part_info.series]
    footprint_content = generate_footprint(part_info, specs)

    filename = f"inductor_footprints.pretty/{part_info.series}.kicad_mod"
    with open(filename, 'w', encoding='utf-8') as output_file:
        output_file.write(footprint_content)
