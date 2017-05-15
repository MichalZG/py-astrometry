from __future__ import print_function

import os
import logging
import glob
import argparse
import functools
from astropy.io import fits
from astropy.coordinates import SkyCoord
from astropy import units
from subprocess import Popen, PIPE, STDOUT
import subprocess

FITS_PATTERN = '*.fits' # eg '*.fits', '*.fit'


#fits keys
RA_KEY = 'OBSRA'
DEC_KEY = 'OBSDEC'

#solve options
RADIUS = 3
DOWNSAMPLE = 8
CPU_LIMIT = 30 
TEMP_DIR = '/tmp/astromety/'
OUT_DIR = '/home/pi/Programs/python-programs/py-astrometry/test/output'

solve_options = {'--ra':None,
                 '--dec':None,
                 '--radius':None,
                 '--overwrite':True,
                 '--no-background-subtraction':True,
                 '--no-plots':True,
                 '--overwrite':True,
                 '--dir':TEMP_DIR,
                 '--cpulimit':CPU_LIMIT,
                 '--downsample':DOWNSAMPLE}



def start_log(main_dir, level):
    numeric_level = getattr(logging, level.upper(), None)
    log_dir = os.path.join(main_dir, 'solve.log')
    logging.basicConfig(filename=log_dir,
                        format='%(asctime)s %(message)s', level=numeric_level)


def get_coo(image):
    
    hdr = fits.getheader(image)
    try:
        ra = hdr[RA_KEY]
        dec = hdr[DEC_KEY]
    except KeyError:
        logging.warninig('coords problem in {}, solve the image blindly'.format(image))
        return None

    coords = functools.partial(SkyCoord, ra, dec)

    return coords(unit=(units.hourangle, units.deg)), RADIUS


def create_command(image, solve_options):

    coo = get_coo(image)
    
    if coo is not None:
        c, r = coo
    else:
        solve_options['--ra'] = c.ra.degree
        solve_options['--dec'] = c.dec.degree
        solve_options['--radius'] = r

    solve_options['--out'] = os.path.basename(image)
    solve_options['--new-fits'] = os.path.join(OUT_DIR, os.path.basename(image))
    
    cmd = ['solve-field', image]

    for key, item in solve_options.iteritems():
        if item is None or item is False:
            pass
        if item is True:
            cmd.append(str(key))
        else:
            cmd.append(str(key))
            cmd.append(str(item))
    
    return cmd


def run_solve(image):
    
    cmd = create_command(image, solve_options)
    
    logging.info('solve command: {}'.format(' '.join(cmd)))
    logging.info('SOLVING START')
    
    try:
        logging.info('Solve: {}'.format(image))
        subprocess.check_call(cmd)
        if os.path.isfile(os.path.join(OUT_DIR, image)):
            logging.info('Solve DONE')
        else:
            logging.warning('Solve FAILED')
    except subprocess.CalledProcessError as e:
        print('Astrometry Error')
        raise e


def load_images(images_dir, patt=FITS_PATTERN):
    
    images = sorted(glob.glob(os.path.join(images_dir, patt)))
    logging.info('{} images found'.format(len(images)))

    return images


def main(args):

    start_log(args.images_dir, args.logger)
    images = load_images(args.images_dir)

    for im in images:
        run_solve(im)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Astrometry-py')
    parser.add_argument('--images_dir', type=str,
                        nargs='?', required=True,
                        help='Path to images to solve')
    parser.add_argument('--logger', choices=['INFO', 'WARNING', 'ERROR'],
                        default='INFO', help='Logger level')
    args = parser.parse_args()
    main(args)



