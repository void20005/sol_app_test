import json
import pytest
import allure
import logging

from api.helpers import create_resume, create_base_resume, find_key_values
from config import PATH_DATA, STATUS_OK, STATUS_CREATED, STATUS_BAD_REQUEST, STATUS_UNPROCESSABLE_ENTITY
from tests.conftest import auth_api_data
from jsonpath_ng import parse


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)



@allure.feature("Resume Builder")
@allure.story("Fetch Resume Details - API-RB1.1")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.integration
@pytest.mark.api
def test_retry_fetch_resume_valid_id(auth_api_data):
    api, data = auth_api_data
    resume_id = create_resume(api, data)
    response = api.request("GET", f"resumes/retry/{resume_id}")
    assert response.status_code == STATUS_OK, f"Unexpected status code: {response.status_code}"
    jsonpath_expr = parse(f"$..status")
    result = [match.value for match in jsonpath_expr.find(response.json())]
    assert result == ["success"], "Resume fetch failed"



@allure.feature("Resume Builder")
@allure.story("Tailor Resume - API-RB2.1")
@pytest.mark.smoke
@pytest.mark.regression
def test_tailor_resume_valid_data(auth_api_data):
    qty_job_description = 3
    api, data = auth_api_data
    payload = {
        "jobDescriptions": data.generate_job_description(qty_job_description),
        "resume": data.generate_resume()
    }
    response = api.request("POST", "resumes/ats-review", json=payload)
    assert response.status_code == STATUS_CREATED, f"Unexpected status code: {response.status_code}"
    jsonpath_expr = parse(f"$..id")
    result = [match.value for match in jsonpath_expr.find(response.json())]
    data.resume_valid_ids.extend(result)
    assert len(result) == qty_job_description, "Qty tailored resumes is incorrect"
    assert all(isinstance(item, int) for item in result), "Unacceptable resume id format"


@allure.feature("Resume Builder")
@allure.story("Tailor Text Resume - API-RB3.1")
@pytest.mark.smoke
@pytest.mark.regression
def test_tailor_resume_text_valid_data(auth_api_data):
    api, data = auth_api_data
    create_resume(api, data)


@allure.feature("Resume Builder")
@allure.story("Tailor Resume to JobID - API-RB4.1")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.integration
def test_tailor_resume_particular_job_valid_data(auth_api_data):
    api, data = auth_api_data
    resume_id = create_base_resume(api, data)
    response = api.request("GET", "job-board/job-listings?page=1&take=1")
    assert response.status_code == STATUS_OK, f"Unexpected status code: {response.status_code}"
    jsonpath_expr = parse(f"$..id")
    result = [match.value for match in jsonpath_expr.find(response.json())]
    assert all(isinstance(item, int) for item in result), "Unacceptable Job Id format"
    if not result:
        pytest.fail('There are no jobs available')
    payload = {
        "jobId": result[0],
        "resumeId": resume_id
    }
    response = api.request("POST", "resumes/ats-review-base", json=payload)
    assert response.status_code == STATUS_CREATED, f"Unexpected status code: {response.status_code}"
    jsonpath_expr = parse(f"$.data.id")
    resume_id = [match.value for match in jsonpath_expr.find(response.json())]
    if not resume_id:
        pytest.fail('There are no resumes tailored')
    data.resume_valid_ids.extend(resume_id)
    jsonpath_expr = parse(f"$..resume")
    result = [match.value for match in jsonpath_expr.find(response.json())]
    assert result, "No resume returned"



@allure.feature("Resume Builder")
@allure.story("Tailor File-Based Resume - API-RB5.1")
@pytest.mark.smoke
@pytest.mark.regression
def test_submit_file_review(auth_api_data):
    api, data = auth_api_data
    file_path = f"{PATH_DATA}/sample_resume.pdf"
    with open(file_path, "rb") as file:
        files = {
            "jobDescriptions": (None, '["{data.generate_job_description(1)[0]}"]'),
            "resumeName": (None, f'"{data.generate_resume_name()}"'),
            "file": ("sample_resume.pdf", file, "application/pdf"),
        }
        response = api.request("POST", "resumes/ats-review-file", files=files)
    assert response.status_code == STATUS_CREATED, f"Unexpected status code: {response.status_code}"
    jsonpath_expr = parse(f"$..id")
    resume_id = [match.value for match in jsonpath_expr.find(response.json())][0]
    if not resume_id:
        pytest.fail('There are no resume tailored')
    data.resume_valid_ids.append(resume_id)
    jsonpath_expr = parse(f"$..status")
    status = [match.value for match in jsonpath_expr.find(response.json())][0]
    if not status:
        pytest.fail('Invalid answer body returned')
    assert status == 'pending', "No resume returned"



