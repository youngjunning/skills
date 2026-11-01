# Verification and recovery

## Define evidence before acting

Choose evidence that directly proves the requested result:

| Requested result | Strong evidence |
| --- | --- |
| setting changed | reopened setting shows the persisted value |
| file saved/exported | application confirmation plus file readback, size, and timestamp |
| message/form submitted | confirmation ID or authoritative destination state |
| install/update completed | installed version and successful launch |
| background job completed | terminal status plus expected artifact or server-side record |
| UI bug reproduced | screenshot/video and minimal repeatable steps |
| UI layout accepted | screenshot at specified scale/window plus accessibility state when relevant |

Use screenshots for visible state. Use files, process data, logs, UIA properties, signatures, or server readback for non-visual claims.

## Make actions idempotent where possible

Before retrying, inspect whether the intended state already exists. Prefer `set to value` over `toggle`, opening a known route over repeated `Back`, and selecting an identified item over arrow-key counts.

For actions that can duplicate external effects—send, publish, submit, purchase, create, upload—do not retry until history or authoritative state proves the first attempt did not complete.

## Retry policy

Use bounded, evidence-driven retries:

1. first failure: re-observe and re-resolve the target;
2. second failure: change the control method if evidence suggests focus, stale element, or unsupported pattern;
3. same failure again: stop and report the repeated condition.

Do not repeat the same click against an unchanged screen. Do not turn a modal error into a timeout by waiting behind it.

## Recover from controller and remote-session errors

Distinguish a controller/transport failure from an application failure. A Computer Use timeout, stale surface, lost remote connection, or failed tool call does not prove whether the last input reached Windows.

Before retrying an action after this kind of error:

1. reacquire the current app or remote-session surface instead of reusing the stale handle;
2. capture fresh visible state and verify the device, Windows session, foreground application, and window title;
3. inspect whether the requested transition already happened, including dialogs that may be behind the foreground window;
4. retry only when the action is idempotent or evidence proves that the first attempt had no effect;
5. after two recovery attempts, switch control method only when the observed failure supports it; stop after the same condition occurs a third time.

Do not stack clicks while a call is pending, reconnect directly into the next workflow step, or restart the target application merely to recover the controller. A successful reconnect proves only that control was restored; repeat the application-level verification separately.

Before operating a shared build or test machine, read the target repository's scoped agent instructions. If they prohibit controlling that machine or session, stop immediately even when the user requested a broader build, test, or release task; report the boundary and continue only with permitted source-side work.

## Common failure diagnosis

### Element not found

- Confirm the correct process and top-level window.
- Increase tree depth and inspect parents and children.
- Check whether the element is offscreen, virtualized, inside a popup, or created only after focus.
- Check localization and wildcard matching.
- Re-resolve after navigation or refresh.

### Access denied or pattern unavailable

- Compare integrity/elevation levels.
- Confirm the app exposes UI Automation rather than a custom canvas.
- Try the appropriate parent or child control.
- Use keyboard navigation or Computer Use as a verified fallback.

### Typing goes to the wrong place

- Stop immediately.
- Capture the current screen and inspect accidental input.
- Restore or clear only when the correction is unambiguous and safe.
- Bring the target window forward and set focus explicitly.
- Prefer `SetValue` over visual typing.

### Stale or detached element

- Discard the cached element.
- Find the current top-level window again.
- Re-run the selector and verify current properties.

### Session appears frozen

- Determine whether only rendering stopped or the remote task stopped.
- Check connection status and target-host logs/process state through a structured channel if available.
- Reconnect and inspect before restarting anything.

### DPI or coordinate mismatch

- Return to a known window mode and scale when authorized.
- Capture a fresh full-window screenshot.
- Locate the target again; do not reuse old coordinates.
- Prefer UIA or keyboard navigation.

## Final verification pass

Before reporting success:

1. return to the surface that shows the final state;
2. verify the exact target, not a similarly named app, profile, file, or environment;
3. collect the strongest available evidence;
4. check persistence if the task claims a saved setting or file;
5. identify any layer not verified, such as server acceptance, signature, deployment, restart persistence, or another user's view.

Report partial completion precisely. For example: “The form was filled and validated, but submission was not authorized” or “The installer finished, but administrator approval and final version readback remain.”
