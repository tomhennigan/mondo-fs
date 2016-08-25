#!/usr/bin/env python
# coding=utf8

import argparse
import logging
import os

import diazed
import fuse
from monzo_fs.decorators import singleton
from monzo_fs.monzo import MonzoAPI


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('mount_point', help='location to mount the file system')
    parser.add_argument('--logfile', default=None)
    parser.add_argument('--verbose', action='store_true', default=False)
    parser.add_argument('--background', action='store_true', default=False)
    parser.add_argument('--client_id',
                        required=True,
                        help='Your Monzo API client.')
    parser.add_argument('--client_secret',
                        required=True,
                        help='Your Monzo API secret.')
    args = parser.parse_args()

    logging.basicConfig(
        filename=args.logfile,
        level=(logging.DEBUG if args.verbose else logging.INFO))

    m = singleton(MonzoAPI, MonzoAPI(args.client_id, args.client_secret))

    # Perform initialization, which involves authorizing the user if required.
    m.initialize()

    if not os.path.exists(args.mount_point):
        os.mkdir(args.mount_point)

    fuse.FUSE(diazed.fs,
              args.mount_point,
              foreground=(not args.background),
              direct_io=True)

if __name__ == '__main__':
    main()
