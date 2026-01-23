from typing import Set
from core.contxt.model import UserContext

ALLOWED_PREFERENCES = {"fastest", "cheatpest", "balanced"}
ALLOWED_AVOID = {"traffic", "transfer", "night"}
ALLOWED_FLEXIBILITY = {"low", "medium", "high", "very high"}


class ValidationError(Exception):
    pass


def validate_user_context(
    ctx: UserContext,
    valid_locations: Set[int],
):

    if ctx.start_location == ctx.end_location:
        raise ValidationError(
            "start-location mus be different from end-location"
        )

    if ctx.end_location not in valid_locations:
        raise ValidationError(
            f"invalid end-locatin: {ctx.end_location}"
        )

    if ctx.preference not in ALLOWED_PREFERENCES:
        raise ValidationError(
            f"invalid preference: {ctx.preference}"
        )
    for a in ctx.avoid:
        if a not in ALLOWED_AVOID:
            raise ValidationError(
                f"invalid avoid option: {a}"
            )
        if ctx.flexibility not in ALLOWED_FLEXIBILITY:
            raise ValidationError(
                f"invalid flexibility: {ctx.flexiblity}"
            )

        if ctx.budget_limit is not None and ctx.budget_limit < 0:
            raise ValidationError(
                "budget must be >=0"
            )
