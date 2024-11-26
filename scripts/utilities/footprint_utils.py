"""todo."""


from uuid import uuid4


def generate_header(model_name: str) -> str:
    """Generate the footprint header section."""
    return (
        f"""(footprint "{model_name}"
    (version 20240108)
    (generator "pcbnew")
    (generator_version "8.0")
    (layer "F.Cu")
    """)


def associate_3d_model(file_path: str, file_name: str) -> str:
    """Generate the 3D model section of the footprint."""
    return (f"""
        (model "${{KIPRJMOD}}/{file_path}/{file_name}.step"
            (offset (xyz 0 0 0))
            (scale (xyz 1 1 1))
            (rotate (xyz 0 0 0))
        )
        """)


def generate_courtyard(width: float, height: float) -> str:
    """Generate KiCad courtyard outline for any rectangular component.

    Creates a rectangular courtyard outline based on body dimensions.
    The courtyard defines the minimum clearance zone around the component.

    Args:
        width: Component body width in millimeters
        height: Component body height in millimeters

    Returns:
        KiCad format courtyard outline specification as a string

    """
    half_width = width / 2
    half_height = height / 2

    return (f"""
        (fp_rect
            (start -{half_width} -{half_height})
            (end {half_width} {half_height})
            (stroke (width 0.00635) (type solid))
            (fill none)
            (layer "F.CrtYd")
            (uuid "{uuid4()}")
        )
        """)


def generate_silkscreen_lines(
        height: float, center_x: float, pad_width: float) -> str:
    """Todo."""
    half_height = height / 2
    silkscreen_x = center_x - pad_width / 2

    shapes: str = ""

    for symbol in ["-", ""]:
        shapes += f"""
            (fp_line
                (start {silkscreen_x} {symbol}{half_height})
                (end -{silkscreen_x} {symbol}{half_height})
                (stroke (width 0.1524) (type solid))
                (layer "F.SilkS")
                (uuid "{uuid4()}")
            )
            """
    return shapes


def generate_fab_rectangle(width: float, height: float) -> str:
    """Todo."""
    half_width = width / 2
    half_height = height / 2

    return (f"""
        (fp_rect
            (start -{half_width} -{half_height})
            (end {half_width} {half_height})
            (stroke (width 0.0254) (type default))
            (fill none)
            (layer "F.Fab")
            (uuid "{uuid4()}")
        )
        """)

def generate_properties(ref_offset_y: float, value: str) -> str:
    """Generate the properties section of the footprint."""
    font_props = ("""
        (effects
            (font (size 0.762 0.762) (thickness 0.1524))
            (justify left)
        )
        """)

    return (f"""
        (property "Reference" "REF**"
            (at 0 {ref_offset_y} 0)
            (unlocked yes)
            (layer "F.SilkS")
            (uuid "{uuid4()}")
            {font_props}
        )
        (property "Value" "{value}"
            (at 0 {-1 * ref_offset_y} 0)
            (unlocked yes)
            (layer "F.Fab")
            (uuid "{uuid4()}")
            {font_props}
        )
        (property "Footprint" ""
            (at 0 0 0)
            (layer "F.Fab")
            (hide yes)
            (uuid "{uuid4()}")
            {font_props}
        )
        (fp_text user "${{REFERENCE}}"
            (at 0 {-1 * ref_offset_y + 1.27} 0)
            (unlocked yes)
            (layer "F.Fab")
            (uuid "{uuid4()}")
            {font_props}
        )
        """)
