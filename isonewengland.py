import uuid
import aiohttp
import argparse
import asyncio
import csv
from datetime import datetime, timedelta
import json
import os

date_format = "%Y%m%d"


def write_file(obj: dict, output_dir: str, filename_suffix: str, convert_to_csv: bool = False):
    if not convert_to_csv:
        write_json(obj, output_dir=output_dir, filename_suffix=filename_suffix)
    else:
        write_csv(obj=obj, output_dir=output_dir,
                  filename_suffix=filename_suffix)


def write_json(obj: dict, output_dir: str, filename_suffix: str):
    print(
        f"Writing data to {output_dir}/iso-newengland-hourlylmp-{filename_suffix}.json")
    with open(os.path.join(output_dir, f"iso-newengland-hourlylmp-{filename_suffix}.json"), 'w') as f:
        f.write(json.dumps(obj))


def write_csv(obj: dict, output_dir: str, filename_suffix: str):
    print(
        f"Writing data to {output_dir}/iso-newengland-hourlylmp-{filename_suffix}.csv")
    # Convert JSON to CSV
    headers = ["id", "BeginDate", "LocationID", "LocationType", "LocationName",
               "LmpTotal", "EnergyComponent", "CongestionComponent", "LossComponent"]
    with open(os.path.join(output_dir, f"iso-newengland-hourlylmp-{filename_suffix}.csv"), 'w', newline='\n') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        # Write CSV
        csv_obj = [{
            "id": item["id"],
            "BeginDate": item["BeginDate"],
            "LocationID": item["Location"]['@LocId'],
            "LocationType": item["Location"]['@LocType'],
            "LocationName": item["Location"]['$'],
            "LmpTotal": item["LmpTotal"],
            "EnergyComponent": item["EnergyComponent"],
            "CongestionComponent": item["CongestionComponent"],
            "LossComponent": item["LossComponent"]
        } for item in obj["HourlyLmps"]["HourlyLmp"]]
        writer.writerows(csv_obj)


async def make_request(session: aiohttp.ClientSession, date: datetime, hr: str, username: str = None, password: str = None, output_dir: str = None, convert_to_csv: bool = False) -> dict:
    url = f"https://webservices.iso-ne.com/api/v1.1/hourlylmp/da/final/day/{date.strftime(date_format)}/hour/{hr}"
    # print(f"Getting data from {url}")
    async with session.get(url, auth=aiohttp.BasicAuth(username, password)) as response:
        # await asyncio.sleep(1)  # Simulating a delay
        data = await response.json()
        if 'HourlyLmps' in data and 'HourlyLmp' in data['HourlyLmps']:
            for hourlylmp in data['HourlyLmps']['HourlyLmp']:
                hourlylmp['id'] = str(uuid.uuid4())
        if output_dir:
            write_file(data, output_dir=output_dir,
                       filename_suffix=f"{date.strftime(date_format)}-{hr}", convert_to_csv=convert_to_csv)
        return {"date": date, "hr": hr, "data": data}


async def make_requests(date: datetime, username: str = None, password: str = None, output_dir: str = None, convert_to_csv: bool = None):
    aggregation = {"HourlyLmps": {"HourlyLmp": []}}
    async with aiohttp.ClientSession(headers={"Accept": "application/json"}) as session:
        tasks = [make_request(session, date, str(i).zfill(2), username, password,
                              output_dir=output_dir, convert_to_csv=convert_to_csv) for i in range(0, 24)]
        results = await asyncio.gather(*tasks)

        # If output_dir==None aka aggregate data by day/month/year/all
        # No need to aggregate data if aggregate_by==hour
        if not output_dir:
            for result in results:
                if 'HourlyLmps' not in result["data"] or 'HourlyLmp' not in result["data"]['HourlyLmps']:
                    print(f"Error aggregating data for date {result['date']} at hour {result['hr']}. HTTP GET response: {result['data']}. Inspect this error and determine if it is expected (e.g., if the error occurred at 2am on the Spring daylight savings change).")
                else:
                    aggregation["HourlyLmps"]["HourlyLmp"] += result["data"]["HourlyLmps"]["HourlyLmp"]
    return aggregation


