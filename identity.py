#!/usr/bin/python


import uuid
import logging

logging.root.setLevel(logging.INFO)
class Identification():
	
	def __init__(self,ip):
		self.ip=ip
		self.uid=uuid.uuid1()
		logging.info("Identity created: UUID ={0}".format(self.uid))


