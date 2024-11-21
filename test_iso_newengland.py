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
        collect(start_date="20240101", end_date="20240103", username="danieljmehler@gmail.com", password="password32", output_dir=target_dir, conver_to_csv=True)
        assert os.path.exists(target_dir)
        for d in range(1, 4):
            day = str(d).zfill(2)
            for h in range(0, 24):
                hr = str(h).zfill(2)
                assert os.path.exists(os.path.join(target_dir, f"iso-newengland-hourlylmp-202401{day}-{hr}.csv"))