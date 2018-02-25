import os
import sys
import logging
import glob
import argparse
import shutil
import functools
from astropy.io import fits
from astropy.coordinates import SkyCoord
from astropy import units
from subprocess import Popen, PIPE, STDOUT
import subprocess


files_to_rm = ['*.axy', '*.corr', '*.xyls', '*.match',
               '*.new', '*.rdls', '*.solved', '*.wcs']


def start_log(main_dir, level):
    numeric_level = getattr(logging, level.upper(), None)
    os.makedirs(os.path.join(
        args.images_dir, config.OUTPUT_FOLDER_NAME), exist_ok=True)
    log_dir = os.path.join(
        main_dir, config.OUTPUT_FOLDER_NAME, config.LOG_FILE_NAME)
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

    cmd = create_command(image, config.solve_options)

    logging.info('Solve command: {}'.format(' '.join(cmd)))
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


def load_images(images_dir, patt):

    images = sorted(glob.glob(os.path.join(images_dir, patt)))
    logging.info('{} images found'.format(len(images)))

    return images


def clear():
    logging.info('Cleaning temp files')
    if args.overwrite:
        logging.info('Overwrite raw images')
        shutil.move(os.path.join(args.images_dir,
                                 config.OUTPUT_FOLDER_NAME), args.images_dir)
    for i in files_to_rm:
        files = glob.glob(os.path.join(args.images_dir, i))
        for j in files:
            os.remove(j)


def main(args):

    start_log(args.images_dir, args.logger)
    for i, k in vars(args).items():
        logging.info('{}: {}'.format(i, k))
    images = load_images(args.images_dir, config.FITS_PATTERN)
    if not images:
        logging.error('No images has been found')
        raise FileNotFoundError('No images has been found')
    for im in images:
        run_solve(im)
    clear()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Astrometry-py')
    parser.add_argument('--overwrite', dest='overwrite', action='store_true',
                        help='overwrite original files, default False')
    parser.set_defaults(overwrite=False)
    parser.add_argument('--config', dest='config', default='Telescope60',
                        nargs='?', help='Configuration name, default Telescope60')
    parser.add_argument('--logger', choices=['INFO', 'WARNING', 'ERROR'],
                        default='INFO', help='Logger level')
    parser.add_argument('images_dir', help='Path to images to solve')
    args = parser.parse_args()
    print(args)
    config = getattr(__import__('config', fromlist=[args.config]), args.config)

    main(args)
