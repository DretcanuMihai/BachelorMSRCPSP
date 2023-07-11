# activities, resources and skill types are indexed from 0

class BasicProjectContext:
    def __init__(self):
        self.nr_activities = 0  # integer representing the number of activities
        self.nr_resources = 0  # integer representing the number of resources
        self.nr_skill_types = 0  # integer representing the number of skill types
        self.deadline = 0  # integer representing a given deadline for the project (a maximum duration)
        self.activities_durations: list[int] = []  # list of integers where the i-th element is the duration of the
        # i-th activity
        self.activities_successors: list[set[int]] = []  # list of sets - the i-th element represents the successors of
        # the i-th activity. the set contains the indices of the successor activities
        self.resource_skills: list[set[int]] = []  # list of sets - the i-th element represents the skills of tbe i-th
        # activity the skills are represented as a set that contains the indices of the mastered skills
        self.activities_skills_requirements: list[
            dict[int, int]] = []  # list of dictionaries - the i-th element represents
        # the skill requirements of the i-th activity - the requirements are represented as a map. the keys of the map
        # represent the indices of the needed skill, while the value represents the amount needed


class DetailedProjectActivity:
    def __init__(self):
        self.duration: int = 0  # integer representing the duration for said activity
        self.predecessors: set[int] = set()  # set of integers representing the indices of the predecessor
        # activities
        self.successors: set[int] = set()  # set of integers representing the indices of the successor
        # activities
        self.required_units_of_skill: dict[int, int] = {}  # dictionary where the keys of the dictionary
        # represent the indices of the needed skill, while the value represents the amount needed


class DetailedProjectContext:
    def __init__(self):
        self.nr_activities: int = 0  # integer representing the number of activities
        self.nr_resources: int = 0  # integer representing the number of resources
        self.nr_skill_types: int = 0  # integer representing the number of skill types
        self.deadline: int = 0  # integer representing a given deadline for the project (a maximum duration)
        self.activities: list[
            DetailedProjectActivity] = []  # is a list of Activity entities. the i-th element represents the i-th
        # activity
        self.skills_of_resource: list[set[int]] = []  # list of sets - the i-th element represents the skills of the
        # i-th activity
        # the skills are represented as a set that contains the indices of the mastered skills
        self.resources_mastering_skill: list[set[int]] = []  # list of sets - the i-th element represents the resources
        # that master the i-th skill. the resources are represented as a set that contains the indices of the resources


def transform_basic_project_context_to_detailed_project_context(project_context: BasicProjectContext) \
        -> DetailedProjectContext:
    detailed_project_context = DetailedProjectContext()
    detailed_project_context.nr_activities = project_context.nr_activities
    detailed_project_context.nr_resources = project_context.nr_resources
    detailed_project_context.nr_skill_types = project_context.nr_skill_types
    detailed_project_context.deadline = project_context.deadline

    activities = [DetailedProjectActivity() for _ in range(project_context.nr_activities)]
    for activity_index in range(project_context.nr_activities):
        activities[activity_index].duration = project_context.activities_durations[activity_index]
        activities[activity_index].required_units_of_skill = \
            project_context.activities_skills_requirements[activity_index]
        activities[activity_index].successors = project_context.activities_successors[activity_index]
        for successor_index in activities[activity_index].successors:
            activities[successor_index].predecessors.add(activity_index)
    detailed_project_context.activities = activities

    detailed_project_context.skills_of_resource = project_context.resource_skills

    detailed_project_context.resources_mastering_skill = [set() for _ in range(detailed_project_context.nr_skill_types)]
    for i in range(detailed_project_context.nr_resources):
        for resource_skill in detailed_project_context.skills_of_resource[i]:
            detailed_project_context.resources_mastering_skill[resource_skill].add(i)

    return detailed_project_context
