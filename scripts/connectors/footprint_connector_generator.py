"""KiCad Footprint Generator Module.

Generates standardized KiCad footprint files (.kicad_mod) for various
connector series.
It handles pad placement, silkscreen generation, and 3D model alignment
based on manufacturer specifications.

The module supports multiple connector series with different pin counts and
pitches, generating complete footprint definitions including:
- Through-hole pad layouts
- Silkscreen outlines
- Component identifiers
- 3D model references
"""

from pathlib import Path
from uuid import uuid4

import symbol_connectors_specs
from footprint_connector_specs import CONNECTOR_SPECS, ConnectorSpecs
from utilities import footprint_utils


def generate_footprint(
        part_info: symbol_connectors_specs.PartInfo,
        specs: ConnectorSpecs,
) -> str:
    """Generate complete KiCad footprint file content for a connector.

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
        footprint_utils.generate_header(part_info.mpn),
        generate_properties(part_info, specs, dimensions),
        generate_shapes(dimensions, specs),
        generate_pads(part_info, specs, dimensions),
        footprint_utils.associate_3d_model(
            "KiCAD_Symbol_Generator/3D_models",
            f"CUI_DEVICES_{part_info.mpn}"),
        ")",  # Close the footprint
    ]
    return "\n".join(sections)


def calculate_dimensions(
    part_info: symbol_connectors_specs.PartInfo,
    specs: ConnectorSpecs,
) -> dict:
    """Calculate key dimensions for footprint generation.

    Determines total width, length, and starting positions based on the
    connector's pin count and physical specifications.

    Args:
        part_info: Component specifications (pin count, pitch)
        specs: Physical specifications for the connector series

    Returns:
        Dictionary containing calculated dimensions and positions

    """
    extra_width_per_side = (part_info.pin_count - 2) * specs.pitch / 2
    total_half_width_left = (
        specs.body_dimensions.width_left + extra_width_per_side
    )
    total_half_width_right = (
        specs.body_dimensions.width_right + extra_width_per_side
    )
    total_length = (part_info.pin_count - 1) * part_info.pitch
    start_position = -total_length / 2

    return {
        "total_half_width_left": total_half_width_left,
        "total_half_width_right": total_half_width_right,
        "total_length": total_length,
        "start_pos": start_position,
    }


def generate_properties(
    part_info: symbol_connectors_specs.PartInfo,
    specs: ConnectorSpecs, dimensions: dict,
) -> str:
    """Generate the properties section of the footprint."""
    font_props = ("""
        (effects (font (size 0.762 0.762) (thickness 0.1524)))
        """)

    hidden_font_props = ("""
        (effects (font (size 1.27 1.27) (thickness 0.15)))
        """)

    return (f"""
        (property "Reference" "REF**"
            (at 0 {specs.ref_y} 0)
            (layer "F.SilkS")
            (uuid "{uuid4()}")
            {font_props}
        )
        (property "Value" "{part_info.mpn}"
            (at 0 {specs.mpn_y} 0)
            (layer "F.Fab")
            (uuid "{uuid4()}")
            {font_props}
        )
        (property "Footprint" ""
            (at {dimensions['start_pos']} 0 0)
            (layer "F.Fab")
            (hide yes)
            (uuid "{uuid4()}")
            {hidden_font_props}
        )
        (property "Datasheet" ""
            (at {dimensions['start_pos']} 0 0)
            (layer "F.Fab")
            (hide yes)
            (uuid "{uuid4()}")
            {hidden_font_props}
        )
        (property "Description" ""
            (at {dimensions['start_pos']} 0 0)
            (layer "F.Fab")
            (hide yes)
            (uuid "{uuid4()}")
            {hidden_font_props}
        )
        """)


def generate_shapes(dimensions: dict, specs: ConnectorSpecs) -> str:
    """Generate the shapes section of the footprint."""
    circle_center = -(
        dimensions["total_half_width_left"] + specs.silk_margin * 6)
    circle_end = -(
        dimensions["total_half_width_left"] + specs.silk_margin * 2)

    rect_start = -dimensions["total_half_width_left"]
    rect_end = dimensions["total_half_width_right"]

    def generate_rect(layer_name: str, stroke_width: str) -> str:
        return (f"""
            (fp_rect
                (start {rect_start:.3f} {specs.body_dimensions.height_bottom})
                (end {rect_end:.3f} {specs.body_dimensions.height_top})
                (stroke (width {stroke_width}) (type default))
                (fill none)
                (layer "{layer_name}")
                (uuid "{uuid4()}")
            )
            """)

    def generate_circle(layer_name: str, fill_type: str) -> str:
        return (f"""
            (fp_circle
                (center {circle_center:.3f} 0)
                (end {circle_end:.3f} 0)
                (stroke (width {specs.silk_margin}) (type solid))
                (fill {fill_type})
                (layer "{layer_name}")
                (uuid "{uuid4()}")
            )
            """)

    shapes = [
        "    (attr through_hole)",
        generate_rect("F.SilkS", specs.silk_margin),
        generate_circle("F.SilkS", "solid"),
        generate_rect("F.CrtYd", "0.00635"),
        generate_rect("F.Fab", specs.silk_margin),
        generate_circle("F.Fab", "none"),
    ]

    return "\n".join(shapes)


def generate_pads(
    part_info: symbol_connectors_specs.PartInfo,
    specs: ConnectorSpecs,
    dimensions: dict,
) -> str:
    """Generate the pads section of the footprint."""
    pads = []
    for pin_num in range(part_info.pin_count):
        xpos = dimensions["start_pos"] + (pin_num * part_info.pitch)
        pad_type = "rect" if pin_num == 0 else "circle"
        pad = (f"""
            (pad "{pin_num + 1}" thru_hole {pad_type}
                (at {xpos:.3f} 0)
                (size {specs.pad_size} {specs.pad_size})
                (drill {specs.drill_size})
                (layers "*.Cu" "*.Mask")
                (remove_unused_layers no)
                (solder_mask_margin {specs.mask_margin})
                (uuid "{uuid4()}")
            )
            """)
        pads.append(pad)
    return "\n".join(pads)


def generate_footprint_file(
        part_info: symbol_connectors_specs.PartInfo,
        output_path: str,
) -> None:
    """Generate and save a complete .kicad_mod file for a connector.

    Creates a KiCad footprint file in the connector_footprints.pretty
    directory using the specified part information and
    corresponding series specifications.

    Args:
        part_info: Component specifications including MPN and series
        output_path: todo

    Raises:
        ValueError: If the specified connector series is not supported
        IOError: If there are problems writing the output file

    """
    if part_info.series not in CONNECTOR_SPECS:
        msg = f"Unknown series: {part_info.series}"
        raise ValueError(msg)

    specs = CONNECTOR_SPECS[part_info.series]
    footprint_content = generate_footprint(part_info, specs)
    filename = f"{part_info.mpn}.kicad_mod"
    file_path = f"{output_path}/{filename}"

    with Path.open(file_path, "w", encoding="utf-8") as file_handle:
        file_handle.write(footprint_content)
