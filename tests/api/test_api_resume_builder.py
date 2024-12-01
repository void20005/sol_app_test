import json
import pytest
import allure
from config import PATH_DATA
from tests.conftest import auth_api_data


def create_resume(api, data):
    """
    Helper function to create a resume and return its ID.
    """
    payload = {
        "jobDescriptions": json.dumps(data.generate_job_description(1)),
        "resumeName": data.generate_resume_name(),
        "resume": json.dumps(data.generate_resume())
    }
    response = api.request("POST", "resumes/ats-review-text", json=payload)
    assert response.status_code == 201, f"Unexpected status code: {response.status_code}"
    response_data = response.json()
    assert len(response_data["data"]) > 0, "No tailored resume returned"

    for item in response_data["data"]:
        data.resume_valid_ids.append(item["id"])
    return data.resume_valid_ids[0]

def create_base_resume(api, data):
    """
    Helper function to create a resume and return its ID.
    """
    payload = {
        "resumeName": data.generate_resume_name(),
        "resume": data.generate_resume()
    }
    response = api.request("POST", "base-resumes", json=payload)
    assert response.status_code == 201, f"Unexpected status code: {response.status_code}"
    response_data = response.json()
    resume_id = response_data["data"]["id"]
    print(f"Extracted Resume ID: {resume_id}")
    #data.resume_valid_ids.append(resume_id)

    return resume_id

@allure.feature("Resume Builder")
@allure.story("Fetch Resume Details - RB1.1")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.integration
@pytest.mark.api
def test_retry_fetch_resume_valid_id(auth_api_data):
    """
    fetching resume details with valid ID.
    """
    api, data = auth_api_data
    resume_id = create_resume(api, data)
    response = api.request("GET", f"resumes/retry/{resume_id}")
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    assert response.json()["data"]["status"] == "success", "Resume fetch failed"




@allure.feature("Resume Builder")
@allure.story("Tailor Resume - RB2.1")
@pytest.mark.smoke
@pytest.mark.regression
def test_tailor_resume_valid_data(auth_api_data):
    """
    tailoring a resume with valid job descriptions.
    """
    api, data = auth_api_data
    payload = {
        "jobDescriptions": data.generate_job_description(1),
        "resume":data.generate_resume()
    }
    response = api.request("POST", "resumes/ats-review", json=payload)
    assert response.status_code == 201, f"Unexpected status code: {response.status_code}"
    assert len(response.json()["data"]) > 0, "No tailored resume returned"
    for i in response.json()["data"]:
        data.resume_valid_ids.append(i["id"])


@allure.feature("Resume Builder")
@allure.story("Tailor Text Resume - RB3.1")
@pytest.mark.smoke
@pytest.mark.regression
def test_tailor_resume_text_valid_data(auth_api_data):
    """
    tailoring a text resume with valid job descriptions.
    """
    api, data = auth_api_data
    create_resume(api, data)


@allure.feature("Resume Builder")
@allure.story("Tailor Resume to JobID- RB4.1")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.integration
def test_tailor_resume_particular_job_valid_data(auth_api_data):
    """
    tailoring a text resume with particular valid job id.
    """
    api, data = auth_api_data
    resume_id = create_base_resume(api, data)
    print(resume_id)
    response = api.request("GET", "job-board/job-listings?page=1&take=1")
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    job_id = response.json()["data"][0]["id"]
    print(job_id)
    payload = {
        "jobId": job_id,
        "resumeId": resume_id
    }
    response = api.request("POST", "resumes/ats-review-base", json = payload)
    response_resume_id = response.json()["data"]["id"]
    print(response_resume_id)
    assert response.status_code == 201, f"Unexpected status code: {response.status_code}"
    assert len(response.json()["data"]) > 0, "No tailored resume returned"
    data.resume_valid_ids.append(response_resume_id)


@allure.feature("Resume Builder")
@allure.story("Submit File-Based Review - RB5.1")
@pytest.mark.smoke
@pytest.mark.regression
def test_submit_file_review(auth_api_data):
    """
    Submit file-based resume review with valid parameters and file.
    """
    api, data = auth_api_data
    payload = {"jobDescriptions": data.generate_job_description(1), "resumeName": data.generate_resume_name()}
    file_path = f"{PATH_DATA}/sample_resume.pdf"    # path to resume file
    with open(file_path, "rb") as file:
        files = {
            "jobDescriptions": (None, f'["{data.generate_job_description(1)[0]}"]'),
            "resumeName": (None, f'"{data.generate_resume_name()}"'),
            "file": ("sample_resume.pdf", file, "application/pdf"),
        }
        print(files['resumeName'])
        print(files['jobDescriptions'])
        response = api.request("POST", "resumes/ats-review-file", files=files)
        print(response)
    assert response.status_code == 201, f"Unexpected status code: {response.status_code}"
    response_data = response.json()
    assert "data" in response_data, "Key 'data' not found in response"
    assert len(response_data["data"]) > 0, "No data in response"
    print(f"Resume ID: {response_data["data"][0]['id']}")
    data.resume_valid_ids.append(response_data["data"][0]["id"])


