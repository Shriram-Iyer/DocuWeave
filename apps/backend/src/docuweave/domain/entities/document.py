from dataclasses import dataclass, field


@dataclass(frozen=True)
class DocumentJob:
    template_id: str
    data_source_id: str
    link_config_id: str
    output_format: str  # docx | xlsx
    selected_ids: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class DocumentOutput:
    file_path: str
    filename: str
    content_type: str  # application/vnd.openxmlformats-officedocument...
