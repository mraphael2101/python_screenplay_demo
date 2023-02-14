import pytest
from screenplay.pattern import Actor

from testlib.interactions import CallReqResApi


@pytest.mark.regression
def test_utilising_dual_abilities(http_library, browser) -> None:
    actor = Actor("Alex")
    actor.can_use(browser="Chrome")
    actor.can_use(http_library="requests")
    print("Actor has browser ability -> " + str(actor.has("browser")))
    print("Actor has api session ability -> " + str(actor.has("http_library")))


base_uri = "https://reqres.in"
base_uri_invalid = "https://fictitious"


@pytest.mark.regression
@pytest.mark.parametrize('end_point_variances', [base_uri + "/api/users?page=2",
                                                 base_uri_invalid + "/api/users?page=2",
                                                 ])
def test_end_points_with_params(http_library, end_point_variances: str) -> None:
    actor = Actor("Alex")
    actor.can_use(http_library=http_library)
    url = end_point_variances + "page=2"
    response = actor.calls(CallReqResApi(url))
    print(response)
    assert response.status_code == 200, "Response code received differs to expected 200"
    # print(response.text)  # Response as plain text
    json_resp = response.json()  # Response as json serialised format
    assert json_resp['total'] == 12, "Mismatch for total"
    assert (json_resp["data"][0]["email"]).endswith("reqres.in"), "Mismatch for Email domain"

