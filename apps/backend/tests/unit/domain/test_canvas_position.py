import pytest
from docuweave.domain.value_objects.canvas_position import CanvasPosition


def test_valid_position() -> None:
    pos = CanvasPosition(x=10, y=20, width=300, height=150)
    assert pos.x == 10
    assert pos.width == 300
    assert pos.is_auto_height is False


def test_auto_height() -> None:
    pos = CanvasPosition(x=0, y=0, width=100, height="auto")
    assert pos.is_auto_height is True


def test_negative_x_raises() -> None:
    with pytest.raises(ValueError, match="x must be"):
        CanvasPosition(x=-1, y=0, width=100, height=50)


def test_negative_y_raises() -> None:
    with pytest.raises(ValueError, match="y must be"):
        CanvasPosition(x=0, y=-5, width=100, height=50)


def test_zero_width_raises() -> None:
    with pytest.raises(ValueError, match="width must be"):
        CanvasPosition(x=0, y=0, width=0, height=50)


def test_negative_height_raises() -> None:
    with pytest.raises(ValueError, match="height must be"):
        CanvasPosition(x=0, y=0, width=100, height=-10)


def test_invalid_string_height_raises() -> None:
    with pytest.raises(ValueError, match="height must be"):
        CanvasPosition(x=0, y=0, width=100, height="fill")  # type: ignore[arg-type]
