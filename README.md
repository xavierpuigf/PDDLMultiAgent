# PDDLMultiAgent
PDDL Definition for tasks in VirtualHome

To find a plan for the `example_problem.pddl` run
```python planner.py domain.pddl eample_program/example_problem.pddl out```
Use this API to solve the PDDL http://planning.domains/


You can also find a plan for some tasks using a VirtualHome environment. Generate the PDDL from a given set of files with

```
python env_parser.py
```
It will generate a set of  PDDL problems under `data_example/out_problems`. You can solve those using:

```
python planner.py --problem_name data_example/out_problems/file_0.pddl
```

You can also create your own environments, to be solved with PDDL. Checkout

```
generate_init_envs.py
```

And you can solve many plans in batch, using `solve_plans.py`
