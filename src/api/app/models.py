from typing import Optional
from pydantic import BaseModel


class FilterProductsModel(BaseModel):
    gender: Optional[str]
    master_category: Optional[str]
    sub_category: Optional[str]
    article_type: Optional[str]
    base_colour: Optional[str]
    season: Optional[str]
    start_year: Optional[int]
    end_year: Optional[int]
    usage: Optional[str]
    apply_model: bool = False
    apply_augmentation: bool = False
