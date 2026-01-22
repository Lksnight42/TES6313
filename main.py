import loader.loader as loader


def inject_user_context(env):
    env.assert_string("""
    (user-context
      (user-id u1)
      (start-location 1)
      (start-location 10)
      (preference fastest)
      (avoid transfer)
      (flexibility medium))
    """)


def path_algorithm(env):
    """
    For future algorithm
    """

    return None


def main():
    print("=== SYSTEM START ")

    env = loader.load_env()

    print("=== Loading static knowledge ===")
    env.reset()

    loader.load_location(env)
    loader.load_edge(env)
    loader.load_line(env)
    loader.load_transfer(env)

    print("Running initial inference...")
    env.run()

    path = path_algorithm(env)

    print("\n === RESULT ===")
    if path:
        print(path)


if __name__ == "__main__":
    main()

