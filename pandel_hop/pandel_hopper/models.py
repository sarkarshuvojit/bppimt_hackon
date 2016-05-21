from __future__ import unicode_literals

from django.db import models
import math, sys
# Create your models here.


class ArpanDaErCode(models.Model):
    n=0
    npow=0
    g=[[-1]*2048]*11
    p=[[-1]*2048]*11
    adj=[[0]*11]*11
    res=[]
    tempres=0
    def compute(self,start,sett):
    	# global g
    	if self.g[start][sett] != -1:
    		return self.g[start][sett]
    	# global n
    	# global npow
    	# global tempres
    	# global adj
    	# global p
    	result=sys.maxint
    	i=0
    	mask=masked=0
    	while i<self.n:
    		mask=(self.npow-1)-(1<<i)
    		masked=sett&mask
    		if masked!=sett:
    			temp=self.adj[start][i]+self.compute(i,masked)
    			if temp<result:
    				result=temp
    				self.p[start][sett]=i
    		i=i+1
    	self.g[start][sett]=result
    	return result

    def getpath(self,start,sett):
    	# global p
    	# global res
    	# global npow
    	if self.p[start][sett]==-1:
    		return;
    	x=self.p[start][sett]
    	mask=(self.npow-1)-(1<<x)
    	masked=sett&mask
    	self.res.append(x)
    	self.getpath(x,masked)

    def solve(self,g1,n1):
    	# global npow
    	# global n
    	# global g
    	# global res
    	# global tempres
    	# global adj
    	self.n=n1
    	self.npow=int(math.pow(2,self.n))
    	self.adj=g1
    	"""for i in adj:
    		tempres=max(tempres,max(i))
    	tempres=tempres+5"""
    	i=0
    	while i<self.n:
    		self.g[i][0]=self.adj[i][0]
    		i=i+1
    	result=self.compute(0,self.npow-2)
        self.res = []
    	self.res.append(0)
    	self.getpath(0,self.npow-2)
    	self.res.append(0)
    	return self.res
