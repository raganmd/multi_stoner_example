UI_sidebar		= op.UI_sidebar
UI_body			= op.UI_body
Stoner			= op.Stoner
CalibrationData	= op.CalibrationData
display_range	= range( op.Mapping.op( 'container_sidebar/container_display_selection/table2' ).numRows + 1 )
test_media		= op.OutputTexture.op( 'moviefilein_test_video' )

class Calibration:
	'''The Calibration class is responsible for setting up the display output.

	The calibration process for flat screens is much easier than with blended
	surfaces. Here we only need to worry about correctly breaking apart
	our input texture, and the geometric distortion needed for any keystoning
	and rudamentary warping.

	Notes
	---------------
	
	'''
	def __init__( self ):
		'''The Class init function.

		There are no major considerations for the init process of this class, 
		instead a simple print line is added to make it easier to see when the
		class has be re initialized from the console.
		'''
		print( 'Calibration Init Succesful' )
		
		return

	def Tool_bar_switcher( self, base_path ):
		'''Facilitatets fast UI switching via the toolbar.

		There are several different modes needed during the calibration process.
		This method allows for easy changes to be made in the process of adding
		UI elements to the control display.
		
		Arguments
		---------------
		base_path (str) - the string path to the base which both a body and side
		bar for the main UI. Two select COMPs are used for the main UI, and this
		allows for fast element swapping.

		Notes
		---------------
		'self' does not need to be included in the Args section.
		'''
		# change select panel elements with toolbar paths

		if base_path == 'base_mapping':
			Stoner.allowCooking			= True
		else:
			Stoner.allowCooking			= False

		UI_body.par.selectpanel			= base_path + '/container_body'
		UI_sidebar.par.selectpanel		= base_path + '/container_sidebar'

		return

	def Stoner_ui_switcher( self, calibration_data_path, target_display ):
		'''Facilitatets fast UI switching via the toolbar.

		There are several different modes needed during the calibration process.
		This method allows for easy changes to be made in the process of adding
		UI elements to the control display.

		Arguments
		---------------
		calibration_data_path (str) - a string path used to change the project
		parameter of the stoner. This allows a single stoner tox to control
		any number of grid warped outputs. Changing the project path for a stoner
		with both update the UI, and ensure that all changes are correctly routed
		for saving

		target_display (int) - an integer value that indicates which of the output
		disaplays is being targed for updates.
						
		Notes
		---------------
		'self' does not need to be included in the Args section.
		'''
		# change select panel elements with toolbar paths

		target_stoner					= eval( str( calibration_data_path ) )
		target_calibration_disp			= 'calibration_display{target_display}/switch1'
		target_warp_texture				= '../container_display{target}/null_cropped'

		# debug lines
		# print( 'the target display is ', target_display )
		# print( CalibrationData.op( target_calibration_disp.format( target_display=target_display ) ) )

		#################################################################
		### DEPRECIATED                                               ###
		#################################################################
		
		# # set active calibration tox to live stoner input
		# for possible_display in display_range[1:]:
			
		# 	# turn off switch for live input on non-active displays
		# 	if target_display != possible_display:
		# 		CalibrationData.op( target_calibration_disp.format( target_display=possible_display ) ).par.index = 0
				
		# 		# debug line
		# 		# print( 'display ' , possible_display, ' is locked' )
			
		# 	# turn on switch for live input on active display
		# 	else:
		# 		CalibrationData.op( target_calibration_disp.format( target_display=target_display ) ).par.index = 1
		# 		# debug line
		# 		print( 'display ' , target_display, ' is live' )
		
		# set stoner to target correct display
		Stoner.par.Project				= target_stoner
		# debug line
		# print( target_warp_texture.format( target = target_display ) )
		
		Stoner.op( 'select1' ).par.top	= target_warp_texture.format( target = target_display )

		return

	def Save_calibration_tox( self ):
		'''Saves all calibration data.

		While this is not the most efficient means of saving the calibration data,
		it's the most complete without a complex set of externalization methods.
		This will save the entire calibration TOX complete with look-up maps, and
		table components for the stoner TOX. This function over-writes the existing
		tox in the project directory. If you save another version of this TOX you 
		can replace it in the project directory to have another version of the mapping.

		Notes
		---------------
		'self' does not need to be included in the Args section.
		'''

		save_path					= 'calibration_tox/base_calibration_data.tox'
		save_name					= 'base_calibration_data'
		
		op.CalibrationData.save( save_path )

		return

	def Change_previs_camera_location( self, camera_index ):
		'''Changes the camera blend sequence.

		A camera blend COMP is used to facilitate multiple camera angles from a
		single camerablend input. By changing the sequence value we are able to
		jump cut between camera locations..

		Arguments
		---------------
		camera_index (int) - this integer controls where in the sequence of the
		camera blend component we are currently located.
						
		Notes
		---------------
		'self' does not need to be included in the Args section.
		'''

		op.Previs.op( 'camblend1' ).par.sequence	= camera_index

		return

	def Load_test_media( self ):
		'''Loads test media plate.

		Media loading is fairly straight forward for a test plate in this project.
		Intended for fast previewing of content, this method allows the user to
		quickly load a panoramic video or image in order to see what it will look
		like through the previs view, or through the outputs.
						
		Notes
		---------------
		'self' does not need to be included in the Args section.
		'''

		# store the old path in case the user clicks cancel
		old_path					= test_media.par.file
		load_title					= 'Choose a Test Media Clip'
		media_path					= ui.chooseFile(
													load = True, 
													fileTypes=tdu.fileTypes['movie'] + tdu.fileTypes['image'],
													title = load_title
													)

		# if the user clicks cancel, None is returend from ui.chooseFile. If this happens
		# we use the old media path to ensure that we have something to display.
		if media_path == None:
			test_media.par.file		= old_path

		# if the user has selected a valid path we load this media.
		else:
			test_media.par.file		= media_path

		# reload and play media 
		test_media.par.reloadpulse.pulse()
		test_media.par.play			= 1
		
		# ensure the "Play" button is clicked to ensure the UI matches application behavior.
		op.TestMedia.op( 'container_sidebar/container_play_controls/container1/button1' ).interactMouse( 0.5, 0.5, leftClick = True )

		return

	def Test_media_play( self ):
		'''Plays the test media.

		Notes
		---------------
		'self' does not need to be included in the Args section.
		'''
		test_media.par.play			= 1

		return

	def Test_media_pause( self ):
		'''Pauses the test media.
		
		Notes
		---------------
		'self' does not need to be included in the Args section.
		'''
		test_media.par.play			= 0

		return

	def Help_pop_up( self, title, help_doc ):
		'''Opens a pop-up help window.

		Pop up help windows can often be useful or helpful in UIs. Here
		we have a simple method to do just that. Our text is pulled from
		another location in the network in order to make more generalized
		method here.

		Arguments
		---------------
		title (str) - This string is used as a title for the message box.

		help_doc (str) - This string is used for retrieving the appropriate
		help document from the base_help tox in the network.
		'''
		title 						= title
		message 					= op.Pop_up_help.op( help_doc ).text
		buttons 					= [ 'Close' ]
		ui.messageBox( 
						title, 
						message, 
						buttons = buttons
					 )

		return

	def Close_project( self ):
		'''Closes the project and prompts the user to save.

		This call will close the project, and prompt the user to save their
		work.
		'''
		message 					= '''
Don't forget that many elements in this network are
probably stored in extenral tox files. Make sure you
save extenral tox files, or displacement maps before
you quit IBERA.
'''
		externals_warning			= ui.messageBox(
													"Before you Quit",
													message,
													buttons = [ 'Cancel', 'Quit' ]
													)
				
		if externals_warning:
			project.quit()
		
		else:
			pass

		return