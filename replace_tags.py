# Olga Zamaraeva 2024
# "predictions.txt" should be the output of the supertagger (see https://github.com/olzama/neural-supertagging), sentence per line:
# x_cp_howabt_le, p_cp_s-unsp_le, n_-_pn-gen_le, n_-_pn-gen_le, n_-_pn-gen_le, n_-_pn-gen_le, pt_-_qmark_le
# x_cp_howabt_le, p_cp_s-unsp_le, n_-_pn-gen_le, v_pp_unacc_le, p_np_i-reg_le, d_-_poss-its_le, n_pp_mc-of_le, pt_-_hyphn-rgt_le, n_-_c-ed_le, pt_-_lparen_le, c_xp_and_le, av_-_i-vp-pr_le, n_-_mc_le, pt_-_rparen_le, n_-_c-pl_le, p_np_i_le, d_-_sg-nmd_le, aj_-_i_le, aj_pp_i-x-to-y_le, v_np_le, v_np*_le, n_pp_c-of_le, pt_-_qmark_le

# Usage:
# python UD_English-EWT/en_ewt-ud-test.conllu supertag-predictions.txt output-conllu.txt grammars/erg/trunk 0

# The format for the input CONLLU files is as here:
# https://github.com/UniversalDependencies/UD_English-EWT/blob/master/en_ewt-ud-dev.conllu

# The format for the supertag predictions is a sentence per line, with comma-separated supertags.
# The grammar is the ERG grammar, as can be found here: https://github.com/delph-in/erg
# The depth is the number of supertypes to use for supertags, as defined in the grammar.
# If 0, the original supertags are used.

import sys
from supertypes import populate_type_defs, get_n_supertypes


def replace_ud_tags(conllu_path, tags_path, output_path, grammar, depth=1):
    with open(conllu_path, 'r', encoding='utf-8') as conllu_file:
        conllu_lines = conllu_file.readlines()
    with open(tags_path, 'r', encoding='utf-8') as tags_file:
        tags_lines = tags_file.readlines()
        print("Supertags for {} sentences".format(len(tags_lines)))
    dataset_name = conllu_path.split('/')[-1]
    output_lines = []
    tag_index = 0
    tags_for_sentence = tags_lines[tag_index].strip().split(', ')
    original_tags = set()
    final_tags = {}
    no_supertypes = set()
    for line in conllu_lines:
        line = line.strip()
        if line.startswith('#') or not line:
            # Copy comments and blank lines as they are
            output_lines.append(line)
        else:
            # Process token line
            parts = line.split('\t')
            if len(parts) == 10 and '-' not in parts[0] and '.' not in parts[0]:
                alternative_tag = tags_for_sentence.pop(0)
                original_tags.add(alternative_tag)
                supertype = None
                if depth > 0:
                    supertypes = get_n_supertypes(grammar, alternative_tag, depth)
                    if not supertypes:
                        print("No supertypes found for {}".format(alternative_tag))
                        no_supertypes.add(alternative_tag)
                    if supertypes:
                        supertype = '+'.join(supertypes[depth-1])
                        # Resplit and rejoin so as to not have duplicate parts:
                        to_rejoin = supertype.split('+')
                        supertype = '+'.join(list(set(to_rejoin)))
                        if not alternative_tag in final_tags:
                            final_tags[alternative_tag] = set()
                        final_tags[alternative_tag].add(supertype)
                parts[3] = supertype if supertype else alternative_tag
                output_lines.append('\t'.join(parts))
                # Move to the next sentence if all tags are used
                if not tags_for_sentence:
                    tag_index += 1
                    if tag_index < len(tags_lines):
                        tags_for_sentence = tags_lines[tag_index].strip().split(', ')
                    else:
                        # No more tags to use
                        break
            else:
                # Not a valid token line, just append as is
                output_lines.append(line)
    with open(output_path + dataset_name + '-hpsg-' + str(depth) + '.txt', 'w', encoding='utf-8') as output_file:
        output_file.write('\n'.join(output_lines) + '\n')
    print("Original tags: {}".format(len(original_tags)))
    if depth > 0:
        flattened_set = {item for tag_set in final_tags.values() for item in tag_set}
    else:
        flattened_set = original_tags
    print("Final tags with depth {}: {}".format(depth, len(flattened_set)))
    # Write the summary to the summary file
    summary_path = output_path + 'run-summaries/' + dataset_name +'_' + str(depth) + '_summary.txt'
    with open(summary_path, 'w', encoding='utf-8') as summary_file:
        summary_file.write(f"Dataset: {conllu_path.split('/')[-1]}\ndepth: {depth}\n")
        summary_file.write(f"Supertags for {len(tags_lines)} sentences\n")
        summary_file.write(f"No supertypes found for {len(no_supertypes)} tags\n")
        summary_file.write(f"Original tags: {len(original_tags)}\n")
        summary_file.write(f"Final tags with depth {depth}: {len(flattened_set)}\n")
    with open(output_path + 'tagsets/' + dataset_name + '_final_tags_' + str(depth) + '.txt', 'w', encoding='utf-8') as final_tags_file:
        for tag in sorted(flattened_set):
            final_tags_file.write(tag + '\n')


#main
if __name__ == "__main__":
    erg_dir = '/home/olga/delphin/erg/trunk'
    type_name = 'main_verb_newltop'  # Replace with the type you're interested in
    erg_types = populate_type_defs(erg_dir)
    replace_ud_tags(sys.argv[1], sys.argv[2], sys.argv[3], erg_types, int(sys.argv[4]))