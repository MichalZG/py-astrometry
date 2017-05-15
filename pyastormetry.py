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
DOWNSAMPE = 8
TEMP_DIR = '/tmp/astromety/'
OUT_DIR = '/home/pi/Programs/python-programs/pyastrometry/test/'

more_solve_options = ['--overwrite',
                      '--no-background-subtraction',
                      '--no-plots',
                      '--overwrite']



def start_log(main_dir):
    logging.basicConfig(filename=os.path.join(main_dir, 'solve.log'),
                        format='%(asctime)s %(message)s', level=logging.INFO)


def get_coo(image):
    
    hdr = fits.getheader(image)
    ra = hdr[RA_KEY]
    dec = hdr[DEC_KEY]
    coords = functools.partial(SkyCoord, ra, dec)

    return coords(unit=(units.hourangle, units.deg))


def create_command(image, more_solve_options, r=RADIUS, dsamp=DOWNSAMPE,
                   tmp=TEMP_DIR, out=OUT_DIR):
    
    coo = get_coo(image)

    cmd = ['solve-field',
           image,
           '--ra',
           '{:.3f}'.format(coo.ra.degree),
           '--dec',
           '{:.3f}'.format(coo.dec.degree),
           '--radius',
           '{}'.format(r),
           '--downsample',
           '{}'.format(dsamp),
           '--dir', 
           '{}'.format(tmp),
           '--new-fits',
           '{}'.format(os.path.join(out, os.path.basename(image)))]

    if len(more_solve_options) > 0:
        cmd += more_solve_options

    return cmd


def run_solve(image):
    
    cmd = create_command(image, more_solve_options, RADIUS, DOWNSAMPE,
                         TEMP_DIR, OUT_DIR)


    logging.info('solve command: {}'.format(' '.join(cmd)))
    logging.info('SOLVING START')
    
    try:
        logging.info('Solve: {}'.format(image))
        subprocess.check_call(cmd)
    except IOError:
        pass

def load_images(images_dir, patt=FITS_PATTERN):
    
    images = sorted(glob.glob(os.path.join(images_dir, patt)))
    logging.info('{} images found'.format(len(images)))

    return images


def main(args):

    start_log(args.images_dir)
    images = load_images(args.images_dir)

    for im in images:
        run_solve(im)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Astrometry-py')
    parser.add_argument('--images_dir', type=str,
                        nargs='?',
                        help='Images to solve dir')
    args = parser.parse_args()
    main(args)



