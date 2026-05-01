from dataclasses import dataclass, field


@dataclass(frozen=True)
class SelectorConfig:
    type: str  # "table_selector"
    table: str
    display_fields: tuple[str, ...] = field(default_factory=tuple)
    multi_select: bool = True


@dataclass(frozen=True)
class SelectorResult:
    selected_ids: tuple[str, ...]
