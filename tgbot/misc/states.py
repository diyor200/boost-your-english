from aiogram.fsm.state import  StatesGroup, State


class Registration(StatesGroup):
    Name = State()
    Surname = State()
    Age = State()
    Language = State()
    Address = State()
    Phone = State()

class Subject(StatesGroup):
    Name = State()
    Surname = State()
    Age = State()
    Address = State()
    Phone = State()
    Language = State()
    SubjectChoice = State()
