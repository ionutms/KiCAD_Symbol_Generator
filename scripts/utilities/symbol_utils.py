"""TODO."""

from typing import TextIO


def write_header(
        symbol_file: TextIO,
) -> None:
    """Write the header of the KiCad symbol file.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.

    """
    symbol_file.write("""
        (kicad_symbol_lib
            (version 20231120)
            (generator kicad_symbol_editor)
            (generator_version 8.0)
        """)


def write_symbol_header(
        symbol_file: TextIO,
        symbol_name: str,
) -> None:
    """Write the header for a single symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.

    """
    symbol_file.write(f"""
        (symbol "{symbol_name}"
            (pin_names(offset 0.254))
            (exclude_from_sim no)
            (in_bom yes)
            (on_board yes)
        """)


def get_all_properties(
        component_data_list: list[dict[str, str]],
) -> list[str]:
    """Get all properties from the component data in a consistent order.

    Args:
        component_data_list (List[Dict[str, str]]): List of component data.

    Returns:
        list[str]:
            List of all unique property names with priority properties first,
            then remaining properties in alphabetical order.

    """
    all_properties = set()

    # Priority properties that should always come first
    priority_properties = [
        "Reference",
        "Value",
        "Footprint",
        "Datasheet",
    ]

    # Collect all unique properties
    for component in component_data_list:
        all_properties.update(component.keys())

    # Create final sorted list:
    # 1. Start with priority properties (if they exist in the data)
    result = [prop for prop in priority_properties if prop in all_properties]

    # 2. Add remaining properties in alphabetical order
    remaining_props = sorted(
        prop for prop in all_properties if prop not in priority_properties)
    result.extend(remaining_props)

    return result


def write_property(  # noqa: PLR0913
    symbol_file: TextIO,
    property_name: str,
    property_value: str,
    x_offset: float,
    y_offset: float,
    font_size: float,
    show_name: bool,  # noqa: FBT001
    hide: bool,  # noqa: FBT001
) -> None:
    """Write a single property for a symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        property_name (str): Name of the property.
        property_value (str): Value of the property.
        x_offset (float): Horizontal offset for property placement.
        y_offset (float): Vertical offset for property placement.
        font_size (float): Size of the font.
        show_name (bool): Whether to show the property name.
        hide (bool): Whether to hide the property.

    """
    symbol_file.write(f"""
        (property "{property_name}" "{property_value}"
            (at {x_offset} {y_offset} 0)
            {('(show_name)' if show_name else '')}
            (effects
                (font(size {font_size} {font_size}))
                (justify left)
                {('(hide yes)' if hide else '')}
            )
        )
        """)


def write_properties(
    symbol_file: TextIO,
    component_data: dict[str, str],
    property_order: list[str],
    text_y_offset: int,
    text_x_offset: int=0,
) -> None:
    """Write properties for a single symbol in the KiCad symbol file.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        component_data (Dict[str, str]): Data for a single component.
        property_order (List[str]): Ordered list of property names.
        component_value: todo
        text_y_offset: todo
        text_x_offset: todo

    """
    property_configs = {
        "Reference": (
            2.54*text_x_offset, 2.54*text_y_offset,
            1.27, False, False, component_data.get("Reference", "-")),
        "Value": (
            2.54*text_x_offset, -2.54*text_y_offset,
            1.27, False, False, component_data.get("Value", "-")),
        "Footprint": (
            2.54*text_x_offset, -2.54*(text_y_offset+1),
            1.27, True, True, None),
        "Datasheet": (
            2.54*text_x_offset, -2.54*(text_y_offset+2),
            1.27, True, True, None),
        "Description": (
            2.54*text_x_offset, -2.54*(text_y_offset+3),
            1.27, True, True, None)}

    y_offset = -2.54*(text_y_offset+4)
    for prop_name in property_order:
        if prop_name in component_data:
            config = property_configs.get(
                prop_name,
                (2.54*text_x_offset, y_offset,1.27, True, True, None))
            value = config[5] or component_data[prop_name]
            write_property(symbol_file, prop_name, value, *config[:5])
            if prop_name not in property_configs:
                y_offset -= 2.54


def write_pin(  # noqa: PLR0913
        symbol_file: TextIO,
        x_pos: float,
        y_pos: float,
        angle: int,
        number: str,
        name: str = "",
        pin_type: str = "unspecified",
        hide: bool = False,  # noqa: FBT001, FBT002
        length: float = 2.54,
) -> None:
    """Write a single pin of the transformer symbol."""
    symbol_file.write(f"""
        (pin {pin_type} line
            (at {x_pos} {y_pos} {angle})
            (length {length})
            (name "{name}"(effects(font(size 1.27 1.27))))
            (number "{number}"(effects(font(size 1.27 1.27))))
            {('hide' if hide else '')}
        )
        """)


def write_capacitor_symbol_drawing(
        symbol_file: TextIO,
        symbol_name: str,
) -> None:
    """Write the graphical representation of a symbol in the KiCad symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.

    """
    symbol_file.write(f"""
        (symbol "{symbol_name}_0_1"
            (polyline
                (pts (xy -0.762 -2.032) (xy -0.762 2.032))
                (stroke (width 0.508) (type default))
                (fill (type none))
            )
            (polyline
                (pts (xy 0.762 -2.032) (xy 0.762 2.032))
                (stroke (width 0.508) (type default))
                (fill (type none))
            )
        )
    """)

    # Write pins
    write_pin(symbol_file, -3.81, 0, 0, "1", length=2.8)
    write_pin(symbol_file, 3.81, 0, 180, "2", length=2.8)


