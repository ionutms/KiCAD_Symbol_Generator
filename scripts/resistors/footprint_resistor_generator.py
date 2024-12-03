"""KiCad Footprint Generator for Surface Mount Resistors.

Generates standardized KiCad footprint files (.kicad_mod) for surface mount
resistors. Uses manufacturer specifications to create accurate footprints
with appropriate pad dimensions and clearances.
"""

from pathlib import Path

from footprint_resistor_specs import FOOTPRINTS_SPECS, FootprintSpecs
from symbol_resistors_specs import SYMBOLS_SPECS, SeriesSpec
from utilities import footprint_utils


def generate_footprint(
    series_spec: SeriesSpec,
    resistor_specs: FootprintSpecs,
) -> str:
    """Generate complete KiCad footprint file content for a resistor.

    Args:
        series_spec: Series specifications from SYMBOLS_SPECS
        resistor_specs: Physical specifications from FOOTPRINTS_SPECS

    Returns:
        Complete .kicad_mod file content as formatted string

    """
    case_in: str = series_spec.case_code_in
    case_mm: str = series_spec.case_code_mm
    footprint_name: str = f"R_{case_in}_{case_mm}Metric"
    step_file_name: str = f"R_{case_in}"

    body_width: float = resistor_specs.body_dimensions.width
    body_height: float = resistor_specs.body_dimensions.height

    pad_center_x: float = resistor_specs.pad_dimensions.center_x
    pad_width: float = resistor_specs.pad_dimensions.width
    pad_height: float = resistor_specs.pad_dimensions.height

    sections: list[str] = [
        footprint_utils.generate_header(footprint_name),
        footprint_utils.generate_properties(
            resistor_specs.ref_offset_y, footprint_name),
        footprint_utils.generate_courtyard(body_width, body_height),
        footprint_utils.generate_fab_rectangle(body_width, body_height),
        footprint_utils.generate_silkscreen_lines(
            body_height, pad_center_x, pad_width),
        footprint_utils.generate_pads(pad_width, pad_height, pad_center_x),
        footprint_utils.associate_3d_model(
            "KiCAD_Symbol_Generator/3D_models", step_file_name),
        ")",  # Close the footprint
    ]
    return "\n".join(sections)


def generate_footprint_file(
    series_name: str,
    output_path: str,
) -> None:
    """Generate and save a complete .kicad_mod file.

    Args:
        series_name: Name of the series
        output_path: Directory to save the generated footprint file

    """
    series_spec: SeriesSpec = SYMBOLS_SPECS[series_name]
    resistor_specs: FootprintSpecs = \
        FOOTPRINTS_SPECS[series_spec.case_code_in]

    footprint_content: str = generate_footprint(series_spec, resistor_specs)

    filename: str = (
        f"R_{series_spec.case_code_in}_{series_spec.case_code_mm}"
        "Metric.kicad_mod")
    file_path: str = f"{output_path}/{filename}"

    with Path.open(file_path, "w", encoding="utf-8") as file_handle:
        file_handle.write(footprint_content)
