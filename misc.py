from enum import Enum
# from Main import Page


class IntervalType(Enum):
    ERROR = 0

    LOWER = 2
    NORMAL = 1
    UPPER = 3

    GRADE1 = 4
    GRADE2 = 5
    GRADE3 = 6
    GRADE4 = 7
    GRADE5 = 8
    GRADE6 = 9



class ShowLabelsForDebug:
    def __init__(self):
        self.value = False
        # Page.actual_page.update()

    def set_true(self):
        self.value = True
        # Page.actual_page.update()
        return self

    def toggle(self):
        self.value = not self.value
        print(self.value)
        # Page.actual_page.update()



def m_8_3_function(m_8_1, m_8_2):
    # давл. ПП, мм.рт.ст - расчёт
    if m_8_1 > 21:
        if m_8_2 < 50:
            return 15
        else:
            return 10
    else:
        if m_8_2 < 50:
            return 10
        else:
            return 5
