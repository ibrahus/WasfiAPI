from pydantic import BaseModel, Field, validator


class Product(BaseModel):
    title: str = Field(..., min_length=1, title="The title of the product")

    @validator("title")
    def title_must_not_be_whitespace(cls, v):
        if v.strip() == "":
            raise ValueError("Product title must not be whitespace")
        return v
