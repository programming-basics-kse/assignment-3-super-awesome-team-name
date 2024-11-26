import argparse


def get_args() -> dict:
    parser = argparse.ArgumentParser("Sample Program")
    parser.add_argument("filepath", type=str, help="Path to the file")
    # parser.add_argument("-medals", action="get_noc", required=True, help="Required argument")
    # parser.add_argument("team",type=str, nargs="+", help="Name of the team")
    # parser.add_argument("year", type=int, help="Year of the olympics")
    parser.add_argument("-total", "--total", type=int, help="Total statistic of the year")
    parser.add_argument("-output", "--output", type=str, help="Name of the output file")
    args = vars(parser.parse_args())
    return args

def get_noc() -> dict:
    noc_dict = {}
    with open('noc.csv', 'r') as noc_file:
        for line in [x.replace("\n", "").split(',') for x in noc_file.readlines()][1:]:
            noc_dict[f"{line[0]}"] = f"{line[1]}"
    return noc_dict


def get_data() -> list[dict]:
    with open('athlete_events.tsv', "r") as file:

        data = []
        for line in [x.replace("\n", "").split("\t") for x in file.readlines()][1:]:
            data.append({
                "name": line[1],
                "team": line[6],
                "noc": line[7],
                "year": line[9],
                "sport": line[13],
                "medal": line[14]
            })

        return data

def validation(data_list: list[dict], user_input: dict) -> list or str:

    if user_input['year'] not in [int(x['year']) for x in data_list]:
        return f"There were no olympics games that year"

    team_list = ([x for x in data_list if int(x['year']) == user_input['year'] and x['team'] in " ".join(user_input['team'])]
                 + [x for x in data_list if int(x['year']) == user_input['year'] and x['noc'] in " ".join(user_input['team'])])

    if not team_list:
        return f"There are no {"".join(user_input['team'])} team in {user_input['year']} olympics games"

    return team_list

def  ten_medalists_summary(team: list) -> None: # Task 1 -medals arg
    gold = [x for x in team if x['medal'] == 'Gold']
    silver = [x for x in team if x['medal'] == 'Silver']
    bronze = [x for x in team if x['medal'] == 'Bronze']

    for x, key in enumerate(gold + silver + bronze):
        if x < 10:
            print(f"{x + 1}: {key['name']} - {key['sport']} - {key['medal']}")
            continue
        break

    print(f"\nGold: {len(gold)}, Silver: {len(silver)}, Bronze: {len(bronze)}")

# ten_medalists_summary(validation(get_data(), get_args()))

def total_statistic(data_list: list[dict], user_input: dict) -> None or str:
    if user_input['total'] not in [int(x['year']) for x in data_list]:
        return f"There were no olympics games that year"

    countries = {}

    for i in range(len(data_list)):
        if int(data_list[i]['year']) == user_input['total']:
            if data_list[i]['noc'] not in ["".join([*el]) for el in countries]:
                countries[f"{data_list[i]['noc']}"] = {
                        "Gold": 0,
                        "Silver": 0,
                        "Bronze": 0,
                        "Total": 0,
                        "Rate": 0
                    }
            if data_list[i]['medal'] != "NA":
                countries[f"{data_list[i]['noc']}"][data_list[i]['medal']] += 1
                countries[f"{data_list[i]['noc']}"]['Total'] += 1

                if data_list[i]['medal'] == "Gold": countries[f"{data_list[i]['noc']}"]['Rate'] += 3
                if data_list[i]['medal'] == "Silver": countries[f"{data_list[i]['noc']}"]['Rate'] += 2
                if data_list[i]['medal'] == "Bronze": countries[f"{data_list[i]['noc']}"]['Rate'] += 1

    countries = dict(sorted(countries.items(), key=lambda x: x[1]['Rate'], reverse=True))
    for key, value in countries.items():
        if value['Gold'] + value['Silver'] + value['Bronze']:
            try:
                print(f"{get_noc()[f'{key}']} || Gold: {value['Gold']} - Silver: {value['Silver']} - Bronze: {value['Bronze']}|"
                      f" Total: {value['Total']}")
            except:
                print(f"{f'{key}'} || Gold: {value['Gold']} - Silver: {value['Silver']} - Bronze: {value['Bronze']}|"
                      f" Total: {value['Total']}")

total_statistic(get_data(), get_args())

