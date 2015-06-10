# -*- coding: utf-8 -*-
# @Author: Marco Benzi <marco.benzi@alumnos.usm.cl>
# @Date:   2015-06-07 19:44:12
# @Last Modified 2015-06-09
# @Last Modified time: 2015-06-09 16:07:05


# ==========================================================================
# This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ==========================================================================


import math

"""
Speed of light constant
"""
c = 3E8
"""
Vacuum permittivity
"""
e0 = 8.8541E-12
"""
Vacuum permeability
"""
u0 = 4E-7*math.pi

def getEffectivePermitivity(WHratio, er):
	"""
	Returns the effective permitivity for a given W/H ratio.

	This function assumes that the thickenss of conductors is insignificant.

	Parameters:

	- `WHratio` : W/H ratio.
	- `er` : Relative permitivity of the dielectric.
	"""
	if WHratio <= 1:
		return (er + 1)/2 + ((1 + 12/WHratio)**(-0.5) + 0.04*(1-WHratio)**2)*(er -1)/2
	else:
		return (er + 1)/2 + ((1 + 12/WHratio)**(-0.5))*(er -1)/2

def getAuxVarA(Zo,er):
	"""
	Returns the auxiliary variable 
		A = (Zo)/60 * math.sqrt((er + 1)/2) + (er-1)/(er+1)*(0.23+0.11/er)

	This function assumes that the thickenss of conductors is insignificant.

	Parameters:

	- `Zo` : Real impedance of the line.
	- `er` : Relative permitivity of the dielectric.
	"""
	return (Zo)/60 * math.sqrt((er + 1)/2) + (er-1)/(er+1)*(0.23+0.11/er)

def getAuxVarB(Zo,er):
	"""
	Returns the auxiliary variable 
		B = (377*math.pi)/(2*Zo*math.sqrt(er))

	This function assumes that the thickenss of conductors is insignificant.

	Parameters:

	- `Zo` : Real impedance of the line.
	- `er` : Relative permitivity of the dielectric.
	"""
	return (377*math.pi)/(2*Zo*math.sqrt(er))

def getWHRatioA(Zo,er):
	"""
	Returns the W/H ratio for W/H < 2. If the result is > 2, then other method
	should be used.

	This function assumes that the thickenss of conductors is insignificant.

	Parameters:

	- `Zo` : Real impedance of the line.
	- `er` : Relative permitivity of the dielectric.
	"""
	A = getAuxVarA(Zo,er)
	return (8*math.e**A)/(math.e**(2*A) - 2)

def getWHRatioB(Zo,er):
	"""
	Returns the W/H ratio for W/H > 2. If the result is < 2, then other method
	should be used.

	This function assumes that the thickenss of conductors is insignificant.

	Parameters:

	- `Zo` : Real impedance of the line.
	- `er` : Relative permitivity of the dielectric.
	"""
	B = getAuxVarB(Zo,er)
	return (2/math.pi)*(B-1 - math.log(2*B - 1) + (er - 1)*(math.log(B-1) + 0.39 - 0.61/er)/(2*er))

def getCharacteristicImpedance(WHratio, ef):
	"""
	Returns the characteristic impedance of the medium, based on the effective
	permitivity and W/H ratio.

	This function assumes that the thickenss of conductors is insignificant.

	Parameters:

	- `WHratio` : W/H ratio.
	- `ef` : Effective permitivity of the dielectric.
	"""
	if WHratio <= 1:
		return (60/math.sqrt(ef))*math.log(8/WHratio + WHratio/4)
	else:
		return (120*math.pi/math.sqrt(ef))/(WHratio + 1.393 + 0.667*math.log(WHratio +1.444))

def getWHRatio(Zo,er):
	"""
	Returns the W/H ratio, after trying with the two possible set of solutions, 
	for	when W/H < 2 or else. When no solution, returns zero.

	This function assumes that the thickenss of conductors is insignificant.

	Parameters:

	- `Zo` : Real impedance of the line.
	- `er` : Relative permitivity of the dielectric.
	"""
	efa = er
	efb = er
	Zoa = Zo
	Zob = Zo
	while 1:
		rA = getWHRatioA(Zoa,efa)
		rB = getWHRatioB(Zob,efb)
		if rA < 2:
			return rA
		if rB > 2:
			return rB
		Zoa = math.sqrt(efa)*Zoa
		Zob = math.sqrt(efb)*Zob
def getCorrectedWidth(W,H,t):
	"""
	For significant conductor thickness, this returns the corrected width.

	Paramenters:

	- `W` : Width
	- `H` : Height
	- `t` : Conductor thickness
	"""
	if t < H and t < W/2:
		if W/H <= math.pi/2:
			return W + (1 + math.log(2*H/t))*(t/math.pi)
		else:
			return W + (1 + math.log(4*math.pi*H/t))*(t/math.pi)
	else:
		print "The conductor is too thick!!"

def getConductorLoss(W,H,t,sigma,f,Zo):
	"""
	Returns the conductor loss in [Np/m].

	Parameters:

	- `W` : Width
	- `H` : Height
	- `t` : Conductor thickness
	- `sigma` : Conductance of medium
	- `f` : Operating frequency
	- `Zo` : Characteristic impedance
	"""
	We = getCorrectedWidth(W,H,t)
	P = 1 - (We/4/H)**2
	Rs = math.sqrt((math.pi*f*u0)/sigma)
	Q = 1 + H/We + (math.log((2*H)/t)-t/W)*H/(We*math.pi)

	if W/H <= 1/(2*math.pi):
		return (1 + H/We + (math.log(4*pi*W/t) + t/W)*H/(math.pi*We))*(8.68*Rs*P)/(2*pi*Zo*H)
	elif W/H <= 2:
		return (8.68*Rs*P*Q)/(2*math.pi*Zo*H)
	else:
		return ((8.68*Rs*Q)/(Zo*H))*(We/H + (We/math.pi/H)/(We/2/H)+0.94)*((H/We + 2*math.log(We/2/H + 0.94)/math.pi)**(-2))

def getDielectricLoss(er,ef,tanD,f):
	"""
	Returns the dielectric loss in [dB/cm].

	Paramenters:

	- `er` : Relative permitivity of the dielectric
	- `ef` : Effective permitivity
	- `tanD` : tan \delta
	- `f` : Operating frequency
	"""
	lam = c/math.sqrt(ef)/f
	return 27.3*(er*(ef-1)*tanD)/(lam*math.sqrt(er)*(er-1)) 		