#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import with_statement, print_function
import sys, os
import tempfile
import warnings
from numpy import arange, array
from pkg_resources import resource_filename
import fitsio
from fitsio import FITS, FITSHDR
#from ._fitsio_wrap import cfitsio_use_standard_strings

import unittest
from math import floor, ceil
from typing import AnyStr
#from astropy.io import fits
import numpy as np
import gzip
import shutil 
import self
#from self import compare_array




'''
hdul = fits.open('CALIFAIC0159.V500.rscube.fits')

print(hdul.info())


data = hdul[0].data
hdul.close()

print(data.shape) #1877,73,78
print(data[600,30,30])

image = data [500,:,:]

fits.write('compr.fits', image, compress='gzip', qlevel=None)
'''

#######################################################################################################################
#######################################################################################################################



filename='./CALIFAIC0159.V500.rscube.fits' #FLOAT
data = fitsio.read(filename)

filename2='./M45_E_B_002_60s.fit'#INT
data2 = fitsio.read(filename2)

filename3='./L5-ELAIS-N1-HerMES_jk_bolo1_SMAP250_DR2.fits'#FLOAT
data3 = fitsio.read(filename3)

filename4='./WISE_0127p348_ac51-w2-int-3.fits' #FLOAT
data4 = fitsio.read(filename4)

filename5='./VIMOS_ADP.2019-10-22T15_31_16.491.fits' #INT
data5 = fitsio.read(filename5)

filename6='./GAIALMCDensFits4k.fits' #FLOAT
data6 = fitsio.read(filename6)

filename7='./DESI_BASSd7032.0084.fits' #INT
data7 = fitsio.read(filename7)

filename8='./M45_NO_V_002_60s.fit' #INT
data8 = fitsio.read(filename8)

filename9='./M45_SO_B_002_60s.fit' #INT
data9 = fitsio.read(filename9)

filename10='./CH_PR300024_TG000101_TU2020-03-09T14-50-33_SCI_RAW_Imagette_V0101.fits' #INT
data10 = fitsio.read(filename10)

#fits=fitsio.FITS('CALIFAIC0159.V500.rscube.fits')
#print(fits)
#cube=fits[0].read()
#image=fits[0][500,:,:] #1877,73,78


fitsio.write('CAL_g.fits', data, compress='gzip', qlevel=None)
fitsio.write('CAL_r.fits', data, compress='rice', qlevel=16)
fitsio.write('CAL_h.fits', data, compress='hcompress', qlevel=16)

fitsio.write('COU_E_g.fits', data2, compress='gzip', qlevel=None)
fitsio.write('COU_E_r.fits', data2, compress='rice', qlevel=None)
fitsio.write('COU_E_h.fits', data2, compress='hcompress', qlevel=None)

fitsio.write('HER_g.fits', data3, compress='gzip', qlevel=None)
fitsio.write('HER_r.fits', data3, compress='rice', qlevel=16)
fitsio.write('HER_h.fits', data3, compress='hcompress', qlevel=16)

fitsio.write('WIS_g.fits', data4, compress='gzip', qlevel=None)
fitsio.write('WIS_r.fits', data4, compress='rice', qlevel=16)
fitsio.write('WIS_h.fits', data4, compress='hcompress', qlevel=16)

fitsio.write('VIM_g.fits', data5, compress='gzip', qlevel=None)
fitsio.write('VIM_r.fits', data5, compress='rice', qlevel=16)
fitsio.write('VIM_h.fits', data5, compress='hcompress', qlevel=16)

fitsio.write('GAI_g.fits', data6, compress='gzip', qlevel=None)
fitsio.write('GAI_r.fits', data6, compress='rice', qlevel=16)
fitsio.write('GAI_h.fits', data6, compress='hcompress', qlevel=16)

fitsio.write('DES_g.fits', data7, compress='gzip', qlevel=None)
fitsio.write('DES_r.fits', data7, compress='rice', qlevel=16)
fitsio.write('DES_h.fits', data7, compress='hcompress', qlevel=16)

fitsio.write('COU_NO_g.fits', data8, compress='gzip', qlevel=None)
fitsio.write('COU_NO_r.fits', data8, compress='rice', qlevel=16)
fitsio.write('COU_NO_h.fits', data8, compress='hcompress', qlevel=16)

fitsio.write('COU_SO_g.fits', data9, compress='gzip', qlevel=None)
fitsio.write('COU_SO_r.fits', data9, compress='rice', qlevel=16)
fitsio.write('COU_SO_h.fits', data9, compress='hcompress', qlevel=16)

fitsio.write('CHE_g.fits', data10, compress='gzip', qlevel=None)
fitsio.write('CHE_r.fits', data10, compress='rice', qlevel=16)
fitsio.write('CHE_h.fits', data10, compress='hcompress', qlevel=16)


#######################################################################################################################
#######################################################################################################################		
'''

nrows=30
ncols=100
tile_dims=[5,10]
compress='rice'
fname=tempfile.mktemp(prefix='fitsio-ImageWrite-',suffix='.fits.fz')
dtypes = ['u1','i1','u2','i2','u4','i4','f4','f8']

try:
	with fitsio.FITS(fname,'rw',clobber=True) as fits:
		# note i8 not supported for compressed!

		for dtype in dtypes:
			if dtype[0] == 'f':
				data = np.random.normal(size=nrows*ncols).reshape(nrows,ncols).astype(dtype)
			else:
				data = np.arange(nrows*ncols,dtype=dtype).reshape(nrows,ncols)

			fits.write_image(data, compress=compress, qlevel=16)
			rdata = fits[-1].read()

			if dtype[0] == 'f':
				self.compare_array_abstol(
					data,
					rdata,
					0.2,
					"%s compressed images ('%s')" % (compress,dtype),
					)
			else:
				# for integers we have chosen a wide range of values, so
				# there will be no quantization and we expect no information
				# loss
				self.compare_array(data, rdata,
				"%s compressed images ('%s')" % (compress,dtype))
				#zero=0

	with fitsio.FITS(fname) as fits:
		for ii in xrange(len(dtypes)):
			i=ii+1
			self.assertEqual(fits[i].is_compressed(), True, "is compressed")

finally:
	if os.path.exists(fname):
		os.remove(fname)
		
		
'''		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		

       
