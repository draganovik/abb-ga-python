import json
import time
from pyquaternion import Quaternion

import abb
from ga import *


def init_robots(config: json):
    rob_dict = {}

    for robot in config["robots"]:
        name = robot["name"]
        ip = robot["ip"]
        port = robot["port"]
        toolData = robot["tool_data"]
        wobj = robot["wobj"]

        newRobot = abb.Robot(
            ip=ip,
            port_motion=port,
            port_logger=port + 1
        )

        newRobot.set_tool(toolData)
        newRobot.set_workobject(wobj)
        newRobot.set_speed([150,75,75,75])

        rob_dict[name] = newRobot

    return rob_dict

def convert_2d_to_3d(list_2d):
    list_3d = []
    for point_array in list_2d:
        list_3d.append([])
        for point in point_array:
            list_3d[-1].append([point[0], point[1], 0])
    return list_3d

def create_targets(xy_list):
    xyz_list = convert_2d_to_3d(xy_list)

    quat = Quaternion(axis=[0, 1, 0], degrees=180)

    quat_list = []
    for rob in xyz_list:
        quat_list.append([])
        for _ in rob:
            quat_list[-1].append(quat.q)

    robo1_target = [[xyz, q] for xyz, q in zip(xyz_list[0], quat_list[0])]
    robo2_target = [[xyz, q] for xyz, q in zip(xyz_list[1], quat_list[1])]
    return [robo1_target, robo2_target]

def check_targets(target_list, robot_list : list[abb.Robot]):
    invalid_targets = []
    quat = Quaternion(axis=[0, 1, 0], degrees=180)
    quat_list = []
    for _ in target_list:
        quat_list.append(quat.q)

    pose_list = [[[target[0], target[1], 0], q] for target, q in zip(target_list, quat_list)]

    for index, pose in enumerate(pose_list):
        for robot in robot_list:
            if robot_list[robot].check_reachibility(pose) == False:
                invalid_targets.append(index)

    if len(invalid_targets) > 0 :
        print("There are targets that can't be reached (they will be skipped):")
        invalid_values = list(target_list[index] for index in invalid_targets)
        print(invalid_values, '\n')

    for chrom in POPULATION:
        for invalid_target in invalid_targets:
            TARGET_LIST.remove(invalid_target)
            chrom = [target for index, target in enumerate(chrom) if target != invalid_target or index < Config.n_robots -1]
            for index, value in enumerate(chrom):
                if index > Config.n_robots -1:
                    break
                if value > len(chrom) - Config.n_robots :
                    chrom[index] = value - 1

def main():
    file = open("config.json")
    config_json = json.load(file)
    robots = init_robots(config_json)

    #TARGET_LIST[0] = (296,296)
    check_targets(TARGET_LIST,robots)

    xy_list = get_best_solution()
    print(xy_list)
    target_list = create_targets(xy_list)

    robots_init_target = dict()
    for robot in robots:
        robots_init_target[robot] = robots[robot].get_cartesian()

    r1 = 0
    r2 = 0

    while (r1 < len(target_list[0]) or r2 < len(target_list[1])):
        for robot in robots:
            if r1 < len(target_list[0]) and robot == "ROB1":
                robots[robot].set_cartesian(target_list[0][r1])
                r1 += 1
            elif r2 < len(target_list[1]):
                robots[robot].set_cartesian(target_list[1][r2])
                r2 += 1
        time.sleep(2)

    for robot in robots:
        robots[robot].set_cartesian(robots_init_target[robot])

if __name__ == "__main__":
    main()
