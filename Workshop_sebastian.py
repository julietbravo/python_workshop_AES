# -*- coding: utf-8 -*-
### Sebastian K. Müller, MPI-M, HH


# start with, importing all the modules needed
import subprocess
import numpy   as np #for all kinds of operations
import scipy
import Nio as nio
import matplotlib.pyplot
from   mpl_toolkits.basemap import Basemap, cm
from   matplotlib.pylab     import *
import time
import os        #for various path/file-actions



# I don't use "object oriented programming", but I set Switches:
Switch_plot_ICON_output    = 1

Switch_str                 = 0
Switch_uns                 = 1

Switch_compute_cdo         = 0



# setting the path of the model output:
path_exp              = '/work/mh0925/m300367/icon-aes-summerschool/experiments/'
path_pywo             = '/work/mh0925/m300367/Python_Workshop/'
path_local_exp        = '/home/bas/Python_Workshop/'

name_exp              = 'APE_echam_R2B5_Z83_hidt_skm'
output_suffix         = '_3d_rmb_DOM01_PL_000'
output_suffix         = '_3d_DOM01_ML_000'
output_prefix         = ''
File_Number_str       = '6'




# loading model output and grid properties, using Nio:
ICON_output    = nio.open_file(path_exp+name_exp+'/'+output_prefix+name_exp+output_suffix+File_Number_str+'.nc')


if Switch_str == 1:
	lat       = ICON_output.variables['lat']
	lon       = ICON_output.variables['lon']
	lon_mg,lat_mg  =  meshgrid(lon,lat)
	z         = ICON_output.variables['zg'][0,:,0,0]
	ik         = 21

if Switch_uns == 1:
	lat       = ICON_output.variables['clat'][:]*180./np.pi
	lon       = ICON_output.variables['clon'][:]*180./np.pi
	z         = ICON_output.variables['zg'][:,0]
	ik        = 33
times     = ICON_output.variables['time'][:]



# setting strings referring to the variable intended to plot:
if Switch_plot_ICON_output == 1:
    	Var_str_lst          = ['ta']#'wap',
	Var_2_str            = ['pfull']#,'lev'
	pros                 = ['moll','sinu','hammer','eck4','eqdc','npstere']#,'spaeqd','vandg','cyl','stere','spstere','kav7']
	#working fine: 	['moll','aeqd','sinu','mill','eqdc','cyl','stere','spstere','hammer','eck4','kav7','npstere','spaeqd','vandg']
	#not working: ,'cea','poly','omerc','gnom','lcc','npaeqd','merc','rotpole','geos','nsper','aea','ortho','cass','laea','splaea','aeqd','mill'
	Time_steps           = [4]
        res                  = 'h'
	plotrange_pearl      = np.array( [-1.0,-0.95,-0.9,-0.85,-0.8,-0.75,-0.7,-0.65,-0.6,-0.55,-0.5,-0.45,-0.4,-0.35,-0.3,-0.25,-0.2,-0.15,-0.1,-0.05,0.0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0])



if Switch_compute_cdo == 1:
	cdo_command = 'zonmin'




