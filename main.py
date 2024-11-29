import argparse


def get_args() -> dict:
    parser = argparse.ArgumentParser("Sample Program")
    parser.add_argument("filepath", type=str, help="Path to the file")
    parser.add_argument("-medals", nargs="+", metavar="team_name year", help="Team name and the year at the end")
    parser.add_argument("-total", type=int, help="Total statistic of the year")
    parser.add_argument("-overall", nargs="+", metavar="team_name1 team_name2 ..." , help="List of countries names")
    parser.add_argument("-interactive", action='store_true', help="Interactive mode")
    parser.add_argument("-output", type=str, help="Name of the output file")
    args = vars(parser.parse_args())
    return args

def get_medals(args: dict) -> dict or str:
    if not args["medals"][-1].isdecimal(): return f"Please write a year at the end"
    args['team'] = args['medals'][:-1]
    args['year'] = int(args['medals'][-1])
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
                "place": line[11],
                "sport": line[13],
                "medal": line[14]
            })

        return data

def validation(data_list: list[dict], user_input: dict) -> list or bool:

    if user_input['year'] not in [int(x['year']) for x in data_list]:
        print(f"There were no olympics games that year")
        return False

    team_list = ([x for x in data_list if int(x['year']) == user_input['year'] and x['team'] in " ".join(user_input['team'])]
                 + [x for x in data_list if int(x['year']) == user_input['year'] and x['noc'] in " ".join(user_input['team'])])

    if not team_list:
        print(f"There were no {"".join(user_input['team'])} team in {user_input['year']} olympics games")
        return False

    return team_list

def ten_medalists_summary(team: list, output_file=None) -> None:
    if not team: return None
    gold = [x for x in team if x['medal'] == 'Gold']
    silver = [x for x in team if x['medal'] == 'Silver']
    bronze = [x for x in team if x['medal'] == 'Bronze']

    for x, key in enumerate(gold + silver + bronze):
        if x < 10:
            output = f"{x + 1}: {key['name']} - {key['sport']} - {key['medal']}\n"
            if output_file: output_file.write(output)
            print(output, end="")
            continue
        break

    summary = f"\nGold: {len(gold)}, Silver: {len(silver)}, Bronze: {len(bronze)}\n"

    if output_file: output_file.write(summary)
    print(summary)


def total_statistic(data_list: list[dict], user_input: dict, output_file=None) -> None:
    if user_input['total'] not in [int(x['year']) for x in data_list]:
        output = f"There were no olympics games that year\n"
        if output_file: output_file.write(output)
        print(output)

    countries = {}

    for i in range(len(data_list)):
        if int(data_list[i]['year']) == user_input['total']:
            if data_list[i]['noc'] not in ["".join([*el]) for el in countries]:
                countries[f"{data_list[i]['noc']}"] = \
                    {
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
                output = f"{get_noc()[f'{key}']} || Gold: {value['Gold']} - Silver: {value['Silver']} - Bronze: {value['Bronze']}| Total: {value['Total']}\n"
                if output_file: output_file.write(output)
                print(output, end="")

            except:
                output = f"{key} || Gold: {value['Gold']} - Silver: {value['Silver']} - Bronze: {value['Bronze']}| Total: {value['Total']}\n"
                if output_file: output_file.write(output)
                print(output, end="")


def country_data(data_list:list[dict], user_input: dict) -> dict:
    overall_dict = {}

    for element in data_list:

        if element['team'] in " ".join(user_input['overall']) or element['noc'] in " ".join(user_input['overall']):

            if element['team'] not in ["".join([*el]) for el in overall_dict]:
                overall_dict[element['team']] = {}


            if element['year'] not in overall_dict[element['team']]:
                overall_dict[element['team']][element['year']] = \
                {
                    "Gold": 0,
                    "Silver": 0,
                    "Bronze": 0,
                    "Total": 0,
                    "Rate": 0
                }

            if element['medal'] != "NA":
                overall_dict[element['team']][element['year']]['Total'] += 1
                overall_dict[element['team']][element['year']][element['medal']] += 1

                match element['medal']:
                    case "Gold": overall_dict[element['team']][element['year']]['Rate'] += 3
                    case "Silver": overall_dict[element['team']][element['year']]['Rate'] += 2
                    case "Bronze": overall_dict[element['team']][element['year']]['Rate'] += 1

    return overall_dict

def overall(data: dict, output_file=None) -> None:
    for key, element in data.items():
        element = sorted(element.items(), key=lambda x: x[1]['Rate'], reverse=True)[0]
        output = f"{key} — {element[0]} — Total: {element[1]['Total']}\n"
        if output_file: output_file.write(output)
        print(output, end="")


def interactive(data_list: list[dict], output_file=None) -> None:
    country = input("Enter a country name: ")

    output = {}
    for element in data_list:
        if country in element['team'] or country in element['noc']:
            if country not in output: output[country] = {}

            if element['year'] not in output[country]:
                output[country][element['year']] = {
                    "Gold": 0,
                    "Silver": 0,
                    "Bronze": 0,
                    "Total": 0,
                    "Rate": 0,
                    "Place": element['place']
                }

            if element['medal'] != 'NA':
                output[country][element['year']][element['medal']] += 1
                output[country][element['year']]['Total'] += 1

            match element['medal']:
                case "Gold": output[country][element['year']]['Rate'] += 3
                case "Silver": output[country][element['year']]['Rate'] += 2
                case "Bronze": output[country][element['year']]['Rate'] += 1

    for key, element in output.items():
        element = sorted(element.items(), key=lambda x: x[1]['Rate'], reverse=True)
        first_output = f"First | year: {sorted(dict(element).items(), key=lambda x: x[0])[0][0]}, place: {sorted(dict(element).items(), key=lambda x: x[0])[0][1]['Place']}\n"
        best_output = f"Best | {element[0][0]}, Total: {element[0][1]['Total']}\n"
        worst_output = f"Worst | {element[-1][0]}, Total: {element[-1][1]['Total']}\n"

        avg_output = (f"Average | Bronze: {round(sum([x[1]['Bronze'] for x in element]) / len(element))}\t"
                      f"Silver: {round(sum([x[1]['Silver'] for x in element]) / len(element))}\t"
                      f"Gold: {round(sum([x[1]['Gold'] for x in element]) / len(element))}\t")

        output = first_output + "\n" + best_output + worst_output + "\n" + avg_output
        print(output)

        if output_file: output_file.write(output)

def main():
    args = get_args()

    output_file = None
    if args['output']:
        output_file = open(args['output'], 'w')

    if args['total']:
        total_statistic(get_data(), args, output_file)
    elif args['medals']:
        ten_medalists_summary(validation(get_data(), get_medals(args)), output_file)
    elif args['overall']:
        overall(country_data(get_data(), args), output_file)
    elif args['interactive']:
        interactive(get_data(), output_file)
    else:
        print("Write -medals or -total or -overall")

    if output_file:
        output_file.close()

main()