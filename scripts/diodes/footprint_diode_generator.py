"""KiCad Footprint Generator for Diodes.

Generates standardized KiCad footprint files (.kicad_mod) for diodes
based on manufacturer specifications. Creates accurate footprints with
appropriate pad dimensions, clearances, and silkscreen markings for surface
mount diodes.
"""

from pathlib import Path
from uuid import uuid4

import symbol_diode_specs
from footprint_diode_specs import DIODE_SPECS, DiodeSpecs
from utilities import footprint_utils


def generate_footprint(
        part_info: symbol_diode_specs.PartInfo,
        specs: DiodeSpecs,
) -> str:
    """Generate complete KiCad footprint file content for a diode.

    Args:
        part_info: Component specifications
        specs: Physical specifications for the diode series from DIODE_SPECS

    Returns:
        Complete .kicad_mod file content as formatted string

    """
    body_width = specs.body_dimensions.width
    body_height = specs.body_dimensions.height
    anode_center_x = specs.pad_dimensions.anode_center_x
    cathode_center_x = specs.pad_dimensions.cathode_center_x
    anode_width = specs.pad_dimensions.anode_width
    anode_height = specs.pad_dimensions.anode_height

    sections = [
        footprint_utils.generate_header(part_info.package),
        footprint_utils.generate_properties(
            specs.ref_offset_y, part_info.package),
        footprint_utils.generate_courtyard(body_width, body_height),
        footprint_utils.generate_fab_rectangle(body_width, body_height),
        footprint_utils.generate_fab_diode(
            anode_width, anode_height, anode_center_x, cathode_center_x),
        footprint_utils.generate_silkscreen_lines(
            body_height, anode_center_x, anode_width),
        generate_pads(specs),
        footprint_utils.associate_3d_model(
            "KiCAD_Symbol_Generator/3D_models", part_info.package),
        ")",  # Close the footprint
    ]
    return "\n".join(sections)


def generate_pads(specs: DiodeSpecs) -> str:
    """Generate the pads section of the footprint with pad dimensions.

    Args:
        specs: DiodeSpecs containing asymmetric pad dimensions

    Returns:
        String containing KiCad footprint pad definitions

    """
    pad_props = specs.pad_dimensions

    # Cathode pad (1)
    cathode = (f"""
        (pad "1" smd roundrect
            (at -{pad_props.cathode_center_x} 0)
            (size {pad_props.cathode_width} {pad_props.cathode_height})
            (layers "F.Cu" "F.Paste" "F.Mask")
            (roundrect_rratio {pad_props.roundrect_ratio})
            (uuid "{uuid4()}")
        )
        """)

    # Anode pad (2)
    anode = (f"""
        (pad "2" smd roundrect
            (at {pad_props.anode_center_x} 0)
            (size {pad_props.anode_width} {pad_props.anode_height})
            (layers "F.Cu" "F.Paste" "F.Mask")
            (roundrect_rratio {pad_props.roundrect_ratio})
            (uuid "{uuid4()}")
        )
        """)

    return f"{cathode}\n{anode}"

def generate_footprint_file(
        part_info: symbol_diode_specs.PartInfo,
        output_dir: str,
) -> None:
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

    filepath = Path(output_dir) / f"{part_info.package}.kicad_mod"
    filepath.write_text(footprint_content, encoding="utf-8")
