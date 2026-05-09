# DX-003 Round 3 - Doctrine/Contract Violator Construction

round_id: DX-003-R3
attack_angle: I attacked D26/D27/D31 as operational tests, not as doctrine prose. The goal was to construct concrete violators that keep the current gates green: source-object aliases that evade exact matching, metadata-based predicates outside the four adversarial transforms, numeric value channels that survive key renaming, and AST read-separation bypasses.
elapsed_at_round_start: 00:13:35
elapsed_at_round_end: 00:17:43
round_end_utc: 2026-05-08T21:59:12.9025057+00:00

## Surfaces Examined

- docs/doctrine_d26.md, docs/doctrine_d27.md, docs/doctrine_d31.md
- ormalism/motif_contracts/schema.py
- ormalism/motif_contracts/adversarial.py
- ormalism/motif_contracts/clean_lenses.py
- ormalism/floor_bfg/read_separation.py
- 	ests/test_motif_contracts_v2.py, 	ests/test_lens_method_campaign024.py, 	ests/test_floor_bfg_d31.py

## Findings

### R3-F1 - RED - D31 AST read-separation can be bypassed by non-contiguous strings and dynamic import

Claim: D31 says a floor lens must fail if it imports the BFG classifier or reads/names outcome_summary. The current AST audit only detects static imports and contiguous string constants containing outcome_summary. A violator can compute "outcome_" + "summary", dynamically import ormalism.floor_bfg.bfg_v2_classifier, read the forbidden field, and still pass ssert_d31_read_separation.

Reproducer: Run python papers/falsification/DX-003/round_3_reproducers/d31_ast_bypass_reproducer.py if extracted from the recipe below, or inspect/run the already captured fixture in ound_3_reproducers/d31_ast_bypass.txt. Expected result: {'passed': True, 'failures': []} for a fake lens that reads the forbidden outcome summary and dynamically imports the classifier.

The fixture files are under ound_3_reproducers/d31_fake_root/.

Mistake-class mapping: doctrine operationalization gap; letter-vs-spirit AST guard.
Doctrine refs: D31, D9, D17.

### R3-F2 - RED - Four-axis adversarial controls miss metadata identity channels

Claim: D26 enforcement blocks event-token/state-key/payload-key/generator-id surfaces, but generator_id_erasure leaves manifest.world_family, parameter_record.family, and similar metadata identity keys untouched. A deliberately illegal predicate that reads world_family == 'crn' returns positive and passes every current adversarial axis.

Reproducer: Run the script captured in ound_3_reproducers/adversarial_controls_metadata_cheat.txt. Expected output includes generator_id_erasure leaves manifest.world_family: crn, ase_verdict positive, and passed True across all four axes.

Mistake-class mapping: adversarial-axis incompleteness; source identity leakage; Class 14 candidate: metadata-channel leakage.
Doctrine refs: D26, D27, D9.

### R3-F3 - AMBER - Source-object independence is exact-string matching, so alias/granularity changes can downgrade BAD to CLEAN/PARTIAL

Claim: derive_independence_verdict treats source objects and fields as exact strings. The same underlying source can be described as source_object='state', field='x' by the predicate and source_object='state.x', field='value' by the lens, producing CLEAN. Parent/child field overlap like payload vs payload.parent_child_ids produces PARTIAL, not BAD. Wildcard-like fields are not special.

Reproducer: Run the probe captured in ound_3_reproducers/source_object_alias_probe.txt. Expected outputs include same underlying state path expressed with object granularity alias => CLEAN, parent field vs child field path alias => PARTIAL, and wildcard-looking field does not collide with concrete field => PARTIAL.

Mistake-class mapping: source-object-map aliasing; schema semantic gap.
Doctrine refs: D26, D27.

### R3-F4 - AMBER - Clean lens controls do not catch value-encoded labels

Claim: The clean state lenses avoid key names by consuming numeric values only, but that means a label can be encoded as numeric state values under any key. State-key renaming removes the label-shaped key names, not the label-shaped values. The lens returns non-declined scores and passes all lens adversarial controls on a trace whose only signal is numeric label values.

Reproducer: Run the fixture captured in ound_3_reproducers/clean_lens_value_label_channel.txt. Expected output: five clean state lenses return declined=False, nonzero scores, and controls_passed=True on a trace with fields like motif_present_label and class_id_numeric.

Mistake-class mapping: value-channel leakage; scientific-integrity adversarial gap.
Doctrine refs: D26, D27, D14 by analogy.

### R3-F5 - YELLOW - Contract test subset is green while mutating signed artifacts

Claim: The focused contract/D31 test subset passes, but leaves tracked signed prereg and method artifacts modified. Passing tests should not dirty claim-bearing signed artifacts unless the command is explicitly a regeneration command.

Reproducer: Run python -m pytest -q tests/test_motif_contracts_v2.py tests/test_lens_method_campaign024.py tests/test_floor_bfg_d31.py, then git status --short. Expected result: tests pass (13 passed) and status lists modified papers/methods/CAMPAIGN_023_MOTIF_CONTRACT_IMPL.md, papers/methods/CAMPAIGN_024_LENS_SIDE_DECOUPLING.md, and campaign 023/024 signed prereg JSON files. Captured outputs: ound_3_reproducers/pytest_contract_green_subset.txt and ound_3_reproducers/contract_subset_mutation_status.txt. I restored the side effects before committing this round.

Mistake-class mapping: test side-effect contamination; signed-artifact mutability.
Doctrine refs: D9, D11, D17.5.

### R3-F6 - AMBER - Current contract tests do not exercise the constructed violators

Claim: The focused suite reports 13 passed, while R3-F1 through R3-F4 all produce deterministic violators against the same operational claims. This is not a failure of the doctrine concepts; it is a test coverage gap around nearby adversarial variants.

Reproducer: Compare ound_3_reproducers/pytest_contract_green_subset.txt with d31_ast_bypass.txt, dversarial_controls_metadata_cheat.txt, source_object_alias_probe.txt, and clean_lens_value_label_channel.txt.

Mistake-class mapping: fake-green; known-class recurrence around Class 13.
Doctrine refs: D26, D27, D31.

## Instrument-held Records

- The shipped private contract subset imports and executes when run explicitly.
- The happy-path derive_independence_verdict exact-overlap case returns BAD as expected.
- 	ests/test_motif_contracts_v2.py, 	ests/test_lens_method_campaign024.py, and 	ests/test_floor_bfg_d31.py pass as currently written.

## Hypotheses

- D26 source maps need canonical source-path normalization, ancestor/descendant overlap rules, wildcard semantics, and an UNKNOWN/INVALID state for underspecified maps.
- D26/D27 controls need metadata-value and value-channel adversarial transforms, not only key/token transforms.
- D31 AST checks should inspect names, subscripts, binops, dynamic imports, and perhaps execute a denylisted import/read monitor against fixtures.
