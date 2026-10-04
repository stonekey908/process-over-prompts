#!/usr/bin/env python3
"""Regression tests for scripts/retro-capture.py transcript discovery.

Focus: find_current_transcript() must resolve a session's transcript even when
the cwd contains consecutive non-alnum chars (hidden dirs / git worktrees under
'/.helm/...'). Claude Code names project dirs by replacing EACH non-alnum char
with '-' (e.g. '/x/.helm' -> '-x--helm'), which the script's run-collapsing
'[^A-Za-z0-9]+' guess does not reproduce — so the old lookup silently returned
"no transcript found" for those sessions. See CLAUDE.md Known Gotchas.

Run: python3 tests/test_retro_capture.py
"""
import importlib.util
import json
import os
import tempfile
import unittest
from unittest import mock

HOOK = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "scripts", "retro-capture.py")


def load_module():
    spec = importlib.util.spec_from_file_location("retro_capture", HOOK)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # top-level is only defs/constants — no side effects
    return mod


def cc_dir_name(cwd):
    """Reproduce Claude Code's project-dir naming: replace EACH non-alnum char."""
    import re
    return re.sub(r"[^A-Za-z0-9]", "-", cwd)


class TestFindCurrentTranscript(unittest.TestCase):
    def setUp(self):
        self.mod = load_module()
        self.tmp = tempfile.mkdtemp()
        self.projects = os.path.join(self.tmp, "projects")
        os.makedirs(self.projects)
        self.mod.PROJECTS_DIR = self.projects

    def _make_session(self, cwd, sid, mtime=None):
        """Create <projects>/<cc-name>/<sid>.jsonl with a recorded cwd line."""
        pdir = os.path.join(self.projects, cc_dir_name(cwd))
        os.makedirs(pdir, exist_ok=True)
        path = os.path.join(pdir, sid + ".jsonl")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(json.dumps({"cwd": cwd, "type": "user"}) + "\n")
        if mtime is not None:
            os.utime(path, (mtime, mtime))
        return path

    def _find(self, cwd, sid):
        env = {} if sid is None else {"CLAUDE_CODE_SESSION_ID": sid}
        with mock.patch("os.getcwd", return_value=cwd), \
             mock.patch.dict(os.environ, env, clear=False):
            if sid is None:
                os.environ.pop("CLAUDE_CODE_SESSION_ID", None)
            return self.mod.find_current_transcript()

    # --- the bug: hidden/worktree path with consecutive non-alnum chars ---
    def test_hidden_worktree_path_resolves_by_sid(self):
        cwd = "/Users/nick/.helm/worktrees/helm/sto-2801"
        sid = "abc123-session"
        expected = self._make_session(cwd, sid)
        # sanity: the old run-collapsing guess would NOT match the real dir name
        import re
        self.assertNotEqual(re.sub(r"[^A-Za-z0-9]+", "-", cwd), cc_dir_name(cwd))
        path, got_sid = self._find(cwd, sid)
        self.assertEqual(path, expected)
        self.assertEqual(got_sid, sid)

    # --- normal path still hits the fast path ---
    def test_normal_path_fast_path(self):
        cwd = "/Users/nick/signal-engine"
        sid = "sid-normal"
        expected = self._make_session(cwd, sid)
        path, got_sid = self._find(cwd, sid)
        self.assertEqual(path, expected)
        self.assertEqual(got_sid, sid)

    # --- no session id: fall back to sniffing the recorded cwd ---
    def test_no_sid_resolves_by_sniffed_cwd(self):
        cwd = "/Users/nick/.helm/hop"
        expected = self._make_session(cwd, "some-old-sid")
        path, got_sid = self._find(cwd, None)
        self.assertEqual(path, expected)
        self.assertEqual(got_sid, "some-old-sid")

    # --- no sid, multiple transcripts in the dir: newest wins ---
    def test_no_sid_picks_newest(self):
        cwd = "/Users/nick/.helm/hop"
        self._make_session(cwd, "older", mtime=1000)
        newer = self._make_session(cwd, "newer", mtime=2000)
        path, _ = self._find(cwd, None)
        self.assertEqual(path, newer)

    # --- unknown session: graceful (None, sid) ---
    def test_unknown_session_returns_none(self):
        path, got_sid = self._find("/Users/nick/nowhere", "ghost-sid")
        self.assertIsNone(path)
        self.assertEqual(got_sid, "ghost-sid")


if __name__ == "__main__":
    unittest.main(verbosity=2)
