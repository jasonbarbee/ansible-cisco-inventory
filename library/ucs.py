#!/usr/bin/python
# -*- mode: python -*-

from ucsmsdk.ucshandle import UcsHandle

class UCS(object):
    def __init__(self, ucsm_ip="", ucsm_login="", ucsm_pw=""):
        self.handle = UcsHandle(ucsm_ip, ucsm_login,ucsm_pw)
        self.ucsm_ip = ucsm_ip
        self.ucsm_pw = ucsm_pw
        self.ucsm_login = ucsm_login


    def login(self):
        self.handle.login()



    def logout(self):
        self.handle.logout()
