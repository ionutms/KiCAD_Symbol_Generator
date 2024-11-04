"""
KiCad Footprint Generator Module

Generates .kicad_mod files for connector series based on specifications.
"""

from typing import Dict, NamedTuple
from uuid import uuid4
import series_specs_connectors as ssc


class FootprintDimensions(NamedTuple):
    """Physical dimensions for footprint generation."""
    width_per_pin: float  # Width contribution per pin
    base_width: float    # Base width for enclosure
    height_top: float    # Height above origin
    height_bottom: float  # Height below origin
    pad_size: float     # Pad diameter/size
    drill_size: float   # Drill hole diameter
    silk_margin: float  # Margin for silkscreen
    mask_margin: float  # Solder mask margin


# Connector series specific dimensions
FOOTPRINT_SPECS: Dict[str, FootprintDimensions] = {
    "TBP02R2-381": FootprintDimensions(
        width_per_pin=3.81,    # Pitch
        base_width=4.445,      # Base enclosure width (half of total for 2-pin)
        height_top=3.2512,     # Height above center
        height_bottom=4.445,   # Height below center
        pad_size=2.1,
        drill_size=1.4,
        silk_margin=0.1524,
        mask_margin=0.102
    ),
    "TBP04R2-500": FootprintDimensions(
        width_per_pin=5.0,     # Pitch
        base_width=5.8,        # Base enclosure width (half of total for 2-pin)
        height_top=4.8,        # Height above center
        height_bottom=4.0,     # Height below origin
        pad_size=2.55,
        drill_size=1.7,
        silk_margin=0.1524,
        mask_margin=0.102
    )
}


def generate_footprint(part: ssc.PartInfo, dims: FootprintDimensions) -> str:
    """
    Generate KiCad footprint file content for a connector.

    Args:
        part: Component specifications
        dims: Physical dimensions for the footprint

    Returns:
        String containing the .kicad_mod file content
    """
    # Calculate enclosure width based on pin count
    extra_width_per_side = (part.pin_count - 2) * dims.width_per_pin / 2
    total_half_width = dims.base_width + extra_width_per_side

    # Calculate pin positions
    total_length = (part.pin_count - 1) * part.pitch
    start_pos = -total_length / 2

    footprint = f'''(footprint "{part.mpn}"
    (version 20240108)
    (generator "pcbnew")
    (generator_version "8.0")
    (layer "F.Cu")
    (property "Reference" "REF**"
        (at 0 {-dims.height_bottom} 0)
        (layer "F.SilkS")
        (uuid "{uuid4()}")
        (effects
            (font
                (size 0.762 0.762)
                (thickness 0.1524)
            )
            (justify left)
        )
    )
    (property "Value" "{part.mpn}"
        (at 0 {dims.height_top + 1.042} 0)
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
    )
    (attr through_hole)
    (fp_rect
        (start {-total_half_width:.3f} {-dims.height_bottom})
        (end {total_half_width:.3f} {dims.height_top})
        (stroke
            (width {dims.silk_margin})
            (type default)
        )
        (fill none)
        (layer "F.SilkS")
        (uuid "{uuid4()}")
    )
    (fp_circle
        (center {-(total_half_width + dims.silk_margin*4):.3f} 0)
        (end {-(total_half_width + dims.silk_margin*2):.3f} 0)
        (stroke
            (width {dims.silk_margin})
            (type solid)
        )
        (fill none)
        (layer "F.SilkS")
        (uuid "{uuid4()}")
    )
    (fp_rect
        (start {-total_half_width:.3f} {-dims.height_bottom})
        (end {total_half_width:.3f} {dims.height_top})
        (stroke
            (width 0.00635)
            (type default)
        )
        (fill none)
        (layer "F.CrtYd")
        (uuid "{uuid4()}")
    )
    (fp_rect
        (start {-total_half_width:.3f} {-dims.height_bottom})
        (end {total_half_width:.3f} {dims.height_top})
        (stroke
            (width {dims.silk_margin})
            (type default)
        )
        (fill none)
        (layer "F.Fab")
        (uuid "{uuid4()}")
    )
    (fp_circle
        (center {-(total_half_width + dims.silk_margin*4):.3f} 0)
        (end {-(total_half_width + dims.silk_margin*2):.3f} 0)
        (stroke
            (width {dims.silk_margin})
            (type solid)
        )
        (fill none)
        (layer "F.Fab")
        (uuid "{uuid4()}")
    )'''

    # Add pads
    for pin in range(part.pin_count):
        x_pos = start_pos + (pin * part.pitch)
        pad_type = "rect" if pin == 0 else "circle"
        footprint += f'''
    (pad "{pin + 1}" thru_hole {pad_type}
        (at {x_pos:.3f} 0)
        (size {dims.pad_size} {dims.pad_size})
        (drill {dims.drill_size})
        (layers "*.Cu" "*.Mask")
        (remove_unused_layers no)
        (solder_mask_margin {dims.mask_margin})
        (uuid "{uuid4()}")
    )'''

    # Add 3D model reference
    if part.series == "TBP02R2-381":
        model_offset = (17.145, -6.477, 18.288)
        model_rotation = (90, 0, -90)
    elif part.series == "TBP04R2-500":
        model_offset = (17.145, -6.477, 18.288)
        model_rotation = (-90, 0, -90)
    else:
        model_offset = (0, 0, 0)
        model_rotation = (0, 0, 0)

    step_path = f"KiCAD_Symbol_Generator/3D_models/CUI_DEVICES_{part.mpn}.step"

    footprint += f'''
    (model "${{KIPRJMOD}}/{step_path}"
        (offset
            (xyz {model_offset[0]:.3f} {model_offset[1]} {model_offset[2]})
        )
        (scale
            (xyz 1 1 1)
        )
        (rotate
            (xyz {model_rotation[0]} {model_rotation[1]} {model_rotation[2]})
        )
    )'''

    # Close the footprint
    footprint += "\n)"

    return footprint


def generate_footprint_file(part: ssc.PartInfo) -> None:
    """
    Generate and save a .kicad_mod file for a connector part.

    Args:
        part: Component specifications
    """
    # Get base series from MPN
    base_series = part.series

    if base_series not in FOOTPRINT_SPECS:
        raise ValueError(f"Unknown series: {base_series}")

    dims = FOOTPRINT_SPECS[base_series]
    footprint_content = generate_footprint(part, dims)

    # Save to file
    filename = f"connector_footprints.pretty/{part.mpn}.kicad_mod"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(footprint_content)
