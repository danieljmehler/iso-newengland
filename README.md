# iso-newengland

Download data from the `https://webservices.iso-ne.com/api/v1.1/hourlylmp/da/final/day/{day}/hour/{hr}` endpoint and output a JSON or CSV file for each hour of the dates specified.

## Usage

```bash
$ python3 iso_newengland.py --help
usage: iso-newengland [-h] [--start-date START_DATE] [--end-date END_DATE] [--username USERNAME] [--password PASSWORD] [--output-dir OUTPUT_DIR] [--csv]

options:
  -h, --help            show this help message and exit
  --start-date START_DATE
                        Date on which to start data collection (e.g., "20210301" for 03/01/2021)
  --end-date END_DATE   Date on which to end data collection (e.g., "20210301" for 03/01/2021)
  --username USERNAME   ISO New England username
  --password PASSWORD   ISO New England password
  --output-dir OUTPUT_DIR
                        Directory to output files
  --csv                 Save files as .CSV instead of .JSON
```

### Examples

To download a JSON file for EACH HOUR for EACH DAY IN SEPTEMBER 2023 and output the files to /Users/johndoe/data (if the directories do not exist, they will be created):

```bash
python3 iso_newengland.py --start-date "20230901" --end-date "20230930" --username "john.doe@email.com" --password 'MyP@$$w0rd01' --output-dir /Users/johndoe/data
```

JSON data will look like the following:

```json
{
    "HourlyLmps":{
        "HourlyLmp":[
            {
                "BeginDate":"2024-01-01T08:00:00.000-05:00",
                "Location":{
                    "@LocId":"321",
                    "@LocType":"NETWORK NODE",
                    "$":"UN.FRNKLNSQ13.810CC"
                },
                "LmpTotal":24.46,
                "EnergyComponent":24.63,
                "CongestionComponent":0,
                "LossComponent":-0.17
            },
            // ...
        ]
    }
}
```

To download a CSV file for EACH HOUR of APRIL 9, 2024 and output the files to /Users/johndoe/data (if the directories do not exist, they will be created):

```bash
python3 iso_newengland.py --start-date "20230409" --end-date "20230409" --username "john.doe@email.com" --password 'MyP@$$w0rd01' --output-dir /Users/johndoe/data --csv
```

CSV data will look like the following:

```csv
BeginDate,LocationID,LocationType,LocationName,LmpTotal,EnergyComponent,CongestionComponent,LossComponent
2024-01-01T13:00:00.000-05:00,321,NETWORK NODE,UN.FRNKLNSQ13.810CC,33.84,34.09,0,-0.25
2024-01-01T13:00:00.000-05:00,322,NETWORK NODE,UN.FRNKLNSQ13.811CC,33.84,34.09,0,-0.25
```
