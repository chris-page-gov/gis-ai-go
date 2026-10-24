/* Provider-free UI seam. No registration, network, storage or model access. */
(function (scope) {
  'use strict';
  const TASKS = Object.freeze(['learn', 'areas', 'groups', 'features', 'settlements', 'history', 'sources']);
  const REFERENCES = Object.freeze(['context', 'glossary', 'dates', 'codelists']);
  const ACTIONS = Object.freeze(['read-state', 'open-task', 'open-reference', 'set-pinned']);
  function refused(code) { const error = new Error(code); error.code = code; throw error; }
  function closed(value, names) {
    if (!value || typeof value !== 'object' || Array.isArray(value)) refused('invalid-input');
    const proto = Object.getPrototypeOf(value);
    if (proto !== Object.prototype && proto !== null) refused('invalid-input');
    const own = Reflect.ownKeys(value);
    if (own.length !== names.length || own.some(k => typeof k !== 'string' || !names.includes(k))) refused('invalid-input');
    const snapshot = Object.create(null);
    for (const key of names) {
      const d = Object.getOwnPropertyDescriptor(value, key);
      if (!d || !Object.hasOwn(d, 'value')) refused('invalid-input');
      Object.defineProperty(snapshot, key, {value: d.value, enumerable: true});
    }
    return Object.freeze(snapshot);
  }
  function state(value) {
    value = closed(value, ['taskId', 'referenceId', 'pinned', 'referenceOpen']);
    if (!TASKS.includes(value.taskId) || !REFERENCES.includes(value.referenceId) ||
        typeof value.pinned !== 'boolean' || typeof value.referenceOpen !== 'boolean') refused('invalid-host-state');
    return Object.freeze({taskId: value.taskId, referenceId: value.referenceId,
      pinned: value.pinned, referenceOpen: value.referenceOpen});
  }
  function create(host) {
    for (const name of ['ready', 'snapshot', 'openTask', 'openReference', 'setPinned']) {
      if (typeof host?.[name] !== 'function') refused('invalid-host-adapter');
    }
    return Object.freeze({execute(action, input, options = {}) {
      let mutationStarted = false;
      try {
        if (!options || typeof options !== 'object') refused('invalid-input');
        options = closed(options, Object.hasOwn(options, 'signal') ? ['signal'] : []);
        const signal = options.signal;
        if (signal !== undefined && (!(signal instanceof AbortSignal))) refused('invalid-input');
        const checkpoint = () => { if (signal?.aborted) refused('cancelled'); };
        checkpoint();
        if (!ACTIONS.includes(action)) refused('invalid-action');
        const keys = action === 'read-state' ? [] : action === 'set-pinned' ? ['pinned'] :
          action === 'open-task' ? ['taskId', 'focus'] : ['referenceId', 'focus'];
        input = closed(input, keys);
        if (action === 'open-task' && !TASKS.includes(input.taskId)) refused('invalid-input');
        if (action === 'open-reference' && !REFERENCES.includes(input.referenceId)) refused('invalid-input');
        if ((action === 'open-task' || action === 'open-reference') && typeof input.focus !== 'boolean') refused('invalid-input');
        if (action === 'set-pinned' && typeof input.pinned !== 'boolean') refused('invalid-input');
        if (host.ready() !== true) refused('not-ready');
        state(host.snapshot()); // Reject a drifted host before a mutation.
        checkpoint();
        if (action !== 'read-state') {
          mutationStarted = true;
          const returned = action === 'open-task' ? host.openTask(input.taskId, input.focus) :
            action === 'open-reference' ? host.openReference(input.referenceId, input.focus) : host.setPinned(input.pinned);
          if (returned !== undefined) refused('invalid-host-adapter'); // Synchronous, no deferred work.
        }
        checkpoint();
        const result = state(host.snapshot());
        checkpoint();
        if (action === 'open-task' && result.taskId !== input.taskId ||
            action === 'open-reference' && (result.referenceId !== input.referenceId || !result.referenceOpen) ||
            action === 'set-pinned' && result.pinned !== input.pinned) refused('postcondition-refused');
        return Object.freeze({ok: true, action, state: result});
      } catch (error) {
        let nativeCode;
        try {
          const descriptor = error && Object.getOwnPropertyDescriptor(error, 'code');
          if (descriptor && Object.hasOwn(descriptor, 'value')) nativeCode = descriptor.value;
        } catch { /* Hostile exception metadata is never returned. */ }
        const code = ['invalid-input', 'invalid-action', 'not-ready', 'invalid-host-state', 'invalid-host-adapter',
          'cancelled', 'postcondition-refused'].includes(nativeCode) ? nativeCode : 'host-action-failed';
        // Never return host errors, selected content, labels, URLs or secrets.
        return Object.freeze({ok: false, code, mutationMayHaveOccurred: mutationStarted});
      }
    }});
  }
  const api = Object.freeze({TASKS, REFERENCES, ACTIONS, create});
  if (typeof module === 'object' && module.exports) module.exports = api;
  else scope.OverlaySharedActions = api;
})(typeof globalThis === 'object' ? globalThis : this);
