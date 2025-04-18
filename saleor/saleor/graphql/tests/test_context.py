from unittest import mock

import graphene
from django.utils import timezone

from ..context import clear_context, get_context_value
from ..core.dataloaders import DataLoader
from .utils import get_graphql_content

QUERY_ORDER_BY_ID = """
query orderById($id: ID!) {
  order(id: $id) {
    lines {
      totalPrice {
        __typename
      }
    }
  }
}
"""


@mock.patch(
    "saleor.plugins.tests.sample_plugins.SampleAuthorizationPlugin.authenticate_user"
)
def test_user_is_cached_on_request(
    mocked_authenticate_user, api_client, order_with_lines, settings, staff_user
):
    """Test the edge case when user isn't cached due to multiple Promises waiting."""
    # given
    settings.PLUGINS = ["saleor.plugins.tests.sample_plugins.SampleAuthorizationPlugin"]
    mocked_authenticate_user.return_value = staff_user
    order = order_with_lines
    order_id = graphene.Node.to_global_id("Order", order.id)
    variables = {
        "id": order_id,
    }

    # when
    response = api_client.post_graphql(QUERY_ORDER_BY_ID, variables)

    # then
    content = get_graphql_content(response)
    data = content["data"]["order"]
    assert len(data["lines"]) > 1
    mocked_authenticate_user.assert_called_once()


def test_get_context_value_not_override_dataloaders_if_passed_already(rf):
    # given
    request = rf.request()
    dataloaders: dict[str, DataLoader] = {}
    dataloaders_id = id(dataloaders)
    request.dataloaders = dataloaders

    # when
    context = get_context_value(request)

    # then
    assert context.dataloaders is dataloaders
    assert id(context.dataloaders) == dataloaders_id


def test_get_context_value_uses_request_time_if_passed_already(rf):
    # given
    request = rf.request()
    request_time = timezone.now()
    request.request_time = request_time

    # when
    context = get_context_value(request)

    # then
    assert context.request_time == request_time


def test_clear_context(rf):
    # given
    context = get_context_value(rf.request())
    context.dataloaders = {"key": NotImplemented}

    # when
    clear_context(context)

    # then
    assert context.dataloaders == {}
