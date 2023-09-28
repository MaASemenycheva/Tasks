from typing import Optional

from pydantic import BaseModel


class Article(BaseModel):
    """Class with parameters similar to the DB table structure

    Args:
        BaseModel: inherits pydantic's BaseModel
    """
    id: Optional[int]
    title: str
    text: str

    def sample_func_1(self):
        """Dummy function 1
        """

    def sample_func_2(self):
        """Dummy function 2
        """