## !!!!no assertions on first and last pages yet
@allure.feature("Resume Builder")
@allure.story("Fetch resumes with pagination - API-RB6.1")
@pytest.mark.smoke
@pytest.mark.regression
def test_fetch_resumes_pagination(authorized_api):
    page = 1
    number_of_pages = 10
    order_by = 'createdAt'
    order = 'ASC'
    api = authorized_api
    response = api.request("GET", "resume-ats", params={"page": page, "take": number_of_pages, "orderBy": order_by, "order": order})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    response_data = response.json()
    items = response_data.get("data", [])
    logger.info(items)
    metadata = response_data.get("metadata", {}).get("pagination", {})
    assert len(items) <= number_of_pages, f"Expected at most {number_of_pages} resumes, got {len(items)}"
    assert metadata.get("page") == page, f"Unexpected page: {metadata.get('page')}"
    assert metadata.get("limit") == number_of_pages, f"Unexpected limit: {metadata.get('limit')}"
    assert metadata.get("hasNextPage") is not None, "Pagination metadata missing 'hasNextPage'"
    assert metadata.get("hasPreviousPage") is not None, "Pagination metadata missing 'hasPreviousPage'"
    jsonpath_expr = parse(f"$..{order_by}")
    sort_by_list = [match.value for match in jsonpath_expr.find(items)]
    sorted_sort_by_list = sorted(sort_by_list)
    logger.info(sort_by_list)
    logger.info(sorted_sort_by_list)
    if order == "DESC":
        sorted_sort_by_list = sorted_sort_by_list[::-1]
    assert sort_by_list == sorted_sort_by_list, f"Items are not sorted by {order_by} in {order} order"
    if metadata.get("hasNextPage"):
        next_page = page + 1
        response_next = api.request("GET", "resume-ats", params={"page": next_page, "take": number_of_pages, "orderBy": order_by, "order": order})
        assert response_next.status_code == 200, f"Expected 200, got {response_next.status_code}"
        next_items = response_next.json().get("data", [])
        assert items != next_items, "Next page items are identical to current page items"

@allure.feature("Resume Builder")
@allure.story("Fetch resumes statuses - API-RB7.1")
@pytest.mark.smoke
@pytest.mark.regression
def test_fetch_resumes_statuses(auth_api_data):
    api, data = auth_api_data
    resume_id_1 = create_resume(api, data)
    response = api.request("GET", "resume-ats/statuses", params={"ids": resume_id_1})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    response_data = response.json()
    for item in response_data.get("data", []):
        assert "id" in item, "Key 'id' not found in response"
        assert "status" in item, "Key 'status' not found in response"




@allure.feature("Resume Builder")
@allure.story("Fetch single resume by ID - API-RB8.1")
@pytest.mark.smoke
@pytest.mark.regression
def test_fetch_resume_by_id(auth_api_data):
    api, data = auth_api_data
    resume_id = create_resume(api, data)
    response = api.request("GET", f"resume-ats/{resume_id}")
    assert response.status_code == STATUS_OK, f"Unexpected status code: {response.status_code}"
    response_data = response.json()
    assert "id" in response_data.get("data", {}), "Key 'id' not found in the response"
    assert "resume" in response_data.get("data", {}), "'Resume' key not found in the response"


@allure.feature("Resume Builder")
@allure.story("Update resume details - API-RB9.1")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.integration
def test_update_resume(auth_api_data):
    api, data = auth_api_data
    resume_id = create_resume(api, data)
    new_resume_payload = data.generate_resume()
    payload = {
        "jobDescriptions": data.generate_job_description(1),
        "resumeName": data.generate_resume_name(),
        "resume": json.dumps(new_resume_payload)
    }
    response = api.request("PATCH", f"resume-ats/{resume_id}", json=payload)
    assert response.status_code == STATUS_OK, f"Unexpected status code: {response.status_code}"
    response = api.request("GET", f"resume-ats/{resume_id}")
    response_data = response.json()
    updated_resume = response_data.get("data", {}).get("resume")
    assert updated_resume, "Updated resume not found in the response"
    # Parse resume from the server response
    resume_string = ''.join(updated_resume[str(i)] for i in range(len(updated_resume)))
    updated_resume = json.loads(resume_string)
    assert updated_resume == new_resume_payload, "Resume update was not successful"


@allure.feature("Resume Builder")
@allure.story("Delete resume by ID - API-RB10.1")
@pytest.mark.smoke
@pytest.mark.regression
def test_delete_resume_by_id(auth_api_data):
    api, data = auth_api_data
    resume_id = create_resume(api, data)
    response = api.request("DELETE", f"resume-ats/{resume_id}")
    data.resume_valid_ids.remove(resume_id)
    assert response.status_code == STATUS_OK, f"Failed to delete resume {resume_id}"
    response = api.request("DELETE", f"resume-ats/{resume_id}")
    assert response.status_code == STATUS_BAD_REQUEST, f"Unexpected status code on second delete for {resume_id}"










