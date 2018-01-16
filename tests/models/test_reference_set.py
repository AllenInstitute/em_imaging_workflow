from development.models import ReferenceSet
import datetime

def test_str():
    ref_set = ReferenceSet(
        project_path="/path/to/project/lorem/ipsum")
    assert "/path/to/project/lorem/ipsum" == ref_set.project_path

def test_clean_acquisition_date():
    ref_set = ReferenceSet(
        project_path="/path/to/project/lorem/ipsum",
        acquisition_date=datetime.datetime.now())
    clean_date = ref_set.clean_acquisition_date()

    assert not ':' in clean_date
    assert not ' ' in clean_date
    assert not '-' in clean_date
    assert not '+' in clean_date
