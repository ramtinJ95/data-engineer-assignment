import argparse
import requests


class SmhiParser:
    """ Class to handle communication with and extract data from the SMHI Open API. """
    BASE_URL = "https://opendata-download-metobs.smhi.se/api"

    def __init__(self, suffix=".json"):
        self.suffix = suffix

    def _make_request(self, path=""):
        r = requests.get(self.BASE_URL + path + self.suffix)
        return r

    def check_connection(self):
        r = self._make_request()
        return r.status_code

    def get_list_of_parameters(self):
        r = self._make_request("/version/latest/parameter")
        if r is not None:
            try:
                data = r.json()["resource"]
                data = [(int(e['key']), e['title'], e['summary'])
                        for e in data]
                data.sort(key=lambda x: x[0])
                return data
            except (KeyError, ValueError) as e:
                print(f"Error parsing JSON: {e}")
                return []
        else:
            print("Failed to retrieve parameters.")
            return []

    def get_active_stations(self):
        r = self._make_request("/version/latest/parameter/2/station")
        if r is not None:
            try:
                data = r.json()["station"]
                data = [e['key'] for e in data if e['active'] == True]
                return data
            except (KeyError, ValueError) as e:
                print(f"Error parsing JSON: {e}")
                return []
        else:
            print("Failed to retrieve parameters.")
            return []

    def get_lowest_highest_temps_past_day_slow(self, active_stations):
        # TODO: have to use session for these requests
        all_station_values = []
        for station_id in active_stations:
            r = self._make_request(
                f"/version/1.0/parameter/2/station/{station_id}/period/latest-day/data")
            e = r.json()
            if e["value"]:
                station_data = (e['station']['name'],
                                float(e['value'][0]['value']))
                all_station_values.append(station_data)
        all_station_values.sort(key=lambda x: x[1])
        return all_station_values


def main():
    parser = argparse.ArgumentParser(
        description="""Script to extract data from SMHI's Open API""")
    parser.add_argument("--parameters", action="store_true",
                        help="List SMHI API parameters")
    parser.add_argument("--temperatures", action="store_true",
                        help="List highest and lowest temperature last day.")
    args = parser.parse_args()
    smhi_parser = SmhiParser()
    if args.parameters:
        list_of_parameters = smhi_parser.get_list_of_parameters()
        for parameter in list_of_parameters:
            print(f"{parameter[0]}, {parameter[1]} ({parameter[2]})")
    elif args.temperatures:
        data = smhi_parser.get_active_stations()
        result = smhi_parser.get_lowest_highest_temps_past_day_slow(data)
        print()
        print(f"Highest {result[-1][0], result[-1][1]}")
        print(f"Lowest {result[0][0], result[0][1]}")


if __name__ == "__main__":
    main()
