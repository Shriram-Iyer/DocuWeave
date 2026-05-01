from dataclasses import dataclass


@dataclass(frozen=True)
class CanvasPosition:
    x: float
    y: float
    width: float
    height: float | str  # float or "auto"

    def __post_init__(self) -> None:
        if self.x < 0:
            raise ValueError("x must be >= 0")
        if self.y < 0:
            raise ValueError("y must be >= 0")
        if self.width <= 0:
            raise ValueError("width must be > 0")
        if isinstance(self.height, (int, float)) and self.height <= 0:
            raise ValueError("height must be > 0 or 'auto'")
        if isinstance(self.height, str) and self.height != "auto":
            raise ValueError("height must be a positive number or 'auto'")

    @property
    def is_auto_height(self) -> bool:
        return self.height == "auto"
