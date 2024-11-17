"""TODO"""


from typing import Dict


CASE_DIMENSIONS: Dict[str, Dict[str, float]] = {
    "0402": {
        "body_width": 1.0,
        "body_height": 0.5,
        "pad_width": 0.54,
        "pad_height": 0.64,
        "pad_center_x": 0.51,
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
        "pad_width": 0.8,
        "pad_height": 0.95,
        "pad_center_x": 0.825,
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
        "pad_width": 1.025,
        "pad_height": 1.4,
        "pad_center_x": 0.9125,
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
        "pad_width": 1.125,
        "pad_height": 1.75,
        "pad_center_x": 1.4625,
        "silk_y": 0.91,
        "silk_extension": 0.727064,
        "silk_inset": 0.25,
        "courtyard_margin": 2.28,
        "ref_y": -2.032,
        "value_y": 2.032,
        "fab_reference_y": 3.302
    }
}
