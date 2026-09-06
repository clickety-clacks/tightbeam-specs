# Try the integrated writing loop

These steps use the preserved checkouts and installed virtual environments on racter and eezo. They start private disposable workspaces. Run the GUI from a terminal in racter's graphical desktop session; use its desktop or your existing remote-desktop connection. An SSH shell alone does not supply a graphical desktop. Do not set Qt's offscreen platform for this human trial. No product command below runs on gibson.

The exact candidate is **b083a8d88b8c76fe2ac59b56226a441ca485eb00**. No checkout, dependency installation or source modification is needed. Use a new directory name if a trial directory already exists; do not delete it or overwrite its store. Stop each service with Ctrl+C before starting another process against that store.

## A. Same-machine workspace on racter

1. In a racter terminal, select the preserved runtime and create a new private trial directory. Run this block once. `mkdir` must succeed before you continue.

```sh
cd /home/clu/.tightbeam/work/e9b4f0f8412d/slice4-integrated-main
git rev-parse HEAD
export DRIFT_PY=/home/clu/.tightbeam/work/d9274efe5684/qt-probe-venv/bin/python
export DRIFT_TRY=/home/clu/.tightbeam/work/e9b4f0f8412d/drift-try-same
export DRIFT_IP=127.0.0.1
umask 077
mkdir "$DRIFT_TRY"
```

2. Generate fresh trial credentials and a seven-day certificate. Use this same block for split setup when instructed below. It creates files exclusively and never opens a store.

```sh
"$DRIFT_PY" - <<'PY'
import json, os, secrets
from pathlib import Path
p = Path(os.environ['DRIFT_TRY'])
registry = {}
for actor, name in [('human', 'Writer'), ('agent', 'External agent')]:
    token = secrets.token_urlsafe(32)
    with (p / (actor + '.token')).open('x') as f:
        f.write(token + '\n')
    registry[token] = {'actorId': actor, 'displayName': name}
with (p / 'tokens.json').open('x') as f:
    json.dump(registry, f)
PY
openssl req -x509 -newkey rsa:2048 -nodes -days 7 \
  -subj /CN=Drift-trial -addext "subjectAltName=IP:$DRIFT_IP" \
  -keyout "$DRIFT_TRY/key.pem" -out "$DRIFT_TRY/cert.pem"
```

3. Start the service. Leave this terminal running. Its first JSON line must say `tls:true`, `access:tokens`, port 47605 and websocketPort 47606.

```sh
"$DRIFT_PY" -m drift --bind "$DRIFT_IP" --port 47605 --websocket-port 47606 \
  --store "$DRIFT_TRY/store.db" --tokens "$DRIFT_TRY/tokens.json" \
  --tls-cert "$DRIFT_TRY/cert.pem" --tls-key "$DRIFT_TRY/key.pem"
```

4. In a second racter desktop terminal, launch the actual editor:

```sh
cd /home/clu/.tightbeam/work/e9b4f0f8412d/slice4-integrated-main
/home/clu/.tightbeam/work/d9274efe5684/qt-probe-venv/bin/python -m drift.gui \
  --endpoint https://127.0.0.1:47605 \
  --websocket-url wss://127.0.0.1:47606/participation \
  --token-file ../drift-try-same/human.token --ca-file ../drift-try-same/cert.pem \
  --recovery-path ../drift-try-same/recovery
```

5. In each racter terminal used for agent commands, define this helper. Give the same commands and context to your active external agent harness. The helper runs the ordinary CLI; it does not embed or launch a model.

```sh
cd /home/clu/.tightbeam/work/e9b4f0f8412d/slice4-integrated-main
agent() {
  /home/clu/.tightbeam/work/d9274efe5684/qt-probe-venv/bin/python -m drift.cli \
    --endpoint https://127.0.0.1:47605 \
    --websocket-url wss://127.0.0.1:47606/participation \
    --token-file ../drift-try-same/agent.token --ca-file ../drift-try-same/cert.pem "$@"
}
```

Continue with C below. Finish this same-machine trial before starting the split trial.

## B. Split workspace: eezo service, racter GUI and agent

