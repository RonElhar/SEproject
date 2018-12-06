import linecache
import os
import shutil
import Parse
import multiprocessing


def merge(files_paths, merge_path, post_files_lines, terms_dicts, shared_dict, is_final_posting, merged_post_name,
          merged_post_lines):
    files_line = {files_paths[0]: 0, files_paths[1]: 0}

    def read_next(file_path):
        line = linecache.getline(file_path, files_line[file_path] + 1).replace('\n', '')
        files_line[file_path] += 1
        tmp_index = line.split('|')
        term = tmp_index[0]
        tf_dicts = tmp_index[1]
        return [term, tf_dicts]

    with open(merge_path + merged_post_name, 'wb') as f:
        merged_line_count = 0
        big_terms = {}
        min_lines = min(post_files_lines)
        count_first_file_lines = 1
        count_second_file_lines = 1
        first_file_index = read_next(files_paths[0])
        second_file_index = read_next(files_paths[1])

        while count_first_file_lines < post_files_lines[0] and count_second_file_lines < post_files_lines[1]:
            inverted_index = []
            if first_file_index[0] < second_file_index[0]:
                inverted_index = [first_file_index[0], first_file_index[1]]
                first_file_index = read_next(files_paths[0])
                count_first_file_lines += 1

            elif first_file_index[0] == second_file_index[0]:
                inverted_index = [first_file_index[0], "{}{}".format(first_file_index[1], second_file_index[1])]
                first_file_index = read_next(files_paths[0])
                count_first_file_lines += 1
                second_file_index = read_next(files_paths[1])
                count_second_file_lines += 1

            else:
                inverted_index = [second_file_index[0], second_file_index[1]]
                second_file_index = read_next(files_paths[1])
                count_second_file_lines += 1
            if is_final_posting:
                if Parse.isWord(inverted_index[0]) and inverted_index[0].isupper() and \
                        (inverted_index[0].lower() in terms_dicts[0] or
                                 inverted_index[0].lower() in terms_dicts[1] or
                                 inverted_index[0].lower() in terms_dicts[2] or
                                 inverted_index[0].lower() in terms_dicts[3]):
                    big_terms[inverted_index[0].lower()] = inverted_index[1]
                else:
                    term = inverted_index[0]
                    shared_dict[term] = [merged_line_count, 0, 0]
                    for i in range(0, len(terms_dicts)):
                        if term in terms_dicts[i]:
                            shared_dict[term] = [shared_dict[term][0], shared_dict[term][1] + \
                                                 terms_dicts[i][term][0],
                                                 shared_dict[term][2] + terms_dicts[i][term][1]]
                    if term in big_terms:
                        inverted_index[1] = '{}{}'.format(inverted_index[1], big_terms[term])
                        for i in range(0, len(terms_dicts)):
                            if term.upper() in terms_dicts[i]:
                                shared_dict[term] = [shared_dict[term][0], shared_dict[term][1] + \
                                                     terms_dicts[i][term.upper()][0],
                                                     shared_dict[term][2] + terms_dicts[i][term.upper()][1]]
                        # print term.upper()
                        big_terms.pop(term)
                    if inverted_index[0] == 'MOSCOW':
                        print '{}|{}|{}\n'.format(inverted_index[0], inverted_index[1])
                    f.write('{}|{}\n'.format(inverted_index[0], inverted_index[1]))
                    merged_line_count += 1

            else:
                f.write('{}|{}\n'.format(inverted_index[0], inverted_index[1]))
                merged_line_count += 1

        count_lines = 0
        post_file_line = 0
        term_index = ''
        path_index = -1
        if count_first_file_lines < post_files_lines[0]:
            count_lines = count_first_file_lines
            post_file_line = post_files_lines[0]
            term_index = first_file_index
            path_index = 0
        elif count_second_file_lines < post_files_lines[1]:
            count_lines = count_second_file_lines
            post_file_line = post_files_lines[1]
            term_index = second_file_index
            path_index = 1

        while count_lines < post_file_line:
            inverted_index = [term_index[0], term_index[1]]
            term_index = read_next(files_paths[path_index])
            count_lines += 1
            if is_final_posting:
                if Parse.isWord(inverted_index[0]) and inverted_index[0].isupper() and \
                        (inverted_index[0].lower() in terms_dicts[0] or
                                 inverted_index[0].lower() in terms_dicts[1] or
                                 inverted_index[0].lower() in terms_dicts[2] or
                                 inverted_index[0].lower() in terms_dicts[3]):
                    big_terms[inverted_index[0].lower()] = inverted_index[1]
                else:
                    term = inverted_index[0]
                    shared_dict[term] = [merged_line_count, 0, 0]
                    for i in range(0, len(terms_dicts)):
                        if term in terms_dicts[i]:
                            shared_dict[term] = [shared_dict[term][0], shared_dict[term][1] + \
                                                 terms_dicts[i][term][0],
                                                 shared_dict[term][2] + terms_dicts[i][term][1]]
                    if term in big_terms:
                        inverted_index[1] = '{}{}'.format(inverted_index[1], big_terms[term])
                        for i in range(0, len(terms_dicts)):
                            if term.upper() in terms_dicts[i]:
                                shared_dict[term] = [shared_dict[term][0], shared_dict[term][1] + \
                                                     terms_dicts[i][term.upper()][0],
                                                     shared_dict[term][2] + terms_dicts[i][term.upper()][1]]
                        # print term.upper()
                        big_terms.pop(term)
                    if inverted_index[0] == 'MOSCOW':
                        print '{}|{}|{}\n'.format(inverted_index[0], inverted_index[1])

                    f.write('{}|{}\n'.format(inverted_index[0], inverted_index[1]))
                    merged_line_count += 1
            else:
                f.write('{}|{}\n'.format(inverted_index[0], inverted_index[1]))
                merged_line_count += 1
    print big_terms
    print len(big_terms)
    print merged_line_count
    merged_post_lines[merge_path + merged_post_name] = merged_line_count


def start_merge(files_names, post_files_lines, terms_dicts, posting_path, to_stem):
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
        terms_dicts, shared_dict, True, "\\Final_Post", merged_post_lines))
    p.start()
    p.join()
    return shared_dict
