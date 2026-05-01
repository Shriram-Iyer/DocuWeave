from pydantic import BaseModel


class GenerateDocumentRequest(BaseModel):
    template_id: str
    data_source_id: str
    link_config_id: str
    output_format: str = "docx"  # docx | xlsx
    selected_ids: list[str] = []
