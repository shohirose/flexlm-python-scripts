from flexlmtools import FlexlmLicenseManager, get_license_status

if __name__ == '__main__':
    """
    Print out the availbale number licenses of a given feature.

    A license server and the path to lmutil must be specified 
    via '-s,--server' and '-c,--cmd' options.
    """

    import argparse

    parser = argparse.ArgumentParser(
        description='Print the number of a given feature '
                    'available from Flexlm License Manager.')
    parser.add_argument(
        '-c', '--cmd', help='Path to lmutil executable', default='lmutil')
    parser.add_argument('-d', '--daemon', help='License daemon', default=None)

    parser.add_argument('-t', '--timeout',
                        help='Duration for time out', default=5)
    parser.add_argument(
        '-s', '--server', help='License server (port@server)', required=True)
    parser.add_argument('-f', '--feature',
                        help='License feature', required=True)
    args = parser.parse_args()

    manager = FlexlmLicenseManager(lmutil=args.cmd, timeout=args.timeout)
    status = get_license_status(
        manager, args.server, args.daemon, args.feature)
    if status:
        issued = status[0]
        used = status[1]
        print(issued - used)
    else:
        print(0)
