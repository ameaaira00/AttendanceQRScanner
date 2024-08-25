from enum import Enum


class EventType(Enum):
    HEADS_MONTHLY_MEETING = "Heads Monthly Meeting"
    MONTHLY_YOUTH_FORMATION = "Monthly Youth Formation"
    YOUTH_ASSEMBLY = "Youth Assembly"
    GENERAL_SADP_PYM_EVENTS = "General SADP PYM Events"

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]
