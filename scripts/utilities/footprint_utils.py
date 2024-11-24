"""todo."""


def generate_header(model_name: str) -> str:
    """Generate the footprint header section."""
    return (
        f"""(footprint "{model_name}"
    (version 20240108)
    (generator "pcbnew")
    (generator_version "8.0")
    (layer "F.Cu")
    """)
