"""Utility functions for generating KiCad PCB footprint components.

This module provides helper functions to generate various sections and
elements of KiCad footprints, including headers, 3D models, courtyards,
silkscreen lines, and component properties.
"""


from uuid import uuid4


def generate_header(model_name: str) -> str:
    """Generate the standard KiCad footprint header section.

    Args:
        model_name (str): Name of the footprint model.

    Returns:
        str: Formatted KiCad footprint header with version and generator
             information.

    """
    return (
        f"""(footprint "{model_name}"
    (version 20240108)
    (generator "pcbnew")
    (generator_version "8.0")
    (layer "F.Cu")
    """)


def associate_3d_model(file_path: str, file_name: str) -> str:
    """Generate the 3D model section for a KiCad footprint.

    Args:
        file_path (str): Relative path to the 3D model file.
        file_name (str): Name of the 3D model file without extension.

    Returns:
        str: Formatted KiCad 3D model association with default
             offset, scale, and rotation.

    """
    return (f"""
        (model "${{KIPRJMOD}}/{file_path}/{file_name}.step"
            (offset (xyz 0 0 0))
            (scale (xyz 1 1 1))
            (rotate (xyz 0 0 0))
        )
        """)


def generate_courtyard(width: float, height: float) -> str:
    """Generate KiCad courtyard outline for rectangular components.

    Creates a rectangular courtyard outline defining the minimum
    clearance zone around a component.

    Args:
        width (float): Component body width in millimeters.
        height (float): Component body height in millimeters.

    Returns:
        str: KiCad format courtyard outline specification.

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
    """Generate silkscreen reference lines for a component.

    Creates horizontal silkscreen lines to help with component
    orientation and placement.

    Args:
        height (float): Total height of the component.
        center_x (float): X-coordinate of the component center.
        pad_width (float): Width of the component's pad.

    Returns:
        str: KiCad formatted silkscreen line definitions.

    """
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
    """Generate fabrication layer rectangular outline.

    Creates a rectangle defining the component's physical
    dimensions on the fabrication layer.

    Args:
        width (float): Width of the rectangle.
        height (float): Height of the rectangle.

    Returns:
        str: KiCad formatted fabrication layer rectangle.

    """
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


def generate_fab_diode(
        width: float,
        height: float,
        anode_center_x: float,
        cathode_center_x: float) -> str:
    """Generate fabrication layer polygon for diode representation.

    Creates a polygon on the fabrication layer depicting a diode's
    physical shape and orientation.

    Args:
        width (float): Total width of the diode.
        height (float): Total height of the diode.
        anode_center_x (float): X-coordinate of the anode center.
        cathode_center_x (float): X-coordinate of the cathode center.

    Returns:
        str: KiCad formatted fabrication layer diode polygon.

    """
    return (f"""
        (fp_poly
            (pts
            (xy {width} 0)
            (xy {anode_center_x} 0)
            (xy {width} 0)
            (xy {width} {height / 2})
            (xy 0 0)
            (xy 0 {height / 2})
            (xy 0 0)
            (xy -{cathode_center_x} 0)
            (xy 0 0)
            (xy 0 -{height / 2})
            (xy 0 0)
            (xy {width} -{height / 2})
            )
            (stroke (width 0.1) (type solid))
            (fill solid)
            (layer "F.Fab")
            (uuid "{uuid4()}")
        )
        """)


def generate_properties(ref_offset_y: float, value: str) -> str:
    """Generate properties section for KiCad footprint.

    Creates text properties including reference, value, and
    footprint description with consistent formatting.

    Args:
        ref_offset_y (float): Vertical offset for reference text.
        value (str): Component value/description.

    Returns:
        str: KiCad formatted properties and text elements.

    """
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
