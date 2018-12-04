import linecache
import os
import shutil
import Parse
import multiprocessing


def merge(files_paths, merge_path, post_files_lines, terms_dict, dict, is_final_posting, merged_post_name,
          merged_post_lines):
    files_line = {files_paths[0]: 0, files_paths[1]: 0}

    def read_next(file_path):
        line = linecache.getline(file_path, files_line[file_path] + 1).replace('\n', '')
        files_line[file_path] += 1
        tmp_index = line.split('|')
        term = tmp_index[0]
        tf_dicts = tmp_index[1]
        loc_dicts = tmp_index[2]
        return [term, tf_dicts, loc_dicts]

    with open(merge_path + merged_post_name, 'wb') as f:
        merged_line_count = 0
        big_terms = {}
        min_lines = min(post_files_lines)
        count_lines_0 = 1
        count_lines_1 = 1
        term_index_0 = read_next(files_paths[0])
        term_index_1 = read_next(files_paths[1])

        while count_lines_0 < post_files_lines[0] and count_lines_1 < post_files_lines[1]:
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
                        # terms_dict[term_index_0[0]] = {"line": merged_line_count,
                        #                                "freq": terms_dict[term_index_0[0],
                        #                                        "df": terms_dict[term_index_0[0]][1]]}
                    f.write('{}|{}|{}\n'.format(inverted_index[0], inverted_index[1], inverted_index[2]))
                    merged_line_count += 1
            else:
                f.write('{}|{}|{}\n'.format(inverted_index[0], inverted_index[1], inverted_index[2]))
                merged_line_count += 1

        if count_lines_0 < post_files_lines[0]:
            while count_lines_0 < post_files_lines[0]:  # - 1:
                f.write('{}|{}|{}\n'.format(term_index_0[0], term_index_0[1], term_index_0[2]))
                term_index_0 = read_next(files_paths[0])
                count_lines_0 += 1

        elif count_lines_1 < post_files_lines[1]:
            while count_lines_1 < post_files_lines[1]:  # - 1:
                f.write('{}|{}|{}\n'.format(term_index_1[0], term_index_1[1], term_index_1[2]))
                term_index_1 = read_next(files_paths[1])
                count_lines_1 += 1

    if is_final_posting:
        dict = terms_dict
    if 'C:\Users\\ronelhar\PycharmProjects\SEproject\Merge2\merge0' == merge_path + merged_post_name:
        print ' '
    merged_post_lines[merge_path + merged_post_name] = merged_line_count


def merge_terms_dict(dirs_dict, terms_dict):
    for directory in dirs_dict.keys():
        for term in dirs_dict[directory][1]:
            if not term in terms_dict:
                terms_dict[term] = [dirs_dict[directory][1][term][0], dirs_dict[directory][1][term][1]]
            else:
                terms_dict[term] = [terms_dict[term][0] + dirs_dict[directory][1][term][0],
                                    terms_dict[term][1] + dirs_dict[directory][1][term][1]]


def merge_cities_dict(dirs_dict, cities):
    for directory in dirs_dict.keys():
        for city in dirs_dict[directory][2]:
            if city in cities:
                cities[city].extend(dirs_dict[directory][2][city])
            else:
                cities[city] = dirs_dict[directory][2][city]


def merge_post_files_name_lines(dirs_dict, files_names, post_files_lines, to_stem):
    for directory in dirs_dict.keys():
        old_post_files_lines = dirs_dict[directory][0]
        for i in range(0, len(old_post_files_lines)):
            files_names.append(directory + "\\Posting" + str(i) if not to_stem else directory + "\\PostingS" + str(i))
            post_files_lines.append(old_post_files_lines[i])


def start_merge(files_names, post_files_lines, terms_dict, posting_path, to_stem):
    manager2 = multiprocessing.Manager()
    merged_post_lines = manager2.dict()
    merge_path = posting_path + "\\Merge" + '0' if not to_stem else posting_path + "\\sMerge" + '0'
    if not os.path.exists(merge_path):
        os.makedirs(merge_path)
    for i in range(0, len(files_names)):
        files_names[i] = posting_path + files_names[i]
    merge_count = 0
    processes = []
    while len(files_names) > 2:
        i = 0
        while i < len(files_names):
            if i + 1 < len(files_names):
                p = multiprocessing.Process(target=merge, args=(
                    [files_names[i], files_names[i + 1]], merge_path,
                    [post_files_lines[i], post_files_lines[i + 1]],
                    {}, {}, False, "\\merge" + str(i), merged_post_lines))
                processes.append(p)
                p.start()
            else:
                shutil.move(files_names[i], merge_path + "\\merge" + str(i))
                merged_post_lines[merge_path + "\\merge" + str(i)] = post_files_lines[i]
            i += 2
        i = 0
        for process in processes:
            process.join()
        processes = []
        merge_count += 1
        post_files_lines = []
        files_names = os.listdir(merge_path)

        for j in range(0, len(files_names)):
            files_names[j] = merge_path + '\\' + files_names[j]
            post_files_lines.append(merged_post_lines[files_names[j]])

        if len(files_names) <= 2:
            break

        merge_path = posting_path + '\\Merge' + str(merge_count) if not to_stem else posting_path + '\\sMerge' + str(
            merge_count)
        if not os.path.exists(merge_path):
            os.makedirs(merge_path)

    merge_path = posting_path + '\\FinalPost' if not to_stem else posting_path + '\\sFinalPost'
    if not os.path.exists(merge_path):
        os.makedirs(merge_path)
    manager = multiprocessing.Manager()
    shared_dict = manager.dict()
    p = multiprocessing.Process(target=merge, args=(
        [files_names[0], files_names[1]], merge_path,
        [merged_post_lines[files_names[0]], merged_post_lines[files_names[1]]],
        terms_dict, shared_dict, True, "\\Final_Post", merged_post_lines))
    p.start()
    p.join()


def posting_dicts_merge(dirs_dict, to_stem):
    print "merging dirs_dicts"
    cities_manager = multiprocessing.Manager()
    terms_manager = multiprocessing.Manager()
    files_names_manager = multiprocessing.Manager()
    post_files_lines_manager = multiprocessing.Manager()

    terms_dict = terms_manager.dict()
    cities = cities_manager.dict()
    files_names = files_names_manager.list()
    post_files_lines = post_files_lines_manager.list()

    p_terms = multiprocessing.Process(target=merge_terms_dict, args=(dirs_dict, terms_dict))
    p_terms.start()

    p_cities = multiprocessing.Process(target=merge_cities_dict, args=(dirs_dict, cities))
    p_cities.start()

    p_names_lines = multiprocessing.Process(target=merge_post_files_name_lines,
                                            args=(dirs_dict, files_names, post_files_lines,to_stem))
    p_names_lines.start()

    docs = {}
    languages = set()
    for dir in dirs_dict.keys():
        docs.update(dirs_dict[dir][4])
    for dir in dirs_dict.keys():
        for language in dirs_dict[dir][3]:
            languages.add(language)

    p_terms.join()
    p_cities.join()
    p_names_lines.join()

    return terms_dict, post_files_lines, cities, docs, languages