def write_resistor_symbol_drawing(
        symbol_file: TextIO,
        symbol_name: str,
) -> None:
    """Write the graphical representation of a symbol in the KiCad file.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.

    """
    symbol_file.write(f"""
        (symbol "{symbol_name}_0_1"
            (polyline
                (pts (xy 2.286 0) (xy 2.54 0))
                (stroke (width 0) (type default))
                (fill (type none))
            )
            (polyline
                (pts (xy -2.286 0) (xy -2.54 0))
                (stroke (width 0) (type default))
                (fill (type none))
            )
            (polyline
                (pts
                    (xy 0.762 0) (xy 1.143 1.016) (xy 1.524 0)
                    (xy 1.905 -1.016) (xy 2.286 0)
                )
                (stroke (width 0) (type default))
                (fill (type none))
            )
            (polyline
                (pts
                    (xy -0.762 0) (xy -0.381 1.016) (xy 0 0)
                    (xy 0.381 -1.016) (xy 0.762 0)
                )
                (stroke (width 0) (type default))
                (fill (type none))
            )
            (polyline
                (pts
                    (xy -2.286 0) (xy -1.905 1.016) (xy -1.524 0)
                    (xy -1.143 -1.016) (xy -0.762 0)
                )
                (stroke (width 0) (type default))
                (fill (type none))
            )
        )
        """)

    # Write pins
    write_pin(symbol_file, -5.08, 0, 0, "1")
    write_pin(symbol_file, 5.08, 0, 180, "2")


def write_inductor_symbol_drawing(
        symbol_file: TextIO,
        symbol_name: str,
) -> None:
    """Write the horizontal graphical representation of an inductor symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.

    """

    def write_arc(
        symbol_file: TextIO,
        start_x: float,
        mid_x: float,
        end_x: float,
    ) -> None:
        """Write a single arc of the inductor symbol."""
        symbol_file.write(f"""
            (arc
                (start {start_x} 0.0056)
                (mid {mid_x} 1.27)
                (end {end_x} 0.0056)
                (stroke (width 0.2032) (type default))
                (fill (type none))
            )
            """)

    # Write symbol drawing section
    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_1"\n')

    # Write arcs
    arc_params = [
        (-2.54, -3.81, -5.08),
        (0, -1.27, -2.54),
        (2.54, 1.27, 0),
        (5.08, 3.81, 2.54),
    ]
    for start_x, mid_x, end_x in arc_params:
        write_arc(symbol_file, start_x, mid_x, end_x)

    # Write pins
    write_pin(symbol_file, -7.62, 0, 0, "1")
    write_pin(symbol_file, 7.62, 0, 180, "2")

    symbol_file.write("\t\t)\n")


def write_transformer_symbol_drawing(
        symbol_file: TextIO,
        symbol_name: str,
        pin_config: dict,
) -> None:
    """Write the horizontal graphical representation of a transformer symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.
        pin_config (dict, optional): Dictionary defining pin configuration.

    """
    def get_symbol_bounds(pin_config: dict) -> tuple:
        """Calculate symbol bounds based on pin configuration."""
        y_positions = (
            [pin["y_pos"] for pin in pin_config["left"]] +
            [pin["y_pos"] for pin in pin_config["right"]]
        )
        max_y = max(y_positions)
        min_y = min(y_positions)
        return min_y, max_y

    # Calculate symbol bounds
    min_y, max_y = get_symbol_bounds(pin_config)

    # Write symbol drawing section - split into two units
    symbol_file.write(f'        (symbol "{symbol_name}_0_1"\n')

    # Write left inductor arcs
    for y_start in range(4):
        symbol_file.write(f"""
            (arc
                (start -2.54 {-5.08 + (y_start * 2.54)})
                (mid -1.27 {-3.81 + (y_start * 2.54)})
                (end -2.54 {-2.54 + (y_start * 2.54)})
                (stroke (width 0) (type default) )
                (fill (type none) )
            )
            """)

    # Write right inductor arcs
    for y_start in range(4):
        symbol_file.write(f"""
            (arc
                (start 2.54 {5.08 - (y_start * 2.54)})
                (mid 1.27 {3.81 - (y_start * 2.54)})
                (end 2.54 {2.54 - (y_start * 2.54)})
                (stroke (width 0) (type default))
                (fill (type none))
            )
            """)

    # Write polarity dots
    for x, y in [(-2.54, 3.81), (2.54, -3.81)]:
        symbol_file.write(f"""
            (circle
                (center {x} {y})
                (radius 0.508)
                (stroke (width 0) (type default))
                (fill (type none))
            )
            """)

    # Write coupling lines
    for x in [-0.254, 0.254]:
        symbol_file.write(f"""
            (polyline
                (pts (xy {x} {max_y}) (xy {x} {min_y}))
                (stroke (width 0) (type default))
                (fill (type none))
            )
            """)

    # Write left side pins
    for pin in pin_config["left"]:
        write_pin(
            symbol_file, -7.62, pin["y_pos"], 0, pin["number"],
            pin["pin_type"], pin.get("hide", False), pin["lenght"])

    # Write right side pins
    for pin in pin_config["right"]:
        write_pin(
            symbol_file, 7.62, pin["y_pos"], 180, pin["number"],
            pin["pin_type"], pin.get("hide", False), pin["lenght"])

    symbol_file.write("        )\n")


