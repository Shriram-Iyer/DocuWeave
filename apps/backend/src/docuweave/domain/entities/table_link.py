from dataclasses import dataclass, field


@dataclass(frozen=True)
class LinkDef:
    """Defines how a child table links back to a parent table."""
    field: str       # column in this table containing the FK value
    ref_table: str   # name of the parent table
    ref_field: str   # primary key column in the parent table


@dataclass(frozen=True)
class TableConfig:
    name: str
    primary_key: str
    link: LinkDef | None = None


@dataclass(frozen=True)
class LinkConfig:
    id: str
    name: str
    tables: tuple[TableConfig, ...] = field(default_factory=tuple)

    def get_table(self, name: str) -> TableConfig | None:
        for t in self.tables:
            if t.name == name:
                return t
        return None

    def root_tables(self) -> list[TableConfig]:
        """Tables with no link (top-level parents)."""
        return [t for t in self.tables if t.link is None]

    def children_of(self, parent_name: str) -> list[TableConfig]:
        """Tables whose link.ref_table == parent_name."""
        return [t for t in self.tables if t.link and t.link.ref_table == parent_name]
