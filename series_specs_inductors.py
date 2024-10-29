"""todo"""

from typing import List, NamedTuple, Dict


class SeriesSpec(NamedTuple):
    """Inductor series specifications."""
    manufacturer: str
    base_series: str
    footprint: str
    tolerance: str
    datasheet: str
    inductance_values: List[float]
    trustedparts_link: str
    has_aec: bool = True
    value_suffix: str = "ME"


class PartInfo(NamedTuple):
    """Component part information structure."""
    symbol_name: str
    reference: str
    value: float
    footprint: str
    datasheet: str
    description: str
    manufacturer: str
    mpn: str
    tolerance: str
    series: str
    trustedparts_link: str


SERIES_SPECS: Dict[str, SeriesSpec] = {
    "XFL2006": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL2006",
        footprint="footprints:XFL2006",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "65419ba7-9eac-409b-830a-74bf182a8aca/xfl2006.pdf",
        inductance_values=[
            1.0, 2.2, 3.3, 4.7, 5.6, 6.8, 8.2,
            10.0, 15.0, 22.0, 33.0, 47.0, 56.0, 68.0, 82.0,
            100.0
        ],
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XFL2010": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL2010",
        footprint="footprints:XFL2010",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "50382b97-998f-4b75-b5ee-4a93b0ac4411/xfl2010.pdf",
        inductance_values=[
            0.04, 0.12, 0.22, 0.38, 0.6, 0.82,
            1.0, 1.5, 2.2, 3.3, 4.7, 6.8, 8.2,
            10.0, 18.0, 22.0, 33.0, 47.0, 56.0, 68.0, 82.0,
            100.0, 220.0
        ],
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XFL3012": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL3012",
        footprint="footprints:XFL3012",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "f76a3c9b-4fff-4397-8028-ef8e043eb200/xfl3012.pdf",
        inductance_values=[
            0.33, 0.56, 0.68, 1.0, 1.5, 2.2, 3.3, 4.7, 6.8,
            10.0, 15.0, 22.0, 33.0, 39.0, 47.0, 56.0, 68.0,
            82.0, 100.0, 220.0
        ],
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XFL3010": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL3010",
        footprint="footprints:XFL3010",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "0118859e-f2e2-4063-93cf-e50ed636ea4e/xfl3010.pdf",
        inductance_values=[
            0.60, 1.0, 1.5, 2.2, 3.3, 4.7, 6.8, 10.0, 15.0,
            22.0, 33.0, 47.0, 68.0, 82.0, 100.0
        ],
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XFL4012": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL4012",
        footprint="footprints:XFL4012",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "2d7c4d90-1677-4c05-9569-33b6dc7153e7/xfl4012.pdf",
        inductance_values=[
            0.12, 0.25, 0.47, 0.6
        ],
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XFL4015": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL4015",
        footprint="footprints:XFL4015",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "84927b8b-f089-421b-a7f4-a0fa23afe908/xfl4015.pdf",
        inductance_values=[
            0.18, 0.33, 0.47, 0.7, 1.2
        ],
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XFL4020": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL4020",
        footprint="footprints:XFL4020",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "50632d43-da1b-4cdb-8ab4-3029cab51df3/xfl4020.pdf",
        inductance_values=[
            0.12, 0.24, 0.33, 0.47, 0.56, 1.0, 1.5, 2.2, 3.3, 4.7
        ],
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XFL4030": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL4030",
        footprint="footprints:XFL4030",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "d12f7f67-cfc1-404a-9993-f09a1451b0a9/xfl4030.pdf",
        inductance_values=[
            0.47, 1.0, 2.0, 3.0, 4.7
        ],
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XFL5015": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL5015",
        footprint="footprints:XFL5015",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "5f7b596c-8f2f-415e-931e-74a5b6804936/xfl5015.pdf",
        inductance_values=[
            0.22, 0.42, 0.68, 1.2, 1.5
        ],
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XFL5018": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL5018",
        footprint="footprints:XFL5018",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "5f7b596c-8f2f-415e-931e-74a5b6804936/xfl5015.pdf",
        inductance_values=[
            2.2, 3.3
        ],
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XFL5030": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL5030",
        footprint="footprints:XFL5030",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "f01e4ccd-6be9-43eb-bb01-c23b4deeb2c5/xfl5030.pdf",
        inductance_values=[
            0.27, 0.56, 1.0, 2.2, 3.3, 4.7
        ],
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XFL6012": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL6012",
        footprint="footprints:XFL6012",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "ae4a44fc-deeb-45d7-81a6-abe1d0432add/xfl6012.pdf",
        inductance_values=[
            0.18, 0.39, 0.6, 0.8, 1.0
        ],
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XFL6060": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL6060",
        footprint="footprints:XFL6060",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "9e8cc1df-cee0-4215-90fb-b5193fa22761/xfl6060-473.pdf",
        inductance_values=[
            47.0
        ],
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XFL7015": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL7015",
        footprint="footprints:XFL7015",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "ccf09628-6e8c-462a-9dc9-fa4346e7cf0a/xfl7015.pdf",
        inductance_values=[
            0.25, 0.47, 0.68, 1.0, 1.5
        ],
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
}
