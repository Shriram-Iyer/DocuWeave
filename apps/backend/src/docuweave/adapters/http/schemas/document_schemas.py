from pydantic import BaseModel


class GenerateDocumentRequest(BaseModel):
    template_id: str
    data_source_id: str
    link_config_id: str
    selected_ids: list[str] = []
