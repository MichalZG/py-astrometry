import os
import sys
import logging
import glob
import argparse
import functools
from astropy.io import fits
from astropy.coordinates import SkyCoord
from astropy import units
from subprocess import Popen, PIPE, STDOUT
import subprocess
from config import Suhora_config as config

files_to_rm = ['*.axy', '*.corr', '*.xyls', '*.match',
               '*.new', '*.rdls', '*.solved', '*.wcs']


def start_log(main_dir, level):
    numeric_level = getattr(logging, level.upper(), None)
    log_dir = os.path.join(main_dir, config.LOG_FILE_NAME)
    logging.basicConfig(filename=log_dir,
                        format='%(asctime)s %(message)s', level=numeric_level)


def get_coo(image):

    hdr = fits.getheader(image)
    try:
        ra = hdr[config.RA_KEY]
        dec = hdr[config.DEC_KEY]
    except KeyError:
        logging.warning(
            'Coords problem in {}, try solve the image blindly'.format(image))
        return None

    coords = functools.partial(SkyCoord, ra, dec)

    return coords(unit=(units.hourangle, units.deg)), config.RADIUS


def create_command(image, solve_options):

    coo = get_coo(image)

    if coo is not None:
        c, r = coo
        solve_options['--ra'] = c.ra.degree
        solve_options['--dec'] = c.dec.degree
        solve_options['--radius'] = r
    else:
        pass

    solve_options['--out'] = os.path.basename(image)
    solve_options['--new-fits'] = os.path.join(
        args.images_dir, config.OUTPUT_FOLDER_NAME, os.path.basename(image))

    cmd = ['solve-field', image]

    for key, item in solve_options.items():
        if item is None or item is False:
            pass
        elif item is True:
            cmd.append(str(key))
        else:
            cmd.append(str(key))
            cmd.append(str(item))

    return cmd


def run_solve(image):

    os.makedirs(os.path.join(
        args.images_dir, config.OUTPUT_FOLDER_NAME), exist_ok=True)
    cmd = create_command(image, config.solve_options)

    logging.info('solve command: {}'.format(' '.join(cmd)))
    logging.info('SOLVING START')

    try:
        logging.info('Solve: {}'.format(image))
        subprocess.check_call(cmd)
        if os.path.isfile(os.path.join(
                args.images_dir, config.OUTPUT_FOLDER_NAME, os.path.basename(image))):
            logging.info('Solve DONE')
        else:
            logging.warning('Solve FAILED')
    except subprocess.CalledProcessError as e:
        clear()
        print('Astrometry Error')
        raise e


def load_images(images_dir, patt=config.FITS_PATTERN):

    images = sorted(glob.glob(os.path.join(images_dir, patt)))
    logging.info('{} images found'.format(len(images)))

    return images


def clear():
    print('cleaning.....')
    for i in files_to_rm:
        files = glob.glob(os.path.join(args.images_dir,i))
        for j in files:
            os.remove(j)


def main(args):

    start_log(args.images_dir, args.logger)
    images = load_images(args.images_dir)
    if not images:
        logging.error('no images has been found')
        raise FileNotFoundError('no images has been found')
    for im in images:
        run_solve(im)
    clear()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Astrometry-py')
    parser.add_argument('--overwrite', dest='overwrite', action='store_true',
                        help='overwrite original files, default False')
    parser.set_defaults(overwrite=False)
    parser.add_argument('--logger', choices=['INFO', 'WARNING', 'ERROR'],
                        default='INFO', help='Logger level')
    parser.add_argument('images_dir', help='Path to images to solve')

    args = parser.parse_args()
    main(args)
