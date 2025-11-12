from dataclasses import dataclass, field
from datetime import date
from typing import List, Union

@dataclass
class CardapioDia:
    id: int
    data: date
    acompanhamento: List[int]
    prato_principal: List[int]
    guarnicao: List[int]
    sobremesa: List[int]
    sem_atendimento: bool
    quantidade_almoco: int
    quantidade_jantar: int

    def stringToList(string):
        m