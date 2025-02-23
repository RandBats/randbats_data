from pathlib import Path


class Paths:
    def __init__(self):
        self.base_folder = Path(r"C:\Users\filos\OneDrive\Desktop\randbats_data")

        # -- DATA
        self.data_folder = self.base_folder / "data"
        self.raw_data_folder = self.data_folder / "raw"