def write_coupled_inductor_symbol_drawing(
    symbol_file: TextIO,
    symbol_name: str,
    pin_config: dict,
) -> None:
    """Write the horizontal graphical representation of an inductor symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.
        pin_config (dict): Pin config.

    """
    # Write symbol drawing section
    symbol_file.write(f'        (symbol "{symbol_name}_1_1"\n')

    # Write left inductor arcs
    for y_start in range(4):
        symbol_file.write(f"""
            (arc
                (start -2.54 {-5.08 + (y_start * 2.54)})
                (mid -1.27 {-3.81 + (y_start * 2.54)})
                (end -2.54 {-2.54 + (y_start * 2.54)})
                (stroke (width 0) (type default))
                (fill (type none))
            )
            """)

    # Write right inductor arcs
    for y_start in range(4):
        symbol_file.write(f"""
            (arc
                (start 2.54 {5.08 - (y_start * 2.54)})
                (mid 1.27 {3.81 - (y_start * 2.54)})
                (end 2.54 {2.54 - (y_start * 2.54)})
                (stroke (width 0) (type default))
                (fill (type none) )
            )""")

    # Write polarity dots
    for x, y in [(-2.54, 3.81), (2.54, -3.81)]:
        symbol_file.write(f"""
            (circle
                (center {x} {y})
                (radius 0.508)
                (stroke (width 0) (type default))
                (fill (type none))
            )""")

    # Write coupling lines
    for x in [-0.254, 0.254]:
        symbol_file.write(f"""
            (polyline
                (pts (xy {x} 5.08) (xy {x} -5.08))
                (stroke (width 0) (type default))
                (fill (type none))
            )""")

    # Write left side pins
    for pin in pin_config["left"]:
        write_pin(
            symbol_file, -7.62, pin["y_pos"], 0, pin["number"],
            pin["pin_type"], pin.get("hide", False), pin["lenght"])

    # Write right side pins
    for pin in pin_config["right"]:
        write_pin(
            symbol_file, 7.62, pin["y_pos"], 180, pin["number"],
            pin["pin_type"], pin.get("hide", False), pin["lenght"])

    symbol_file.write("        )\n")


def write_schottky_symbol_drawing(
        symbol_file: TextIO,
        symbol_name: str,
) -> None:
    """Write the horizontal graphical representation of a diode symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.

    """
    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_0"\n')

    symbol_file.write("""
        (polyline
            (pts
                (xy 0.635 1.27) (xy 0.635 1.905) (xy 1.27 1.905) (xy 1.27 0)
                (xy -1.27 1.905) (xy -1.27 -1.905) (xy 1.27 0)
                (xy 1.27 -1.905) (xy 1.905 -1.905) (xy 1.905 -1.27)
            )
            (stroke (width 0.2032) (type default))
            (fill (type none))
        )
        """)

    # Write pins
    write_pin(symbol_file, 5.08, 0, 180, "1", length=3.81)
    write_pin(symbol_file, -5.08, 0, 0, "2", length=3.81)

    symbol_file.write("\t\t)\n")


def write_zener_symbol_drawing(
        symbol_file: TextIO,
        symbol_name: str,
) -> None:
    """Write the horizontal graphical representation of a diode symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.

    """
    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_0"\n')

    symbol_file.write("""
        (polyline
            (pts
                (xy 0.635 1.905) (xy 1.27 1.27) (xy 1.27 0)
                (xy -1.27 1.905) (xy -1.27 -1.905) (xy 1.27 0)
                (xy 1.27 -1.27) (xy 1.905 -1.905)
            )
            (stroke (width 0.2032) (type default))
            (fill (type none))
        )
        """)

    # Write pins
    write_pin(symbol_file, 5.08, 0, 180, "1", length=3.81)
    write_pin(symbol_file, -5.08, 0, 0, "2", length=3.81)

    symbol_file.write("\t\t)\n")


def write_circle(
    symbol_file: TextIO,
    x_pos: float,
    y_pos: float,
) -> None:
    """Write circle."""
    symbol_file.write(f"""
        (circle
            (center {x_pos} {y_pos})
            (radius 0.0254)
            (stroke (width 0.381) (type default))
            (fill (type none))
        )
    """)


