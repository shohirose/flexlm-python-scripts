import os
import re
import subprocess as sp


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
            if daemon is None:
                return cmd + ['-a'] if feature is None \
                    else cmd + ['-f', feature]
            else:
                return cmd + ['-a', '-S', daemon] if feature is None \
                    else cmd + ['-f', feature, '-S', daemon]
    
        cmd = create_command()
        proc = sp.run(cmd, stdout=sp.PIPE, stderr=sp.PIPE, \
                      encoding='utf-8', timeout=self.timeout)
        return proc.stdout


def parse_query(lines, features=None):
    """
    Parse a query and returns the issued and used number of a given feature
    
    Parameters
    ----------
    lines : str
        Query result
    features : list(str) or None
        Feature names to extract (optional)
        If features is None, return all the features

    Returns
    -------
    dict(feature, tuple(int, int))
        Dictionary of feature name and a tuple of issued and used feature
    """
    def create_regexpr():
        s = '\w' if features is None else '|'.join(features)
        return re.compile('Users of (?P<feature>' + s + '):' \
            '  \(Total of (?P<issued>\d+) licenses?? issued;' \
            '  Total of (?P<used>\d+) licenses?? in use\)')

    def to_tuple(match):
        feature = match.group('feature')
        issued = int(match.group('issued')) if match else 0
        used = int(match.group('used')) if match else 0
        return feature, (issued, used)

    reg = create_regexpr()
    matches = reg.findall(lines)
    return dict(map(to_tuple, matches))
