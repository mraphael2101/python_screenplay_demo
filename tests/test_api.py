import pytest
from screenplay.pattern import Actor

from testlib.interactions import CallReqResApi, Load
from testlib.pages import BtHomePage, ReqResApiModel


@pytest.mark.regression
def test_utilising_dual_abilities(http_library, browser) -> None:
    actor = Actor("Alex")
    actor.can_use(browser="Chrome")
    actor.can_use(http_library="requests")
    print("Actor has browser ability -> " + str(actor.has("browser")))
    print("Actor has api session ability -> " + str(actor.has("http_library")))


@pytest.mark.regression
def test_e2e_with_multiple_actors(browser, http_library) -> None:
    """
    Having two actors is a very powerful concept for end-to-end testing. This
    would be valuable as we could enact scenarios such as:
    User 1 places an order on the Amazon website via their Mobile Device
    User 2 logs into CRM and checks the status of the order placed by User 1 on their PC
    """
    mark = Actor("Mark")
    mark.can_use(browser=browser)
    mark.attempts_to(Load(BtHomePage.URL))

    john = Actor("John")
    john.can_use(http_library=http_library)
    response = john.calls(CallReqResApi("https://reqres.in/api/users?delay=3"))
    print(response)


@pytest.mark.regression
@pytest.mark.parametrize('end_point_variances', [ReqResApiModel.BASE_URI + "/api/users?page=2",
                                                 ReqResApiModel.BASE_URI_INVALID + "/api/users?page=2",
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