def write_p_mos_transistor_symbol_drawing(
    symbol_file: TextIO,
    symbol_name: str,
    vertical_offset: float = 0.0,
) -> None:
    """Write the graphical representation of a P-MOS transistor symbol.

    Args:
        symbol_file: File object for writing the symbol file.
        symbol_name: Name of the symbol.
        vertical_offset:
            Vertical translation in units.
            Positive moves up, negative moves down. Defaults to 0.0.

    """
    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_0"\n')

    def offset_y(y: float) -> float:
        """Offset y-coordinate by vertical translation."""
        return y + vertical_offset

    symbol_file.write(f"""
        (polyline
            (pts
                (xy 0 {offset_y(-6.35)}) (xy 0 {offset_y(-2.54)})
                (xy -2.54 {offset_y(-2.54)}) (xy 2.54 {offset_y(-2.54)})
                (xy 0 {offset_y(-2.54)}) (xy 0 {offset_y(-6.35)})
            )
            (stroke (width 0) (type default))
            (fill (type outline))
        )
        (polyline
            (pts
                (xy -5.08 {offset_y(1.27)}) (xy -5.08 {offset_y(0)})
                (xy -2.54 {offset_y(0)}) (xy -2.032 {offset_y(0)})
                (xy -2.032 {offset_y(-2.032)}) (xy -2.54 {offset_y(-2.032)})
                (xy -1.524 {offset_y(-2.032)}) (xy -2.032 {offset_y(-2.032)})
                (xy -2.032 {offset_y(0)}) (xy -2.54 {offset_y(0)})
                (xy -2.54 {offset_y(1.27)}) (xy -0.508 {offset_y(1.27)})
                (xy -0.508 {offset_y(0.762)}) (xy 0.508 {offset_y(1.27)})
                (xy 0.508 {offset_y(0.762)}) (xy 0.508 {offset_y(1.27)})
                (xy 2.54 {offset_y(1.27)}) (xy 2.54 {offset_y(0)})
                (xy 0 {offset_y(0)}) (xy -0.508 {offset_y(-1.016)})
                (xy 0 {offset_y(-1.016)}) (xy 0 {offset_y(-2.032)})
                (xy -0.508 {offset_y(-2.032)}) (xy 0.508 {offset_y(-2.032)})
                (xy 0 {offset_y(-2.032)}) (xy 0 {offset_y(-1.016)})
                (xy 0.508 {offset_y(-1.016)}) (xy 0 {offset_y(0)})
                (xy 2.032 {offset_y(0)}) (xy 2.032 {offset_y(-2.032)})
                (xy 1.524 {offset_y(-2.032)}) (xy 2.54 {offset_y(-2.032)})
                (xy 2.032 {offset_y(-2.032)}) (xy 2.032 {offset_y(0)})
                (xy 2.54 {offset_y(0)}) (xy 5.08 {offset_y(0)})
                (xy 5.08 {offset_y(-3.81)}) (xy 5.08 {offset_y(1.27)})
                (xy 5.08 {offset_y(0)}) (xy 2.54 {offset_y(0)})
                (xy 2.54 {offset_y(1.27)}) (xy 0.508 {offset_y(1.27)})
                (xy 0.508 {offset_y(1.778)}) (xy 0.508 {offset_y(1.27)})
                (xy -0.508 {offset_y(1.778)}) (xy -0.508 {offset_y(1.27)})
                (xy -2.54 {offset_y(1.27)}) (xy -2.54 {offset_y(0)})
                (xy -5.08 {offset_y(0)}) (xy -5.08 {offset_y(1.27)})
            )
            (stroke (width 0) (type default))
            (fill (type outline))
        )
        """)

    # Write symbol circles with vertical offset
    write_circle(symbol_file, -2.54, offset_y(0))
    write_circle(symbol_file, 2.032, offset_y(0))
    write_circle(symbol_file, 2.54, offset_y(0))

    # Write pins with vertical offset
    write_pin(symbol_file, -7.62, offset_y(1.27), 0, "5", "D", length=2.54)
    write_pin(symbol_file, 7.62, offset_y(1.27), 180, "1", "S", length=2.54)
    write_pin(symbol_file, 7.62, offset_y(-1.27), 180, "2", "S", length=2.54)
    write_pin(symbol_file, 7.62, offset_y(-3.81), 180, "3", "S", length=2.54)
    write_pin(symbol_file, 2.54, offset_y(-6.35), 180, "4", "G", length=2.54)

    symbol_file.write("\t\t)\n")


