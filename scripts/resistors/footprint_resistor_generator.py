"""KiCad Footprint Generator for Surface Mount Resistors.

Generates standardized KiCad footprint files (.kicad_mod) for surface mount
resistors. Uses manufacturer specifications to create accurate footprints
with appropriate pad dimensions and clearances.
"""

from pathlib import Path
from typing import NamedTuple

from footprint_resistor_specs import RESISTOR_SPECS, ResistorSpecs
from symbol_resistors_specs import SERIES_SPECS, SeriesSpec
from utilities import footprint_utils


class FootprintSpecs(NamedTuple):
    """Complete specifications for generating a resistor footprint.

    Combines physical dimensions with series-specific properties for
    generating accurate KiCad footprints.
    """

    series_spec: SeriesSpec  # Original series specifications
    resistor_specs: ResistorSpecs  # Physical specifications


def create_footprint_specs(series_spec: SeriesSpec) -> FootprintSpecs:
    """Create complete footprint specifications from series specifications.

    Args:
        series_spec: SeriesSpec object containing basic specifications

    Returns:
        FootprintSpecs object with complete physical dimensions

    Raises:
        KeyError: If case code is not found in RESISTOR_SPECS

    """
    return FootprintSpecs(
        series_spec=series_spec,
        resistor_specs=RESISTOR_SPECS[series_spec.case_code_in],
    )


def generate_footprint(specs: FootprintSpecs) -> str:
    """Generate complete KiCad footprint file content for a resistor.

    Args:
        specs: Combined specifications for the resistor

    Returns:
        Complete .kicad_mod file content as formatted string

    """
    case_in = specs.series_spec.case_code_in
    case_mm = specs.series_spec.case_code_mm
    footprint_name = f"R_{case_in}_{case_mm}Metric"
    step_file_name = f"R_{case_in}"

    body_width = specs.resistor_specs.body_dimensions.width
    body_height = specs.resistor_specs.body_dimensions.height

    pad_center_x = specs.resistor_specs.pad_dimensions.center_x
    pad_width = specs.resistor_specs.pad_dimensions.width
    pad_height = specs.resistor_specs.pad_dimensions.height

    sections = [
        footprint_utils.generate_header(footprint_name),
        footprint_utils.generate_properties(
            specs.resistor_specs.text_positions.reference, footprint_name),
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
    series_spec = SERIES_SPECS[series_name]
    footprint_specs = create_footprint_specs(series_spec)
    footprint_content = generate_footprint(footprint_specs)

    filename = (
        f"R_{series_spec.case_code_in}_{series_spec.case_code_mm}"
        "Metric.kicad_mod")
    file_path = f"{output_path}/{filename}"

    with Path.open(file_path, "w", encoding="utf-8") as file_handle:
        file_handle.write(footprint_content)
