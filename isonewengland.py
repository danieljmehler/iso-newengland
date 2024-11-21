import argparse
import base64
import csv
from datetime import datetime, timedelta
import json
import os
import urllib.request

date_format = "%Y%m%d"

def write_json(obj: dict, output_dir: str, filename_suffix: str):
    with open(os.path.join(output_dir, f"iso-newengland-hourlylmp-{filename_suffix}.json"), 'w') as f:
            f.write(obj)

def write_csv(obj: dict, output_dir: str, filename_suffix: str):
    # Convert JSON to CSV
    headers = ["BeginDate", "LocationID", "LocationType", "LocationName", "LmpTotal", "EnergyComponent", "CongestionComponent", "LossComponent"]
    with open(os.path.join(output_dir, f"iso-newengland-hourlylmp-{filename_suffix}.csv"), 'w', newline='\n') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        # Write CSV
        csv_obj = [{
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

def collect(start_date: str, end_date: str, username: str, password: str, output_dir: str = os.getcwd(), aggregate_by: str = None, convert_to_csv: bool = False):
    # Create output folder
    os.makedirs(output_dir, exist_ok=True)

    # Convert "YYYYMMDD" strings to datetime objects
    start = datetime.strptime(start_date, date_format)
    end = datetime.strptime(end_date, date_format)

    # base64 encode username:password
    auth_bytes = base64.urlsafe_b64encode(bytes(f"{username}:{password}", 'utf-8'))

    aggragation = {"HourlyLmps": {"HourlyLmp": []}}
    current = start
    # For each day
    while current <= end:
        # For each hour 00-23
        for i in range(0, 24):
            hr = str(i).zfill(2)  # Pad with zeros to 2 characters
            url = f"https://webservices.iso-ne.com/api/v1.1/hourlylmp/da/final/day/{current.strftime(date_format)}/hour/{hr}"
            req = urllib.request.Request(url)
            req.add_header("Authorization", f"Basic {auth_bytes.decode('utf-8')}")
            req.add_header("Accept", "application/json")
            resp = None
            with urllib.request.urlopen(req) as response:
                resp = response.read().decode('utf-8')
            if not convert_to_csv:
                write_json(obj=json.loads(resp), output_dir=output_dir, filename_suffix=f"{current.strftime(date_format)}-{hr}")
            else:
                write_csv(obj=json.loads(resp), output_dir=output_dir, filename_suffix=f"{current.strftime(date_format)}-{hr}")
        # Increase "current" by 1 day
        current += timedelta(days=1)
                    
                    

def main():
    print("MAIN FN CALLED")
    parser = argparse.ArgumentParser(prog='iso-newengland')
    parser.add_argument("--start-date", help="Date on which to start data collection (e.g., \"20210301\" for 03/01/2021)")
    parser.add_argument("--end-date", help="Date on which to end data collection (e.g., \"20210301\" for 03/01/2021)")
    parser.add_argument("--username", help="ISO New England username")
    parser.add_argument("--password", help="ISO New England password")
    parser.add_argument("--output-dir", help="Directory to output files")
    parser.add_argument("--aggregate-by", default="hour", help="How to aggregate data. Default is \"hour\", meaning 1 file will be created for each hour of data. Other options are \"day\", \"month\", \"year\", and \"all\".")
    parser.add_argument("--csv", action="store_true", help="Save files as .CSV instead of .JSON")
    args = parser.parse_args()
    collect(start_date=args.start_date, end_date=args.end_date, username=args.username, password=args.password, output_dir=args.output_dir, aggregate_by=args.aggregate_by, convert_to_csv=args.csv)

if __name__ == "__main__":
    main()