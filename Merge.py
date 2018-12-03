import linecache

import os

import Parse
import multiprocessing


def merge(files_paths, merge_path, post_files_lines, terms_dict, is_final_posting, post_name):
    files_line = {files_paths[0]: 0, files_paths[1]: 0}

    def read_next(file_path):
        line = linecache.getline(file_path, files_line[file_path])
        files_line[file_path] += 1
        tmp_index = line.split('|')
        term = tmp_index[0]
        tf_dicts = tmp_index[1]
        loc_dicts = tmp_index[2]
        return [term, tf_dicts, loc_dicts]

    f = open(merge_path + post_name, 'ab+')
    merged_line_count = 0
    big_terms = {}
    min_lines = min(post_files_lines)
    count_lines_0 = 1
    count_lines_1 = 1
    term_index_0 = read_next(files_paths[0])
    term_index_1 = read_next(files_paths[1])

    while count_lines_0 < post_files_lines[0] and count_lines_1 < post_files_lines[0]:
        inverted_index = ''

        if term_index_0[0] < term_index_1[0]:
            inverted_index = [term_index_0[0], term_index_0[1], term_index_0[2]]
            term_index_0 = read_next(files_paths[0])
            count_lines_0 += 1

        elif term_index_0[0] == term_index_1[0]:
            inverted_index = [term_index_0[0], "{}{}".format(term_index_0[1], term_index_1[1]),
                              "{}{}".format(term_index_0[2], term_index_1[2])]
            term_index_0 = read_next(files_paths[0])
            count_lines_0 += 1
            term_index_1 = read_next(files_paths[1])
            count_lines_1 += 1

        else:
            inverted_index = [term_index_1[0], term_index_1[1], term_index_1[2]]
            term_index_1 = read_next(files_paths[1])
            count_lines_1 += 1

        if is_final_posting:
            if Parse.isWord(inverted_index[0]) and inverted_index[0].isupper() and \
                            inverted_index[0].lower() in terms_dict:
                big_terms[inverted_index[0].lower()] = [inverted_index[1], inverted_index[2]]
            else:
                if inverted_index[0] in big_terms:
                    inverted_index = '{}|{}{}|{}{}'.format(inverted_index[0], inverted_index[1],
                                                           big_terms[inverted_index[0]][0], inverted_index[2],
                                                           big_terms[inverted_index[0]][1])
                    terms_dict[term_index_0[0]] = {"line": merged_line_count, "freq": terms_dict[term_index_0[0]]}
                    f.write('{}|{}|{}'.format(inverted_index[0], inverted_index[1], inverted_index[2]))
                    merged_line_count += 1
        else:
            f.write('{}|{}|{}'.format(inverted_index[0], inverted_index[1], inverted_index[2]))
            merged_line_count += 1

    if count_lines_0 < post_files_lines[0]:
        while count_lines_0 < post_files_lines[0]:
            f.write('{}|{}|{}'.format(term_index_0[0], term_index_0[1], term_index_0[2]))
            term_index_0 = read_next(files_paths[0])
            count_lines_0 += 1

    elif count_lines_1 < post_files_lines[1]:
        while count_lines_1 < post_files_lines[1]:
            f.write('{}|{}|{}'.format(term_index_1[0], term_index_1[1], term_index_1[2]))
            term_index_1 = read_next(files_paths[1])
            count_lines_1 += 1


def start_merge(files_names, post_files_lines, terms_dict, posting_path):
    merge_path = posting_path + "\\Merge" + '0'
    merge_level = 0
    currnent_post_count = len(post_files_lines)
    merge_count = 0
    processes = []
    while len(files_names) > 2:
        i = 0
        while i < len(files_names):
            if i + 1 < len(files_names):
                p = multiprocessing.Process(target=merge, args=(
                    [files_names[i], files_names[i + 1]], merge_path, post_files_lines, {},False, "merge" + str(i)))
                p.start()
                processes.append(p)
            else:
                tmp_name = '\\' + str.split(files_names[i],'\\')[1]
                os.rename(tmp_name, merge_path + tmp_name)
            i += 2
        for p in processes:
            p.join()
        files_names = os.listdir(merge_path)
        
