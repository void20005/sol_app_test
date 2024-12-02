import json
import allure


@allure.step("Create a resume")
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
    # Check new vail id is present in the response
    assert "id" in response_data["data"][0], "Key 'id' not found in the response"
    assert isinstance(response_data["data"][0]["id"], int), "id is not an integer"
    # add new resumes ids into the list
    for item in response_data["data"]:
        data.resume_valid_ids.append(item["id"])
    return data.resume_valid_ids[0]

@allure.step("Create a base-resume")
def create_base_resume(api, data):
    """
    Helper function to create a base-resume and return its ID.
    """
    payload = {
        "resumeName": data.generate_resume_name(),
        "resume": data.generate_resume()
    }
    response = api.request("POST", "base-resumes", json=payload)
    assert response.status_code == 201, f"Unexpected status code: {response.status_code}"
    response_data = response.json()
    print(response_data['data']['id'])
    assert "id" in response_data['data'], "Key 'id' not found in the response"
    assert isinstance(response_data["data"]["id"], int), "id is not an integer"
    resume_id = response_data["data"]["id"]
    return resume_id