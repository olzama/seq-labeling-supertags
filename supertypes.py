# Given a lexical type, search in the ERG grammar files for its supertypes, for N levels of the hierarchy

import os
from delphin import tdl
from copy import copy, deepcopy

import copy

import copy

import copy

import copy


def get_n_supertypes(lex, type_name, n):
    # Helper function to recursively retrieve supertypes
    def get_supertypes_recursive(type_name, remaining_depth):
        if remaining_depth == 0 or type_name not in lex:
            return [], []  # Return empty lists if no supertypes or no more depth

        # Retrieve the supertypes for the current type and convert them to strings
        supertypes = [str(supertype) for supertype in lex[type_name].supertypes]
        all_supertypes = copy.deepcopy(supertypes)

        # Group the supertypes at the current level
        combined_same_level_supertypes = [str(supertype) for supertype in lex[type_name].supertypes]

        # If there's more depth, recurse for each supertype
        combined_depth_supertypes = []
        if remaining_depth > 1:
            for supertype in supertypes:
                deeper_supertypes, deeper_combined = get_supertypes_recursive(str(supertype), remaining_depth - 1)
                all_supertypes.extend(deeper_supertypes)
                combined_depth_supertypes.extend(deeper_combined)

        # Combine supertypes at the same level by joining them with "+"
        combined_same_level_supertypes_str = '+'.join(sorted(set(combined_same_level_supertypes)))

        # Return all supertypes and combined supertypes for the current depth level
        return all_supertypes, [combined_same_level_supertypes_str] + combined_depth_supertypes

    # Start the recursive process
    all_supertypes, combined_supertypes = get_supertypes_recursive(type_name, n)

    # Return the combined supertypes for the given type up to level n
    return all_supertypes, combined_supertypes

def get_n_supertypes2(lex, type_name, n):
    # Helper function to recursively retrieve supertypes
    def get_supertypes_recursive(type_name, remaining_depth):
        if remaining_depth == 0 or type_name not in lex:
            return []

        supertypes = lex[type_name].supertypes
        all_supertypes = deepcopy(supertypes)

        # Recurse for each supertype, reducing remaining depth by 1
        if remaining_depth > 1:
            for supertype in supertypes:
                all_supertypes.extend(get_supertypes_recursive(str(supertype), remaining_depth - 1))

        return all_supertypes

    # Start the recursive process
    return get_supertypes_recursive(type_name, n)
def get_n_supertypes1(lex, type_name, n):
    # Retrieve the supertypes for the given type_name up to level n
    if type_name in lex:
        first_supertypes = lex[type_name].supertypes
        more_supertypes = copy(first_supertypes)
        if n > 1:
            for supertype in first_supertypes:
                cur = supertype
                for i in range(n - 1):
                    if str(cur) in lex:
                        cur_super = lex[str(cur)].supertypes
                        more_supertypes.extend(cur_super)
                        cur = cur_super[0]
        return more_supertypes
    else:
        return None
def get_supertype_of_type(lex, type_name):
    # Retrieve the supertype for the given type_name
    if type_name in lex:
        return lex[type_name].supertypes
    else:
        return None


def populate_type_defs(directory):
    global lex
    # Initialize an empty dictionary to store the lexicon
    lex = {}
    # Iterate through all files in the directory with the .tdl extension
    for filename in os.listdir(directory):
        if filename.endswith('.tdl'):
            file_path = os.path.join(directory, filename)

            # Parse the TDL file
            for event, obj, lineno in tdl.iterparse(file_path):
                if event == 'TypeDefinition':
                    # Add the object to the lexicon
                    lex[obj.identifier] = obj
    # sort the lexicon by type name
    lex = dict(sorted(lex.items()))
    return lex


if __name__ == "__main__":
    # Example usage
    directory = '/home/olga/delphin/erg/trunk'
    type_name = 'v_-_it_le'  # Replace with the type you're interested in

    lex = populate_type_defs(directory)
    # slice the portion of lex which starts with "n_":
    lex_slice = {k: v for k, v in lex.items() if k.startswith('n_intr')}

    supertype = get_supertype_of_type(lex, type_name)
    supertypes = get_n_supertypes(lex, type_name, 4)

    if supertype:
        print(f"Supertypes of {type_name}: {str(supertype[0])}")
    else:
        print(f"Type {type_name} not found.")
