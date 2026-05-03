# Substance Audit W8 Cognitive

Campaign: 008
Doctrine: D17.5
Measured simulation logic: 432 lines against a 600-line proxy floor

## v1.0 Section 3 components

- Sensors: interoceptive, exteroceptive, and disturbance channels have declared noise, saturation, range, maintenance cost, health, and attention gating.
- Prediction: an online local-error predictive module updates weights from sensed state and disturbance history, and controls compare it against a no-prediction baseline.
- Memory: bounded internal memory entries decay by half-life; external marks are written with strength and read back as an action cue.
- Attention: a finite attention budget is allocated among sensor channels from recent error, entropy, and task pressure.
- Body-environment coupling: action changes the environment and controlled variable under energy and action-cost constraints; energy recovery and survival are explicit state.

## Implementation pointers

- `worlds/cognitive/model.py:SensorChannel` and `MemoryEntry` define the sensor and memory primitives.
- `CognitiveWorld.step` runs attention allocation, disturbance, noisy sensing, prediction update, memory write/read, action, environment feedback, energy recovery, and trace recording.
- `_configure_sensors`, `_allocate_attention`, `_sense`, `_update_predictive_model`, `_write_memory`, `_read_memory`, `_choose_action`, and `_recover_energy` implement the requested cognitive machinery.
- `_cognitive_diagnostics`, `_benchmark_success`, and `export_trace` expose deviation, prediction error, memory effect, attention entropy, energy, sensor health, and invariants.

## Behavior gate evidence

- W8 positive benchmarks cover `homeostasis`, `anticipation`, `externalized_memory`, and `attention_budget`.
- Controls require active action to improve homeostasis and active prediction to reduce prediction error relative to a no-prediction baseline.
- The Campaign 008 report requires the W8 positive traces, controls, event surface, and invariants to pass together.

## Invariant evidence

- Trace exports include energy boundedness, live sensor health, attention entropy, memory size, and action state.
- The validation report requires every positive W8 trace to have `invariants_passed = true`.
- D14 lint reports zero benchmark-conditional state-writing violations for W8.

## Substance judgment

W8 remains below the original proxy line floor because the implementation is compact, not because it is still a stub. It now contains the full intended closed perception-prediction-memory-action loop with noise, decay, energy costs, attention allocation, and controls.

Architect verdict: meets_spec_with_caveats
