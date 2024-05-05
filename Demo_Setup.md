# Demo Setup

Deploy setup to management account.

Deploy with logging off or without changing the logging setting.

```bash
rain deploy --yes cloudtrail_stack_set.yaml
```

Deploy with logging on.

```bash
rain deploy --yes cloudtrail_stack_set.yaml --params IsLogging=True
```

Force update the stack set to resolve errors.

```bash
PATH="$PATH:$HOME/Repos/VWAG/codecommit/vulcan-res/backend-deployment-tools/bin/"

force-update-stack-set AccountTrails-fdd6 SELF
```
