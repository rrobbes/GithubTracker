import csv
import os

def get(config):

    weights = {}

    # add_minus_del has a min of 0
    # total contrib is add minus del + msglen / 5
    # bugfix is not boolean but int
    # refac is not boolean but int
    # merge and conflict words as int, as well as being merge commit
    if os.path.isfile(config['pathSpecialCommits']):
        with open(config['pathSpecialCommits']) as d_file:
            reader = csv.reader(d_file, quotechar='|')
            for line in reader:
                num, url, weight = line
                weights[url] = float(weight)


    with open(config["exportMissing"]) as data_file:
        with open(config['exportLost'], 'w') as csvfile:
            reader = csv.reader(data_file, quotechar='|')
            writer = csv.writer(csvfile, quotechar='|')
            index = 0
            for line in reader:
                if index > 0:
                    #print line
                    line = line[:-3]
                    #print line
                    url = line[4]
                    message = line[6]
                    msglen = len(message)
                    add_minus_del = line[-1]
                    line = line[:-1]
                    #print add_minus_del
                    bugfix = 0
                    refac = 0
                    merge = 0
                    if add_minus_del == "":
                        add_minus_del = "0"
                    add_minus_del = int(add_minus_del)
                    if add_minus_del < 0:
                        add_minus_del_pos = 0
                    else: add_minus_del_pos = add_minus_del
                    total_contrib = add_minus_del + (msglen / 5.0)
                    total_contrib_pos = add_minus_del_pos + (msglen / 5.0)
                    if url in weights:
                        total_contrib = total_contrib * weights[url]
                    if 'bug' in message or 'fix' in message:
                        bugfix = 1
                    if 'merg' in message or 'conflict' in message or 'Merg' in message:
                        merge = 1
                    if 'refac' in message or 'Refac' in message:
                        refac = 1
                    typ = line[3]
                    if typ == 'commit': commit = 1
                    else: commit = 0
                    if typ == 'comment': comment = 1
                    else: comment = 0
                    if typ == 'issue': issue = 1
                    else: issue = 0
                    line.extend([commit, comment, issue, merge, bugfix, refac, msglen, add_minus_del, total_contrib, total_contrib_pos])
                else:
                    line = line[:-4] + ['commit', 'comment', 'issue','merge_words','bugfix_words','refac_words', 'message_length', 'add_minus_del', 'total_contrib', 'total_contrib_pos']
                index += 1
                writer.writerow(line)