def write_n_mos_transistor_symbol_drawing(
    symbol_file: TextIO,
    symbol_name: str,
    vertical_offset: float = 0.0,
) -> None:
    """Write the graphical representation of an N-MOS transistor symbol.

    Args:
        symbol_file: File object for writing the symbol file.
        symbol_name: Name of the symbol.
        vertical_offset:
            Vertical translation in units.
            Positive moves up, negative moves down. Defaults to 0.0.

    """
    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_0"\n')

    def offset_y(y: float) -> float:
        """Offset y-coordinate by vertical translation."""
        return y + vertical_offset

    symbol_file.write(f"""
        (polyline
            (pts
                (xy 0 {offset_y(-6.35)}) (xy 0 {offset_y(-2.54)})
                (xy -2.54 {offset_y(-2.54)}) (xy 2.54 {offset_y(-2.54)})
                (xy 0 {offset_y(-2.54)}) (xy 0 {offset_y(-6.35)})
            )
            (stroke (width 0) (type default))
            (fill (type none))
        )
        (polyline
            (pts
                (xy 5.08 {offset_y(1.27)}) (xy 5.08 {offset_y(0)})
                (xy 2.54 {offset_y(0)}) (xy 2.54 {offset_y(1.27)})
                (xy 0.508 {offset_y(1.27)}) (xy 0.508 {offset_y(1.778)})
                (xy -0.508 {offset_y(1.27)}) (xy -0.508 {offset_y(1.778)})
                (xy -0.508 {offset_y(1.27)}) (xy -2.54 {offset_y(1.27)})
                (xy -2.54 {offset_y(0)}) (xy -5.08 {offset_y(0)})
                (xy -5.08 {offset_y(1.27)}) (xy -5.08 {offset_y(0)})
                (xy -2.032 {offset_y(0)}) (xy -2.032 {offset_y(-2.032)})
                (xy -2.54 {offset_y(-2.032)}) (xy -1.524 {offset_y(-2.032)})
                (xy -2.032 {offset_y(-2.032)}) (xy -2.032 {offset_y(0)})
                (xy -2.54 {offset_y(0)}) (xy -2.54 {offset_y(1.27)})
                (xy -0.508 {offset_y(1.27)}) (xy -0.508 {offset_y(0.762)})
                (xy -0.508 {offset_y(1.27)}) (xy 0.508 {offset_y(0.762)})
                (xy 0.508 {offset_y(1.27)}) (xy 2.54 {offset_y(1.27)})
                (xy 2.54 {offset_y(0)}) (xy 0 {offset_y(0)})
                (xy 0 {offset_y(-1.016)}) (xy -0.508 {offset_y(-1.016)})
                (xy 0 {offset_y(-2.032)}) (xy -0.508 {offset_y(-2.032)})
                (xy 0.508 {offset_y(-2.032)}) (xy 0 {offset_y(-2.032)})
                (xy 0.508 {offset_y(-1.016)}) (xy 0 {offset_y(-1.016)})
                (xy 0 {offset_y(0)}) (xy 2.032 {offset_y(0)})
                (xy 2.032 {offset_y(-2.032)}) (xy 1.524 {offset_y(-2.032)})
                (xy 2.54 {offset_y(-2.032)}) (xy 2.032 {offset_y(-2.032)})
                (xy 2.032 {offset_y(0)}) (xy 5.08 {offset_y(0)})
                (xy 5.08 {offset_y(-3.81)})
            )
            (stroke (width 0) (type default))
            (fill (type outline))
        )
        """)

    # Write symbol circles with vertical offset
    write_circle(symbol_file, -2.54, offset_y(0))
    write_circle(symbol_file, 2.032, offset_y(0))
    write_circle(symbol_file, 2.54, offset_y(0))

    # Write pins with vertical offset
    write_pin(symbol_file, -7.62, offset_y(1.27), 0, "5", "D", length=2.54)
    write_pin(symbol_file, 7.62, offset_y(1.27), 180, "1", "S", length=2.54)
    write_pin(symbol_file, 7.62, offset_y(-1.27), 180, "2", "S", length=2.54)
    write_pin(symbol_file, 7.62, offset_y(-3.81), 180, "3", "S", length=2.54)
    write_pin(symbol_file, 2.54, offset_y(-6.35), 180, "4", "G", length=2.54)

    symbol_file.write("\t\t)\n")


