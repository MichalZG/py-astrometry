class Config:

	FITS_PATTERN = '*.fits'  # eg '*.fits', '*.fit'
	# log name
	LOG_FILE_NAME = 'solve.log'
	# output folder name, used if overwrite False
	OUTPUT_FOLDER_NAME = 'astrometry_output'

class Suhora_config(Config):
	# fits keys
	RA_KEY = 'OBSRA'
	DEC_KEY = 'OBSDEC'
	RADIUS = 3  # deg
	DOWNSAMPLE = 4
	CPU_LIMIT = 30  # sec
	LO_PIX_SCALE = 2.5  # arcsec/pix
	HI_PIX_SCALE = 2.55  # arcsec/pix
	SCALE_UNITS = 'arcsecperpix'
	TEMP_DIR = '/tmp/astromety'

	# solve options
	RADIUS = 3  # deg
	DOWNSAMPLE = 4
	CPU_LIMIT = 30  # sec
	LO_PIX_SCALE = 2.5  # arcsec/pix
	HI_PIX_SCALE = 2.55  # arcsec/pix
	SCALE_UNITS = 'arcsecperpix'
	TEMP_DIR = '/tmp/astromety'
	DOWNSAMPLE = 4

	solve_options = {
	    '--ra': None,
	    '--dec': None,
	    '--radius': None,
	    '--scale-low': LO_PIX_SCALE,
	    '--scale-high': HI_PIX_SCALE,
	    '--scale-units': SCALE_UNITS,
#	    '--no-background-subtraction': True,
	    '--no-plots': True,
	    '--cpulimit': CPU_LIMIT,
#	    '--downsample': DOWNSAMPLE
	}