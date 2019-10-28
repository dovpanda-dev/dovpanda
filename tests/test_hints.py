import numpy as np
import pandas as pd
import pytest

d1 = np.random.randint(0, 100, size=(4, 3))
d2 = np.random.randint(0, 100, size=(2, 3))
df1 = pd.DataFrame(d1, columns=list('ABC'))
df2 = pd.DataFrame(d2, columns=list('ABC'), index=[100, 200])
c = [pd.concat((df1, df2), axis=0), pd.concat((df1, df2), axis=1)]



### Begin testsing
import dovpanda
@pytest.mark.parametrize('axis', [0, 1])
def test_wrong_concat_axis(axis):
    expected = c[axis]
    result = pd.concat((df1, df2), axis=axis)
    pd.testing.assert_frame_equal(result, expected)