def write_n_mos_dual_transistor_symbol_drawing(
        symbol_file: TextIO,
        symbol_name: str,
        vertical_offset: float = 1.27,
) -> None:
    """Write the horizontal graphical representation of a diode symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.
        vertical_offset:
            Vertical translation in units.
            Positive moves up, negative moves down. Defaults to 0.0.

    """
    def offset_y(y: float) -> float:
        """Offset y-coordinate by vertical translation."""
        return y + vertical_offset

    pin_specs = (
        {"1": "S1", "2": "G1", "6": "D1"},
        {"3": "S2", "4": "G2", "5": "D2"},
    )

    number = [list(pin_spec.keys()) for pin_spec in pin_specs]
    name = [list(pin_spec.values()) for pin_spec in pin_specs]

    symbol_file.write(f"""
		(symbol "{symbol_name}_1_0"
			(polyline
				(pts
					(xy 0 {offset_y(-5.08)})
                    (xy 0 {offset_y(-1.27)})
                    (xy -2.54 {offset_y(-1.27)})
                    (xy 2.54 {offset_y(-1.27)})
                    (xy 0 {offset_y(-1.27)})
                    (xy 0 {offset_y(-5.08)})
				)
				(stroke (width 0) (type default))
				(fill (type none))
			)
			(polyline
				(pts
					(xy 7.62 {offset_y(2.54)})
                    (xy 7.62 {offset_y(1.27)})
                    (xy 2.54 {offset_y(1.27)})
                    (xy 2.54 {offset_y(2.54)})
                    (xy 0.508 {offset_y(2.54)})
                    (xy 0.508 {offset_y(3.048)})
                    (xy -0.508 {offset_y(2.54)})
                    (xy -0.508 {offset_y(3.048)})
                    (xy -0.508 {offset_y(2.54)})
                    (xy -2.54 {offset_y(2.54)})
                    (xy -2.54 {offset_y(1.27)})
                    (xy -7.62 {offset_y(1.27)})
                    (xy -7.62 {offset_y(2.54)})
                    (xy -7.62 {offset_y(1.27)})
                    (xy -2.032 {offset_y(1.27)})
                    (xy -2.032 {offset_y(-0.762)})
                    (xy -2.54 {offset_y(-0.762)})
                    (xy -1.524 {offset_y(-0.762)})
                    (xy -2.032 {offset_y(-0.762)})
                    (xy -2.032 {offset_y(1.27)})
                    (xy -2.54 {offset_y(1.27)})
                    (xy -2.54 {offset_y(2.54)})
                    (xy -0.508 {offset_y(2.54)})
                    (xy -0.508 {offset_y(2.032)})
                    (xy -0.508 {offset_y(2.54)})
                    (xy 0.508 {offset_y(2.032)})
                    (xy 0.508 {offset_y(2.54)})
                    (xy 2.54 {offset_y(2.54)})
                    (xy 2.54 {offset_y(1.27)})
                    (xy 0 {offset_y(1.27)})
                    (xy 0 {offset_y(0.254)})
                    (xy -0.508 {offset_y(0.254)})
                    (xy 0 {offset_y(-0.762)})
                    (xy -0.508 {offset_y(-0.762)})
                    (xy 0.508 {offset_y(-0.762)})
                    (xy 0 {offset_y(-0.762)})
                    (xy 0.508 {offset_y(0.254)})
                    (xy 0 {offset_y(0.254)})
                    (xy 0 {offset_y(1.27)})
                    (xy 2.032 {offset_y(1.27)})
                    (xy 2.032 {offset_y(-0.762)})
                    (xy 1.524 {offset_y(-0.762)})
                    (xy 2.54 {offset_y(-0.762)})
                    (xy 2.032 {offset_y(-0.762)})
                    (xy 2.032 {offset_y(1.27)})
                    (xy 7.62 {offset_y(1.27)})
                    (xy 7.62 {offset_y(2.54)})
				)
				(stroke (width 0) (type default))
				(fill (type outline))
			)
        """)

    # Write symbol circles with vertical offset
    write_circle(symbol_file, -2.54, offset_y(1.27))
    write_circle(symbol_file, 2.032, offset_y(1.27))
    write_circle(symbol_file, 2.54, offset_y(1.27))

    # Write pins with vertical offset
    write_pin(
        symbol_file, 10.16, offset_y(2.54), 180, number[0][0], name[0][0])
    write_pin(
        symbol_file, 2.54, offset_y(-5.08), 180, number[0][1], name[0][1])
    write_pin(
        symbol_file, -10.16, offset_y(2.54), 0, number[0][2], name[0][2])

    symbol_file.write(")")

    symbol_file.write(f"""
		(symbol "{symbol_name}_2_0"
			(polyline
				(pts
					(xy 0 {offset_y(-5.08)})
                    (xy 0 {offset_y(-1.27)})
                    (xy -2.54 {offset_y(-1.27)})
                    (xy 2.54 {offset_y(-1.27)})
                    (xy 0 {offset_y(-1.27)})
                    (xy 0 {offset_y(-5.08)})
				)
				(stroke (width 0) (type default))
				(fill (type none))
			)
			(polyline
				(pts
					(xy 7.62 {offset_y(2.54)})
                    (xy 7.62 {offset_y(1.27)})
                    (xy 2.54 {offset_y(1.27)})
                    (xy 2.54 {offset_y(2.54)})
                    (xy 0.508 {offset_y(2.54)})
                    (xy 0.508 {offset_y(3.048)})
                    (xy -0.508 {offset_y(2.54)})
                    (xy -0.508 {offset_y(3.048)})
                    (xy -0.508 {offset_y(2.54)})
                    (xy -2.54 {offset_y(2.54)})
                    (xy -2.54 {offset_y(1.27)})
                    (xy -7.62 {offset_y(1.27)})
                    (xy -7.62 {offset_y(2.54)})
                    (xy -7.62 {offset_y(1.27)})
                    (xy -2.032 {offset_y(1.27)})
                    (xy -2.032 {offset_y(-0.762)})
                    (xy -2.54 {offset_y(-0.762)})
                    (xy -1.524 {offset_y(-0.762)})
                    (xy -2.032 {offset_y(-0.762)})
                    (xy -2.032 {offset_y(1.27)})
                    (xy -2.54 {offset_y(1.27)})
                    (xy -2.54 {offset_y(2.54)})
                    (xy -0.508 {offset_y(2.54)})
                    (xy -0.508 {offset_y(2.032)})
                    (xy -0.508 {offset_y(2.54)})
                    (xy 0.508 {offset_y(2.032)})
                    (xy 0.508 {offset_y(2.54)})
                    (xy 2.54 {offset_y(2.54)})
                    (xy 2.54 {offset_y(1.27)})
                    (xy 0 {offset_y(1.27)})
                    (xy 0 {offset_y(0.254)})
                    (xy -0.508 {offset_y(0.254)})
                    (xy 0 {offset_y(-0.762)})
                    (xy -0.508 {offset_y(-0.762)})
                    (xy 0.508 {offset_y(-0.762)})
                    (xy 0 {offset_y(-0.762)})
                    (xy 0.508 {offset_y(0.254)})
                    (xy 0 {offset_y(0.254)})
                    (xy 0 {offset_y(1.27)})
                    (xy 2.032 {offset_y(1.27)})
                    (xy 2.032 {offset_y(-0.762)})
                    (xy 1.524 {offset_y(-0.762)})
                    (xy 2.54 {offset_y(-0.762)})
                    (xy 2.032 {offset_y(-0.762)})
                    (xy 2.032 {offset_y(1.27)})
                    (xy 7.62 {offset_y(1.27)})
                    (xy 7.62 {offset_y(2.54)})
				)
				(stroke (width 0) (type default))
				(fill (type outline))
			)
        """)

    # Write symbol circles with vertical offset
    write_circle(symbol_file, -2.54, offset_y(1.27))
    write_circle(symbol_file, 2.032, offset_y(1.27))
    write_circle(symbol_file, 2.54, offset_y(1.27))

    # Write pins with vertical offset
    write_pin(
        symbol_file, 10.16, offset_y(2.54), 180, number[1][0], name[1][0])
    write_pin(
        symbol_file, 2.54, offset_y(-5.08), 180, number[1][1], name[1][1])
    write_pin(
        symbol_file, -10.16, offset_y(2.54), 0, number[1][2], name[1][2])

    symbol_file.write(")")


