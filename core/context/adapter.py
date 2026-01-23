def assert_user_context(env, ctx):
    avoid = " ".join(ctx.avoid)

    env.assert_string(f"""
    (user-context
      (id {ctx.id})
      (start-location {ctx.start_location})
      (end-location {ctx.end_locatoin})
      (preference {ctx.preference})
      (avoid {avoid})
      (flexibility {ctx.flexibility}))
    """)
