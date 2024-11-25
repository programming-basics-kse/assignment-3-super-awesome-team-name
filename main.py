import argparse


def get_args() -> dict:
    parser = argparse.ArgumentParser("Sample Program")
    parser.add_argument("filepath", type=str, help="Path to the file")
    parser.add_argument("-medals", action="store_true", required=True, help="Required argument")
    parser.add_argument("team",type=str, nargs="+", help="Name of the team")
    parser.add_argument("year", type=int, help="Year of the olympics")
    parser.add_argument("-output", "--output", type=str, help="Name of the output file")
    args = vars(parser.parse_args())
    return args

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

    if 1992 not in [int(x['year']) for x in data_list]:
        return f"There were no olympics games that year"

    team_list = ([x for x in data_list if int(x['year']) == user_input['year'] and x['team'] in " ".join(user_input['team'])]
                 + [x for x in data_list if int(x['year']) == user_input['year'] and x['noc'] in " ".join(user_input['team'])])

    if not team_list:
        return f"There are no {"".join(user_input['team'])} team in {user_input['year']} olympics games"

    return team_list

def  ten_medalists_summary(team: list) -> None:
    gold = [x for x in team if x['medal'] == 'Gold']
    silver = [x for x in team if x['medal'] == 'Silver']
    bronze = [x for x in team if x['medal'] == 'Bronze']

    for x, key in enumerate(gold + silver + bronze):
        if x < 10:
            print(f"{x + 1}: {key['name']} - {key['sport']} - {key['medal']}")
            continue
        break

    print(f"\nGold: {len(gold)}, Silver: {len(silver)}, Bronze: {len(bronze)}")

ten_medalists_summary(validation(get_data(), get_args()))