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
    Category = State()
    File = State()
    PassageNumber = State()
    Word = State()


class VocabularyTraining(StatesGroup):
    Category = State()
    Slices = State()
    Word = State()


class Quiz(StatesGroup):
    Category = State()
    Slices = State()
    Word = State()


class Collection(StatesGroup):
    Title = State()


class CollectionWord(StatesGroup):
    Collection = State()
    Word = State()


class CollectionWordTraining(StatesGroup):
    Collection = State()
    Word = State()

