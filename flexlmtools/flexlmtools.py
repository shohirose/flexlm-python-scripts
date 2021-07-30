import os
import re
import subprocess as sp


def validate_server_name(server):
    """
    Validate server name if it is in the form of '1234@server-name'

    Parameters
    ----------
    server : str
        Server name

    Returns
    -------
    bool
    """
    m = re.match(r'^[1-9][0-9]*@[a-zA-Z0-9-.]+$', server)
    return True if m else False


class FlexlmLicenseManager:
    """
    Flexlm License Manager class.

    Attributes
    ----------
    lmutil : str
        Path to lmutil execution file
    timeout : int
        Duration for time-out (optional, default=5)
    """

    def __init__(self, lmutil, timeout=5):
        """
        Parameters
        ----------
        lmutil : str
            Path to lmutil execution file
        timeout : int
            Duration for time-out (optional, default=5)
        """
        if not os.path.exists(lmutil):
            raise ValueError(f'Error: {lmutil} is not found.')
        self.lmutil = lmutil
        self.timeout = timeout

    def query(self, server, daemon=None, feature=None):
        """
        Query to a server

        Parameters
        ----------
        server : str
            License server in the form of 'port@host'
        daemon : str
            Vendor daemon (optional)
            Specifying daemon makes a query faster.
        feature : str
            License feature (optional, default=None)
            If feature is None, query all features.

        Returns
        -------
        str
            Query result output to stdout
        """
        def create_command():
            cmd = [self.lmutil, 'lmstat', '-c', server]

            if feature is None:
                cmd.append('-a')
            else:
                cmd.extend('-f', feature)

            if daemon is not None:
                cmd.extend('-S', daemon)

            return cmd

        if not validate_server_name(server):
            raise ValueError(f'Incorrect server format: {server}')

        cmd = create_command()
        proc = sp.run(cmd, stdout=sp.PIPE, stderr=sp.PIPE,
                      encoding='utf-8', timeout=self.timeout)
        return proc.stdout


def parse_query(lines, features=None):
    """
    Parse a query and returns the issued and used number of a given feature

    Parameters
    ----------
    lines : str
        Query result
    features : list[str] or None
        Feature names to extract (optional)
        If features is None, return all the features

    Returns
    -------
    dict(feature, tuple(int, int))
        Dictionary of feature name and a tuple of issued and used feature
    """
    def create_regexpr():
        s = r'[a-zA-Z][a-zA-Z0-9_-]*' if features is None else '|'.join(
            features)
        return re.compile(r'Users of (' + s + '):'
                          r'  \(Total of (\d+) licenses?? issued;'
                          r'  Total of (\d+) licenses?? in use\)')

    def to_tuple(match):
        feature = match[0]
        issued = int(match[1])
        used = int(match[2])
        return feature, (issued, used)

    reg = create_regexpr()
    matches = reg.findall(lines)
    return dict(map(to_tuple, matches))


def get_license_status(manager, server, daemon, feature):
    """
    Get license status of a given feature

    Parameters
    ----------
    manager : flexlmtools.FlexlmLicenseManager
        Flexlm License Manager
    server : str
        Server in the form of "port@server"
    daemon : str
        License daemon
    feature : str
        Feature name

    Returns
    -------
    dict or None
        Dictionary of feature name and the tuple of the number
        of issued and used licenses
    """
    result = manager.query(server, daemon, feature)
    dct = parse_query(result, features=[feature])
    return dct[feature] if dct else None
