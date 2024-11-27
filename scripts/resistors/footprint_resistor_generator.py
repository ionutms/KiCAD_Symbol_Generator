"""KiCad Footprint Generator for Surface Mount Resistors.

Generates standardized KiCad footprint files (.kicad_mod) for surface mount
resistors. Uses manufacturer specifications to create accurate footprints
with appropriate pad dimensions and clearances.
"""

from pathlib import Path
from typing import NamedTuple

from footprint_resistor_specs import RESISTOR_SPECS, ResistorSpecs
from symbol_resistors_specs import SERIES_SPECS, SeriesSpec
from utilities import footprint_utils as fu


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

    sections = [
        fu.generate_header(footprint_name),
        fu.generate_properties(
            specs.resistor_specs.text_positions.reference, footprint_name),
        fu.generate_courtyard(
            specs.resistor_specs.body_dimensions.width,
            specs.resistor_specs.body_dimensions.height),
        fu.generate_fab_rectangle(
            specs.resistor_specs.body_dimensions.width,
            specs.resistor_specs.body_dimensions.height),
        fu.generate_silkscreen_lines(
            specs.resistor_specs.body_dimensions.height,
            specs.resistor_specs.pad_dimensions.center_x,
            specs.resistor_specs.pad_dimensions.width),
        fu.generate_pads(
            specs.resistor_specs.pad_dimensions.width,
            specs.resistor_specs.pad_dimensions.height,
            specs.resistor_specs.pad_dimensions.center_x),
        fu.associate_3d_model(
            "KiCAD_Symbol_Generator/3D_models", step_file_name),
        ")",  # Close the footprint
    ]
    return "\n".join(sections)


def generate_footprint_file(series_name: str, output_dir: str) -> None:
    """Generate and save a complete .kicad_mod file for a resistor.

    Args:
        series_name: Name of the resistor series (e.g., "ERJ-2RK")
        output_dir: Directory to save the generated footprint file

    Raises:
        KeyError: If series_name is not found in SERIES_SPECS
        IOError: If there are problems writing the output file

    """
    series_spec = SERIES_SPECS[series_name]
    footprint_specs = create_footprint_specs(series_spec)
    footprint_content = generate_footprint(footprint_specs)

    filename = (
        f"{output_dir}/"  # noqa: ISC003
        + "R_"
        + f"{series_spec.case_code_in}_"
        + f"{series_spec.case_code_mm}"
        + "Metric.kicad_mod"
    )
    with Path.open(filename, "w", encoding="utf-8") as f:
        f.write(footprint_content)
