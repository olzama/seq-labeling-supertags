# Given a lexical type, search in the ERG grammar files for its supertypes, for N levels of the hierarchy

import sys
from delphin import tdl

def get_supertypes(lextype, n):
    if n == 0:
        return [lextype]
    else:
        supertypes = []

        for supertype in lextype.supertypes:
            supertypes.extend(get_supertypes(supertype, n - 1))
        return supertypes
