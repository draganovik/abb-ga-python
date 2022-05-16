import json
import time

from pyquaternion import Quaternion

import abb


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

        rob_dict[name] = newRobot

    return rob_dict


def main():
    file = open("config.json")
    config_json = json.load(file)
    robots = init_robots(config_json)

    xyz = [500, 0, 350]
    quat = Quaternion(axis=[0, 1, 0], degrees=180)
    target = [xyz, quat.q]

    xyz_list = [[500, i * 50, 350] for i in range(5)]
    quat_list =[quat.q for i in range(5)]

    target_list = [[xyz, q] for xyz, q in zip(xyz_list, quat_list)]

    for target in target_list:
        for robot in robots:
            print(target)
            robots[robot].set_cartesian(target)
        time.sleep(0.5)




if __name__ == "__main__":
    main()