1. In an eezo terminal, run this setup block. Confirm the printed commit equals the candidate. Then run the credential-generation block from A.2 in this same eezo terminal.

```sh
cd /Users/mike/.tightbeam/work/e9b4f0f8412d/slice4-final
git rev-parse HEAD
export DRIFT_PY=/Users/mike/.tightbeam/work/e9b4f0f8412d/slice4-venv/bin/python
export DRIFT_TRY=/Users/mike/.tightbeam/work/e9b4f0f8412d/drift-try-split
export DRIFT_IP=100.71.19.27
umask 077
mkdir "$DRIFT_TRY"
```

2. Start the service on eezo with the exact A.3 command. The bind is now 100.71.19.27. Store, token registry and private key stay on eezo. The tested private-network route must be available between the hosts.

3. Transfer only the public certificate and participant token files to the racter trial directory. These are operator transfer commands, not product execution. In an operator terminal with the existing SSH aliases for both hosts:

```sh
ssh racter 'umask 077; mkdir /home/clu/.tightbeam/work/e9b4f0f8412d/drift-try-split'
scp -3 eezo:/Users/mike/.tightbeam/work/e9b4f0f8412d/drift-try-split/cert.pem racter:/home/clu/.tightbeam/work/e9b4f0f8412d/drift-try-split/cert.pem
scp -3 eezo:/Users/mike/.tightbeam/work/e9b4f0f8412d/drift-try-split/human.token racter:/home/clu/.tightbeam/work/e9b4f0f8412d/drift-try-split/human.token
scp -3 eezo:/Users/mike/.tightbeam/work/e9b4f0f8412d/drift-try-split/agent.token racter:/home/clu/.tightbeam/work/e9b4f0f8412d/drift-try-split/agent.token
```

4. In a racter desktop terminal, launch the editor:

```sh
cd /home/clu/.tightbeam/work/e9b4f0f8412d/slice4-integrated-main
/home/clu/.tightbeam/work/d9274efe5684/qt-probe-venv/bin/python -m drift.gui \
  --endpoint https://100.71.19.27:47605 \
  --websocket-url wss://100.71.19.27:47606/participation \
  --token-file ../drift-try-split/human.token --ca-file ../drift-try-split/cert.pem \
  --recovery-path ../drift-try-split/recovery
```

5. In each racter agent terminal, define the split helper:

```sh
cd /home/clu/.tightbeam/work/e9b4f0f8412d/slice4-integrated-main
agent() {
  /home/clu/.tightbeam/work/d9274efe5684/qt-probe-venv/bin/python -m drift.cli \
    --endpoint https://100.71.19.27:47605 \
    --websocket-url wss://100.71.19.27:47606/participation \
    --token-file ../drift-try-split/agent.token --ca-file ../drift-try-split/cert.pem "$@"
}
```

Repeat C using this helper. The human actions and command envelopes are identical.

## C. Drive the writing loop yourself

1. In the GUI, enter a document title, choose Markdown, and click **New document**. Wait until the blank document is open before typing. Paste the following text. Click **Save** and wait for **Saved · revision N**.

```text
# Working together
😀 é
The draft is clear. The ending is weak.
The ending is weak.
```

2. In the agent terminal, run `agent list`. Copy the new `documentId`. Replace `DOC` below with it. Run `agent read --document DOC`; note the current `revision` and full `cursor`. Do not assume revision 2: real typing may save several revisions.

3. Ask the active external agent harness to run `agent wait --document DOC --after DOC:N --timeout 120`, replacing `DOC:N` with that exact cursor. Wait for its `status:waiting` notice. In the GUI, select the first `The ending is weak.` sentence. Enter “Can you strengthen this sentence and keep the duplicate below?” in the discussion box. Click **Ask**. The active wait returns the new thread. This does not wake an idle harness.

4. Have the agent inspect the returned anchor revision and range. For the unmodified pasted text the range is [44,63). Replace `REV` and run `agent passage --document DOC --revision REV --start 44 --end 63`. The response must contain the exact selected sentence and its context. Have the agent answer with this command, replacing `DOC`, `REV` and `THREAD` from the response. Use a new command ID for a new action; retain an unchanged command ID only to retry that same action.

