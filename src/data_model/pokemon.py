from math import floor
from typing import Optional
from typing_extensions import Self

from pydantic import BaseModel
from pydantic import model_validator


class Pokemon(BaseModel):
    # -- FIXED DATA
    name: str
    level: int
    gender: str

    # -- BATTLE STATE DATA
    fainted: bool = False
    has_been_revealed: bool = False
    current_hp_percentage: Optional[int] = None

    # -- TURN DATA
    start_turn_hp_percentage: Optional[int] = None
    end_turn_hp_percentage: Optional[int] = None
    start_turn_hp_number: Optional[int] = None
    end_turn_hp_number: Optional[int] = None
    total_hp_number: Optional[int] = None

    # -- MODEL VALIDATORS TO MAKE SURE EVERYTHING IS UPDATED PROPERLY
    @model_validator(mode="after")
    def validate_end_turn_hp_percentage(self) -> Self:
        if not self.has_been_revealed:
            self.end_turn_hp_percentage = 100
            self.has_been_revealed = True
            return self

        if self.end_turn_hp_percentage is not None:
            return self

        if self.end_turn_hp_number is None:
            raise ValueError("HP Number is null, HP Percentage must be not null")
        else:
            if self.total_hp_number is None or self.total_hp_number <= 0:
                raise ValueError(
                    "HP Number is not null, Total HP Number must be positive"
                )

            self.end_turn_hp_percentage = floor(
                self.end_turn_hp_number / self.total_hp_number * 100
            )
        return self

    @model_validator(mode="after")
    def validate_current_hp_percentage(self) -> Self:
        self.current_hp_percentage = self.end_turn_hp_percentage
        return self