#The plotting routine:
if Switch_plot_ICON_output == 1:

	for pro in pros:
		if pro == 'npstere':
			m = Basemap(projection=pro,lon_0=10,boundinglat=60.,resolution=res)
		elif pro == 'spstere' or pro == 'spaeqd':
			m = Basemap(projection=pro,lon_0=10,boundinglat=-45.,resolution=res)	
		elif pro == 'stere':
			m = Basemap(width=12000000,height=8000000,resolution=res,projection=pro,lat_ts=50,lat_0=50,lon_0=-107.)	
		elif pro == 'eqdc':
			m  = Basemap(width=12000000,height=9000000,resolution=res,projection=pro,lat_1=45.,lat_2=55,lat_0=50,lon_0=-107.)



		#generating a Basemap projektion object m and setting its properties:
		else:		
			m  = Basemap(projection=pro,lat_0=0.0,lon_0=0.0,llcrnrlon=-180.,llcrnrlat=-90.,urcrnrlon=180.,urcrnrlat=90.,resolution=res)
		

		#going through the variables:
		for Var_str in Var_str_lst:

			#making a directory for saving the plots:
			path   = path_pywo+Var_str+'_Basemap/'
			if not os.path.isdir(path):
				os.makedirs(path)
		
			# load the Variable and set a plotrange:
			Var                  = ICON_output.variables[Var_str]
			Var_2                = ICON_output.variables[Var_2_str[0]]

			if Switch_str == 1:
				plotrange_central_0  = plotrange_pearl*abs((Var[:,ik,:,:])).max()
				plotrange_mintomax   = np.linspace(Var[:,ik,:,:].min(),Var[:,ik,:,:].max(),41)

			if Switch_uns == 1:
				plotrange_central_0  = plotrange_pearl*abs((Var[:,ik,:])).max()
				plotrange_mintomax   = np.linspace(Var[:,ik,:].min(),Var[:,ik,:].max(),41)

			#going through the time steps:
			for it in Time_steps:
				
				plt.title(Var.standard_name +' ['+Var.units+'] and '+Var_2.standard_name +'['+Var_2.units+'], pro='+ pro +', at level = %01.0f' %z[ik] +'m and date = %01.0f' %times[it])

				if Switch_str == 1:

					m.contourf(lon,lat,Var[it,ik,:,:],plotrange_mintomax,cmap=cm.RdBu_r,tri=False,latlon=True)
					plt.colorbar()
					m.contour(lon_mg,lat_mg,Var_2[it,ik,:,:],15,colors='black')

				elif Switch_uns == 1:
					lon_m,lat_m=m(lon[:],lat[:])

					plt.tricontourf(lon_m,lat_m,Var[it,ik,:],plotrange_mintomax,cmap=cm.RdBu_r)
					#m.contourf(lon_mg,lat_mg,Var[it,ik,:],plotrange_central_0,tri=True)
					plt.colorbar()

					plt.tricontour(lon_m,lat_m,Var_2[it,ik,:],15,colors='black')


				m.drawparallels(np.arange(-90.,91.,30.),labels=[1,0,0,0])
				m.drawmeridians(np.arange(-180.,181.,60.),labels=[0,0,0,1])

				m.drawcoastlines(color='purple', linewidth=1.5)

				plt.show()

				if Switch_str == 1:
					plt.savefig(path+Var_str+'_'+pro+'_struct_time=%01.2f' %times[it] +'_height=%01.0f' %(int(z[ik]))+'.png', dpi=600)
				elif Switch_uns == 1:
					plt.savefig(path+Var_str+'_'+pro+'_unstruc_time=%01.2f' %times[it] +'_height=%01.0f' %(int(z[ik]))+'.png', dpi=600)
								
                plt.clf()
				
			#printing a sftp statement for downloading plots:
			print ('   cd '+path+'\n   lmkdir '+path_local_exp+'\n   lcd '+path_local_exp+'\n   lmkdir '+Var_str+'_Basemap\n   lcd '+Var_str+'_Basemap\n   get *')



if Switch_compute_cdo == 1:
	if not os.path.isfile(path_exp+name_exp+'/'+ cdo_command+'_'+name_exp+'_oooo.nc'):
		i_file        = 1
		i_file_str    = '01'
		path_tofile   = path_exp+name_exp+'/'+output_prefix+name_exp+output_suffix+i_file_str+'.nc'
	
		while os.path.isfile(path_tofile):
			subprocess.call('cdo' +' '+ cdo_command +' '+ path_tofile +' '+ path_exp+name_exp+'/'+ cdo_command+'_'+name_exp+'_00'+i_file_str+'.nc',shell=True)
		
			print ('cdoed: '+path_exp+name_exp+'/'+ cdo_command+'_'+output_prefix+name_exp+i_file_str+'.nc')
		
			i_file        = i_file + 1
			if i_file < 10:
				i_file_str = '0'+ str(i_file)
			else:
				i_file_str = str(i_file)
		
			path_tofile   = path_exp+name_exp+'/'+output_prefix+name_exp+output_suffix+i_file_str+'.nc'
		
		subprocess.call('cdo cat' +' '+ path_exp+name_exp+'/'+ cdo_command+'_'+name_exp+'_00*.nc' +' '+ path_exp+name_exp+'/'+ cdo_command+'_'+name_exp+'_oooo.nc', shell=True)
	
		subprocess.call('rm' +' '+ path_exp+name_exp+'/'+ cdo_command+'_'+name_exp+'_00*.nc', shell=True)
	
		print ('cdoed: '+cdo_command+'_'+name_exp+'_'+'*.nc' +' '+ path_exp+name_exp+'/'+ cdo_command+'_'+name_exp+'_oooo.nc')


