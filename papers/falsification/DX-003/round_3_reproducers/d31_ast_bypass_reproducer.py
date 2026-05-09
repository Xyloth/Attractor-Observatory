from pathlib import Path
from formalism.floor_bfg.read_separation import assert_d31_read_separation

root = Path('papers/falsification/DX-003/round_3_reproducers/d31_fake_root')
(root / 'formalism/floor_bfg').mkdir(parents=True, exist_ok=True)
(root / 'formalism/motif_contracts/predicates').mkdir(parents=True, exist_ok=True)
(root / 'formalism/floor_bfg/lenses.py').write_text('''
def evil_lens(trace):
    key = "outcome_" + "summary"
    classifier = __import__("formalism.floor_bfg." + "bfg_v2_classifier", fromlist=["classify_source_row"])
    return classifier.classify_source_row(trace["perturbation_event"][key])
''', encoding='utf-8')
(root / 'formalism/motif_contracts/predicates/floor_connectivity.py').write_text('def p(trace): return None\n', encoding='utf-8')
(root / 'formalism/motif_contracts/predicates/floor_connectivity_bfg_v2.py').write_text('def p(trace): return None\n', encoding='utf-8')
(root / 'formalism/floor_bfg/floor_join.py').write_text('def join_unit_outputs(): return None\n', encoding='utf-8')
print(assert_d31_read_separation(root))
