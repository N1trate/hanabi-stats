import csv


def open_notes_stats(username):
    with open(f'../output/portraits/{username}_portrait.tsv', 'r', encoding='utf-8') as file:
        user_notes = []
        for line in file.readlines():
            user_notes.append(line.rstrip().split('\t'))
    for n in user_notes:
        try:
            return {n[0]: n[1] for n in user_notes[1:]}
        except IndexError:
            print(username, n)


def most_talkative(data):
    talk = {}
    for k, v in data.items():
        talk[k] = sum([int(r) for r in v.values()])
    return {k: v for k, v in sorted(talk.items(), key=lambda x: (-x[1]))}


def compare(stats1, stats2):
    num1 = len(stats1)
    inter = len(stats1.keys() & stats2.keys())
    return round(inter / num1 * 100, 2)


def save(data):
    with open(f'../output/vocabulary_intersection.tsv', 'w', encoding='utf-8', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(['Player', *data.keys()])
        for k, v in data.items():
            w.writerow([k, *v])


with open('../input/list_of_players_test.txt', 'r') as f:
    users = [line.rstrip() for line in f.readlines()]


notes_stats = {}
for u in users:
    notes_stats[u] = open_notes_stats(u)


all_p = {}
for k1, v1 in notes_stats.items():
    k1_p = []
    for k2, v2 in notes_stats.items():
        k1_p.append(compare(v1, v2))
        print(k1, k2)
        print(compare(v1, v2))
    all_p[k1] = k1_p

print(all_p)
save(all_p)

for p1, p2 in most_talkative(notes_stats).items():
    print(p1, p2)



