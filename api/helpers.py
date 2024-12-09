import json
import allure
import pytest
from jsonpath_ng import parse
from config import STATUS_CREATED
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
@allure.step("Create a resume")
def create_resume(api, data):
    payload = {
        "jobDescriptions": json.dumps(data.generate_job_description(1)),
        "resumeName": data.generate_resume_name(),
        "resume": json.dumps(data.generate_resume())
    }
    response = api.request("POST", "resumes/ats-review-text", json=payload)
    assert response.status_code == STATUS_CREATED, f"Unexpected status code: {response.status_code}"
    jsonpath_expr = parse(f"$..id")
    result = [match.value for match in jsonpath_expr.find(response.json())]
    if not result:
        pytest.fail("Attempt to create base resume failed")
    data.resume_valid_ids.extend(result)
    assert all(isinstance(item, int) for item in result), "Unacceptable resume id format"
    return result[0]

@allure.step("Create a base-resume")
def create_base_resume(api, data):
    payload = {
        "resumeName": data.generate_resume_name(),
        "resume": data.generate_resume()
    }
    #logger.info(payload)
    response = api.request("POST", "base-resumes", json=payload)
    assert response.status_code == STATUS_CREATED, f"Unexpected status code: {response.status_code}"
    jsonpath_expr = parse(f"$..id")
    result = [match.value for match in jsonpath_expr.find(response.json())]
    if not result:
        pytest.fail("Attempt to create base resume failed")
    data.base_resume_valid_ids.extend(result)
    assert all(isinstance(item, int) for item in result), "Unacceptable resume id format"
    return result[0]



def find_key_values(data, key_to_find):
    results = []
    if isinstance(data, dict):
        for key, value in data.items():
            if key == key_to_find:
                results.append(value)
            if isinstance(value, (dict, list)):
                results.extend(find_key_values(value, key_to_find))
    elif isinstance(data, list):
        for item in data:
            results.extend(find_key_values(item, key_to_find))
    return results


def find_key_values_(data, key_to_find):
    jsonpath_expr = parse(f"$..{key_to_find}")
    return [match.value for match in jsonpath_expr.find(data)]