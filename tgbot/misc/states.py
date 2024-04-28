from aiogram.fsm.state import StatesGroup, State


class NewBook(StatesGroup):
    Name = State()


class NewTest(StatesGroup):
    BookTitle = State()
    TestNumber = State()


class NewPassage(StatesGroup):
    BookTitle = State()
    TestNumber = State()
    PassageNumber = State()


class NewWord(StatesGroup):
    BookTitle = State()
    TestNumber = State()
    PassageNumber = State()
    Word = State()


class VocabularyTraining(StatesGroup):
    BookTitle = State()
    TestNumber = State()
    PassageNumber = State()
    Word = State()


class Quiz(StatesGroup):
    Name = State()
