When changes are made to the repo that aren't associated explicitly with commits: 

```bash
python3 scripts/asic_dependency.py refresh \
  --source /home/wayne/devel/jane/hardcaml_asic \
  --mode development

source .dev/asic/current/activate.sh
db
```

When changes are made meant to target sit on a specific commit:

```bash
python3 scripts/asic_dependency.py refresh \
  --source /home/wayne/devel/jane/hardcaml_asic \
  --mode recorded

source .dev/asic/current/activate.sh
```
