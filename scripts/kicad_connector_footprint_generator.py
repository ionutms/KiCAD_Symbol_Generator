"""
KiCad Footprint Generator Module

Generates .kicad_mod files for connector series based on specifications.
"""

from typing import Dict, NamedTuple, Callable, Tuple
from uuid import uuid4
import series_specs_connectors as ssc


class ConnectorSpecs(NamedTuple):
    """Complete specifications for footprint generation."""
    width_per_pin: float      # Width contribution per pin
    base_width: float         # Base width for enclosure
    height_top: float         # Height above origin
    height_bottom: float      # Height below origin
    pad_size: float          # Pad diameter/size
    drill_size: float        # Drill hole diameter
    silk_margin: float       # Margin for silkscreen
    mask_margin: float       # Solder mask margin
    ref_x: float            # Reference X position
    ref_y: float            # Reference Y position
    model_offset_base: tuple[float, float, float]  # Base 3D model offset
    model_rotation: tuple[float, float, float]     # 3D model rotation
    step_multiplier: float   # Multiplier for step offset calculation
    model_offset_func: Callable  # Function to calculate model offset


def offset_add(
        base: Tuple[float, float, float],
        step: float
) -> Tuple[float, float, float]:
    """
    Calculate offset by adding step to base X coordinate.

    Args:
        base: Base offset coordinates (x, y, z)
        step: Step value to add to x coordinate

    Returns:
        Tuple containing updated (x, y, z) coordinates with modified x value
    """
    return (base[0] + step, base[1], base[2])


def offset_sub(
        base: Tuple[float, float, float],
        step: float
) -> Tuple[float, float, float]:
    """
    Calculate offset by subtracting step from base X coordinate.

    Args:
        base: Base offset coordinates (x, y, z)
        step: Step value to subtract from x coordinate

    Returns:
        Tuple containing updated (x, y, z) coordinates with modified x value
    """
    return (base[0] - step, base[1], base[2])


# Consolidated connector series specifications using common offset patterns
CONNECTOR_SPECS: Dict[str, ConnectorSpecs] = {
    "TBP02R1-381": ConnectorSpecs(
        width_per_pin=3.81,
        base_width=4.4,
        height_top=-7.9,
        height_bottom=1.4,
        pad_size=2.1,
        drill_size=1.4,
        silk_margin=0.1524,
        mask_margin=0.102,
        ref_x=0.0,
        ref_y=2.4,
        model_offset_base=(-17.15, 17.000, -3.4),
        model_rotation=(0, 90, 180),
        step_multiplier=1.905,
        model_offset_func=offset_add
    ),
    "TBP02R2-381": ConnectorSpecs(
        width_per_pin=3.81,
        base_width=4.445,
        height_top=3.2512,
        height_bottom=-4.445,
        pad_size=2.1,
        drill_size=1.4,
        silk_margin=0.1524,
        mask_margin=0.102,
        ref_x=0.0,
        ref_y=4.2,
        model_offset_base=(17.145, -6.477, 18.288),
        model_rotation=(90, 0, -90),
        step_multiplier=1.905,
        model_offset_func=offset_sub
    ),
    "TBP04R1-500": ConnectorSpecs(
        width_per_pin=5.0,
        base_width=5.2,
        height_top=-2.2,
        height_bottom=9.9,
        pad_size=2.55,
        drill_size=1.7,
        silk_margin=0.1524,
        mask_margin=0.102,
        ref_x=0.0,
        ref_y=-3.0,
        model_offset_base=(-1.65, 1.0, -3.81),
        model_rotation=(-90, 0, 90),
        step_multiplier=2.5,
        model_offset_func=offset_add
    ),
    "TBP04R12-500": ConnectorSpecs(
        width_per_pin=5.0,
        base_width=5.8,
        height_top=-2.2,
        height_bottom=9.9,
        pad_size=2.55,
        drill_size=1.7,
        silk_margin=0.1524,
        mask_margin=0.102,
        ref_x=0.0,
        ref_y=-3.0,
        model_offset_base=(-5, -5.6, -3.81),
        model_rotation=(-90, 0, 0),
        step_multiplier=2.5,
        model_offset_func=offset_sub
    ),
    "TBP04R2-500": ConnectorSpecs(
        width_per_pin=5.0,
        base_width=5.8,
        height_top=4.8,
        height_bottom=-4.0,
        pad_size=2.55,
        drill_size=1.7,
        silk_margin=0.1524,
        mask_margin=0.102,
        ref_x=0.0,
        ref_y=5.8,
        model_offset_base=(5, -0.75, -3.81),
        model_rotation=(-90, 0, 180),
        step_multiplier=2.5,
        model_offset_func=offset_add
    ),
    "TBP04R3-500": ConnectorSpecs(
        width_per_pin=5.0,
        base_width=5.2,
        height_top=4.8,
        height_bottom=-4.0,
        pad_size=2.55,
        drill_size=1.7,
        silk_margin=0.1524,
        mask_margin=0.102,
        ref_x=0.0,
        ref_y=5.8,
        model_offset_base=(5, -0.75, -3.81),
        model_rotation=(-90, 0, 180),
        step_multiplier=2.5,
        model_offset_func=offset_add
    ),
    "TB004-508": ConnectorSpecs(
        width_per_pin=5.08,
        base_width=5.2,
        height_top=5.2,
        height_bottom=-5.2,
        pad_size=2.55,
        drill_size=1.7,
        silk_margin=0.1524,
        mask_margin=0.102,
        ref_x=0.0,
        ref_y=6.096,
        model_offset_base=(0.0, 0.0, 0.0),
        model_rotation=(0.0, 0.0, 0.0),
        step_multiplier=0.0,
        model_offset_func=offset_sub
    ),
}


