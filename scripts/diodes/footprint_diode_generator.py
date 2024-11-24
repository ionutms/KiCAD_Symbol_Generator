"""KiCad Footprint Generator for Diodes.

Generates standardized KiCad footprint files (.kicad_mod) for diodes
based on manufacturer specifications. Creates accurate footprints with
appropriate pad dimensions, clearances, and silkscreen markings for surface
mount diodes.
"""

from pathlib import Path
from uuid import uuid4

import symbol_diode_specs as sds
from footprint_diode_specs import DIODE_SPECS, DiodeSpecs


def generate_footprint(part_info: sds.PartInfo, specs: DiodeSpecs) -> str:
    """Generate complete KiCad footprint file content for a diode.

    Args:
        part_info: Component specifications
        specs: Physical specifications for the diode series from DIODE_SPECS

    Returns:
        Complete .kicad_mod file content as formatted string

    """
    sections = [
        generate_header(part_info),
        generate_properties(specs),
        generate_shapes(specs),
        generate_pads(specs),
        generate_3d_model(part_info),
        ")",  # Close the footprint
    ]
    return "\n".join(sections)


def generate_header(part_info: sds.PartInfo) -> str:
    """Generate the footprint header section."""
    return (
        f'(footprint "{part_info.mpn}"\n'
        '    (version 20240108)\n'
        '    (generator "pcbnew")\n'
        '    (generator_version "8.0")\n'
        '    (layer "F.Cu")\n'
        f'    (descr "{part_info.description}")\n'
        f'    (tags "Diode {part_info.package} {part_info.mpn}")\n'
        '    (attr smd)'
    )


def generate_properties(specs: DiodeSpecs) -> str:
    """Generate the properties section of the footprint."""
    text_size = 0.762
    text_thickness = 0.1524

    ref_text = (
        '    (fp_text reference "REF**"\n'
        f'        (at 0 {specs.ref_offset_y} 0)\n'
        '        (layer "F.SilkS")\n'
        f'        (uuid "{uuid4()}")\n'
        '        (effects\n'
        '            (font\n'
        f'                (size {text_size} {text_size})\n'
        f'                (thickness {text_thickness})\n'
        '            )\n'
        "            (justify left)\n"
        '        )\n'
        '    )'
    )

    val_text = (
        f'    (fp_text value "to do"\n'
        f'        (at 0 {-specs.ref_offset_y} 0)\n'
        '        (layer "F.Fab")\n'
        f'        (uuid "{uuid4()}")\n'
        '        (effects\n'
        '            (font\n'
        f'                (size {text_size} {text_size})\n'
        f'                (thickness {text_thickness})\n'
        '            )\n'
        "            (justify left)\n"
        '        )\n'
        '    )'
    )

    user_text = (
        '    (fp_text user "${REFERENCE}"\n'
        '        (at 0 0 0)\n'
        '        (layer "F.Fab")\n'
        f'        (uuid "{uuid4()}")\n'
        '        (effects\n'
        '            (font\n'
        f'                (size {text_size} {text_size})\n'
        f'                (thickness {text_thickness})\n'
        '            )\n'
        "            (justify left)\n"
        '        )\n'
        '    )'
    )

    return "\n".join([ref_text, val_text, user_text])  # noqa: FLY002


def generate_shapes(specs: DiodeSpecs) -> str:
    """Generate the shapes section of the footprint."""
    half_width = specs.body_dimensions.width / 2
    half_height = specs.body_dimensions.height / 2

    shapes = []

    # Fabrication layer outline
    shapes.append(
        "    (fp_rect\n"
        f"        (start -{half_width} -{half_height})\n"
        f"        (end {half_width} {half_height})\n"
        "        (stroke\n"
        "            (width 0.0254)\n"
        "            (type default)\n"
        "        )\n"
        "        (fill none)\n"
        '        (layer "F.Fab")\n'
        f'        (uuid "{uuid4()}")\n'
        "    )",
    )

    # Silkscreen lines
    shapes.append(
        "    (fp_rect\n"
        f"        (start -{half_width} -{half_height})\n"
        f"        (end {half_width} {half_height})\n"
        "        (stroke\n"
        "            (width 0.1524)\n"
        "            (type default)\n"
        "        )\n"
        "        (fill none)\n"
        '        (layer "F.SilkS")\n'
        f'        (uuid "{uuid4()}")\n'
        "    )",
    )

    # Courtyard
    shapes.append(
        "    (fp_rect\n"
        f"        (start -{half_width} -{half_height})\n"
        f"        (end {half_width} {half_height})\n"
        "        (stroke\n"
        "            (width 0.00635)\n"
        "            (type default)\n"
        "        )\n"
        "        (fill none)\n"
        '        (layer "F.CrtYd")\n'
        f'        (uuid "{uuid4()}")\n'
        "    )",
    )

    return "\n".join(shapes)


def generate_pads(specs: DiodeSpecs) -> str:
    """Generate the pads section of the footprint with pad dimensions.

    Args:
        specs: DiodeSpecs containing asymmetric pad dimensions

    Returns:
        String containing KiCad footprint pad definitions

    """
    pad_props = specs.pad_dimensions

    # Cathode pad (1)
    cathode = (
        '    (pad "1" smd roundrect\n'
        f'        (at -{pad_props.cathode_center_x} 0)\n'
        '        (size '
        f'{pad_props.cathode_width} {pad_props.cathode_height})\n'
        '        (layers "F.Cu" "F.Paste" "F.Mask")\n'
        f"        (roundrect_rratio {pad_props.roundrect_ratio})\n"
        f'        (uuid "{uuid4()}")\n'
        '    )'
    )

    # Anode pad (2)
    anode = (
        '    (pad "2" smd roundrect\n'
        f'        (at {pad_props.anode_center_x} 0)\n'
        f'        (size {pad_props.anode_width} {pad_props.anode_height})\n'
        '        (layers "F.Cu" "F.Paste" "F.Mask")\n'
        f"        (roundrect_rratio {pad_props.roundrect_ratio})\n"
        f'        (uuid "{uuid4()}")\n'
        '    )'
    )

    return "\n".join([cathode, anode])  # noqa: FLY002


def generate_3d_model(part_info: sds.PartInfo) -> str:
    """Generate the 3D model section of the footprint."""
    return (
        '    (model "${KIPRJMOD}/3D_models/'
        f'{part_info.mpn}.step"\n'
        '        (offset (xyz 0 0 0))\n'
        '        (scale (xyz 1 1 1))\n'
        '        (rotate (xyz 0 0 0))\n'
        '    )'
    )


def generate_footprint_file(part_info: sds.PartInfo, output_dir: str) -> None:
    """Generate and save a complete .kicad_mod file for a diode.

    Args:
        part_info: Component specifications including MPN and package type
        output_dir: Directory path where the footprint file will be saved

    Raises:
        ValueError: If the specified diode package is not supported
        IOError: If there are problems writing the output file

    """
    if part_info.package not in DIODE_SPECS:
        msg = f"Unknown package type: {part_info.package}"
        raise ValueError(msg)

    specs = DIODE_SPECS[part_info.package]
    footprint_content = generate_footprint(part_info, specs)

    filepath = Path(output_dir) / f"{part_info.mpn}.kicad_mod"
    filepath.write_text(footprint_content, encoding="utf-8")
