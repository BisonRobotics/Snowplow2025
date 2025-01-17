from waypoint.waypoint import Waypoint

from geometry_msgs.msg import Point, Polygon
from custom_msgs.srv import WaypointServ

import rclpy
from rclpy.node import Node

import json

class WaypointService(Node):

    def __init__(self):
        super().__init__('waypoint_service')

        with open('src/waypoint/waypoint/waypoints.json') as json_file:
            data = json.load(json_file)

        self.obstacle_sub = self.create_subscription(
            Polygon,
            '/obstacle_locations',
            self.obstacle_callback,
            10
        )
        self.got_obstacles: bool = False

        self.waypoints: list[Waypoint] = [Waypoint(point["x"], point["y"]) for point in data]

        self.srv = self.create_service(WaypointServ, '/waypoint', self.waypoint_callback)

    def obstacle_callback(self, msg: Polygon):
        """Moves the waypoints if an obstacle is within the range"""
        for point in msg.points:
            for waypoint in self.waypoints:
                if waypoint.within_range(point.x, point.y, 0.75):
                    # naively moves it away 1 meter from the garage, might be a problem
                    waypoint.y += 1
                    break

        # makes it so it runs once
        self.destroy_subscription(self.obstacle_sub)
        self.got_obstacles = True

    def waypoint_callback(self, request, response: Point):
        if not self.got_obstacles:
            self.get_logger().info('/obstacle_locations subscription stream is empty')
            return

        self.get_logger().info('Incoming request\na: %d b: %d' % (request.position.center.x, request.position.center.y))

        point = request.position.center

        # Check if the waypoints are within range
        if self.waypoints[0].within_range(point.x, point.y):

            # Get rid of visited waypoint
            self.waypoints.pop(0)

        # Create the response
        response.x = self.waypoints[0].x
        response.y = self.waypoints[0].y
        response.z = 0

        return response


def main(args=None):
    rclpy.init(args=args)

    waypoint_service = WaypointService()

    rclpy.spin(waypoint_service)

    rclpy.shutdown()