"""Independent tests for verification infrastructure; never train a model.

Library-backed fixtures below are test oracles only, not student cell code.
"""
import contextlib
import io
import nbformat
import torch
from torch import nn


def definitions(path, start=0):
    scope = {'torch': torch}
    notebook = nbformat.read(path, as_version=4)
    with contextlib.redirect_stdout(io.StringIO()):
        for cell in notebook.cells[start:]:
            if cell.source.startswith(('# Problem 1 — Task 3:', '# Problem 2 — Experiments')):
                break
            if cell.cell_type == 'code':
                exec(compile(cell.source, path, 'exec'), scope)
    return scope


p1 = nbformat.read('problem1/problem1.ipynb', as_version=4)
start = next(i for i, c in enumerate(p1.cells) if c.source.startswith('# Problem 1 — Task 2:'))
a = definitions('problem1/problem1.ipynb', start)
b = definitions('problem2/problem2.ipynb')


def expect_failure(action, exception, label):
    try:
        action()
    except exception:
        print('PASS:', label)
    else:
        raise AssertionError('Expected failure: ' + label)


# Direct parameter fixture copied from a library reference; no forward implementation.
def reference_parameter_fixture(d, h):
    reference = nn.RNN(d, h)
    fixture = nn.Module()
    for name, parameter in reference.named_parameters():
        fixture.register_parameter(name.removesuffix('_l0'), nn.Parameter(parameter.detach().clone()))
    return fixture

assert a['verify_constructor'](reference_parameter_fixture, 'RNN')['params'] == 4800
print('PASS: constructor checker accepts valid reference-backed parameter fixture')


def invalid_fixture(d, h, defect):
    fixture = reference_parameter_fixture(d, h)
    if defect == 'nan':
        with torch.no_grad():
            fixture.bias_ih.fill_(float('nan'))
    elif defect == 'shape':
        fixture.weight_ih = nn.Parameter(torch.ones(1, 1))
    elif defect == 'unregistered':
        del fixture.bias_hh
        fixture.bias_hh = torch.ones(h)
    elif defect == 'frozen':
        fixture.bias_hh.requires_grad_(False)
    return fixture


for defect in ('nan', 'shape', 'unregistered', 'frozen'):
    expect_failure(lambda: a['verify_constructor'](lambda d, h: invalid_fixture(d, h, defect), 'RNN'),
                   AssertionError, 'constructor rejects ' + defect)

if any(result['status'] != 'Completed' for result in a['CELL_RESULTS'].values()):
    expect_failure(a['require_task2_complete'], NotImplementedError, 'strict recurrent gate rejects placeholders')
else:
    a['require_task2_complete']()
    print('PASS: completed recurrent implementations pass strict gate')
if any(status != 'Verified' for status in b['P2_RESULTS'].values()):
    expect_failure(b['require_problem2_components'], NotImplementedError, 'strict Transformer gate rejects placeholders')
else:
    b['require_problem2_components']()
    print('PASS: completed Transformer implementations pass strict gate')

# Library-backed attention oracle also returns weights by attending to an identity V.
# This is only for testing the verifier, never a custom attention implementation.
def attention_oracle(q, k, v, allowed=None):
    output = torch.nn.functional.scaled_dot_product_attention(q, k, v, attn_mask=allowed)
    identity = torch.eye(k.shape[-2], dtype=q.dtype, device=q.device).expand(*k.shape[:-2], -1, -1)
    weights = torch.nn.functional.scaled_dot_product_attention(q, k, identity, attn_mask=allowed)
    return output, weights

b['verify_attention'](attention_oracle)
b['verify_hand_example'](attention_oracle)
print('PASS: attention random and hand-fixture verifiers accept library oracle')


def ignores_mask(q, k, v, allowed=None):
    return attention_oracle(q, k, v, None)

expect_failure(lambda: b['verify_attention'](ignores_mask), AssertionError,
               'attention verifier rejects future-token leakage')
expect_failure(lambda: b['verify_positions'](lambda length, d: torch.zeros(length, d)),
               AssertionError, 'position verifier rejects zero encoding')
print('Verification infrastructure passed; component completion is reported by the strict gates above.')
