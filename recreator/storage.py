"""Single-writer artifact workspace; no local database and no implicit global memory."""

from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import tempfile


class SuiteError(ValueError):
    pass


def canonical(value):
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"), allow_nan=False)


def sha(value):
    return hashlib.sha256(value).hexdigest()


def check(condition, message):
    if not condition:
        raise SuiteError(message)


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        check(key not in result, "duplicate JSON key")
        result[key] = value
    return result


def parse(raw):
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs,
                       parse_constant=lambda _: (_ for _ in ()).throw(SuiteError("non-finite JSON")))
    canonical(value)
    return value


def now():
    return datetime.now(timezone.utc).isoformat()


def inside(root, relative):
    relative = Path(relative)
    check(not relative.is_absolute() and not relative.drive, "path must be relative")
    path = (Path(root) / relative).resolve()
    check(path.is_relative_to(Path(root).resolve()), "path escapes root")
    return path


def atomic_write(path, raw):
    path = Path(path)
    mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else None
    path.parent.mkdir(parents=True, exist_ok=True)
    name = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".recreator-", delete=False) as handle:
            name = Path(handle.name)
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        if mode is not None:
            os.chmod(name, mode)
        os.replace(name, path)
        name = None
    finally:
        if name is not None and name.exists():
            name.unlink()


class Workspace:
    def __init__(self, root):
        self.root = Path(root).resolve()
        repository = Path(__file__).resolve().parents[1]
        check(not self.root.is_relative_to(repository), "private runtime workspace must be outside the public reference repository")
        self.root.mkdir(parents=True, exist_ok=True)
        self.artifacts = self.root / "artifacts"
        self.artifacts.mkdir(exist_ok=True)
        self.state_path = self.root / "state.json"

    @contextmanager
    def locked(self):
        lock = self.root / ".writer.lock"
        try:
            descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError as error:
            raise SuiteError("workspace writer lock exists; inspect its owner before recovery") from error
        try:
            os.write(descriptor, str(os.getpid()).encode("ascii"))
            os.close(descriptor)
            descriptor = None
            yield
        finally:
            if descriptor is not None:
                os.close(descriptor)
            lock.unlink()

    def put(self, raw):
        check(isinstance(raw, bytes), "artifact must be bytes")
        check(len(raw) <= 32 * 1024 * 1024, "artifact exceeds 32 MiB; use an external evidence-store adapter")
        identity = sha(raw)
        path = self.artifacts / identity
        if path.exists():
            check(sha(path.read_bytes()) == identity, "existing artifact is corrupt")
        else:
            try:
                with path.open("xb") as handle:
                    handle.write(raw)
                    handle.flush()
                    os.fsync(handle.fileno())
            except FileExistsError:
                check(sha(path.read_bytes()) == identity, "concurrent artifact corruption")
        return identity

    def get(self, identity):
        check(isinstance(identity, str) and re.fullmatch(r"[0-9a-f]{64}", identity), "invalid artifact identity")
        raw = (self.artifacts / identity).read_bytes()
        check(sha(raw) == identity, "artifact hash mismatch")
        return raw

    def read(self):
        state = parse(self.state_path.read_bytes())
        checksum = state.pop("checksum", None)
        check(checksum == sha(canonical(state).encode()), "state checksum mismatch; original file preserved")
        previous = "0" * 64
        for index, event in enumerate(state["events"], 1):
            body = {key: value for key, value in event.items() if key != "hash"}
            check(event["sequence"] == index and event["previous"] == previous,
                  "event history sequence mismatch")
            check(event["hash"] == sha(canonical(body).encode()), "event hash mismatch")
            previous = event["hash"]
        check(state["revision"] == len(state["events"]), "state revision mismatch")
        return state

    def _write(self, state):
        document = deepcopy(state)
        document["checksum"] = sha(canonical(state).encode())
        atomic_write(self.state_path, (canonical(document) + "\n").encode())

    def create(self, manifest, corpus_sha, protected):
        with self.locked():
            check(not self.state_path.exists(), "workspace already initialized")
            state = {"schema_version": 1, "revision": 0, "manifest": manifest,
                     "corpus_sha256": corpus_sha, "protected": protected, "phase": "initialized",
                     "events": [], "tasks": [], "runs": {}, "repairs": {}, "lessons": {},
                     "verifications": {}, "hypotheses": {}, "evidence": {}, "budget_spent": {"repairs": 0, "model_calls": 0}}
            self._event(state, "initialized", {"project_id": manifest["project_id"]})
            self._write(state)
        return state

    def _event(self, state, kind, data):
        event = {"sequence": state["revision"] + 1, "at": now(), "kind": kind, "data": data,
                 "previous": state["events"][-1]["hash"] if state["events"] else "0" * 64}
        event["hash"] = sha(canonical(event).encode())
        state["events"].append(event)
        state["revision"] += 1

    def update(self, kind, data, mutation, expected_revision=None):
        with self.locked():
            state = self.read()
            check(expected_revision is None or state["revision"] == expected_revision,
                  "stale workspace revision; recompute the operation")
            mutation(state)
            self._event(state, kind, data)
            self._write(state)
        return state
