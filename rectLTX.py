#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Marco Benzi <marco.benzi@alumnos.usm.cl>
# @Date:   2015-06-08 17:35:52
# @Last Modified 2015-06-08
# @Last Modified time: 2015-06-08 23:54:14


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

def getCutoffFrequency(a,b,er,m,n):
	"""
	Returns the cutoff frequency for a given rectangular waveguide.

	This assumes that a > b.

	Parameters:

	- `a` : Width
	- `b` : Height
	- `er`: Relative permittivity
	- `m` : M parameter
	- `n` : N parameter
	"""
	return (c/(2*math.sqrt(er)))*math.sqrt((m/a)**2 + (n/b)**2)

def getWaveNumber2(omega,ur,er):
	"""
	Returns the wavenumber for an specific dielectric in [m^-1].

	Parameters:

	- `omega` : Angular speed
	- `ur` : Relative permeability
	- `er` : Relative permittivity
	"""
	return omega*math.sqrt(ur*u0*er*e0)

def getWaveNumber(f,er):
	"""
	Returns the wavenumber for an specific dielectric in [m^-1].

	Parameters:

	- `f` : Operating frequency
	- `er` : Relative permittivity
	"""
	return 2*math.pi*f*math.sqrt(er)/c

def getPhaseConstant(k,a,b,m,n):
	"""
	Returns the phase constant (beta) of a medium. 

	Parameters:

	- `k` : Wavenumber
	- `a` : Width
	- `b` : Height
	- `er`: Relative permittivity
	- `m` : M parameter
	- `n` : N parameter
	"""
	return math.sqrt(k**2 - (m*math.pi/a)**2 - (n*math.pi/b)**2)

def getDielectricLoss2(k,tanD,beta):
	"""
	Returns the dielectric loss per meter.

	Parameters:

	- `k` : Wavenumber
	- `tanD` : tan \delta
	- `beta` : phase constant
	"""
	return ((k**2)*tanD)/(2*beta)

def getDielectricLoss(f,tanD,a,b,er,m,n):
	"""
	Returns the dielectric loss (alpha_d) in [Np/m].

	Parameters:

	- `f` : Operating frequency
	- `tanD` : tan \delta
	- `a` : Width
	- `b` : Height
	- `er`: Relative permittivity
	- `m` : M parameter
	- `n` : N parameter
	"""
	k = getWaveNumber(f,er)
	beta = getPhaseConstant(k,a,b,m,n)
	return getDielectricLoss2(k,tanD,beta)

def getDielectricLossdB(f,tanD,a,b,er,m,n):
	"""
	Returns the dielectric loss (alpha_d) in [dB/m].

	Parameters:

	- `f` : Operating frequency
	- `tanD` : tan \delta
	- `a` : Width
	- `b` : Height
	- `er`: Relative permittivity
	- `m` : M parameter
	- `n` : N parameter
	"""
	np = getDielectricLoss(f,tanD,a,b,er,m,n)
	return np / 0.11512925465

def getSurfaceResistivity(omega,ur,sigma):
	"""
	Returns the surface resistivity in [Ohm]

	Parameters:

	- `omega` : Operating angular speed
	- `ur` : Relative permeability
	- `sigma` :  Conductivity of material
	"""
	return math.sqrt((omega*ur*u0)/(2*sigma))

def getConductionLossTE10(Rs,beta,k,a,b,ur,er):
	"""
	Returns the conduction loss (alpha_c) in [Np/m] for TE10.

	Parameters:

	- `Rs` : Surface resistivity
	- `beta` : Phase constant
	- `k` : Wavenumber
	- `a` : Width
	- `b` : Height
	- `ur` : Relative permeability
	- `er`: Relative permittivity
	"""
	n = math.sqrt((ur*u0)/(er*e0))
	return Rs*(2*b*math.pi**2 + a**3 * k**2)/(a**3 * b * beta * k * n)

def getCharacteristicWaveImpedance(ur,er,fc,f):
	"""
	Returns the characteristic wave impedance.

	Parameters:

	- `ur` : Relative permeability
	- `er`: Relative permittivity
	- `fc`: Cutoff frequency
	- `f` : Operating frecuency
	"""
	n = math.sqrt((ur*u0)/(er*e0))
	return n/math.sqrt(1 - (fc/f)**2)

def getVSWR(RC):
	"""
	Returns the Voltage Standing Wave Ratio (VSWR)

	Parameters:
	- `RC` : Reflection coefficient
	"""
	return (1+math.fabs(RC))/(1-math.fabs(RC))
