"""KiCad Footprint Generator for Power Inductors.

Generates standardized KiCad footprint files (.kicad_mod) for power inductors
based on manufacturer specifications. Creates accurate footprints with
appropriate pad dimensions, clearances, and silkscreen markings for surface
mount power inductors.
"""

from pathlib import Path
from uuid import uuid4

import symbol_inductors_specs as ssi
from footprint_inductor_specs import INDUCTOR_SPECS, InductorSpecs
from utilities import footprint_utils as fu


def generate_footprint(part_info: ssi.PartInfo, specs: InductorSpecs) -> str:
    """Generate complete KiCad footprint file content for an inductor.

    Args:
        part_info: Component specifications
        specs:
            Physical specifications for the inductor series
            from INDUCTOR_SPECS

    Returns:
        Complete .kicad_mod file content as formatted string

    """
    # Get silkscreen lines as a list
    silkscreen_lines = fu.generate_silkscreen_lines(
        specs.body_dimensions.height,
        specs.pad_dimensions.center_x,
        specs.pad_dimensions.width)

    sections = [
        fu.generate_header(part_info.series),
        generate_properties(part_info, specs),
        fu.generate_courtyard(
            specs.body_dimensions.width,
            specs.body_dimensions.height),
        fu.generate_fab_rectangle(
            specs.body_dimensions.width,
            specs.body_dimensions.height),
        # Join the silkscreen lines with newlines before adding to sections
        "\n".join(silkscreen_lines),
        generate_shapes(specs),
        generate_pads(specs),
        fu.associate_3d_model(part_info.series),
        ")",  # Close the footprint
    ]
    return "\n".join(sections)


def generate_properties(part_info: ssi.PartInfo, specs: InductorSpecs) -> str:
    """Generate the properties section of the footprint."""
    font_props = (
        "        (effects\n"
        "            (font\n"
        "                (size 0.762 0.762)\n"
        "                (thickness 0.1524)\n"
        "            )\n"
        "            (justify left)\n"
        "        )"
    )

    ref_offset_y = specs.ref_offset_y

    return (
        '    (property "Reference" "REF**"\n'
        f"        (at 0 {ref_offset_y} 0)\n"
        "        (unlocked yes)\n"
        '        (layer "F.SilkS")\n'
        f'        (uuid "{uuid4()}")\n'
        f"{font_props}\n"
        "    )\n"
        f'    (property "Value" "{part_info.series}"\n'
        f"        (at 0 {-1 * ref_offset_y} 0)\n"
        "        (unlocked yes)\n"
        '        (layer "F.Fab")\n'
        f'        (uuid "{uuid4()}")\n'
        f"{font_props}\n"
        "    )\n"
        '    (property "Footprint" ""\n'
        "        (at 0 0 0)\n"
        '        (layer "F.Fab")\n'
        "        (hide yes)\n"
        f'        (uuid "{uuid4()}")\n'
        "        (effects\n"
        "            (font\n"
        "                (size 1.27 1.27)\n"
        "                (thickness 0.15)\n"
        "            )\n"
        "        )\n"
        "    )"
    )


def generate_shapes(specs: InductorSpecs) -> str:
    """Generate the shapes section of the footprint."""
    shapes = []

    # Polarity marker
    shapes.append(
        "    (fp_circle\n"
        f"        (center -{specs.pad_dimensions.center_x} 0)\n"
        "        (end "
        f"-{specs.pad_dimensions.center_x - 0.0762} 0)\n"
        "        (stroke\n"
        "            (width 0.0254)\n"
        "            (type solid)\n"
        "        )\n"
        "        (fill none)\n"
        '        (layer "F.Fab")\n'
        f'        (uuid "{uuid4()}")\n'
        "    )",
    )

    # Reference on fab layer
    shapes.append(
        f'    (fp_text user "${{REFERENCE}}"\n'
        f"        (at 0 {-1 * specs.ref_offset_y + 1.27} 0)\n"
        "        (unlocked yes)\n"
        '        (layer "F.Fab")\n'
        f'        (uuid "{uuid4()}")\n'
        "        (effects\n"
        "            (font\n"
        "                (size 0.762 0.762)\n"
        "                (thickness 0.1524)\n"
        "            )\n"
        "            (justify left)\n"
        "        )\n"
        "    )",
    )

    return "\n".join(shapes)


def generate_pads(specs: InductorSpecs) -> str:
    """Generate the pads section of the footprint."""
    pads = []

    for pad_number, symbol in enumerate(["-", ""], start=1):
        pads.append(
            f'    (pad "{pad_number}" smd rect\n'
            f"        (at {symbol}{specs.pad_dimensions.center_x} 0)\n"
            "        (size "
            f"{specs.pad_dimensions.width} {specs.pad_dimensions.height})\n"
            '        (layers "F.Cu" "F.Paste" "F.Mask")\n'
            f'        (uuid "{uuid4()}")\n'
            "    )",
        )

    return "\n".join(pads)


def generate_footprint_file(part_info: ssi.PartInfo, output_dir: str) -> None:
    """Generate and save a complete .kicad_mod file for an inductor.

    Args:
        part_info: Component specifications including MPN and series
        output_dir: Directory path where the footprint file will be saved

    Raises:
        ValueError: If the specified inductor series is not supported
        IOError: If there are problems writing the output file

    """
    if part_info.series not in INDUCTOR_SPECS:
        msg = f"Unknown series: {part_info.series}"
        raise ValueError(msg)

    specs = INDUCTOR_SPECS[part_info.series]
    footprint_content = generate_footprint(part_info, specs)

    filename = f"{output_dir}/{part_info.series}.kicad_mod"
    with Path.open(filename, "w", encoding="utf-8") as file_handle:
        file_handle.write(footprint_content)
