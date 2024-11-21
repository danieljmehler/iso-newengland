import shutil
from isonewengland import collect
import os

target_dir = os.path.join(os.getcwd(), "target")

class TestIsoNewEngland:
    def setup_method(self):
        try:
            shutil.rmtree(target_dir)
        except Exception as e:
            print(e)

    def test_json(self):
        collect(start_date="20240101", end_date="20240103", username="danieljmehler@gmail.com", password="password32", output_dir=target_dir)
        assert os.path.exists(target_dir)
        for d in range(1, 4):
            day = str(d).zfill(2)
            for h in range(0, 24):
                hr = str(h).zfill(2)
                assert os.path.exists(os.path.join(target_dir, f"iso-newengland-hourlylmp-202401{day}-{hr}.json"))
    
    def test_csv(self):
        collect(start_date="20240101", end_date="20240103", username="danieljmehler@gmail.com", password="password32", output_dir=target_dir, convert_to_csv=True)
        assert os.path.exists(target_dir)
        for d in range(1, 4):
            day = str(d).zfill(2)
            for h in range(0, 24):
                hr = str(h).zfill(2)
                assert os.path.exists(os.path.join(target_dir, f"iso-newengland-hourlylmp-202401{day}-{hr}.csv"))
    
    def test_csv_aggregate_by_day(self):
        collect(start_date="20240101", end_date="20240103", username="danieljmehler@gmail.com", password="password32", output_dir=target_dir, aggregate_by="day", convert_to_csv=True)
        assert os.path.exists(target_dir)
        for d in range(1, 3):
            day = str(d).zfill(2)
            assert os.path.exists(os.path.join(target_dir, f"iso-newengland-hourlylmp-202401{day}.csv"))
    
    def test_csv_aggregate_by_month(self):
        collect(start_date="20230227", end_date="20230302", username="danieljmehler@gmail.com", password="password32", output_dir=target_dir, aggregate_by="month", convert_to_csv=True)
        assert os.path.exists(target_dir)
        assert os.path.exists(os.path.join(target_dir, f"iso-newengland-hourlylmp-202302.csv"))
        assert os.path.exists(os.path.join(target_dir, f"iso-newengland-hourlylmp-202303.csv"))
    
    def test_csv_aggregate_by_year(self):
        collect(start_date="20231231", end_date="20240101", username="danieljmehler@gmail.com", password="password32", output_dir=target_dir, aggregate_by="year", convert_to_csv=True)
        assert os.path.exists(target_dir)
        assert os.path.exists(os.path.join(target_dir, f"iso-newengland-hourlylmp-2023.csv"))
        assert os.path.exists(os.path.join(target_dir, f"iso-newengland-hourlylmp-2024.csv"))
    
    def test_csv_aggregate_by_all(self):
        collect(start_date="20231231", end_date="20240101", username="danieljmehler@gmail.com", password="password32", output_dir=target_dir, aggregate_by="all", convert_to_csv=True)
        assert os.path.exists(target_dir)
        assert os.path.exists(os.path.join(target_dir, f"iso-newengland-hourlylmp-20231231-20240101.csv"))
