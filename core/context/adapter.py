from core.context.model import UserContext
from core.context.validator import validate_user_context, ValidationError

def assert_user_context(env, ctx):
    avoid = " ".join(ctx.avoid)

    env.assert_string(f"""
    (user-context
      (id {ctx.user_id})
      (start-location {ctx.start_location})
      (end-location {ctx.end_location})
      (preference {ctx.preference})
      (avoid {avoid})
      (flexibility {ctx.flexibility}))
    """)

def build_user_context_from_gui(
  src_name: str,
  dst_name: str,
  name_to_id: dict[str, int],
  preference: str = "cheapest",
  avoid: list[str] | None = None,
  flexibility: str = "medium",
):
  
  if not src_name or not dst_name:
    raise ValidationError("Source and destination must be must be selected")

  if src_name == dst_name:
    raise ValidationError("Source and destination cannot be the same")

  try:
    start_id = int(name_to_id[src_name])
    end_id = int(name_to_id[dst_name])
  except KeyError:
    raise ValidationError("Invalid station selection")

  ctx = UserContext(
    user_id="gui_user",
    start_location=start_id,
    end_location=end_id,
    preference=preference,
    avoid=avoid or [],
    flexibility=flexibility,
  )

  return ctx