def write_p_mos_dual_transistor_symbol_drawing(
        symbol_file: TextIO,
        symbol_name: str,
        vertical_offset: float = 1.27,
) -> None:
    """Write the horizontal graphical representation of a diode symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.
        vertical_offset:
            Vertical translation in units.
            Positive moves up, negative moves down. Defaults to 0.0.

    """
    def offset_y(y: float) -> float:
        """Offset y-coordinate by vertical translation."""
        return y + vertical_offset

    pin_specs = (
        {"1": "S1", "2": "G1", "6": "D1"},
        {"3": "S2", "4": "G2", "5": "D2"},
    )

    number = [list(pin_spec.keys()) for pin_spec in pin_specs]
    name = [list(pin_spec.values()) for pin_spec in pin_specs]

    symbol_file.write(f"""
		(symbol "{symbol_name}_1_0"
			(polyline
				(pts
					(xy 0 {offset_y(-5.08)})
                    (xy 0 {offset_y(-1.27)})
                    (xy -2.54 {offset_y(-1.27)})
                    (xy 2.54 {offset_y(-1.27)})
                    (xy 0 {offset_y(-1.27)})
                    (xy 0 {offset_y(-5.08)})
				)
				(stroke (width 0) (type default))
				(fill (type outline))
			)
			(polyline
				(pts
					(xy -7.62 {offset_y(2.54)})
                    (xy -7.62 {offset_y(1.27)})
                    (xy -2.54 {offset_y(1.27)})
                    (xy -2.032 {offset_y(1.27)})
                    (xy -2.032 {offset_y(-0.762)})
                    (xy -2.54 {offset_y(-0.762)})
					(xy -1.524 {offset_y(-0.762)})
                    (xy -2.032 {offset_y(-0.762)})
                    (xy -2.032 {offset_y(1.27)})
                    (xy -2.54 {offset_y(1.27)})
                    (xy -2.54 {offset_y(2.54)})
                    (xy -0.508 {offset_y(2.54)})
					(xy -0.508 {offset_y(2.032)})
                    (xy 0.508 {offset_y(2.54)})
                    (xy 0.508 {offset_y(2.032)})
                    (xy 0.508 {offset_y(2.54)})
                    (xy 2.54 {offset_y(2.54)})
                    (xy 2.54 {offset_y(1.27)})
					(xy 0 {offset_y(1.27)})
                    (xy -0.508 {offset_y(0.254)})
                    (xy 0 {offset_y(0.254)})
                    (xy 0 {offset_y(-0.762)})
                    (xy -0.508 {offset_y(-0.762)})
                    (xy 0.508 {offset_y(-0.762)})
                    (xy 0 {offset_y(-0.762)})
                    (xy 0 {offset_y(0.254)})
                    (xy 0.508 {offset_y(0.254)})
                    (xy 0 {offset_y(1.27)})
                    (xy 2.032 {offset_y(1.27)})
                    (xy 2.032 {offset_y(-0.762)})
                    (xy 1.524 {offset_y(-0.762)})
                    (xy 2.54 {offset_y(-0.762)})
                    (xy 2.032 {offset_y(-0.762)})
                    (xy 2.032 {offset_y(1.27)})
                    (xy 2.54 {offset_y(1.27)})
                    (xy 7.62 {offset_y(1.27)})
                    (xy 7.62 {offset_y(2.54)})
                    (xy 7.62 {offset_y(2.54)})
                    (xy 7.62 {offset_y(1.27)})
					(xy 2.54 {offset_y(1.27)})
                    (xy 2.54 {offset_y(2.54)})
                    (xy 0.508 {offset_y(2.54)})
                    (xy 0.508 {offset_y(3.048)})
                    (xy 0.508 {offset_y(2.54)})
                    (xy -0.508 {offset_y(3.048)})
					(xy -0.508 {offset_y(2.54)})
                    (xy -2.54 {offset_y(2.54)})
                    (xy -2.54 {offset_y(1.27)})
                    (xy -7.62 {offset_y(1.27)})
                    (xy -7.62 {offset_y(2.54)})
				)
				(stroke (width 0) (type default))
				(fill (type outline))
			)
        """)

    # Write symbol circles with vertical offset
    write_circle(symbol_file, -2.54, offset_y(1.27))
    write_circle(symbol_file, 2.032, offset_y(1.27))
    write_circle(symbol_file, 2.54, offset_y(1.27))

    # Write pins with vertical offset
    write_pin(
        symbol_file, 10.16, offset_y(2.54), 180, number[0][0], name[0][0])
    write_pin(
        symbol_file, 2.54, offset_y(-5.08), 180, number[0][1], name[0][1])
    write_pin(
        symbol_file, -10.16, offset_y(2.54), 0, number[0][2], name[0][2])

    symbol_file.write(")")

    symbol_file.write(f"""
		(symbol "{symbol_name}_2_0"
			(polyline
				(pts
					(xy 0 {offset_y(-5.08)})
                    (xy 0 {offset_y(-1.27)})
                    (xy -2.54 {offset_y(-1.27)})
                    (xy 2.54 {offset_y(-1.27)})
                    (xy 0 {offset_y(-1.27)})
                    (xy 0 {offset_y(-5.08)})
				)
				(stroke (width 0) (type default))
				(fill (type outline))
			)
			(polyline
				(pts
					(xy -7.62 {offset_y(2.54)})
                    (xy -7.62 {offset_y(1.27)})
                    (xy -2.54 {offset_y(1.27)})
                    (xy -2.032 {offset_y(1.27)})
                    (xy -2.032 {offset_y(-0.762)})
                    (xy -2.54 {offset_y(-0.762)})
					(xy -1.524 {offset_y(-0.762)})
                    (xy -2.032 {offset_y(-0.762)})
                    (xy -2.032 {offset_y(1.27)})
                    (xy -2.54 {offset_y(1.27)})
                    (xy -2.54 {offset_y(2.54)})
                    (xy -0.508 {offset_y(2.54)})
					(xy -0.508 {offset_y(2.032)})
                    (xy 0.508 {offset_y(2.54)})
                    (xy 0.508 {offset_y(2.032)})
                    (xy 0.508 {offset_y(2.54)})
                    (xy 2.54 {offset_y(2.54)})
                    (xy 2.54 {offset_y(1.27)})
					(xy 0 {offset_y(1.27)})
                    (xy -0.508 {offset_y(0.254)})
                    (xy 0 {offset_y(0.254)})
                    (xy 0 {offset_y(-0.762)})
                    (xy -0.508 {offset_y(-0.762)})
                    (xy 0.508 {offset_y(-0.762)})
                    (xy 0 {offset_y(-0.762)})
                    (xy 0 {offset_y(0.254)})
                    (xy 0.508 {offset_y(0.254)})
                    (xy 0 {offset_y(1.27)})
                    (xy 2.032 {offset_y(1.27)})
                    (xy 2.032 {offset_y(-0.762)})
                    (xy 1.524 {offset_y(-0.762)})
                    (xy 2.54 {offset_y(-0.762)})
                    (xy 2.032 {offset_y(-0.762)})
                    (xy 2.032 {offset_y(1.27)})
                    (xy 2.54 {offset_y(1.27)})
                    (xy 7.62 {offset_y(1.27)})
                    (xy 7.62 {offset_y(2.54)})
                    (xy 7.62 {offset_y(2.54)})
                    (xy 7.62 {offset_y(1.27)})
					(xy 2.54 {offset_y(1.27)})
                    (xy 2.54 {offset_y(2.54)})
                    (xy 0.508 {offset_y(2.54)})
                    (xy 0.508 {offset_y(3.048)})
                    (xy 0.508 {offset_y(2.54)})
                    (xy -0.508 {offset_y(3.048)})
					(xy -0.508 {offset_y(2.54)})
                    (xy -2.54 {offset_y(2.54)})
                    (xy -2.54 {offset_y(1.27)})
                    (xy -7.62 {offset_y(1.27)})
                    (xy -7.62 {offset_y(2.54)})
				)
				(stroke (width 0) (type default))
				(fill (type outline))
			)
        """)

    # Write symbol circles with vertical offset
    write_circle(symbol_file, -2.54, offset_y(1.27))
    write_circle(symbol_file, 2.032, offset_y(1.27))
    write_circle(symbol_file, 2.54, offset_y(1.27))

    # Write pins with vertical offset
    write_pin(
        symbol_file, 10.16, offset_y(2.54), 180, number[1][0], name[1][0])
    write_pin(
        symbol_file, 2.54, offset_y(-5.08), 180, number[1][1], name[1][1])
    write_pin(
        symbol_file, -10.16, offset_y(2.54), 0, number[1][2], name[1][2])

    symbol_file.write(")")


