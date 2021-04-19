import csv
import py.calc as c


def get_players_list(username):
    with open(f'../temp/{username}_players.txt', 'r') as f:
        return [line.rstrip() for line in f.readlines()]


def get_players_dict(username, players):
    results = {}
    for p in players:
        main_stats, list_easy, list_null, list_sd, list_dd = c.group_stats_by_eff(username)
        p_wins = c.get_wins(get_filtered_by_player(p, main_stats))
        p_losses = c.get_losses(get_filtered_by_player(p, main_stats))
        p_total = p_wins + p_losses
        p_ratio = c.p(p_wins, p_losses)
        # p_w_ratio = c.p(p_wins, p_total)
        # p_l_ratio = c.p(p_losses, p_total)
        ms = len(main_stats)
        easy_ratio, null_ratio, sd_ratio, dd_ratio = c.p(len(list_easy), ms), c.p(len(list_null), ms),\
                                                     c.p(len(list_sd), ms), c.p(len(list_dd), ms)
        results[p] = {'wl': p_ratio, 'total': p_total, 'easy': easy_ratio, 'null': null_ratio,
                      'sd': sd_ratio, 'dd': dd_ratio}
        # print(results.items())
        # for k, v in results.items():
        #     print(k, v)
    # print(list(reversed(sorted(results.items(), key=lambda item: item[0]))))
    # return list(reversed(sorted(results.items(), key=lambda item: item[0])))
    return {k: v for k, v in sorted(results.items(), key=lambda item: item[1]['wl'], reverse=True)}


def get_filtered_by_player(player, stats):
    return [row for row in stats if player in row.players]


def save_players_dict(username, data):
    with open(f'../output/{username}_wl_by_players.tsv', 'w', newline='') as file:
        w = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow([
            'Player name', 'W/L(%)', 'Total(#)', 'Easy', 'Null', 'Single dark', 'Double dark']
        )
        for k, v in data.items():
            w.writerow([
                k,
                v['wl'],
                v['total'],
                v['easy'],
                v['null'],
                v['sd'],
                v['dd']
            ])
