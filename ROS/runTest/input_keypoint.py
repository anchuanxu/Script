#!/usr/bin/env python
#coding=utf-8

import rospy, sys, termios, tty
import yaml,json

from geometry_msgs.msg import Pose, PoseStamped
from visualization_msgs.msg import Marker, MarkerArray
from move_base_msgs.msg import MoveBaseActionResult





class input_kp():
	"""docstring for input_kp"""
	def __init__(self):
		self.total_kp = input('请输入需要标记点的个数:\n')
		# print type(self.total_kp)
		# print self.total_kp
		self.num_kp = 1
		self.kp = []
		self.marker=Marker()
		self.marker.color.r=1.0
		self.marker.color.g=0.0
		self.marker.color.b=0.0
		self.marker.color.a=1.0
		self.marker.ns='input_kp'
		self.marker.scale.x=1
		self.marker.scale.y=0.1
		self.marker.scale.z=0.1
		self.marker.header.frame_id='map'
		self.marker.type=Marker.ARROW
		self.marker.action=Marker.ADD
		self.arraymarker = MarkerArray()
		self.markers_pub = rospy.Publisher('/kp',MarkerArray,queue_size=1)
		self.goal_sub = rospy.Subscriber('/move_base_simple/goal',PoseStamped, self.mark_kpCB)

		
		
		tip = '请在rviz当中使用鼠标点击第 ' + str(self.num_kp) +' 个目标点的位置。'
		print tip
		rospy.spin()

	def mark_kpCB(self, pos):
		if self.num_kp <= self.total_kp:
			kptmp = {"recog": False, "pose": [[pos.pose.position.x,pos.pose.position.y,pos.pose.position.z],[pos.pose.orientation.x,pos.pose.orientation.y,pos.pose.orientation.z,pos.pose.orientation.w]], "play": True, "chat": False}
			
			self.kp.append(kptmp)
			print self.kp
			
			
			print 'added '+str(self.num_kp)+' keypoints'
			self.marker.header.stamp =rospy.Time.now()
			self.marker.pose = pos.pose
			self.marker.id = self.num_kp
			self.arraymarker.markers.append(self.marker)
			self.markers_pub.publish(self.arraymarker)
			if self.num_kp + 1 <= self.total_kp:
				tip = '请在rviz当中使用鼠标点击第' + str(self.num_kp+1) +' 个目标点的位置。'
			else:
				tip = '输入结束'
			print tip
		
		if self.num_kp == self.total_kp:
			with open('kp.json', 'w') as f:
				json.dump(self.kp,f,ensure_ascii=False)
			
			# print '您已完成所有关键点的录入，关键点文件已成功存入运行目录下的kp.json文件，请使用ctrl+c退出程序即可。'
			print '请使用ctrl+c退出程序。'

		self.num_kp+=1

	def goal_resultCB(self, result):
		pass






if __name__ == '__main__':
	rospy.init_node('input_kp_serve')
	try:
		rospy.loginfo('office lady initialized...')
		input_kp()
	except rospy.ROSInterruptException:
		rospy.loginfo('office lady initialize failed, please retry...')