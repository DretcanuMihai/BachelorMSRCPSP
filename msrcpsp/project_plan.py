from msrcpsp.project_context import DetailedProjectContext


class BasicProjectPlan:
    def __init__(self):
        self.activities_start_times: list[int] = []  # the i-th element of the list represents the start time of the
        # i-th activity
        self.assignments: list[dict[int, set[int]]] = []  # the i-th element of the list
        # represents the resource allocation for the activity i. the allocation is represented as a dictionary
        # the keys are the skills, and the values are the sets of resources allocated for that skill


class DetailedProjectPlanActivity:
    def __init__(self):
        self.start_time: int = 0
        self.duration: int = 0
        self.end_time: int = 0
        self.resources_assigned_for_skill: dict[int, set[int]] = {}

    def __str__(self):
        result = ""
        result += "\tStart Time : " + str(self.start_time) + "\n"
        result += "\tDuration : " + str(self.duration) + "\n"
        result += "\tEnd Time : " + str(self.end_time) + "\n"
        result += "\tAssignments\n"
        for skill in self.resources_assigned_for_skill.keys():
            result += "\t\tSkill " + str(skill) + " - "
            for resource in self.resources_assigned_for_skill[skill]:
                result += "Resource " + str(resource) + " , "
            if len(self.resources_assigned_for_skill[skill]) > 0:
                result = result[0:-2]
            result += "\n"
        return result


class DetailedProjectPlanResource:
    def __init__(self):
        self.skill_used_in_activity: dict[int, int] = dict()  # the key is the activity, the value is the skill used

    def __str__(self):
        result = ""
        for activity in self.skill_used_in_activity.keys():
            result += "\tActivity " + str(activity) + " - Skill " + str(self.skill_used_in_activity[activity]) + "\n"
        return result


class DetailedProjectPlan:
    def __init__(self):
        self.activities: list[DetailedProjectPlanActivity] = []
        self.resources: list[DetailedProjectPlanResource] = []

    def __str__(self):
        result = "Activities:\n"
        for index, activity in enumerate(self.activities):
            result += "Activity " + str(index) + "\n"
            result += str(activity)
        result += "\nResources:\n"
        for index, resource in enumerate(self.resources):
            result += "Resource " + str(index) + "\n"
            result += str(resource)
        return result


def transform_basic_plan_to_detailed_plan(basic_plan: BasicProjectPlan, project_context: DetailedProjectContext) \
        -> DetailedProjectPlan:
    plan = DetailedProjectPlan()

    nr_activities = project_context.nr_activities
    nr_resources = project_context.nr_resources

    for index in range(nr_resources):
        plan.resources.append(DetailedProjectPlanResource())

    for index in range(nr_activities):
        activity = DetailedProjectPlanActivity()
        activity.start_time = basic_plan.activities_start_times[index]
        activity.duration = project_context.activities[index].duration
        activity.end_time = activity.start_time + activity.duration
        activity.resources_assigned_for_skill = basic_plan.assignments[index]
        plan.activities.append(activity)

        for skill in activity.resources_assigned_for_skill.keys():
            for resource in activity.resources_assigned_for_skill[skill]:
                plan.resources[resource].skill_used_in_activity[index] = skill

    return plan