@allure.feature("Resume Builder")
@allure.story("Fetch resumes with pagination - RB6.1")
@pytest.mark.smoke
@pytest.mark.regression
def test_fetch_resumes_pagination(authorized_api):
    """
    Fetch resumes with pagination
    """
    api = authorized_api
    response = api.request("GET", "resume-ats", params={"page": 1, "take": 10, "orderBy": "createdAt", "order": "ASC"})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"


@allure.feature("Resume Builder")
@allure.story("Fetch resumes statuses - RB7.1")
@pytest.mark.smoke
@pytest.mark.regression
def test_fetch_resumes_statuses(auth_api_data):
    """
    Fetch resumes statuses
    """
    api, data = auth_api_data
    resume_id_1 = create_resume(api, data)
    response = api.request("GET", "resume-ats/statuses", params={"ids": resume_id_1})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"


@allure.feature("Resume Builder")
@allure.story("Fetch single resume by ID - RB8.1")
@pytest.mark.smoke
@pytest.mark.regression
def test_fetch_resume_by_id(auth_api_data):
    """
    Fetch single resume by ID
    """
    api, data = auth_api_data
    resume_id = create_resume(api, data)
    response = api.request("GET", f"resume-ats/{resume_id}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"














@allure.feature("Resume Builder")
@allure.story("Retry Fetch Resume Details - RB1.2")
@pytest.mark.regression
@pytest.mark.api
def test_retry_fetch_resume_invalid_id(auth_api_data):
    """
    fetching resume details with invalid ID.
    """
    api, data = auth_api_data
    response = api.request("GET", f"resumes/retry/{data.generate_resume_invalid_id()}")
    assert response.status_code == 400, f"Unexpected status code: {response.status_code}"
    assert response.json()["message"] == "error in retry", "Expected error in response"


@allure.feature("Resume Builder")
@allure.story("Retry Fetch Resume Details - RB1.3")
@pytest.mark.regression
@pytest.mark.api
def test_retry_fetch_resume_nonexistent_id(auth_api_data):
    """
    fetching resume details with non-existent ID.
    """
    api, data = auth_api_data
    response = api.request("GET", f"resumes/retry/{data.generate_resume_non_existent_id()}")
    assert response.status_code == 400, f"Unexpected status code: {response.status_code}"
    assert response.json()["message"] == "error in retry", "Error message mismatch"



@allure.feature("Resume Builder")
@allure.story("Tailor Resume - RB2.2")
@pytest.mark.regression
def test_tailor_resume_empty_body(authorized_api):
    """
    tailoring a resume with empty body.
    """
    payload = {
        #"jobDescriptions": data.job_description,
        #"resume":data.resume
    }
    response = authorized_api.request("POST", "resumes/ats-review", json=payload)
    assert response.status_code == 422, f"Unexpected status code: {response.status_code}"
    assert response.json()["errors"][0] == "jobDescriptions: must be a valid string", "The response is not valid"
    assert response.json()["errors"][1] == "jobDescriptions should be a non-empty array", "The response is not valid"



@allure.feature("Resume Builder")
@allure.story("Tailor Resume - RB2.3")
@pytest.mark.regression
def test_tailor_resume_resume_missing(auth_api_data):
    """
    tailoring a resume without resume in the body.
    """
    api, data = auth_api_data
    payload = {
        "jobDescriptions": data.generate_job_description(1)
        #"resume":data.resume
    }
    response = api.request("POST", "resumes/ats-review", json=payload)
    assert response.status_code == 400, f"Unexpected status code: {response.status_code}"
    assert response.json()["message"] == "Resume is required", "The response is not valid"
    if "data" in response.json() :
        for i in response.json()["data"]:
            data.resume_valid_ids.append(i["id"])
        print(data.resume_valid_ids)


@allure.feature("Resume Builder")
@allure.story("Tailor Resume - RB2.4")
@pytest.mark.regression
def test_tailor_resume_missed_job_description(auth_api_data):
    """
    tailoring a resume without jobDescription.
    """
    api, data = auth_api_data
    payload = {
        #"jobDescriptions": data.job_description,
        "resume":data.generate_resume()
    }
    response = api.request("POST", "resumes/ats-review", json=payload)
    assert response.status_code == 422, f"Unexpected status code: {response.status_code}"
    assert response.json()["errors"][0] == "jobDescriptions: must be a valid string", "The response is not valid"
    assert response.json()["errors"][1] == "jobDescriptions should be a non-empty array", "The response is not valid"
    if "data" in response.json() :
        for i in response.json()["data"]:
            data.resume_valid_ids.append(i["id"])







