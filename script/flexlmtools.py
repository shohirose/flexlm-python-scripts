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

    def query(self, server, feature=None):
        """
        Query to a server

        Parameters
        ----------
        server : str
                License server in the form of 'port@host'
        feature : str
                License feature (optional, default=None)
                If feature is None, query all features.

        Returns
        -------
        str
            Query result output to stdout
        """
        def create_command():
            return [self.lmutil, 'lmstat', '-a', '-c', server] if feature is None \
                else [self.lmutil, 'lmstat', '-c', server, '-f', feature]
    
        cmd = create_command()
        proc = sp.run(cmd, stdout=sp.PIPE, stderr=sp.PIPE, \
                      encoding='utf-8', timeout=self.timeout)
        return proc.stdout


def parse_query(lines, features):
    """
    Parse a query and returns the issued and used number of a given feature
    
    Parameters
    ----------
    lines : str
        Query result
    features : list(str)
        Feature names to extract

    Returns
    -------
    dict(feature, tuple(int, int))
        Dictionary of feature name and a tuple of issued and used feature
    """
    def create_regexpr(feature):
        return re.compile('Users of ' + feature + ':' \
            '  \(Total of (?P<issued>\d+) licenses?? issued;' \
            '  Total of (?P<used>\d+) licenses?? in use\)')

    def get_feature_status(reg):
        m = reg.search(lines)
        return int(m.group('issued')), int(m.group('used')) if m else 0, 0

    regs = list(map(create_regexpr, features))
    status = list(map(get_feature_status, regs))
    return dict(zip(features, status))

