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


def associate_3d_model(step_file_name: str) -> str:
    """Generate the 3D model section of the footprint."""
    return (
        f'    (model "${{KIPRJMOD}}/KiCAD_Symbol_Generator/3D_models/'
        f'{step_file_name}.step"\n'
        '        (offset (xyz 0 0 0))\n'
        '        (scale (xyz 1 1 1))\n'
        '        (rotate (xyz 0 0 0))\n'
        '    )'
    )


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
            (stroke
                (width 0.00635)
                (type solid)
            )
            (fill none)
            (layer "F.CrtYd")
            (uuid "{uuid4()}")
        )
        """)


def generate_silkscreen_lines(
        height: float, center_x: float, pad_width: float) -> list[str]:
    """Todo."""
    half_height = height / 2
    silkscreen_x = center_x - pad_width / 2

    shapes: list = []

    for symbol in ["-", ""]:
        shapes.append(f"""
            (fp_line
                (start {silkscreen_x} {symbol}{half_height})
                (end -{silkscreen_x} {symbol}{half_height})
                (stroke (width 0.1524) (type solid) )
                (layer "F.SilkS")
                (uuid "{uuid4()}")
            )
            """)  # noqa: PERF401
    return shapes


def generate_fab_rectangle(width: float, height: float) -> str:
    """Todo."""
    half_width = width / 2
    half_height = height / 2

    return (f"""
        (fp_rect
            (start -{half_width} -{half_height})
            (end {half_width} {half_height})
            (stroke
                (width 0.0254)
                (type default)
            )
            (fill none)
            (layer "F.Fab")
            (uuid "{uuid4()}")
        )
        """)
