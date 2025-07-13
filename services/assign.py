import json

def is_resource_matching(area, truck):
    return all((key in truck["AvailableResources"]) for key in area["RequiredResources"])

def is_fulfill(area, truck):
    required = area["RequiredResources"]
    available = truck["AvailableResources"]
    diff = {key:available.get(key, 0) - required[key] for key in required}
    return all(available.get(key, 0) >= required[key] for key in required)

def is_travel_time_include(area, truck):
    time_constaint = area["TimeConstaint"]
    travel_times = truck["TravelTimeToArea"]
    return False if area["AreaID"] not in travel_times else True

def is_time_achieve(area, truck):
    if not is_travel_time_include(area, truck):
        return False
    time_constaint = area["TimeConstaint"]
    travel_times = truck["TravelTimeToArea"]
    # if area["AreaID"] not in travel_times:
    #     return False
    resource_delivered = travel_times[area["AreaID"]]
    return time_constaint >= resource_delivered

def assign_check(area, truck):
    resource_matching = is_resource_matching(area, truck)
    fulfill = is_fulfill(area, truck)
    travel_time_include = is_travel_time_include(area, truck)
    time_achieve = is_time_achieve(area, truck)
    return {
        # "AreaID": area["AreaID"],
        # "TruckID": truck["TruckID"],
        "is_resource_matching": resource_matching,
        "is_fulfill": fulfill,
        "is_travel_time_include": travel_time_include,
        "is_time_achieve": time_achieve,
        # "is_truck_available": True,
        "is_urgent": True,
    }
    
def print_json(obj):
    print(json.dumps(obj,indent=4))

# def find_non_assign(inputs,outputs):
#     assigned_areas = {output["AreaID"] for output in outputs}
#     return [area for area in inputs if area["AreaID"] not in assigned_areas]

def find_non_assign(assign_log):
    non_assigns = []
    assigns = [x["AreaID"] for x in assign_log if x["is_assign"]]
    print(assigns)
    for log in [x for x in assign_log if x["AreaID"] not in assigns]:
        is_duplicate =False
        current = {
                "AreaID": log["AreaID"],
                "assign_flag": {x: [log["assign_flag"][x]] for x in log["assign_flag"].keys()}
            }
        if len(non_assigns) == 0:
            non_assigns.append(current)
            continue
        for non_assign in non_assigns:
            if current["AreaID"] == non_assign["AreaID"]:
                # print(log["AreaID"])
                for x in non_assign["assign_flag"].keys():
                    non_assign["assign_flag"][x] = non_assign["assign_flag"][x] + current["assign_flag"][x]
                    is_duplicate = True
                break

        if not is_duplicate:
            non_assigns.append(current)

    # sumary assign flag
    for area in non_assigns:
        for key in area["assign_flag"]:
            if key == 'is_urgent':
                area["assign_flag"][key] = all(area["assign_flag"][key])
            else:
                area["assign_flag"][key] = any(area["assign_flag"][key])

    # non assign reason
    for area in non_assigns:
        area["reason"] = ""
        for key in area["assign_flag"]:
            if not area["assign_flag"][key]:
                match key:
                    case "is_resource_matching":
                        area["reason"] += "Truck resource doesn't match all area requirement."
                        break
                    case "is_fulfill":
                        area["reason"] += "Truck resource matching but not fulfill."
                        break
                    case "is_travel_time_include":
                        area["reason"] += "No truck that include travel time in this area."
                        break
                    case "is_time_achieve":
                        area["reason"] += "Truck can't acheive time required."
                        break
                    case "is_urgent":
                        area["reason"] += "No truck available because truck is support another area that more urgenthly."
                        break
                    case default:
                        area["reason"] += "No truck left for this area"
                        break

        if area["reason"] == "":
            area["reason"] = "No truck left for this area"
            
    return non_assigns

def assign_resources(affect_area, resource_truck):
    non_assigns = []
    assign_logs = []
    sample_spaces = []
    assigns = []
    for area in affect_area:
        for truck in resource_truck:
            assign_flag = assign_check(area,truck)
            # print_json(assign_flag)
            current = {
                    "AreaID": area["AreaID"],
                    "TruckID": truck["TruckID"],
                    "ResourcesDelivered": area["RequiredResources"],
                    "UrgencyLevel": area["UrgencyLevel"],
                    "is_assign":False,
                    "assign_flag":assign_flag
                }

            if all([value for value in assign_flag.values()]):
                current["is_assign"] = True
                # assigns = list(filter(lambda x: x["is_assign"] == True, sample_spaces))
                for assign in assigns:
                    if current["AreaID"] == assign["AreaID"]:
                        current["is_assign"] = False
                    if current["TruckID"] == assign["TruckID"]:
                        if current["UrgencyLevel"] > assign["UrgencyLevel"]:
                            assign["is_assign"] = False
                            assign["assign_flag"]["is_urgent"] = False
                        else:
                            current["is_assign"] = False 
                            current["assign_flag"]["is_urgent"] = False
            else:
                current["is_assign"] = False

            sample_spaces.append(current)
            assigns = list(filter(lambda x: x["is_assign"] == True, sample_spaces))

    # non_assigns = find_non_assign(affect_area,assigns)
    assign_logs = sample_spaces
    non_assigns = find_non_assign(assign_logs)

    return assigns, non_assigns, assign_logs