def generate_footprint(part: ssc.PartInfo, specs: ConnectorSpecs) -> str:
    """
    Generate KiCad footprint file content for a connector.

    This function creates a complete KiCad footprint definition including:
    - Component properties and metadata
    - Silkscreen and fabrication layer shapes
    - Through-hole pad definitions
    - 3D model references

    Args:
        part: Component specifications including MPN, pin count, and pitch
        specs:
            Complete connector specifications defining
            physical dimensions and properties

    Returns:
        String containing the complete .kicad_mod file content in KiCad format
    """
    # Calculate enclosure width based on pin count
    extra_width_per_side = (part.pin_count - 2) * specs.width_per_pin / 2
    total_half_width = specs.base_width + extra_width_per_side

    # Calculate pin positions
    total_length = (part.pin_count - 1) * part.pitch
    start_pos = -total_length / 2

    header = f'''(footprint "{part.mpn}"
    (version 20240108)
    (generator "pcbnew")
    (generator_version "8.0")
    (layer "F.Cu")'''

    # Properties section
    properties = f'''    (property "Reference" "REF**"
        (at {specs.ref_x} {specs.ref_y} 0)
        (layer "F.SilkS")
        (uuid "{uuid4()}")
        (effects
            (font
                (size 0.762 0.762)
                (thickness 0.1524)
            )
        )
    )
    (property "Value" "{part.mpn}"
        (at 0 {specs.height_top + 1.042} 0)
        (layer "F.Fab")
        (uuid "{uuid4()}")
        (effects
            (font
                (size 0.762 0.762)
                (thickness 0.1524)
            )
            (justify left)
        )
    )
    (property "Footprint" ""
        (at {start_pos} 0 0)
        (layer "F.Fab")
        (hide yes)
        (uuid "{uuid4()}")
        (effects
            (font
                (size 1.27 1.27)
                (thickness 0.15)
            )
        )
    )
    (property "Datasheet" ""
        (at {start_pos} 0 0)
        (layer "F.Fab")
        (hide yes)
        (uuid "{uuid4()}")
        (effects
            (font
                (size 1.27 1.27)
                (thickness 0.15)
            )
        )
    )
    (property "Description" ""
        (at {start_pos} 0 0)
        (layer "F.Fab")
        (hide yes)
        (uuid "{uuid4()}")
        (effects
            (font
                (size 1.27 1.27)
                (thickness 0.15)
            )
        )
    )'''

    # Shape definitions
    shapes = f'''    (attr through_hole)
    (fp_rect
        (start {-total_half_width:.3f} {specs.height_bottom})
        (end {total_half_width:.3f} {specs.height_top})
        (stroke
            (width {specs.silk_margin})
            (type default)
        )
        (fill none)
        (layer "F.SilkS")
        (uuid "{uuid4()}")
    )
    (fp_circle
        (center {-(total_half_width + specs.silk_margin*4):.3f} 0)
        (end {-(total_half_width + specs.silk_margin*2):.3f} 0)
        (stroke
            (width {specs.silk_margin})
            (type solid)
        )
        (fill none)
        (layer "F.SilkS")
        (uuid "{uuid4()}")
    )
    (fp_rect
        (start {-total_half_width:.3f} {specs.height_bottom})
        (end {total_half_width:.3f} {specs.height_top})
        (stroke
            (width 0.00635)
            (type default)
        )
        (fill none)
        (layer "F.CrtYd")
        (uuid "{uuid4()}")
    )
    (fp_rect
        (start {-total_half_width:.3f} {specs.height_bottom})
        (end {total_half_width:.3f} {specs.height_top})
        (stroke
            (width {specs.silk_margin})
            (type default)
        )
        (fill none)
        (layer "F.Fab")
        (uuid "{uuid4()}")
    )
    (fp_circle
        (center {-(total_half_width + specs.silk_margin*4):.3f} 0)
        (end {-(total_half_width + specs.silk_margin*2):.3f} 0)
        (stroke
            (width {specs.silk_margin})
            (type solid)
        )
        (fill none)
        (layer "F.Fab")
        (uuid "{uuid4()}")
    )'''

    # Combine initial sections
    footprint = f"{header}\n{properties}\n{shapes}"

    # Add pads
    for pin in range(part.pin_count):
        x_pos = start_pos + (pin * part.pitch)
        pad_type = "rect" if pin == 0 else "circle"
        footprint += f'''
    (pad "{pin + 1}" thru_hole {pad_type}
        (at {x_pos:.3f} 0)
        (size {specs.pad_size} {specs.pad_size})
        (drill {specs.drill_size})
        (layers "*.Cu" "*.Mask")
        (remove_unused_layers no)
        (solder_mask_margin {specs.mask_margin})
        (uuid "{uuid4()}")
    )'''

    # Calculate 3D model position
    step_offset = (part.pin_count - 2) * specs.step_multiplier
    model_offset = specs.model_offset_func(
        specs.model_offset_base, step_offset)

    # Add 3D model reference
    model_path = (f"KiCAD_Symbol_Generator/3D_models/"
                  f"CUI_DEVICES_{part.mpn}.step")

    footprint += f'''
    (model "${{KIPRJMOD}}/{model_path}"
        (offset
            (xyz {model_offset[0]:.3f} {model_offset[1]} {model_offset[2]})
        )
        (scale
            (xyz 1 1 1)
        )
        (rotate
            (xyz {specs.model_rotation[0]} {specs.model_rotation[1]} '''
    footprint += f'''{specs.model_rotation[2]})
        )
    )'''

    # Close the footprint
    footprint += "\n)"

    return footprint


def generate_footprint_file(part: ssc.PartInfo) -> None:
    """
    Generate and save a .kicad_mod file for a connector part.

    This function takes a part specification, generates the appropriate
    footprint content, and saves it to a file in the
    connector_footprints.pretty directory.

    Args:
        part:
            Component specifications including MPN, series, pin count,
            and pitch

    Raises:
        ValueError:
            If the specified connector series is not found in CONNECTOR_SPECS
        IOError: If there are issues writing to the output file
    """
    if part.series not in CONNECTOR_SPECS:
        raise ValueError(f"Unknown series: {part.series}")

    specs = CONNECTOR_SPECS[part.series]
    footprint_content = generate_footprint(part, specs)

    # Save to file
    filename = f"connector_footprints.pretty/{part.mpn}.kicad_mod"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(footprint_content)