def collect(start_date: str, end_date: str, username: str, password: str, output_dir: str = os.getcwd(), aggregate_by: str = "hour", convert_to_csv: bool = False):
    # Create output folder
    print(f"Creating output directory at {output_dir}")
    os.makedirs(output_dir, exist_ok=True)

    # Convert "YYYYMMDD" strings to datetime objects
    start = datetime.strptime(start_date, date_format)
    end = datetime.strptime(end_date, date_format)

    aggregation = {"HourlyLmps": {"HourlyLmp": []}}
    current_day = start
    # For each day
    while current_day <= end:
        # Bust of 24 async requests for each day (one async req per hour)
        current_day_data = asyncio.run(make_requests(current_day, username, password, output_dir=(
            None if aggregate_by != 'hour' else output_dir), convert_to_csv=(None if aggregate_by != 'hour' else convert_to_csv)))
        # Write 1 file per day
        if aggregate_by == "day":
            write_file(current_day_data, output_dir=output_dir,
                       filename_suffix=f"{current_day.strftime(date_format)}", convert_to_csv=convert_to_csv)
            aggregation = {"HourlyLmps": {"HourlyLmp": []}}
        # Otherwise, add data to aggregation
        else:
            aggregation["HourlyLmps"]["HourlyLmp"] += current_day_data["HourlyLmps"]["HourlyLmp"]

        # Increase "current_day" by 1 day
        current_day += timedelta(days=1)

        # If current_day is now the first day of a month
        if current_day.day == 1:
            # If current_day is 01/01/YYYY and we want to aggregate by year, save to file
            if current_day.month == 1 and aggregate_by == "year":
                write_file(aggregation, output_dir=output_dir, filename_suffix=str(
                    current_day.year - 1), convert_to_csv=convert_to_csv)
                # Reset aggregation dict
                aggregation = {"HourlyLmps": {"HourlyLmp": []}}
            # Else, if we are aggregating by month
            elif aggregate_by == "month":
                write_file(aggregation, output_dir=output_dir,
                           filename_suffix=f"{current_day.year}{str(current_day.month-1).zfill(2)}", convert_to_csv=convert_to_csv)
                # Reset aggregation dict
                aggregation = {"HourlyLmps": {"HourlyLmp": []}}

    # If there is data left in aggregation, need to write last month, last year, or all
    if len(aggregation["HourlyLmps"]["HourlyLmp"]) > 0:
        if aggregate_by == "all":
            filename_suffix = f"{start_date}-{end_date}"
        elif aggregate_by == "year":
            filename_suffix = current_day.year
        elif aggregate_by == "month":
            filename_suffix = f"{current_day.year}{str(current_day.month).zfill(2)}"
        write_file(aggregation, output_dir=output_dir,
                   filename_suffix=filename_suffix, convert_to_csv=convert_to_csv)


def main():
    parser = argparse.ArgumentParser(prog='isonewengland')
    parser.add_argument(
        "--start-date", help="Date on which to start data collection (e.g., \"20210301\" for 03/01/2021)")
    parser.add_argument(
        "--end-date", help="Date on which to end data collection (e.g., \"20210301\" for 03/01/2021)")
    parser.add_argument("--username", help="ISO New England username")
    parser.add_argument("--password", help="ISO New England password")
    parser.add_argument("--output-dir", help="Directory to output files")
    parser.add_argument("--aggregate-by", default="hour",
                        help="How to aggregate data. Default is \"hour\", meaning 1 file will be created for each hour of data. Other options are \"day\", \"month\", \"year\", and \"all\".")
    parser.add_argument("--csv", action="store_true",
                        help="Save files as .CSV instead of .JSON")
    args = parser.parse_args()
    collect(start_date=args.start_date, end_date=args.end_date, username=args.username, password=args.password,
            output_dir=args.output_dir, aggregate_by=args.aggregate_by, convert_to_csv=args.csv)


if __name__ == "__main__":
    main()
