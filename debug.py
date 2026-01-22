import loader.loader as loader
from log.logger import setup_logging
from log.logger import dump_logs


logger = setup_logging()


env = loader.load_env()

print("=== RUN CLIPS ===")
env.reset()

loader.load_location(env)
loader.load_edge(env)
loader.load_line(env)
loader.load_transfer(env)


env.run()

print("=== RUN CLIPS ===")
dump_logs(env, min_level="DEBUG")

loader.load_edge
print("=== RUN CLIPS ===")
for fact in env.facts():
    print(fact)

# routes = [
#     r for r in env.facts()
#     if r.template.name == "route" and r["mode"] == "mrt"
# ]
#
# for r in routes:
#     print(r)

del env


# for r in env.rules():
#     print(r.name)
