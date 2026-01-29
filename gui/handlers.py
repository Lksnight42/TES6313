from data.map.index import NAME_TO_ID, VALID_LOCATION_IDS
from core.context.model import UserContext
from core.context.validator import validate_user_context
from core.service import find_route


def find_route_handler(src_name: str, dst_name: str, pref: str):

    if not src_name or not dst_name:
        raise ValueError("Source and destination required")

    if src_name == dst_name:
        raise ValueError("Source and destination cannot be the same")

    ctx = UserContext(
        user_id="gui_user",
        start_location=NAME_TO_ID[src_name],
        end_location=NAME_TO_ID[dst_name],
        preference=pref,
        avoid=[],
        flexibility="medium",
    )

    validate_user_context(ctx, VALID_LOCATION_IDS)

    return find_route(ctx)
