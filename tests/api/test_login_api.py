import pytest
import allure


@allure.feature("Authentication")
@allure.story("Successful Authentication")
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("type", "API")
@pytest.mark.api
def test_successful_authentication(auth_token):
    """
    Test to verify that authentication works and a token is returned.
    """
    # Assertions
    assert auth_token is not None, "Authentication token is None"
    assert len(auth_token) > 0, "Authentication token is empty"
    allure.attach(
        auth_token,
        name="Authentication Token",
        attachment_type=allure.attachment_type.TEXT
    )