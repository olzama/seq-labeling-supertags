# Olga Zamaraeva 2024
# "predictions.txt" should be the output of the supertagger (see https://github.com/olzama/neural-supertagging), sentence per line:
# x_cp_howabt_le, p_cp_s-unsp_le, n_-_pn-gen_le, n_-_pn-gen_le, n_-_pn-gen_le, n_-_pn-gen_le, pt_-_qmark_le
# x_cp_howabt_le, p_cp_s-unsp_le, n_-_pn-gen_le, v_pp_unacc_le, p_np_i-reg_le, d_-_poss-its_le, n_pp_mc-of_le, pt_-_hyphn-rgt_le, n_-_c-ed_le, pt_-_lparen_le, c_xp_and_le, av_-_i-vp-pr_le, n_-_mc_le, pt_-_rparen_le, n_-_c-pl_le, p_np_i_le, d_-_sg-nmd_le, aj_-_i_le, aj_pp_i-x-to-y_le, v_np_le, v_np*_le, n_pp_c-of_le, pt_-_qmark_le

# python UD_English-EWT/en_ewt-ud-test.conllu supertag-predictions.txt output-conllu.txt
import sys


def replace_ud_tags(conllu_path, tags_path, output_path):
    with open(conllu_path, 'r', encoding='utf-8') as conllu_file:
        conllu_lines = conllu_file.readlines()
    with open(tags_path, 'r', encoding='utf-8') as tags_file:
        tags_lines = tags_file.readlines()
        print("Supertags for {} sentences".format(len(tags_lines)))
    output_lines = []
    tag_index = 0
    tags_for_sentence = tags_lines[tag_index].strip().split(', ')
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
                parts[3] = alternative_tag
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
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write('\n'.join(output_lines) + '\n')

#main
if __name__ == "__main__":
    replace_ud_tags(sys.argv[1], sys.argv[2], sys.argv[3])