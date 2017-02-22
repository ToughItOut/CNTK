# Copyright (c) Microsoft. All rights reserved.

# Licensed under the MIT license. See LICENSE.md file in the project root
# for full license information.
# ==============================================================================

import pytest
import numpy as np
from cntk import *

def test_outputs():
    fwd_state = placeholder_variable("placeholder")
    prev_state = past_value(fwd_state, name="prev_state")
    z = abs(prev_state, "abs")
    output = z.output
    z = z.replace_placeholders({fwd_state: z.output})

    fwd_state = None
    prev_state = None
    z = None

    for arg in output.owner.arguments:
        print("Argument name: {}, argument owner name {}".format(arg.name, arg.owner.name))

def test_0d_data_1d_sample_shape():
    x = input_variable(shape=(1,))
    op = x + x

    with pytest.raises(ValueError):
        op.eval({x : [np.asarray(2)]})

def test_1d_NDArrayView_copy():
    x = input_variable(shape=(1,))
    op = x + 1
    result = op.eval({x : [np.asarray([1])]}, as_numpy=False)
    result_slice = result.data().slice_view((0, 0, 0), (1,))

    w = parameter(init=np.asarray([1]))
    w.set_value(result_slice)
    
    assert np.array_equal(w.value, np.asarray(result_slice))
