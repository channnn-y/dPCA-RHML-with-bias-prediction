import os
import re
import numpy as np
import io


def freq(filename):
    fc = {}
    fr = {}
    relation = {}  
    count = {}
    try:
        fl = io.open(filename, encoding='UTF-16')
        lines = [line for line in fl.readlines()]
    except:
        try:
            fl = open(filename, encoding='UTF-8')
            lines = [line for line in fl.readlines()]
        except:
            fl = open(filename)
            lines = [line for line in fl.readlines()]

    le = {}
    for li in lines[1:]:
        sline = li.split("\t")

        for i in sline:
            if re.search('[\d]', i):
                continue
            else:
                sline.remove(i)
                print(sline)
        le['len'] = le.get('len', len(sline))
        indices = le['len']
        if len(sline) == le['len']:
            for index in range(indices):
                tag = re.match('\d', sline[index])
                if tag!= None:
                    tindex = index
                    break
            value = np.float(sline[tindex + 6])  
            keys = sline[tindex + 9].split('=>')  
            for i in range(len(keys)):
                try:
                    keys[i] = keys[i].split(':')[1]
                    keys[i] = keys[i].split('\n')[0]
                    no = True
                except:
                    no = False
            if no:
                for i in range(len(keys)):
                    fc[keys[i]] = fc.get(keys[i], 0) + value
                    relation[keys[i]] = relation.get(keys[i], [])
                    count[keys[i]] = count.get(keys[i], 1) + 1
                    try:
                        nextele = keys[i + 1]
                        isexit = False
                        for m in relation[keys[i]]:
                            if m == nextele:
                                isexit = True
                        relation[nextele] = relation.get(nextele, [])
                        for n in relation[nextele]:
                            if n == keys[i]:
                                isexit = True
                        if isexit == False:
                            relation[keys[i]].append(nextele)
                    except:
                        pass

    # 求总频率
    vals = list(fc.values())
    # print(vals)
    summary = 0
    fr.update(fc)
    for i in vals:
        summary = summary + i
    kys = fc.keys()
    for i in kys:
        fc[i] = fc.get(i) / summary
    return fc, fr, relation, count


def freqs(dirs):
    filenames = os.listdir(dirs)
    results = []
    details = []
    rels = []
    for filename in filenames:
        result, detail, rel, count = freq(os.path.join(dirs, filename)) 
        details.append(detail)
        rels.append(rel)
    return results, details, rels, count


def handleFreq(source, save_dir):
    rs, de, relt, counts = freqs(source)
    files = os.listdir(source)
    num = 0
    f3 = open(os.path.join(save_dir, files[num].split('.')[0] + '_count.txt'), 'w')  
    for cs in counts.keys():
        f3.write(cs)
        f3.write(" ")
        f3.write(str(counts[cs]))
        f3.write("\n")
    for i, m, p in zip(rs, de, relt):
        f = open(os.path.join(save_dir, files[num].split('.')[0] + '_resut.txt'), 'w')  
        f2 = open(os.path.join(save_dir, files[num].split('.')[0] + '_relation.txt'), 'w')  

        for j in i.keys():
            f.write(j)
            f.write(" ")
            f.write(str(m[j]))
            f.write(" ")
            f.write(str(i[j]))
            f.write('\n')
        for q in p.keys():
            if p[q]!= []:
                for w in p[q]:
                    f2.write(q)
                    f2.write(" ")
                    f2.write(w)
                    f2.write("\n")
        num = num + 1
        f.close()
        f2.close()

#
handleFreq(r'/file_path_to_your_shortest_pathways_file/', r'/file_path_to_save_your_frequency_resut/')