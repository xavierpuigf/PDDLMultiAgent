# PDDLMultiAgent
PDDL Definition for tasks in VirtualHome

To find a plan for the `example_problem.pddl` run
```python planner.py domain.pddl eample_program/example_problem.pddl out```
Use this API to solve the PDDL http://planning.domains/


You can also find a plan (for set up a table) using a real environment. Generate the pddl from a given set of files with

```
python env_parser.py
```

And then solve it using
```
python planner.py
```

You can also create your own environments, to be solved with PDDL. Checkout
```
generate_init_envs.py
```

And you can solve many plans in batch, using `solve_plans.py`
