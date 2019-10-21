# dovpanda
## Directions OVer PANDAs

Directions overlay for working with pandas in an analysis environment.    
If you think your task is common enough, it probably is, and Pandas probably has a built-in solution.
dovpanda is an overlay module that tries to understand what you are trying to do with your data, and help you
find easier ways to write you code.

## Usage
The basic usage of `dovpanda` is very east. you just import it after you import pandas
```python
import pandas as pd
import dovpanda
```     
This is it. From now on you can expect `dovpanda` to come with helpful directions while
you are writing you code.

### Example
```ipython
In [3]: df = pd.DataFrame({'a':list('xxyy'),'b':[40,50,60,70], 'time':['18:02','18:45','20:12','21:50']})
   ...: df['time'] = pd.to_datetime(df.time)
   ...: df['hour'] = df.time.dt.hour

In [4]: df.groupby('hour').b.sum()
===== Seems like you are grouping by a column named 'hour', consider using df.resample =====
Out[4]:
hour
18    90
20    60
21    70
Name: b, dtype: int64
```

### Notebook Support
Running `dovpanda` in a notebook environment will display rendered dismissable html.
<img width="1017" alt="notebook example" src="https://user-images.githubusercontent.com/7852981/67239045-f9fd4280-f456-11e9-9b28-5c8ed865872d.png">

## Advanced Usage
### Random Tips
`dovpanda.tip()` will give you a random `pandas` tip.

### Change Display
use `dovpanda.set_output` if you want to change output.

```ipython
In [14]: dovpanda.set_output('display')

In [15]: df.iterrows()
===== iterrows is not recommended, and in the majority of cases will have better alternatives =====
Out[15]: <generator object DataFrame.iterrows at 0x110fe4318>

In [16]: dovpanda.set_output('print')

In [17]: df.iterrows()
iterrows is not recommended, and in the majority of cases will have better alternatives
Out[17]: <generator object DataFrame.iterrows at 0x112c408b8>

In [18]: dovpanda.set_output('warning')

In [19]: df.iterrows()
WARNING:dovpanda:iterrows is not recommended, and in the majority of cases will have better alternatives
Out[19]: <generator object DataFrame.iterrows at 0x110ee7e58>

In [20]: dovpanda.set_output('off')

In [21]: df.iterrows()
Out[21]: <generator object DataFrame.iterrows at 0x1047c4d68>```
 