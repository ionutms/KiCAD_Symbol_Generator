"""TODO"""

from typing import Dict


CASE_DIMENSIONS: Dict[str, Dict[str, float]] = {
    "0402": {
        "body_width": 1.0,
        "body_height": 0.5,
        "pad_width": 0.6,
        "pad_height": 0.7,
        "pad_center_x": 0.54,
        "silk_y": 0.38,
        "silk_extension": 0.153641,
        "silk_inset": 0.15,
        "courtyard_margin": 0.91,
        "ref_y": -1.27,
        "value_y": 1.27,
        "fab_reference_y": 2.54
    },
    "0603": {
        "body_width": 1.6,
        "body_height": 0.8,
        "pad_width": 0.9,
        "pad_height": 1.0,
        "pad_center_x": 0.875,
        "silk_y": 0.5225,
        "silk_extension": 0.237258,
        "silk_inset": 0.24,
        "courtyard_margin": 1.48,
        "ref_y": -1.524,
        "value_y": 1.524,
        "fab_reference_y": 2.794
    },
    "0805": {
        "body_width": 2.0,
        "body_height": 1.25,
        "pad_width": 1.15,
        "pad_height": 1.45,
        "pad_center_x": 0.95,
        "silk_y": 0.735,
        "silk_extension": 0.227064,
        "silk_inset": 0.23,
        "courtyard_margin": 1.68,
        "ref_y": -1.778,
        "value_y": 1.778,
        "fab_reference_y": 3.048
    },
    "1206": {
        "body_width": 3.2,
        "body_height": 1.6,
        "pad_width": 1.25,
        "pad_height": 1.8,
        "pad_center_x": 1.5,
        "silk_y": 0.91,
        "silk_extension": 0.727064,
        "silk_inset": 0.25,
        "courtyard_margin": 2.28,
        "ref_y": -2.032,
        "value_y": 2.032,
        "fab_reference_y": 3.302
    }
}
