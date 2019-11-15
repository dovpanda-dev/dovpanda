<h1><img src="https://github.com/dovpanda-dev/dovpanda/blob/master/img/logo.png" alt="logo" width="100"> dovpanda </h1>


[![pypi](https://img.shields.io/pypi/v/dovpanda.svg)](https://pypi.python.org/pypi/dovpanda)
[![Build Status](https://travis-ci.org/dovpanda-dev/dovpanda.svg?branch=master)](https://travis-ci.org/dovpanda-dev/dovpanda)
[![Documentation Status](https://readthedocs.org/projects/dovpanda/badge/?version=latest)](https://dovpanda.readthedocs.io/en/latest/?badge=latest)
[![Updates](https://pyup.io/repos/github/dovpanda-dev/dovpanda/shield.svg)](https://pyup.io/repos/github/dovpanda-dev/dovpanda/)
![python3](https://pyup.io/repos/github/dovpanda-dev/dovpanda/python-3-shield.svg?t=1572213773477)
[![license](https://img.shields.io/pypi/l/pandas.svg)](https://github.com/dovpanda-dev/dovpanda/blob/master/LICENS)


## Directions OVer PANDAs

Directions are hints and tips for using pandas in an analysis environment.
dovpanda is an overlay companion for working with pandas in an analysis environment.  
It is an overlay module that tries to understand what you are trying to do with your data, and helps you
make you code more concise with readable.  
If you think your task is common enough, it probably is, and pandas probably has a built-in solution. dovpanda will help you find them.

## Usage

### Hints
The main usage of `dovpanda` is its hints mechanism, which is very easy and works out-of-the-box.
Just import it after you import pandas, whether inside a notebook or in a console.

```python
import pandas as pd
import dovpanda
```     
This is it. From now on you can expect `dovpanda` to come up with helpful hints while you are writing your code.

### Notebook
Running `dovpanda` in a notebook environment will display rendered dismissable html.  
![random tip](https://github.com/dovpanda-dev/dovpanda/blob/master/img/readme_example.png)

### Console
```python
df = pd.DataFrame({'a':list('xxyy'),'b':[40,50,60,70], 'time':['18:02','18:45','20:12','21:50']})
df['time'] = pd.to_datetime(df.time)
df['hour'] = df.time.dt.hour
df.groupby('hour').b.sum()
```
```
===== Seems like you are grouping by a column named 'hour', consider setting the your
time column as index and then use df.resample('h') =====
Out[4]:
hour
18    90
20    60
21    70
Name: b, dtype: int64
```

## Installation
```bash
pip install dovpanda
```




## Extended Usage
### Random Tips
`dovpanda.tip()` will give you a random `pandas` tip.  
![random tip](https://github.com/dovpanda-dev/dovpanda/blob/master/img/readme_tip.png)

### Change Display
use `dovpanda.set_output` if you want to change output.

```
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
Out[21]: <generator object DataFrame.iterrows at 0x1047c4d68>

```

<hr> 

#### BTW

"dov" means bear in Hebrew <img src="https://github.com/dovpanda-dev/dovpanda/blob/master/img/logo.png" alt="logo" width="15">


