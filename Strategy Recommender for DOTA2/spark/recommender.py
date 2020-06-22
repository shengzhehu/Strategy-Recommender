from collections import Counter
from itertools import islice

class recommender():
    def cold_start(self, matches):
        hero_pool = []
        for i in range(len(matches['picks_bans'])):
            hero_pool += [k['hero_id'] for k in matches['picks_bans'][i] if k['is_pick'] == True]
        hero_dict = Counter(hero_pool)
        hero_dict = sorted(hero_dict.items(), key=lambda x:x[1],reverse=True)
        cold = [i[0] for i in hero_dict[:5]]
        return cold

    def combo(self, matches,input_list):
        hero_match_info = {}
        for i in range(len(matches['picks_bans'])):
            hero_match_info[matches['match_id'][i]] = ([k['hero_id'] for k in matches['picks_bans'][i] if k['is_pick'] == True], matches['radiant_win'][i])

        hero_matches = [i for i in hero_match_info.values() if all(x in i[0][:5] for x in input_list) or all(x in i[0][5:] for x in input_list)]

        teammates = {}
        enemies = {}
        for i in hero_matches:
            if input_list in i[0][:5] and i[1] == True:
                for j in i[0][:5]:
                    if j not in teammates:
                        teammates[j] = [0,1]
                    else:
                        teammates[j][0] += 1
                        teammates[j][1] += 1
            if input_list in i[0][:5] and i[1] != True:
                for j in i[0][:5]:
                    if j not in teammates:
                        teammates[j] = [0,1]
                    else:
                        teammates[j][1] += 1
            if input_list in i[0][5:] and i[1] == True:
                for j in i[0][5:]:
                    if j not in teammates:
                        teammates[j] = [0,1]
                    else:
                        teammates[j][1] += 1
            if input_list in i[0][5:] and i[1] != True:
                for j in i[0][5:]:
                    if j not in teammates:
                        teammates[j] = [0,1]
                    else:
                        teammates[j][0] += 1
                        teammates[j][1] += 1
        result = {}
        for k,v in teammates.items():
            if v[1] >= 5: # for ranking the heroes with same win rate
                result[k] = v[0]/v[1]
        result = sorted(result.items(),key=lambda x:x[1],reverse=True
        return result.keys()[:5]
