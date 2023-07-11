ORDER_REPRESENTATION = "order_representation"
PRIORITY_REPRESENTATION = "priority_representation"


class GAProjectPlan:
    def __init__(self):
        self.activities: list[int] = []  # depending on the interpretation:
        # 1. the order in which the activities are to be executed. the i-th activity in this list is the i-th to be
        # executed. activities are represented by their ids
        # 2. the order in which the activities are to be prioritized. the i-th activity in this list is the i-th most
        # important. activities are represented by their ids
        self.assignments: list[dict[int, set[int]]] = []  # the i-th element of the list
        # represents the resource allocation for the activity i. the allocation is represented as a dictionary
        # the keys are the skills, and the values are the sets of resources allocated for that skill
