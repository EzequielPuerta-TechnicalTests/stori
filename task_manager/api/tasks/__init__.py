import api.tasks.resources as resources
from flask_restful import Api


def initialize_routes(api: Api) -> None:
    api.add_resource(
        resources.TaskListResource,
        "/api/tasks/",
        endpoint="task_resources",
    )
    api.add_resource(
        resources.TaskResource,
        "/api/tasks/<task_id>",
        endpoint="task_resource",
    )
    api.add_resource(
        resources.SuccessfulTaskStateResource,
        "/api/tasks/<task_id>/success",
        endpoint="successful_task_state_resource",
    )
    api.add_resource(
        resources.FailedTaskStateResource,
        "/api/tasks/<task_id>/failed",
        endpoint="failed_task_state_resource",
    )
