from botocove import cove

@cove()
def hello_world(session):
    return "Hello, world!"


@cove()
def describe_account_trails(session):
    client = session.client("cloudtrail")
    return [
        {"Name": trail["Name"], "HomeRegion": trail["HomeRegion"]}
        for trail in client.describe_trails()["trailList"]
        if not trail["IsOrganizationTrail"]
    ]


@cove(regions=["eu-central-1", "eu-west-1"])
def describe_account_trails_in_more_regions(session):
    client = session.client("cloudtrail")
    return [
        {"Name": trail["Name"], "HomeRegion": trail["HomeRegion"]}
        for trail in client.describe_trails()["trailList"]
        if not trail["IsOrganizationTrail"]
    ]


@cove(regions=["eu-central-1", "eu-west-1"])
def get_logging_statuses(session):
    client = session.client("cloudtrail")
    trail_list = [
        trail
        for trail in client.describe_trails()["trailList"]
        if not trail["IsOrganizationTrail"]
    ]

    return [
        {
            "Name": trail["Name"],
            "IsLogging": client.get_trail_status(Name=trail["Name"])["IsLogging"],
        }
        for trail in trail_list
    ]


@cove(regions=["eu-central-1", "eu-west-1"])
def stop_logging(session):
    client = session.client("cloudtrail")
    trail_list = [
        trail
        for trail in client.describe_trails()["trailList"]
        if not trail["IsOrganizationTrail"]
    ]

    for trail in trail_list:
        client.stop_logging(Name=trail["Name"])

    return "Stopped"

# To reset the demo.
@cove(regions=["eu-central-1", "eu-west-1"])
def start_logging(session):
    client = session.client("cloudtrail")
    trail_list = [
        trail
        for trail in client.describe_trails()["trailList"]
        if not trail["IsOrganizationTrail"]
    ]

    for trail in trail_list:
        client.start_logging(Name=trail["Name"])

    return "Started"


# TODO: Set up the pretty printer to run this automatically for botocove results.
# TODO: Hack botocove to do this always in the demo.
def simplify(obj):
    if isinstance(obj, dict) and obj.keys() == {
        "Results",
        "Exceptions",
        "FailedAssumeRole",
    }:
        return {k: [simplify(r) for r in v] for k, v in obj.items()}

    # Too lazy to write out all the keys. Need to write out the required keys
    # explicitly because Python 3.8 doesn't have TypedDict.__required_keys__.
    # TypedDict.__annotations__ erases that info. Botocove should use a thin
    # dataclass instead.
    if isinstance(obj, dict) and {"Id", "RoleName", "RoleSessionName"} <= obj.keys():
        return {
            k: v
            for k, v in obj.items()
            if k in {"Id", "Region", "Result", "ExceptionDetails"}
        }

    return None
