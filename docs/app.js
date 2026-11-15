'use strict';
const original = `VALID_USERS = {
    "admin": "secret123",
    "developer": "dev2026!",
    "tester": "testpass"
}

def login(username: str, password: str) -> bool:
    # BUG: every login is accepted
    return True`;
const fixed = original.replace('    # BUG: every login is accepted\n    return True', '    if not username or not password:\n        return False\n    return VALID_USERS.get(username) == password');
const cases = [
  {name: 'Valid admin credentials', user: 'admin', password: 'secret123', expected: true},
  {name: 'Incorrect password rejected', user: 'admin', password: 'wrongpassword', expected: false},
  {name: 'Unknown user rejected', user: 'ghost_user', password: 'somepassword', expected: false},
  {name: 'Empty credentials rejected', user: '', password: '', expected: false}
];
const users = new Map([['admin', 'secret123'], ['developer', 'dev2026!'], ['tester', 'testpass']]);
const correctedLogin = (user, password) => Boolean(user && password && users.get(user) === password);
const el = id => document.getElementById(id);
let state = 'idle';
let downloadUrl;
function showTests(login) {
  const results = cases.map(test => login ? login(test.user, test.password) === test.expected : null);
  el('tests').replaceChildren(...cases.map((test, index) => {
    const row = document.createElement('div'); row.className = 'test-row';
    const name = document.createElement('span'); name.textContent = test.name;
    const result = document.createElement('span');
    result.textContent = results[index] === null ? '— PENDING' : results[index] ? '✓ PASS' : '× FAIL';
    result.className = results[index] === null ? '' : results[index] ? 'pass' : 'fail';
    row.append(name, result); return row;
  }));
  el('test-count').textContent = login ? `${results.filter(Boolean).length} / ${cases.length} passed · JavaScript` : 'Waiting for a run';
  return results.every(Boolean);
}
function log(message) { el('activity').textContent += '\n' + message; }
const wait = ms => new Promise(resolve => setTimeout(resolve, ms));
el('run').addEventListener('click', async () => {
  if (state !== 'idle') return;
  const issue = el('issue-id').value.trim();
  if (!issue) { el('issue-id').setCustomValidity('Enter an issue reference.'); el('issue-id').reportValidity(); return; }
  state = 'running'; el('run').disabled = true; el('issue-id').disabled = true;
  el('status').textContent = 'Inspecting sample…';
  el('activity').textContent = `[${issue}] Loaded sample_target/auth.py.`;
  await wait(500);
  showTests(() => true); log('Baseline: 1 passed, 3 failed. Login accepts invalid credentials.');
  el('status').textContent = 'Baseline failure confirmed';
  await wait(1100);
  el('code').textContent = fixed; el('code-label').textContent = 'Proposed fix · Python';
  log('Prepared the predefined credential-validation fix.');
  el('status').textContent = 'Verifying equivalent browser logic…';
  await wait(700);
  if (showTests(correctedLogin)) {
    state = 'review'; el('status').textContent = 'Awaiting your review'; el('review').hidden = false;
    log('4 browser checks passed. Python was not executed.');
  } else { state = 'failed'; el('status').textContent = 'Verification failed'; }
  el('reset').disabled = false;
});
el('issue-id').addEventListener('input', () => el('issue-id').setCustomValidity(''));
el('approve').addEventListener('click', () => {
  if (state !== 'review') return;
  state = 'approved'; el('review').hidden = true; el('status').textContent = 'Demo fix approved';
  log('Approved in this browser session. No files were changed or pushed.');
  downloadUrl = URL.createObjectURL(new Blob([fixed + '\n'], {type: 'text/plain'}));
  el('download').href = downloadUrl; el('download').hidden = false;
});
el('reset').addEventListener('click', () => {
  if (state === 'running') return;
  if (downloadUrl) { URL.revokeObjectURL(downloadUrl); downloadUrl = undefined; }
  state = 'idle'; el('run').disabled = false; el('issue-id').disabled = false;
  el('reset').disabled = true; el('review').hidden = true; el('download').hidden = true;
  el('download').removeAttribute('href'); el('code').textContent = original;
  el('code-label').textContent = 'Original · Python'; el('status').textContent = 'Ready to trace';
  el('activity').textContent = 'Ready. Start a trace to inspect the sample.'; showTests();
});
el('code').textContent = original;
showTests();
