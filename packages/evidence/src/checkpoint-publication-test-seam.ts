export type EvidenceCheckpointPublicationTestPhase =
  | "before-stage-file-sync"
  | "after-stage-file-sync"
  | "after-stage-parent-sync"
  | "before-linked-recovery-reopen"
  | "before-target-link"
  | "after-target-link"
  | "before-existing-target-open"
  | "before-existing-target-verification"
  | "before-target-parent-sync"
  | "after-target-parent-sync"
  | "before-stage-unlink"
  | "after-stage-unlink"
  | "before-cleanup-parent-sync"
  | "after-transaction-directory-remove";

export interface EvidenceCheckpointPublicationTestState {
  readonly phase: EvidenceCheckpointPublicationTestPhase;
  readonly stagePath: string;
  readonly targetPath: string;
}

type EvidenceCheckpointPublicationTestHook = (
  state: EvidenceCheckpointPublicationTestState,
) => void;

const TEST_ONLY_PUBLICATION_HOOKS = new WeakMap<
  object,
  EvidenceCheckpointPublicationTestHook
>();

/** Return the bounded publication hook attached to this exact options object. */
export function evidenceCheckpointPublicationTestHook(
  options: object,
): EvidenceCheckpointPublicationTestHook | undefined {
  return TEST_ONLY_PUBLICATION_HOOKS.get(options);
}

/**
 * Internal test seam for exact filesystem publication boundaries. The hook is
 * tied to one options object, survives neither copying nor serialisation, and
 * is not exported by the package barrel.
 */
export function withEvidenceCheckpointPublicationHookForTest<T extends object>(
  options: T,
  hook: EvidenceCheckpointPublicationTestHook,
): T {
  if (typeof hook !== "function") {
    throw new TypeError("Test checkpoint publication hook must be a function");
  }
  TEST_ONLY_PUBLICATION_HOOKS.set(options, hook);
  return options;
}
