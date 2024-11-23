"""
KiCad Footprint Generator for Diodes

Generates standardized KiCad footprint files (.kicad_mod) for diodes
based on manufacturer specifications. Creates accurate footprints with
appropriate pad dimensions, clearances, and silkscreen markings for surface
mount diodes.
"""

from uuid import uuid4
import symbol_diode_specs as sds
from footprint_diode_specs import DIODE_SPECS, DiodeSpecs


def generate_footprint(part_info: sds.PartInfo, specs: DiodeSpecs) -> str:
    """
    Generate complete KiCad footprint file content for a diode.

    Args:
        part_info: Component specifications
        specs: Physical specifications for the diode series from DIODE_SPECS

    Returns:
        Complete .kicad_mod file content as formatted string
    """
    sections = [
        generate_header(part_info.mpn),
        generate_properties(part_info, specs),
        generate_shapes(specs),
        generate_pads(specs),
        generate_3d_model(part_info),
        ")"  # Close the footprint
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


def generate_properties(part_info: sds.PartInfo, specs: DiodeSpecs) -> str:
    """Generate the properties section of the footprint."""
    font_props = (
        '        (effects\n'
        '            (font\n'
        '                (size 0.762 0.762)\n'
        '                (thickness 0.1524)\n'
        '            )\n'
        '            (justify left)\n'
        '        )'
    )

    ref_offset_y = specs.ref_offset_y

    return (
        '    (property "Reference" "D"\n'
        f'        (at 0 {ref_offset_y} 0)\n'
        '        (unlocked yes)\n'
        '        (layer "F.SilkS")\n'
        f'        (uuid "{uuid4()}")\n'
        f'{font_props}\n'
        '    )\n'
        f'    (property "Value" "{part_info.mpn}"\n'
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


def generate_shapes(specs: DiodeSpecs) -> str:
    """Generate the shapes section of the footprint."""
    half_width = specs.body_dimensions.width / 2
    half_height = specs.body_dimensions.height / 2
    silkscreen_x = specs.pad_dimensions.center_x - specs.pad_dimensions.width / 2

    shapes = []

    # Silkscreen lines
    for symbol in ['-', '']:
        shapes.append(
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
            '    )'
        )

    # Add cathode marker line
    shapes.append(
        '    (fp_line\n'
        f'        (start -{silkscreen_x} -{half_height})\n'
        f'        (end -{silkscreen_x} {half_height})\n'
        '        (stroke\n'
        '            (width 0.254)\n'
        '            (type solid)\n'
        '        )\n'
        '        (layer "F.SilkS")\n'
        f'        (uuid "{uuid4()}")\n'
        '    )'
    )

    # Courtyard
    shapes.append(
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

    # Fabrication layer outline
    shapes.append(
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

    # Cathode marker on fabrication layer
    shapes.append(
        '    (fp_line\n'
        f'        (start -{half_width} -{half_height})\n'
        f'        (end -{half_width} {half_height})\n'
        '        (stroke\n'
        '            (width 0.0254)\n'
        '            (type solid)\n'
        '        )\n'
        '        (layer "F.Fab")\n'
        f'        (uuid "{uuid4()}")\n'
        '    )'
    )

    # Reference on fab layer
    shapes.append(
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

    return "\n".join(shapes)


def generate_pads(specs: DiodeSpecs) -> str:
    """Generate the pads section of the footprint."""
    pads = []

    # Cathode pad (1)
    pads.append(
        '    (pad "1" smd rect\n'
        f'        (at -{specs.pad_dimensions.center_x} 0)\n'
        '        (size '
        f'{specs.pad_dimensions.width} {specs.pad_dimensions.height})\n'
        '        (layers "F.Cu" "F.Paste" "F.Mask")\n'
        f'        (uuid "{uuid4()}")\n'
        '    )'
    )

    # Anode pad (2)
    pads.append(
        '    (pad "2" smd rect\n'
        f'        (at {specs.pad_dimensions.center_x} 0)\n'
        '        (size '
        f'{specs.pad_dimensions.width} {specs.pad_dimensions.height})\n'
        '        (layers "F.Cu" "F.Paste" "F.Mask")\n'
        f'        (uuid "{uuid4()}")\n'
        '    )'
    )

    # Add thermal pad if specified
    if specs.has_thermal_pad and specs.pad_dimensions.thermal_width > 0:
        pads.append(
            '    (pad "3" smd rect\n'
            '        (at 0 0)\n'
            '        (size '
            f'{specs.pad_dimensions.thermal_width} '
            f'{specs.pad_dimensions.thermal_height})\n'
            '        (layers "F.Cu" "F.Paste" "F.Mask")\n'
            f'        (uuid "{uuid4()}")\n'
            '    )'
        )

    return "\n".join(pads)


def generate_3d_model(part_info: sds.PartInfo) -> str:
    """Generate the 3D model section of the footprint."""
    return (
        f'    (model "${{KIPRJMOD}}/KiCAD_Symbol_Generator/3D_models/'
        f'{part_info.mpn}.step"\n'
        '        (offset (xyz 0 0 0))\n'
        '        (scale (xyz 1 1 1))\n'
        '        (rotate (xyz 0 0 0))\n'
        '    )'
    )


def generate_footprint_file(part_info: sds.PartInfo, output_dir: str) -> None:
    """
    Generate and save a complete .kicad_mod file for a diode.

    Args:
        part_info: Component specifications including MPN and package type
        output_dir: Directory path where the footprint file will be saved

    Raises:
        ValueError: If the specified diode package is not supported
        IOError: If there are problems writing the output file
    """
    if part_info.package not in DIODE_SPECS:
        raise ValueError(f"Unknown package type: {part_info.package}")

    specs = DIODE_SPECS[part_info.package]
    footprint_content = generate_footprint(part_info, specs)

    filename = f"{output_dir}/{part_info.mpn}.kicad_mod"
    with open(filename, 'w', encoding='utf-8') as file_handle:
        file_handle.write(footprint_content)
