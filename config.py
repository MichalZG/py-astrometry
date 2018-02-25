class Config:

	FITS_PATTERN = '*.fits'  # eg '*.fits', '*.fit'
	# log name
	LOG_FILE_NAME = 'solve.log'
	# output folder name, used if overwrite False
	OUTPUT_FOLDER_NAME = 'astrometry_output'

class Suhora_config(Config):
	# fits keys
	RA_KEY = 'RA'
	DEC_KEY = 'DEC'

	# solve options
	RADIUS = 0.5  # deg
	DOWNSAMPLE = 4
	CPU_LIMIT = 30  # sec
	LO_PIX_SCALE = 1.11  # arcsec/pix
	HI_PIX_SCALE = 1.13  # arcsec/pix
	SCALE_UNITS = 'arcsecperpix'
	TEMP_DIR = '/tmp/astromety'
	SOLVE_DEPTH = '40,80,100,160,250'
	
	

	solve_options = {
	    '--ra': None,
	    '--dec': None,
	    '--radius': None,
	    '--depth': SOLVE_DEPTH,
	    '--scale-low': LO_PIX_SCALE,
	    '--scale-high': HI_PIX_SCALE,
	    '--scale-units': SCALE_UNITS,
#	    '--no-background-subtraction': True,
        '--overwrite': True,
        '--dir': OUTPUT_FOLDER_NAME,
	    '--no-plots': True,
	    '--cpulimit': CPU_LIMIT,
	    '--no-verify': True,
#	    '--downsample': DOWNSAMPLE
	}