```sh
agent command --document DOC <<'JSON'
{"commandId":"try-reply-1","type":"reply","baseRevision":REV,"payload":{"threadId":"THREAD","body":"I suggest making the next step explicit while keeping the duplicate below."}}
JSON
agent command --document DOC <<'JSON'
{"commandId":"try-suggest-1","type":"suggest","baseRevision":REV,"payload":{"start":44,"end":63,"text":"The ending makes the next step clear."}}
JSON
```

5. Click **Accept** on the suggestion in the GUI. Confirm the sentence changes and its agent author remains visible. Run `agent read --document DOC` again for the current revision. Submit another suggestion with that revision, command ID `try-suggest-2`, range [24,43), and text “A bolder opening.” Click **Decline** in the GUI. Confirm the opening stays unchanged.

6. To see independent attention, start `agent adapter --port 47607` in another agent-configured terminal and leave it running. In the first agent terminal, replace DOC and REV with the current values:

```sh
agent --adapter-url http://127.0.0.1:47607 presence <<'JSON'
{"documentId":"DOC","update":{"kind":"selection","revision":REV,"start":24,"end":43}}
JSON
agent --adapter-url http://127.0.0.1:47607 presence <<'JSON'
{"documentId":"DOC","update":{"kind":"point","revision":REV,"start":0,"end":18}}
JSON
```

Select text in the GUI before sending these updates. Its selection and caret should remain yours. Type a character; it edits at your caret. The overlays distinguish agent selection and pointing.

7. For reciprocal discussion, the agent can send `type:comment` with `{start:24,end:43,body:"Keep this opening?"}` at the current revision. In the GUI, enter an answer and click that thread's **Reply**. Select text, enter a replacement, and click **Suggest**. The agent can read its `suggestionId`, then send `type:decline` with `{suggestionId:"…"}`. Either participant can resolve a thread: GUI **Resolve**, or agent `type:resolve` with `{threadId:"…"}`. Every command uses the same envelope shown above, with a unique command ID and current baseRevision.

8. Try stale safety: have the agent retain a revision, then edit and save in the GUI. Submit an agent `type:edit` against the retained older revision. It must refuse with `stale_revision`. Read the current document and choose a fresh edit with a new command ID. For an uncertain network outcome, retry the exact original envelope; do not alter it or assume it failed.

9. Try replay: note a current cursor, stop the continuing adapter with Ctrl+C, and ask a GUI question. Run `agent wait` after the noted cursor. It should replay the question. Restart the adapter if you want new presence; old attention must not return automatically.

10. Try saving and reopening: wait for **Saved**, stop the service with Ctrl+C, restart it with the identical A.3 command in its original terminal, and click **Reconnect**. To reopen the GUI, run its same launch command and click the document. If it offers **Recover draft**, inspect and recover before editing or discussion. **Retry save** resolves an unknown saved-command outcome. **Inspect** shows conflicts. **Export…** writes acknowledged text. Keep the recovery directory and store. Close the GUI and stop the adapter/service when finished.

## D. Optional live revocation check

In the service's original shell, with DRIFT_TRY and DRIFT_PY still set, remove only the agent token from the registry atomically. This intentionally revokes the trial agent and keeps the writer usable. It does not restart the service or change its store.

```sh
"$DRIFT_PY" - <<'PY'
import json, os
from pathlib import Path
p = Path(os.environ['DRIFT_TRY'])
registry = json.loads((p / 'tokens.json').read_text())
registry.pop((p / 'agent.token').read_text().strip(), None)
with (p / 'tokens.next.json').open('x') as f:
    json.dump(registry, f)
os.replace(p / 'tokens.next.json', p / 'tokens.json')
PY
```

`agent list` now returns unauthorized and the agent's existing socket closes. The writer can still save. No timing-hardening, multi-tenant access or idle-model wake is promised. These instructions were checked against the exact candidate CLI and GUI code; the new trial directory names are instructions for your run, not an additional claimed execution.
