class SegmentationRegion:
    DEFAULT = "Default"
    BACKGROUND = "Background"

    def __init__(self):
        self.id = None
        self.color = None
        self.vertices = []
        self.segments = []
        self.mask = None
        self.image = None
        self.measures = None
