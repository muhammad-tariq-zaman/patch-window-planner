# patch-window-planner

Plan a patching window: reboot-required hosts first, each host costed at 5 minutes plus 2 per critical patch, with overflow listed honestly.

## How to run

```sh
python3 main.py hosts.csv --window-minutes 120
```

## Example output

```
Scheduled (105 min): srv-a, srv-b
Overflow: srv-c
```

Standard library only. Run the tests with `python3 -m unittest discover`.