def write_connector_symbol_drawing(
    symbol_file: TextIO,
    symbol_name: str,
    component_data: dict[str, str],
) -> None:
    """Write the symbol drawing with dimensions adjusted for pin count."""
    pin_count = int(component_data.get("Pin Count", "2"))
    pin_spacing = 2.54

    min_height = 7.62
    calculated_height = (pin_count * pin_spacing) + 2.54
    rectangle_height = max(min_height, calculated_height)

    symbol_file.write(f'\t\t(symbol "{symbol_name}_0_0"\n')

    start_y = (pin_count - 1) * pin_spacing / 2
    for pin_num in range(1, pin_count + 1):
        y_pos = start_y - (pin_num - 1) * pin_spacing
        write_pin(symbol_file, -5.08, y_pos, 0, str(pin_num))

    symbol_file.write("\t\t)\n")

    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_0"\n')
    write_rectangle(
        symbol_file, -2.54, rectangle_height / 2, 2.54, -rectangle_height / 2)
    symbol_file.write("\t\t)\n")


def write_rectangle(
    symbol_file: TextIO,
    start_x: float,
    start_y: float,
    end_x: float,
    end_y: float,
) -> None:
    """Write a rectangle definition with specific formatting."""
    symbol_file.write(f"""
        (rectangle
            (start {start_x} {start_y})
            (end {end_x} {end_y})
            (stroke (width 0.254) (type solid))
            (fill (type none))
        )
        """)
