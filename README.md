# Hypothesis Testing

## Description
SQL data extraction for performing A/B Testing to inform buisiness decisions making for global retailer.
___
## Main Files:

student.ipynb - Notebook inclues data, methodologies and modeling around hypothesis testing

Mod_3_preso.pdf - presentation summarizing findings for a non-technical audience

Additional Files
Blog Post: Categorical Data
____
### SQL Database Table Schematic Layout:

<img src="https://raw.githubusercontent.com/jirvingphd/dsc-mod-3-project-online-ds-ft-100719/master/Northwind_ERD_updated.png">


```python
# !pip install -U fsds_100719
# from fsds_100719.imports import *

import pandas as pd

```


```python
import functions as fn

## Uncomment the line below to see the source code for the imported functions
# fs.ihelp(Cohen_d,False),fs.ihelp(find_outliers_IQR,False), fs.ihelp(find_outliers_Z,False)
```


```python
import sqlite3
connect = sqlite3.connect('Northwind_small.sqlite')
cur = connect.cursor()
```

# List of Tables:


```python
cur.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
df_tables = pd.DataFrame(cur.fetchall(), columns=['Table'])
df_tables
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Table</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>Employee</td>
    </tr>
    <tr>
      <td>1</td>
      <td>Category</td>
    </tr>
    <tr>
      <td>2</td>
      <td>Customer</td>
    </tr>
    <tr>
      <td>3</td>
      <td>Shipper</td>
    </tr>
    <tr>
      <td>4</td>
      <td>Supplier</td>
    </tr>
    <tr>
      <td>5</td>
      <td>Order</td>
    </tr>
    <tr>
      <td>6</td>
      <td>Product</td>
    </tr>
    <tr>
      <td>7</td>
      <td>OrderDetail</td>
    </tr>
    <tr>
      <td>8</td>
      <td>CustomerCustomerDemo</td>
    </tr>
    <tr>
      <td>9</td>
      <td>CustomerDemographic</td>
    </tr>
    <tr>
      <td>10</td>
      <td>Region</td>
    </tr>
    <tr>
      <td>11</td>
      <td>Territory</td>
    </tr>
    <tr>
      <td>12</td>
      <td>EmployeeTerritory</td>
    </tr>
  </tbody>
</table>
</div>




```python
cur.execute("""SELECT * FROM `Order`;""")
df = pd.DataFrame(cur.fetchall(), columns=[x[0] for x in cur.description])
df.head()

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Id</th>
      <th>CustomerId</th>
      <th>EmployeeId</th>
      <th>OrderDate</th>
      <th>RequiredDate</th>
      <th>ShippedDate</th>
      <th>ShipVia</th>
      <th>Freight</th>
      <th>ShipName</th>
      <th>ShipAddress</th>
      <th>ShipCity</th>
      <th>ShipRegion</th>
      <th>ShipPostalCode</th>
      <th>ShipCountry</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>10248</td>
      <td>VINET</td>
      <td>5</td>
      <td>2012-07-04</td>
      <td>2012-08-01</td>
      <td>2012-07-16</td>
      <td>3</td>
      <td>32.38</td>
      <td>Vins et alcools Chevalier</td>
      <td>59 rue de l'Abbaye</td>
      <td>Reims</td>
      <td>Western Europe</td>
      <td>51100</td>
      <td>France</td>
    </tr>
    <tr>
      <td>1</td>
      <td>10249</td>
      <td>TOMSP</td>
      <td>6</td>
      <td>2012-07-05</td>
      <td>2012-08-16</td>
      <td>2012-07-10</td>
      <td>1</td>
      <td>11.61</td>
      <td>Toms Spezialitäten</td>
      <td>Luisenstr. 48</td>
      <td>Münster</td>
      <td>Western Europe</td>
      <td>44087</td>
      <td>Germany</td>
    </tr>
    <tr>
      <td>2</td>
      <td>10250</td>
      <td>HANAR</td>
      <td>4</td>
      <td>2012-07-08</td>
      <td>2012-08-05</td>
      <td>2012-07-12</td>
      <td>2</td>
      <td>65.83</td>
      <td>Hanari Carnes</td>
      <td>Rua do Paço, 67</td>
      <td>Rio de Janeiro</td>
      <td>South America</td>
      <td>05454-876</td>
      <td>Brazil</td>
    </tr>
    <tr>
      <td>3</td>
      <td>10251</td>
      <td>VICTE</td>
      <td>3</td>
      <td>2012-07-08</td>
      <td>2012-08-05</td>
      <td>2012-07-15</td>
      <td>1</td>
      <td>41.34</td>
      <td>Victuailles en stock</td>
      <td>2, rue du Commerce</td>
      <td>Lyon</td>
      <td>Western Europe</td>
      <td>69004</td>
      <td>France</td>
    </tr>
    <tr>
      <td>4</td>
      <td>10252</td>
      <td>SUPRD</td>
      <td>4</td>
      <td>2012-07-09</td>
      <td>2012-08-06</td>
      <td>2012-07-11</td>
      <td>2</td>
      <td>51.30</td>
      <td>Suprêmes délices</td>
      <td>Boulevard Tirou, 255</td>
      <td>Charleroi</td>
      <td>Western Europe</td>
      <td>B-6000</td>
      <td>Belgium</td>
    </tr>
  </tbody>
</table>
</div>




```python
## looking at dates to get an idea of timeframe
df['OrderDate']=pd.to_datetime(df['OrderDate'])
```


```python
df['OrderDate'].describe()
```




    count                     830
    unique                    480
    top       2014-02-26 00:00:00
    freq                        6
    first     2012-07-04 00:00:00
    last      2014-05-06 00:00:00
    Name: OrderDate, dtype: object



Timespan is ~ 2 years : April 7 2012 - June 5 2014

# HYPOTHESIS 1

> ***Does discount amount have a statistically significant effect on the quantity of a product in an order? If so, at what level(s) of discount?***

- $H_0$:There is no statistcally significant effect on the quantity of a product in an order in relation to a discount amount.
- $H_1$:Discounts have a statistically significant effect on the quantiy of a product in an order.
- $H_1a$:Certain discount values have a greater effect than others.

## Importing and inspecting data from OrderDetail table:

This table from the Northwind database includes order information on:

    1) Quantity
    2) Discount 

Once imported, the data will be grouped by discount level and the means of the quantity sold for each will be compared against each other to evaluate if they are statistically significantly different.  This will determine if the null hypothesis can be rejected with a probability of 5% error in reporting a false negative.


```python
cur.execute("""SELECT * FROM OrderDetail;""")
df = pd.DataFrame(cur.fetchall(), columns=[x[0] for x in cur.description])
df.head()

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Id</th>
      <th>OrderId</th>
      <th>ProductId</th>
      <th>UnitPrice</th>
      <th>Quantity</th>
      <th>Discount</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>10248/11</td>
      <td>10248</td>
      <td>11</td>
      <td>14.0</td>
      <td>12</td>
      <td>0.0</td>
    </tr>
    <tr>
      <td>1</td>
      <td>10248/42</td>
      <td>10248</td>
      <td>42</td>
      <td>9.8</td>
      <td>10</td>
      <td>0.0</td>
    </tr>
    <tr>
      <td>2</td>
      <td>10248/72</td>
      <td>10248</td>
      <td>72</td>
      <td>34.8</td>
      <td>5</td>
      <td>0.0</td>
    </tr>
    <tr>
      <td>3</td>
      <td>10249/14</td>
      <td>10249</td>
      <td>14</td>
      <td>18.6</td>
      <td>9</td>
      <td>0.0</td>
    </tr>
    <tr>
      <td>4</td>
      <td>10249/51</td>
      <td>10249</td>
      <td>51</td>
      <td>42.4</td>
      <td>40</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
#explorting dataset
specs = df.describe()
specs
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>OrderId</th>
      <th>ProductId</th>
      <th>UnitPrice</th>
      <th>Quantity</th>
      <th>Discount</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>count</td>
      <td>2155.000000</td>
      <td>2155.000000</td>
      <td>2155.000000</td>
      <td>2155.000000</td>
      <td>2155.000000</td>
    </tr>
    <tr>
      <td>mean</td>
      <td>10659.375870</td>
      <td>40.793039</td>
      <td>26.218520</td>
      <td>23.812993</td>
      <td>0.056167</td>
    </tr>
    <tr>
      <td>std</td>
      <td>241.378032</td>
      <td>22.159019</td>
      <td>29.827418</td>
      <td>19.022047</td>
      <td>0.083450</td>
    </tr>
    <tr>
      <td>min</td>
      <td>10248.000000</td>
      <td>1.000000</td>
      <td>2.000000</td>
      <td>1.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <td>25%</td>
      <td>10451.000000</td>
      <td>22.000000</td>
      <td>12.000000</td>
      <td>10.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <td>50%</td>
      <td>10657.000000</td>
      <td>41.000000</td>
      <td>18.400000</td>
      <td>20.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <td>75%</td>
      <td>10862.500000</td>
      <td>60.000000</td>
      <td>32.000000</td>
      <td>30.000000</td>
      <td>0.100000</td>
    </tr>
    <tr>
      <td>max</td>
      <td>11077.000000</td>
      <td>77.000000</td>
      <td>263.500000</td>
      <td>130.000000</td>
      <td>0.250000</td>
    </tr>
  </tbody>
</table>
</div>



General Observation: Pricing ranges from `$2` - `$263` with an average price of `$26.21` and average qty of 23 items ordered, no null values


```python
df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 2155 entries, 0 to 2154
    Data columns (total 6 columns):
    Id           2155 non-null object
    OrderId      2155 non-null int64
    ProductId    2155 non-null int64
    UnitPrice    2155 non-null float64
    Quantity     2155 non-null int64
    Discount     2155 non-null float64
    dtypes: float64(2), int64(3), object(1)
    memory usage: 101.1+ KB
    


```python
len(df['OrderId'].unique())
```




    830




```python

```

### Initial Visual Inspection:

From this dataset of 2155 line items that span 830 orders, the average quantity ordered is 24 regardless of discount, the minimum ordered is 0 and max ordered is 130, although the IQR is between 10 and 30.


```python
qty = df['Quantity']
qty_specs = qty.describe()
qty_specs
```




    count    2155.000000
    mean       23.812993
    std        19.022047
    min         1.000000
    25%        10.000000
    50%        20.000000
    75%        30.000000
    max       130.000000
    Name: Quantity, dtype: float64




```python
qty_mu = round(qty_specs['mean'],0)
n = len(df)
print(f'The average quantity ordered from this sample is : {qty_mu}')
print(f'There are {n} orders in this sample.')
```

    The average quantity ordered from this sample is : 24.0
    There are 2155 orders in this sample.
    


```python
d =list(df['Discount'].unique())
d
#Dscounts are as follows:
```




    [0.0, 0.15, 0.05, 0.2, 0.25, 0.1, 0.02, 0.03, 0.04, 0.06, 0.01]




```python
import matplotlib.pyplot as plt
import seaborn as sns
sns.distplot(qty)
plt.axvline(qty_mu, label='Qty Mean', color='purple')
plt.show()

```


    <Figure size 640x480 with 1 Axes>






```python
import seaborn as sns
from ipywidgets import interact
```


```python

@interact
def plt_discounts(d=d):
    sns.distplot(df.groupby('Discount').get_group(d)['Quantity'])
    plt.axvline(qty_mu, color='purple')
    
```


    interactive(children=(Dropdown(description='d', options=(0.0, 0.15, 0.05, 0.2, 0.25, 0.1, 0.02, 0.03, 0.04, 0.…



```python
dfa = df.groupby('Discount').count()['Quantity']
display(dfa)

```


    Discount
    0.00    1317
    0.01       1
    0.02       2
    0.03       3
    0.04       1
    0.05     185
    0.06       1
    0.10     173
    0.15     157
    0.20     161
    0.25     154
    Name: Quantity, dtype: int64


**The sample sizes associated with discounts .01, .02, .03, .04 and .06 are relatively nominal <4, and will be dropped as without a normal or comperable dataset to evaulate their impact in comparison with the other groups.**


```python
discs = {}
for disc in df['Discount'].unique():
    discs[disc] = df.groupby('Discount').get_group(disc)['Quantity']
```


```python
for k,v in discs.items():
    print(k)
```

    0.0
    0.15
    0.05
    0.2
    0.25
    0.1
    0.02
    0.03
    0.04
    0.06
    0.01
    


```python
l=[.01,.02,.03,.04,.06]
oneper = discs.pop(.01)
twoper = discs.pop(.02)
threeper = discs.pop(.03)
fourper = discs.pop(.04)
sixper = discs.pop(.06)
```


```python
#visualizing distributions
fig, ax = plt.subplots(figsize=(10,5))
for k,v in discs.items():
    sns.distplot(v,label=v)

plt.title('Quantity Distribution')
plt.legend()
print('Distributions appear roughly equal,')
```

    Distributions appear roughly equal,
    


![png](output_37_1.png)


## Initial Observations:

Datatype is numeric.  

The average quantity ordered from this sample is : 24.0
There are 2155 orders in this sample. 

Discounts are as follows:
0.0, 0.15, 0.05, 0.2, 0.25, 0.1, 0.02, 0.03, 0.04, 0.06, 0.01

The majority of product purchases are without the discount(1317/2155) 61%, and frequency of discounts are as follows:
5%
10%
20%
15%
25%

For discounts 1%,2%,3%,4%, and 6% , the amount of data provided was relatively small to evaluate the impact on the whole.  This data was removed from further testing.

Overall distributions appears relatively uniform. 

### Since we are comparing multiple discounts to inspect it's impact on quantity ordered an AVNOVA or Kruksal test will be run depending on how assumptions are met: 
   
    
Assumptions for ANOVA Testing: 
(see corresponding sections

1) No significant outliers 
    * Upon a quick visual inspection, the distribution is skewed and visually there appears to be some outliers

2) Equal variance
    * Lavene's testing demonstrates NOT equal variance


3) Normality (if n>15)
      * Not required for discounts: 5%, 10%, 15%, 20% and 25% since n > 15




### Assumption 1:  Outliers 

Evaluation and removal via Z-Score testing:



```python
for disc, disc_data in discs.items():
    idx_outs = fn.find_outliers_Z(disc_data)
    print(f'Found {idx_outs.sum()} outliers in Discount Group {disc}')
    discs[disc] = disc_data[~idx_outs]
print('\n All of these outliers were removed')
```

    Found 20 outliers in Discount Group 0.0
    Found 2 outliers in Discount Group 0.15
    Found 3 outliers in Discount Group 0.05
    Found 2 outliers in Discount Group 0.2
    Found 3 outliers in Discount Group 0.25
    Found 3 outliers in Discount Group 0.1
    
     All of these outliers were removed
    

### Assumption 2: Equal Variance

Levines testing conducted on cleaned dataset



```python
#preparing data for levene's testing
datad = []
for k,v in discs.items():
    datad.append(v)
```


```python
import scipy.stats as stats
stat,p = stats.levene(discs[0.0],discs[0.05],discs[0.1],discs[0.25], discs[0.15], discs[0.20])
print(f'Lavene test for equal variance results are {round(p,4)}')
sig = 'do NOT' if p < .05 else 'DO'

print(f'The groups {sig} have equal variance')

```

    Lavene test for equal variance results are 0.0003
    The groups do NOT have equal variance
    

#### Since group does not prove to be equal variance, a **kruksal** will be conducted.
Looking at sample sizes to determine if normality needs to be tested.

### Assumption 3: Normality

First, checking sample sizes since assumption for normality depends on sample size. If 2-9 groups, each group n >= 15

For Discounts of 5%, 10%, 15%, 20% and 25% n>15 


```python
n = []
for disc, disc_data in discs.items():
    print(f'There are {len(disc_data)} samples in the {disc} discount group.')    
    n.append(len(disc_data)>15)
if all(n):
    print('\nAll samples are >15: Normality Assumption Criterion is met.')

```

    There are 1297 samples in the 0.0 discount group.
    There are 155 samples in the 0.15 discount group.
    There are 182 samples in the 0.05 discount group.
    There are 159 samples in the 0.2 discount group.
    There are 151 samples in the 0.25 discount group.
    There are 170 samples in the 0.1 discount group.
    
    All samples are >15: Normality Assumption Criterion is met.
    

## Kruksal Testing:


```python
stat, p = stats.kruskal(discs[0.0],discs[0.05],discs[0.1],discs[0.25], discs[0.15], discs[0.20])
print(f"Kruskal test p value: {round(p,4)}")
if p < .05 :
    print(f'Reject the null hypothesis')
else: 
    print(f'Null hypotheis remains true')
    
```

    Kruskal test p value: 0.0
    Reject the null hypothesis
    

#### ANOVA Testing for comparison


```python
stat, p = stats.f_oneway(*datad)
print(f"ANOVA test p value: {round(p,4)}")
if p < .05 :
    print(f'Reject the null hypothesis')
else: 
    print(f'Null hypotheis remains true')

```

    ANOVA test p value: 0.0
    Reject the null hypothesis
    

### Post-Hoc Testing: 


```python
disc_df = fn.prep_data_for_tukeys(discs)
disc_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>data</th>
      <th>group</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>12.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <td>1</td>
      <td>10.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <td>2</td>
      <td>5.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <td>3</td>
      <td>9.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <td>4</td>
      <td>40.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <td>2095</td>
      <td>30.0</td>
      <td>0.1</td>
    </tr>
    <tr>
      <td>2096</td>
      <td>77.0</td>
      <td>0.1</td>
    </tr>
    <tr>
      <td>2098</td>
      <td>25.0</td>
      <td>0.1</td>
    </tr>
    <tr>
      <td>2099</td>
      <td>4.0</td>
      <td>0.1</td>
    </tr>
    <tr>
      <td>2135</td>
      <td>2.0</td>
      <td>0.1</td>
    </tr>
  </tbody>
</table>
<p>2114 rows × 2 columns</p>
</div>




```python
disc_df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    Int64Index: 2114 entries, 0 to 2135
    Data columns (total 2 columns):
    data     2114 non-null float64
    group    2114 non-null object
    dtypes: float64(1), object(1)
    memory usage: 49.5+ KB
    


```python
d =list(disc_df['group'].unique())
d
```




    ['0.0', '0.15', '0.05', '0.2', '0.25', '0.1']




```python
import statsmodels.api as sms
tukey = sms.stats.multicomp.pairwise_tukeyhsd(disc_df['data'],disc_df['group'])
tukey.summary()


```




<table class="simpletable">
<caption>Multiple Comparison of Means - Tukey HSD, FWER=0.05</caption>
<tr>
  <th>group1</th> <th>group2</th> <th>meandiff</th>  <th>p-adj</th>  <th>lower</th>   <th>upper</th>  <th>reject</th>
</tr>
<tr>
    <td>0.0</td>   <td>0.05</td>   <td>6.0639</td>   <td>0.001</td> <td>2.4368</td>   <td>9.691</td>   <td>True</td> 
</tr>
<tr>
    <td>0.0</td>    <td>0.1</td>   <td>2.9654</td>  <td>0.2098</td> <td>-0.7723</td> <td>6.7031</td>   <td>False</td>
</tr>
<tr>
    <td>0.0</td>   <td>0.15</td>   <td>6.9176</td>   <td>0.001</td> <td>3.0233</td>  <td>10.8119</td>  <td>True</td> 
</tr>
<tr>
    <td>0.0</td>    <td>0.2</td>   <td>5.6293</td>   <td>0.001</td> <td>1.7791</td>  <td>9.4796</td>   <td>True</td> 
</tr>
<tr>
    <td>0.0</td>   <td>0.25</td>   <td>6.1416</td>   <td>0.001</td> <td>2.2016</td>  <td>10.0817</td>  <td>True</td> 
</tr>
<tr>
   <td>0.05</td>    <td>0.1</td>   <td>-3.0985</td> <td>0.4621</td> <td>-7.9861</td>  <td>1.789</td>   <td>False</td>
</tr>
<tr>
   <td>0.05</td>   <td>0.15</td>   <td>0.8537</td>    <td>0.9</td>  <td>-4.1547</td>  <td>5.862</td>   <td>False</td>
</tr>
<tr>
   <td>0.05</td>    <td>0.2</td>   <td>-0.4346</td>   <td>0.9</td>  <td>-5.4088</td> <td>4.5396</td>   <td>False</td>
</tr>
<tr>
   <td>0.05</td>   <td>0.25</td>   <td>0.0777</td>    <td>0.9</td>  <td>-4.9663</td> <td>5.1218</td>   <td>False</td>
</tr>
<tr>
    <td>0.1</td>   <td>0.15</td>   <td>3.9522</td>  <td>0.2311</td> <td>-1.1368</td> <td>9.0412</td>   <td>False</td>
</tr>
<tr>
    <td>0.1</td>    <td>0.2</td>   <td>2.6639</td>  <td>0.6409</td> <td>-2.3915</td> <td>7.7193</td>   <td>False</td>
</tr>
<tr>
    <td>0.1</td>   <td>0.25</td>   <td>3.1762</td>  <td>0.4872</td> <td>-1.9479</td> <td>8.3004</td>   <td>False</td>
</tr>
<tr>
   <td>0.15</td>    <td>0.2</td>   <td>-1.2883</td>   <td>0.9</td>  <td>-6.4605</td>  <td>3.884</td>   <td>False</td>
</tr>
<tr>
   <td>0.15</td>   <td>0.25</td>   <td>-0.7759</td>   <td>0.9</td>  <td>-6.0154</td> <td>4.4635</td>   <td>False</td>
</tr>
<tr>
    <td>0.2</td>   <td>0.25</td>   <td>0.5123</td>    <td>0.9</td>  <td>-4.6945</td> <td>5.7191</td>   <td>False</td>
</tr>
</table>



There is a statistically significant effect on quantity purchased based on discount. The discounts below are statistically considered equal:




```python
disc_tukey = fn.tukey_df(tukey)
disc_tukey_trues = disc_tukey.loc[disc_tukey['reject']==True]
disc_tukey_trues
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>group1</th>
      <th>group2</th>
      <th>meandiff</th>
      <th>p-adj</th>
      <th>lower</th>
      <th>upper</th>
      <th>reject</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>0.0</td>
      <td>0.05</td>
      <td>6.0639</td>
      <td>0.001</td>
      <td>2.4368</td>
      <td>9.6910</td>
      <td>True</td>
    </tr>
    <tr>
      <td>2</td>
      <td>0.0</td>
      <td>0.15</td>
      <td>6.9176</td>
      <td>0.001</td>
      <td>3.0233</td>
      <td>10.8119</td>
      <td>True</td>
    </tr>
    <tr>
      <td>3</td>
      <td>0.0</td>
      <td>0.2</td>
      <td>5.6293</td>
      <td>0.001</td>
      <td>1.7791</td>
      <td>9.4796</td>
      <td>True</td>
    </tr>
    <tr>
      <td>4</td>
      <td>0.0</td>
      <td>0.25</td>
      <td>6.1416</td>
      <td>0.001</td>
      <td>2.2016</td>
      <td>10.0817</td>
      <td>True</td>
    </tr>
  </tbody>
</table>
</div>







```python
disc_df['group']=disc_df['group'].astype(str)
d=disc_df['group']
```


```python

@interact
def plt_discounts(d=d):
    sns.distplot(disc_df.groupby('group').get_group(d)['data'])
    plt.axvline(qty_mu, color='purple')
    
```


    interactive(children=(Dropdown(description='d', options=('0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0…



```python
stats = disc_df['data'].describe()
dataqty = stats['mean']
print(f'Revised average quantity sold across all orders {round(dataqty)}')
zeros = disc_df.groupby('group').get_group('0.0')['data']
nodiscav = zeros.mean()
print(f'Average quantity sold for orders where no discount was extended was: {round(nodiscav)}')
```

    Revised average quantity sold across all orders 23.0
    Average quantity sold for orders where no discount was extended was: 21.0
    


```python
for k,v in discs.items():
    print(f'The average quantity sold for {k} discount is {round(v.mean())}')
```

    The average quantity sold for 0.0 discount is 21.0
    The average quantity sold for 0.15 discount is 27.0
    The average quantity sold for 0.05 discount is 27.0
    The average quantity sold for 0.2 discount is 26.0
    The average quantity sold for 0.25 discount is 27.0
    The average quantity sold for 0.1 discount is 24.0
    


```python
data_mu = disc_df['data'].mean()
print(f'The average qty purchased regardless of discount or none offered is {round(data_mu)}')
```

    The average qty purchased regardless of discount or none offered is 23.0
    

### Various EDA to understand distributions and remaining potential outliers

The following hex-bin visualization illustrates the density of data in the 0% category. Visually, this appears that equal quantitites are purchased, but might be due to light markings relative to sample sizes.  Clearly not the best choice for EDA, and further exploration is required.


```python
disc_df['group'] = disc_df['group'].astype(float)
sns.jointplot(data=disc_df, x='group', y='data', kind='hex')
plt.ylabel('Qty')
```




    Text(336.9714285714286, 0.5, 'Qty')




![png](output_66_1.png)


Visual on distributions and potential remaining outliers:


```python
#boxen plot
sns.catplot(data=disc_df, x='group', y='data', kind='boxen')
ax.axhline(26.75, color='k')
plt.gca()
plt.show()
```


![png](output_68_0.png)


This plot may not best suit non-technical audience with the additional information potentially could cause confusion.  However, the above boxen plot clearly illustrates distributions as well as remaining potential outliers in the .05, .15, .2 and .25 groups.  These outliers will not be removed at the present moment with the intention to preserve as much of the initial dataset as possible.  Sample sizes can be referenced under 'Assumption 3: Normality' where this is observed.


```python
fig, ax = plt.subplots(figsize=(10,8))
sns.barplot(data=disc_df, x='group', y='data', ci=68)
#plt.axhline(data_mu, linestyle='--', color='darkgray')
plt.axhline(26.75, linestyle='--', color='lightblue')
plt.title('Average Quanity Purchased at Varying Discont Levels', fontsize=20)
plt.xlabel('Discount Extended')
plt.ylabel('Average Quantity Purchased')
```




    Text(0, 0.5, 'Average Quantity Purchased')




![png](output_70_1.png)


Effect Sizes: 


```python
for disc, disc_data in discs.items():
    es = fn.Cohen_d(zeros, disc_data)
    print(f'The effect size for {disc} is {round(np.abs(es),4)}')
```

    The effect size for 0.0 is 0.0
    The effect size for 0.15 is 0.453
    The effect size for 0.05 is 0.3949
    The effect size for 0.2 is 0.3751
    The effect size for 0.25 is 0.4109
    The effect size for 0.1 is 0.1982
    

## Hypothesis 1 Findings and Recommendation:

### Findings:
**Rejecting the null hypothesis :**
*   𝐻0 :There is no statistcally significant effect on the quantity of a product in an order in relation to a discount amount.


**Alternative hypothesese:**

    *  𝐻1 :Discounts have a statistically significant effect on the quantiy of a product in an order.
    *  𝐻1𝑎 :Certain discount values have a greater effect than others.(see below for findings)

A 10% discount had no statistical significance on the quantiy purchased.

Discounts extended at 5%, 15%, 20%, and 25% statistically are equal in terms of their effect on quantity sold when compared to none offered, with a p-value of .001 meaning there is a .01 percent chance of classifying them as such due to chance. Each have varying effect sizes in compared to orders placed with no discount extended.
 
Discount |AvQty | Effect Size | Effect
 -- | -- | -- | --|
5 % | 27| .1982 | Small
15 % | 27| .454 | Medium
20 % |26| .3751 | Medium
25 % |27 | .454 | Medium

Additional notes:
For discounts 1%,2%,3%,4%, and 6% that were included in the original dataset, the amount of data provided was relatively small to evaluate the impact on the whole. This data was removed from further testing

With additional outliers removed for each of the discount groups, the revised average qty purchased was 23 overall.


 
###  Recommendation:

While larger discounts did deomonstrate significant effect on quantity purchased, smaller discounts held a statistically equal effect.  To recognize the effect of driving higher quantities purchased and realize larger profit margins, offer the smaller discount.


# HYPOTHESIS 2:

> ***Do some categories generate more revenue than others ??*** 
  **Which ones?**
 
 


- $𝐻0$ : All categories generate equal revenues.
- $𝐻1$ : Certain categories sell at statistically higher rates of revneu than others.
- $𝐻1𝑎$ : 

### Importing and inspecting data from Product and OrderDetail tables:

These tables includes product information data including:

1) Categories 

2) Pricing and discount information to generate revenues



```python
##clean sql notation
cur.execute("""SELECT 
                ProductId, 
                ProductName, 
                od.UnitPrice,
                CategoryID, 
                CategoryName, 
                Discount, 
                Quantity
                FROM Product AS p
                JOIN OrderDetail as od
                ON p.ID = Od.ProductId
                JOIN Category as c 
                ON c.ID = p.CategoryID;""")
catavs = pd.DataFrame(cur.fetchall(), columns=[x[0] for x in cur.description])
catavs.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ProductId</th>
      <th>ProductName</th>
      <th>UnitPrice</th>
      <th>CategoryId</th>
      <th>CategoryName</th>
      <th>Discount</th>
      <th>Quantity</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>11</td>
      <td>Queso Cabrales</td>
      <td>14.0</td>
      <td>4</td>
      <td>Dairy Products</td>
      <td>0.0</td>
      <td>12</td>
    </tr>
    <tr>
      <td>1</td>
      <td>42</td>
      <td>Singaporean Hokkien Fried Mee</td>
      <td>9.8</td>
      <td>5</td>
      <td>Grains/Cereals</td>
      <td>0.0</td>
      <td>10</td>
    </tr>
    <tr>
      <td>2</td>
      <td>72</td>
      <td>Mozzarella di Giovanni</td>
      <td>34.8</td>
      <td>4</td>
      <td>Dairy Products</td>
      <td>0.0</td>
      <td>5</td>
    </tr>
    <tr>
      <td>3</td>
      <td>14</td>
      <td>Tofu</td>
      <td>18.6</td>
      <td>7</td>
      <td>Produce</td>
      <td>0.0</td>
      <td>9</td>
    </tr>
    <tr>
      <td>4</td>
      <td>51</td>
      <td>Manjimup Dried Apples</td>
      <td>42.4</td>
      <td>7</td>
      <td>Produce</td>
      <td>0.0</td>
      <td>40</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Revenue is calculated by subtracting discounts from the UnitPrice and multiplying by quantity ordered.
catavs['Revenue'] = (catavs['UnitPrice'] * (1 - catavs['Discount']))*catavs['Quantity']
```


```python
avcrev = catavs['Revenue'].mean()
print (round(avcrev),2)
cg = catavs['CategoryName'].unique()



```

    587.0 2
    


```python

```

### Initial Visual Inspection and Observations:

There are 8 different categories sold in this company that represent 77 products.

The average revenue generated across all categories is `$587.00`

Visually, it appears that there are three categories that significantly generate higher revenues than others, additional testing will demonstrate their siginficance and effect.



```python
fig, ax = plt.subplots(figsize=(12,8))
sns.barplot(data=catavs, x='CategoryName', y='Revenue', ci=68, ax=ax)
plt.title('Initial Inspection: Average Revenue Generated Accross All Categories', fontsize=18)
plt.axhline(avcrev,linestyle="--", color='k', linewidth=.8 )
plt.xlabel('Category')
plt.ylabel('Revenue')
plt.show()
```


![png](output_83_0.png)



```python
catcount = len(catavs['CategoryId'].unique())
avrev = catavs['Revenue'].mean()
print(f'There are {catcount} different categories sold in this company')
print(f'The average revenue generated accross all categories is {round(avcrev,0)}')
```

    There are 8 different categories sold in this company
    The average revenue generated accross all categories is 587.0
    


```python
cats = {}
for cat in catavs['CategoryName'].unique():
    cats[cat] = catavs.groupby('CategoryName').get_group(cat)['Revenue']
```

In each of the different categories, the products align as such: 


```python
catsprods = {}
for cat in catavs['CategoryName'].unique():
    catsprods[cat] = catavs.groupby('CategoryName').get_group(cat)['ProductId'].unique()
```


```python
for k,v in catsprods.items():
    print(f'There are {len(v)} products in the {k} Category')

```

    There are 10 products in the Dairy Products Category
    There are 7 products in the Grains/Cereals Category
    There are 5 products in the Produce Category
    There are 12 products in the Seafood Category
    There are 12 products in the Condiments Category
    There are 13 products in the Confections Category
    There are 12 products in the Beverages Category
    There are 6 products in the Meat/Poultry Category
    

### Assumption 1: Outliers
Outliers removed via z-score testing.


```python
for cat, cat_data in cats.items():
    idx_outs = fn.find_outliers_Z(cat_data)
    print(f'Found {idx_outs.sum()} outliers in Category # {cat}')
    cats[cat] = cat_data[~idx_outs]
print('\n All of these outliers were removed')
```

    Found 5 outliers in Category # Dairy Products
    Found 6 outliers in Category # Grains/Cereals
    Found 1 outliers in Category # Produce
    Found 8 outliers in Category # Seafood
    Found 4 outliers in Category # Condiments
    Found 9 outliers in Category # Confections
    Found 12 outliers in Category # Beverages
    Found 4 outliers in Category # Meat/Poultry
    
     All of these outliers were removed
    


```python
pids = catavs['ProductName'].unique()
pids
print(f'There are {len(pids)} products')
```

    There are 77 products
    


```python

```

### Assumption 2: Equal Variance

Testing cleaned dataset for equal variance.

Since the groups do NOT have euqal variance, a Kruksal test will be conducted.


```python
datac = []
for k,v in cats.items():
    datac.append(v)
```


```python
import scipy.stats as stats
stat,p = stats.levene(*datac)
print(f'Lavene test for equal variance results are {round(p,4)}')
sig = 'do NOT' if p < .05 else 'DO'

print(f'The groups {sig} have equal variance')
```

    Lavene test for equal variance results are 0.0
    The groups do NOT have equal variance
    

### Assumption 3: Normality

All groups are > 15 samples = Assumption for normality is met.


```python
n = []

for cat, cat_data in cats.items():
    print(f'There are {len(cat_data)} samples in the data set for Employee #{cat}.')
    n.append(len(cat_data)>15)
if all(n):
    print('\nAll samples are >15: Normality Assumption Criterion is met.')



```

    There are 361 samples in the data set for Employee #Dairy Products.
    There are 190 samples in the data set for Employee #Grains/Cereals.
    There are 135 samples in the data set for Employee #Produce.
    There are 322 samples in the data set for Employee #Seafood.
    There are 212 samples in the data set for Employee #Condiments.
    There are 325 samples in the data set for Employee #Confections.
    There are 392 samples in the data set for Employee #Beverages.
    There are 169 samples in the data set for Employee #Meat/Poultry.
    
    All samples are >15: Normality Assumption Criterion is met.
    

### Kruksal Testing:

Results, reject the null hypothesis.


```python
stat, p = stats.kruskal(*datac)
print(f"Kruskal test p value: {round(p,4)}")
if p < .05 :
    print(f'Reject the null hypothesis')
else: 
    print(f'Null hypotheis remains true')
```

    Kruskal test p value: 0.0
    Reject the null hypothesis
    

### Post-Hoc Testing: 


```python
cat_df = fn.prep_data_for_tukeys(cats)
cat_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>data</th>
      <th>group</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>168.00</td>
      <td>Dairy Products</td>
    </tr>
    <tr>
      <td>2</td>
      <td>174.00</td>
      <td>Dairy Products</td>
    </tr>
    <tr>
      <td>12</td>
      <td>47.50</td>
      <td>Dairy Products</td>
    </tr>
    <tr>
      <td>13</td>
      <td>1088.00</td>
      <td>Dairy Products</td>
    </tr>
    <tr>
      <td>14</td>
      <td>200.00</td>
      <td>Dairy Products</td>
    </tr>
    <tr>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <td>2096</td>
      <td>2702.70</td>
      <td>Meat/Poultry</td>
    </tr>
    <tr>
      <td>2098</td>
      <td>738.00</td>
      <td>Meat/Poultry</td>
    </tr>
    <tr>
      <td>2099</td>
      <td>86.40</td>
      <td>Meat/Poultry</td>
    </tr>
    <tr>
      <td>2102</td>
      <td>111.75</td>
      <td>Meat/Poultry</td>
    </tr>
    <tr>
      <td>2148</td>
      <td>48.00</td>
      <td>Meat/Poultry</td>
    </tr>
  </tbody>
</table>
<p>2106 rows × 2 columns</p>
</div>



#### Visual Inspection Post Data Cleaning:


```python

@interact
def plt_discounts(d=cg):
    sns.distplot(cat_df.groupby('group').get_group(d)['data'])
    plt.axvline(cat_df['data'].mean(), color='purple')
    plt.title('Average Revenue Generated by Category')
    plt.ylabel('Distribution')
```


    interactive(children=(Dropdown(description='d', options=('Dairy Products', 'Grains/Cereals', 'Produce', 'Seafo…



```python
tukeyc = sms.stats.multicomp.pairwise_tukeyhsd(cat_df['data'],cat_df['group'])
tukeyc.summary()
```




<table class="simpletable">
<caption>Multiple Comparison of Means - Tukey HSD, FWER=0.05</caption>
<tr>
      <th>group1</th>         <th>group2</th>     <th>meandiff</th>   <th>p-adj</th>   <th>lower</th>     <th>upper</th>   <th>reject</th>
</tr>
<tr>
     <td>Beverages</td>     <td>Condiments</td>    <td>55.7712</td>    <td>0.9</td>   <td>-78.858</td>  <td>190.4005</td>   <td>False</td>
</tr>
<tr>
     <td>Beverages</td>     <td>Confections</td>   <td>27.0669</td>    <td>0.9</td>  <td>-91.4026</td>  <td>145.5364</td>   <td>False</td>
</tr>
<tr>
     <td>Beverages</td>   <td>Dairy Products</td> <td>194.0913</td>   <td>0.001</td>  <td>78.8965</td>   <td>309.286</td>   <td>True</td> 
</tr>
<tr>
     <td>Beverages</td>   <td>Grains/Cereals</td>  <td>21.4034</td>    <td>0.9</td>  <td>-118.1928</td> <td>160.9996</td>   <td>False</td>
</tr>
<tr>
     <td>Beverages</td>    <td>Meat/Poultry</td>   <td>411.042</td>   <td>0.001</td> <td>265.7215</td>  <td>556.3625</td>   <td>True</td> 
</tr>
<tr>
     <td>Beverages</td>       <td>Produce</td>    <td>296.1055</td>   <td>0.001</td>  <td>138.516</td>   <td>453.695</td>   <td>True</td> 
</tr>
<tr>
     <td>Beverages</td>       <td>Seafood</td>    <td>-46.1557</td>    <td>0.9</td>  <td>-164.9266</td>  <td>72.6151</td>   <td>False</td>
</tr>
<tr>
    <td>Condiments</td>     <td>Confections</td>  <td>-28.7043</td>    <td>0.9</td>  <td>-168.1193</td> <td>110.7106</td>   <td>False</td>
</tr>
<tr>
    <td>Condiments</td>   <td>Dairy Products</td>  <td>138.32</td>   <td>0.0449</td>  <td>1.6769</td>   <td>274.9631</td>   <td>True</td> 
</tr>
<tr>
    <td>Condiments</td>   <td>Grains/Cereals</td> <td>-34.3678</td>    <td>0.9</td>  <td>-192.129</td>  <td>123.3933</td>   <td>False</td>
</tr>
<tr>
    <td>Condiments</td>    <td>Meat/Poultry</td>  <td>355.2707</td>   <td>0.001</td> <td>192.4225</td>   <td>518.119</td>   <td>True</td> 
</tr>
<tr>
    <td>Condiments</td>       <td>Produce</td>    <td>240.3342</td>   <td>0.001</td>  <td>66.4494</td>  <td>414.2191</td>   <td>True</td> 
</tr>
<tr>
    <td>Condiments</td>       <td>Seafood</td>    <td>-101.927</td>  <td>0.3439</td> <td>-241.5981</td>  <td>37.7441</td>   <td>False</td>
</tr>
<tr>
    <td>Confections</td>  <td>Dairy Products</td> <td>167.0244</td>   <td>0.001</td>  <td>46.2712</td>  <td>287.7776</td>   <td>True</td> 
</tr>
<tr>
    <td>Confections</td>  <td>Grains/Cereals</td>  <td>-5.6635</td>    <td>0.9</td>  <td>-149.8807</td> <td>138.5537</td>   <td>False</td>
</tr>
<tr>
    <td>Confections</td>   <td>Meat/Poultry</td>  <td>383.9751</td>   <td>0.001</td> <td>234.2101</td>  <td>533.7401</td>   <td>True</td> 
</tr>
<tr>
    <td>Confections</td>      <td>Produce</td>    <td>269.0386</td>   <td>0.001</td> <td>107.3415</td>  <td>430.7357</td>   <td>True</td> 
</tr>
<tr>
    <td>Confections</td>      <td>Seafood</td>    <td>-73.2226</td>  <td>0.6099</td> <td>-197.392</td>   <td>50.9467</td>   <td>False</td>
</tr>
<tr>
  <td>Dairy Products</td> <td>Grains/Cereals</td> <td>-172.6879</td> <td>0.0054</td> <td>-314.2272</td> <td>-31.1485</td>   <td>True</td> 
</tr>
<tr>
  <td>Dairy Products</td>  <td>Meat/Poultry</td>  <td>216.9507</td>   <td>0.001</td>  <td>69.7626</td>  <td>364.1389</td>   <td>True</td> 
</tr>
<tr>
  <td>Dairy Products</td>     <td>Produce</td>    <td>102.0142</td>  <td>0.5181</td> <td>-57.2991</td>  <td>261.3276</td>   <td>False</td>
</tr>
<tr>
  <td>Dairy Products</td>     <td>Seafood</td>    <td>-240.247</td>   <td>0.001</td> <td>-361.2959</td> <td>-119.1982</td>  <td>True</td> 
</tr>
<tr>
  <td>Grains/Cereals</td>  <td>Meat/Poultry</td>  <td>389.6386</td>   <td>0.001</td> <td>222.6607</td>  <td>556.6164</td>   <td>True</td> 
</tr>
<tr>
  <td>Grains/Cereals</td>     <td>Produce</td>    <td>274.7021</td>   <td>0.001</td>  <td>96.9438</td>  <td>452.4604</td>   <td>True</td> 
</tr>
<tr>
  <td>Grains/Cereals</td>     <td>Seafood</td>    <td>-67.5591</td>   <td>0.831</td> <td>-212.024</td>   <td>76.9057</td>   <td>False</td>
</tr>
<tr>
   <td>Meat/Poultry</td>      <td>Produce</td>    <td>-114.9365</td> <td>0.5359</td> <td>-297.2246</td>  <td>67.3516</td>   <td>False</td>
</tr>
<tr>
   <td>Meat/Poultry</td>      <td>Seafood</td>    <td>-457.1977</td>  <td>0.001</td> <td>-607.2012</td> <td>-307.1942</td>  <td>True</td> 
</tr>
<tr>
      <td>Produce</td>        <td>Seafood</td>    <td>-342.2612</td>  <td>0.001</td> <td>-504.1792</td> <td>-180.3432</td>  <td>True</td> 
</tr>
</table>




```python
for cat, cat_data in cats.items():
    print(f'The average revenue for {cat} is ${round(cat_data.mean(),2)}')
```

    The average revenue for Dairy Products is $593.86
    The average revenue for Grains/Cereals is $421.17
    The average revenue for Produce is $695.87
    The average revenue for Seafood is $353.61
    The average revenue for Condiments is $455.54
    The average revenue for Confections is $426.83
    The average revenue for Beverages is $399.77
    The average revenue for Meat/Poultry is $810.81
    

### Hypothesis 2: A Clean Vizualization


```python
#help(cat_df.groupby('group').mean().sort_values('data').plot)
```


```python
index = list(cat_df.groupby('group').mean().sort_values('data', ascending=False).index)
index
```




    ['Meat/Poultry',
     'Produce',
     'Dairy Products',
     'Condiments',
     'Confections',
     'Grains/Cereals',
     'Beverages',
     'Seafood']




```python
import matplotlib.ticker as ticker
plt.style.use('seaborn')
fig, ax = plt.subplots(figsize=(10,8))
sns.barplot(data=cat_df, x=round(cat_df['data']), y=cat_df['group'],order=index, ci=68, palette='Wistia_r')
formatter = ticker.FormatStrFormatter('$%1.2f')
ax.xaxis.set_major_formatter(formatter)
plt.axvline(cat_df['data'].mean(), linestyle='--', color='gray')
plt.ylabel('Category')
plt.xlabel('Average Revenue Generated')
plt.xticks(rotation=45)
plt.title('Average Revenue* Generated By Category', fontsize=20)
```




    Text(0.5, 1.0, 'Average Revenue* Generated By Category')




![png](output_109_1.png)



```python
f, ax = plt.subplots(figsize=(10,8))
#sns.despine(f, left=True, bottom=True)
sns.catplot(data=cat_df, x='group', y='data', ax=ax)

```




    <seaborn.axisgrid.FacetGrid at 0x201332e4c88>




![png](output_110_1.png)



![png](output_110_2.png)



```python
tukeycdf = fn.tukey_df(tukeyc)
```

The following groups are statistically similar and accept the null hypothesis that all categories generate equal revenue:


```python
tukeycfalse  = tukeycdf.loc[tukeycdf['reject']==False]
tukeycfalse
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>group1</th>
      <th>group2</th>
      <th>meandiff</th>
      <th>p-adj</th>
      <th>lower</th>
      <th>upper</th>
      <th>reject</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>Beverages</td>
      <td>Condiments</td>
      <td>55.7712</td>
      <td>0.9000</td>
      <td>-78.8580</td>
      <td>190.4005</td>
      <td>False</td>
    </tr>
    <tr>
      <td>1</td>
      <td>Beverages</td>
      <td>Confections</td>
      <td>27.0669</td>
      <td>0.9000</td>
      <td>-91.4026</td>
      <td>145.5364</td>
      <td>False</td>
    </tr>
    <tr>
      <td>3</td>
      <td>Beverages</td>
      <td>Grains/Cereals</td>
      <td>21.4034</td>
      <td>0.9000</td>
      <td>-118.1928</td>
      <td>160.9996</td>
      <td>False</td>
    </tr>
    <tr>
      <td>6</td>
      <td>Beverages</td>
      <td>Seafood</td>
      <td>-46.1557</td>
      <td>0.9000</td>
      <td>-164.9266</td>
      <td>72.6151</td>
      <td>False</td>
    </tr>
    <tr>
      <td>7</td>
      <td>Condiments</td>
      <td>Confections</td>
      <td>-28.7043</td>
      <td>0.9000</td>
      <td>-168.1193</td>
      <td>110.7106</td>
      <td>False</td>
    </tr>
    <tr>
      <td>9</td>
      <td>Condiments</td>
      <td>Grains/Cereals</td>
      <td>-34.3678</td>
      <td>0.9000</td>
      <td>-192.1290</td>
      <td>123.3933</td>
      <td>False</td>
    </tr>
    <tr>
      <td>12</td>
      <td>Condiments</td>
      <td>Seafood</td>
      <td>-101.9270</td>
      <td>0.3439</td>
      <td>-241.5981</td>
      <td>37.7441</td>
      <td>False</td>
    </tr>
    <tr>
      <td>14</td>
      <td>Confections</td>
      <td>Grains/Cereals</td>
      <td>-5.6635</td>
      <td>0.9000</td>
      <td>-149.8807</td>
      <td>138.5537</td>
      <td>False</td>
    </tr>
    <tr>
      <td>17</td>
      <td>Confections</td>
      <td>Seafood</td>
      <td>-73.2226</td>
      <td>0.6099</td>
      <td>-197.3920</td>
      <td>50.9467</td>
      <td>False</td>
    </tr>
    <tr>
      <td>20</td>
      <td>Dairy Products</td>
      <td>Produce</td>
      <td>102.0142</td>
      <td>0.5181</td>
      <td>-57.2991</td>
      <td>261.3276</td>
      <td>False</td>
    </tr>
    <tr>
      <td>24</td>
      <td>Grains/Cereals</td>
      <td>Seafood</td>
      <td>-67.5591</td>
      <td>0.8310</td>
      <td>-212.0240</td>
      <td>76.9057</td>
      <td>False</td>
    </tr>
    <tr>
      <td>25</td>
      <td>Meat/Poultry</td>
      <td>Produce</td>
      <td>-114.9365</td>
      <td>0.5359</td>
      <td>-297.2246</td>
      <td>67.3516</td>
      <td>False</td>
    </tr>
  </tbody>
</table>
</div>



The folowing groups can reject the null hypothesis:


```python
tukeyctrues  = tukeycdf.loc[tukeycdf['reject']==True]
tukeyctrues
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>group1</th>
      <th>group2</th>
      <th>meandiff</th>
      <th>p-adj</th>
      <th>lower</th>
      <th>upper</th>
      <th>reject</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2</td>
      <td>Beverages</td>
      <td>Dairy Products</td>
      <td>194.0913</td>
      <td>0.0010</td>
      <td>78.8965</td>
      <td>309.2860</td>
      <td>True</td>
    </tr>
    <tr>
      <td>4</td>
      <td>Beverages</td>
      <td>Meat/Poultry</td>
      <td>411.0420</td>
      <td>0.0010</td>
      <td>265.7215</td>
      <td>556.3625</td>
      <td>True</td>
    </tr>
    <tr>
      <td>5</td>
      <td>Beverages</td>
      <td>Produce</td>
      <td>296.1055</td>
      <td>0.0010</td>
      <td>138.5160</td>
      <td>453.6950</td>
      <td>True</td>
    </tr>
    <tr>
      <td>8</td>
      <td>Condiments</td>
      <td>Dairy Products</td>
      <td>138.3200</td>
      <td>0.0449</td>
      <td>1.6769</td>
      <td>274.9631</td>
      <td>True</td>
    </tr>
    <tr>
      <td>10</td>
      <td>Condiments</td>
      <td>Meat/Poultry</td>
      <td>355.2707</td>
      <td>0.0010</td>
      <td>192.4225</td>
      <td>518.1190</td>
      <td>True</td>
    </tr>
    <tr>
      <td>11</td>
      <td>Condiments</td>
      <td>Produce</td>
      <td>240.3342</td>
      <td>0.0010</td>
      <td>66.4494</td>
      <td>414.2191</td>
      <td>True</td>
    </tr>
    <tr>
      <td>13</td>
      <td>Confections</td>
      <td>Dairy Products</td>
      <td>167.0244</td>
      <td>0.0010</td>
      <td>46.2712</td>
      <td>287.7776</td>
      <td>True</td>
    </tr>
    <tr>
      <td>15</td>
      <td>Confections</td>
      <td>Meat/Poultry</td>
      <td>383.9751</td>
      <td>0.0010</td>
      <td>234.2101</td>
      <td>533.7401</td>
      <td>True</td>
    </tr>
    <tr>
      <td>16</td>
      <td>Confections</td>
      <td>Produce</td>
      <td>269.0386</td>
      <td>0.0010</td>
      <td>107.3415</td>
      <td>430.7357</td>
      <td>True</td>
    </tr>
    <tr>
      <td>18</td>
      <td>Dairy Products</td>
      <td>Grains/Cereals</td>
      <td>-172.6879</td>
      <td>0.0054</td>
      <td>-314.2272</td>
      <td>-31.1485</td>
      <td>True</td>
    </tr>
    <tr>
      <td>19</td>
      <td>Dairy Products</td>
      <td>Meat/Poultry</td>
      <td>216.9507</td>
      <td>0.0010</td>
      <td>69.7626</td>
      <td>364.1389</td>
      <td>True</td>
    </tr>
    <tr>
      <td>21</td>
      <td>Dairy Products</td>
      <td>Seafood</td>
      <td>-240.2470</td>
      <td>0.0010</td>
      <td>-361.2959</td>
      <td>-119.1982</td>
      <td>True</td>
    </tr>
    <tr>
      <td>22</td>
      <td>Grains/Cereals</td>
      <td>Meat/Poultry</td>
      <td>389.6386</td>
      <td>0.0010</td>
      <td>222.6607</td>
      <td>556.6164</td>
      <td>True</td>
    </tr>
    <tr>
      <td>23</td>
      <td>Grains/Cereals</td>
      <td>Produce</td>
      <td>274.7021</td>
      <td>0.0010</td>
      <td>96.9438</td>
      <td>452.4604</td>
      <td>True</td>
    </tr>
    <tr>
      <td>26</td>
      <td>Meat/Poultry</td>
      <td>Seafood</td>
      <td>-457.1977</td>
      <td>0.0010</td>
      <td>-607.2012</td>
      <td>-307.1942</td>
      <td>True</td>
    </tr>
    <tr>
      <td>27</td>
      <td>Produce</td>
      <td>Seafood</td>
      <td>-342.2612</td>
      <td>0.0010</td>
      <td>-504.1792</td>
      <td>-180.3432</td>
      <td>True</td>
    </tr>
  </tbody>
</table>
</div>




```python
def mult_Cohn_d(tukey_result_df, df_dict):
    '''Using a dataframe from Tukey Test Results and a 
    corresponding dictionary, this function loops through 
    each variable and returns the adjusted p-value and Cohn_d test'''
    import pandas as pd
    
    res = [['g1', 'g2','padj', 'd']]
    for i, row in tukey_result_df.iterrows():
        g1 = row['group1']
        g2 = row['group2']
        padj = row['p-adj']
        d = fn.Cohen_d(df_dict[g1], df_dict[g2])

        res.append([g1, g2,padj, d])

    mdc = pd.DataFrame(res[1:], columns=res[0])
    return mdc
```

The table below illustrates those categories that can reject the null hypothesis that states all categories generate equal revenue.  The padj is the probability this is due to chance and the d column shows the effect size. 


```python
mult_Cohn_d(tukeyctrues, cats)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>g1</th>
      <th>g2</th>
      <th>padj</th>
      <th>d</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>Beverages</td>
      <td>Dairy Products</td>
      <td>0.0010</td>
      <td>-0.351635</td>
    </tr>
    <tr>
      <td>1</td>
      <td>Beverages</td>
      <td>Meat/Poultry</td>
      <td>0.0010</td>
      <td>-0.596175</td>
    </tr>
    <tr>
      <td>2</td>
      <td>Beverages</td>
      <td>Produce</td>
      <td>0.0010</td>
      <td>-0.520603</td>
    </tr>
    <tr>
      <td>3</td>
      <td>Condiments</td>
      <td>Dairy Products</td>
      <td>0.0449</td>
      <td>-0.277491</td>
    </tr>
    <tr>
      <td>4</td>
      <td>Condiments</td>
      <td>Meat/Poultry</td>
      <td>0.0010</td>
      <td>-0.517399</td>
    </tr>
    <tr>
      <td>5</td>
      <td>Condiments</td>
      <td>Produce</td>
      <td>0.0010</td>
      <td>-0.490099</td>
    </tr>
    <tr>
      <td>6</td>
      <td>Confections</td>
      <td>Dairy Products</td>
      <td>0.0010</td>
      <td>-0.340630</td>
    </tr>
    <tr>
      <td>7</td>
      <td>Confections</td>
      <td>Meat/Poultry</td>
      <td>0.0010</td>
      <td>-0.600173</td>
    </tr>
    <tr>
      <td>8</td>
      <td>Confections</td>
      <td>Produce</td>
      <td>0.0010</td>
      <td>-0.560435</td>
    </tr>
    <tr>
      <td>9</td>
      <td>Dairy Products</td>
      <td>Grains/Cereals</td>
      <td>0.0054</td>
      <td>0.349940</td>
    </tr>
    <tr>
      <td>10</td>
      <td>Dairy Products</td>
      <td>Meat/Poultry</td>
      <td>0.0010</td>
      <td>-0.310545</td>
    </tr>
    <tr>
      <td>11</td>
      <td>Dairy Products</td>
      <td>Seafood</td>
      <td>0.0010</td>
      <td>0.525083</td>
    </tr>
    <tr>
      <td>12</td>
      <td>Grains/Cereals</td>
      <td>Meat/Poultry</td>
      <td>0.0010</td>
      <td>-0.563832</td>
    </tr>
    <tr>
      <td>13</td>
      <td>Grains/Cereals</td>
      <td>Produce</td>
      <td>0.0010</td>
      <td>-0.570886</td>
    </tr>
    <tr>
      <td>14</td>
      <td>Meat/Poultry</td>
      <td>Seafood</td>
      <td>0.0010</td>
      <td>0.754594</td>
    </tr>
    <tr>
      <td>15</td>
      <td>Produce</td>
      <td>Seafood</td>
      <td>0.0010</td>
      <td>0.798069</td>
    </tr>
  </tbody>
</table>
</div>



### Hypothesis 2 Findings and Recommendation:

#### Findings:

***Reject the null hypothesis:***
* 𝐻0  : All categories generate equal revenues.

***Alternative hypotheis***
* 𝐻1  : Certain categories sell at statistically higher rates of revnue than others.

Top three revenue-generating categories: Meat/Poultry, Produce, and Dairy Products.

Statistically, Meat/Poultry & Produce were statistically equivalent and ranked as top sellers, Dairy & Produce were statiscally equal. 
(Definition of statistically equal: they returned false value from Tukey test, indicating they had a simliar mean and therefore statiticaly equal with a .05 chance of falsely being classified as such)


 
 
Category | Average Revenue
-- | -- |
Meat/Poultry | `$810.81`
Produce | `$695.87`
Dairy Products | `$593.86`
Condiments | `$455.54`
Confections | `$426.83`
Grains/Cereals | `$421.17``
Beverages | `$399.77`
Seafood | `$353.61`

The table(s) above outlines how the various categories compare to each other.  If the adjusted p-value in column padj is >.05, they are statistically equal.  Conversely of the adjusted p-value 'adjp' is <.05 the two samples are statistically not-equal.  This is further examined by the effect size illustrated in column d.   d=0.2 be considered a 'small' effect size, 0.5 represents a 'medium' effect size and 0.8 a 'large' effect size. 

Notes:
Revenue is calculated by subtracting any extended discounts from the salesprice and multiplying that by quantity sold.


#### Recommendation: 

If there are additional products that align with the higher revenue generating categories, that category could be broadened to maximize revenue generating potential.  

Example: Meat/Poultry currently has 6 products, this could be expanded.  Conversely, the seafood category carries 12 products which could be narrowed.  Additional analysis could demonstrate which seafood are the best sellers which would be preserved.

Knowing what revenue each category generates could potentially influence the ability to appropriately categorize discounts.  However, not knowing profit margins - we'd need to take this into consideration.






# HYPOTHESIS 3

> ***Do certain sales representatives sell more than others?  Who are the top sellers?***

$H0$: All sales representatives generate equal revenue.

$H1$: Some sales representatives generate more than others in revenue.

### Importing and inspecting data from Product, OrderDetail, Order and Employee Tables
These table includes information on:

    1) Product information including SalesPrice, Discount and Quantity Sold
    2) Sales Representative Information


```python
cur.execute("""SELECT 
                ProductID, 
                ProductName, 
                Discontinued,
                OrderID, 
                ProductID, 
                od.UnitPrice AS SalesPrice, 
                Quantity, 
                Discount,
                EmployeeID, 
                LastName, 
                FirstName, 
                e.Region, 
                ShippedDate
                FROM Product AS p
                JOIN OrderDetail AS od
                ON od.ProductID = p.Id 
                JOIN 'Order' AS o
                ON o.Id = od.OrderId
                JOIN Employee AS e
                ON o.EmployeeID = e.ID;""")
dfr = pd.DataFrame(cur.fetchall(), columns=[x[0] for x in cur.description])
dfr
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ProductId</th>
      <th>ProductName</th>
      <th>Discontinued</th>
      <th>OrderId</th>
      <th>ProductId</th>
      <th>SalesPrice</th>
      <th>Quantity</th>
      <th>Discount</th>
      <th>EmployeeId</th>
      <th>LastName</th>
      <th>FirstName</th>
      <th>Region</th>
      <th>ShippedDate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>11</td>
      <td>Queso Cabrales</td>
      <td>0</td>
      <td>10248</td>
      <td>11</td>
      <td>14.00</td>
      <td>12</td>
      <td>0.00</td>
      <td>5</td>
      <td>Buchanan</td>
      <td>Steven</td>
      <td>British Isles</td>
      <td>2012-07-16</td>
    </tr>
    <tr>
      <td>1</td>
      <td>42</td>
      <td>Singaporean Hokkien Fried Mee</td>
      <td>1</td>
      <td>10248</td>
      <td>42</td>
      <td>9.80</td>
      <td>10</td>
      <td>0.00</td>
      <td>5</td>
      <td>Buchanan</td>
      <td>Steven</td>
      <td>British Isles</td>
      <td>2012-07-16</td>
    </tr>
    <tr>
      <td>2</td>
      <td>72</td>
      <td>Mozzarella di Giovanni</td>
      <td>0</td>
      <td>10248</td>
      <td>72</td>
      <td>34.80</td>
      <td>5</td>
      <td>0.00</td>
      <td>5</td>
      <td>Buchanan</td>
      <td>Steven</td>
      <td>British Isles</td>
      <td>2012-07-16</td>
    </tr>
    <tr>
      <td>3</td>
      <td>14</td>
      <td>Tofu</td>
      <td>0</td>
      <td>10249</td>
      <td>14</td>
      <td>18.60</td>
      <td>9</td>
      <td>0.00</td>
      <td>6</td>
      <td>Suyama</td>
      <td>Michael</td>
      <td>British Isles</td>
      <td>2012-07-10</td>
    </tr>
    <tr>
      <td>4</td>
      <td>51</td>
      <td>Manjimup Dried Apples</td>
      <td>0</td>
      <td>10249</td>
      <td>51</td>
      <td>42.40</td>
      <td>40</td>
      <td>0.00</td>
      <td>6</td>
      <td>Suyama</td>
      <td>Michael</td>
      <td>British Isles</td>
      <td>2012-07-10</td>
    </tr>
    <tr>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <td>2150</td>
      <td>64</td>
      <td>Wimmers gute Semmelknödel</td>
      <td>0</td>
      <td>11077</td>
      <td>64</td>
      <td>33.25</td>
      <td>2</td>
      <td>0.03</td>
      <td>1</td>
      <td>Davolio</td>
      <td>Nancy</td>
      <td>North America</td>
      <td>None</td>
    </tr>
    <tr>
      <td>2151</td>
      <td>66</td>
      <td>Louisiana Hot Spiced Okra</td>
      <td>0</td>
      <td>11077</td>
      <td>66</td>
      <td>17.00</td>
      <td>1</td>
      <td>0.00</td>
      <td>1</td>
      <td>Davolio</td>
      <td>Nancy</td>
      <td>North America</td>
      <td>None</td>
    </tr>
    <tr>
      <td>2152</td>
      <td>73</td>
      <td>Röd Kaviar</td>
      <td>0</td>
      <td>11077</td>
      <td>73</td>
      <td>15.00</td>
      <td>2</td>
      <td>0.01</td>
      <td>1</td>
      <td>Davolio</td>
      <td>Nancy</td>
      <td>North America</td>
      <td>None</td>
    </tr>
    <tr>
      <td>2153</td>
      <td>75</td>
      <td>Rhönbräu Klosterbier</td>
      <td>0</td>
      <td>11077</td>
      <td>75</td>
      <td>7.75</td>
      <td>4</td>
      <td>0.00</td>
      <td>1</td>
      <td>Davolio</td>
      <td>Nancy</td>
      <td>North America</td>
      <td>None</td>
    </tr>
    <tr>
      <td>2154</td>
      <td>77</td>
      <td>Original Frankfurter grüne Soße</td>
      <td>0</td>
      <td>11077</td>
      <td>77</td>
      <td>13.00</td>
      <td>2</td>
      <td>0.00</td>
      <td>1</td>
      <td>Davolio</td>
      <td>Nancy</td>
      <td>North America</td>
      <td>None</td>
    </tr>
  </tbody>
</table>
<p>2155 rows × 13 columns</p>
</div>




```python


#Sales Revenue is calculated by multiplying the adjusted price (accounting for any discounts) times quantity
dfr['SaleRev'] = (dfr['SalesPrice'] * (1-dfr['Discount'])) * dfr['Quantity']

```


```python
empcount = len(dfr['EmployeeId'].unique())
avrev = dfr['SaleRev'].mean()
print(f'There are {empcount} employees in this company associated with sales information')
print(f'The calculated avarage revenue generated by a sales representative in this dataset is ${round(avrev)}')
```

    There are 9 employees in this company associated with sales information
    The calculated avarage revenue generated by a sales representative in this dataset is $587.0
    

### Hypothesis 3 Preliminary Visualizations:


```python
fig, ax = plt.subplots(figsize=(8,5))
sns.distplot(dfr['SaleRev'], color='green')
plt.axvline(avrev, color='lightgreen' )
plt.xlabel('Sales Revenue')
plt.ylabel('Distribution')
plt.title('Average Sales Revenue Distribution', fontsize=18)
plt.show()
```


![png](output_126_0.png)



```python
fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(data=dfr, x='EmployeeId', y='SaleRev', ci=68, ax=ax)
plt.title('Average Revenue by Sales Representative', fontsize=16)
plt.axhline(avrev,linestyle="--", color='gray', linewidth=.6 )
plt.xlabel('Employee Id')
plt.ylabel('Sales Revenue')
plt.show()

```


![png](output_127_0.png)


Employees are listed in the table below:
Although the employee names are unique, for the sake of data inspection we'll continue to use Employee Id as the unique identifier and reference the table above to gather additional insight.


```python
cur.execute("""SELECT ID, LastName, FirstName, Title, Region
                from Employee""")
empsdata = pd.DataFrame(cur.fetchall(), columns=[x[0] for x in cur.description])
empsdata
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Id</th>
      <th>LastName</th>
      <th>FirstName</th>
      <th>Title</th>
      <th>Region</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>1</td>
      <td>Davolio</td>
      <td>Nancy</td>
      <td>Sales Representative</td>
      <td>North America</td>
    </tr>
    <tr>
      <td>1</td>
      <td>2</td>
      <td>Fuller</td>
      <td>Andrew</td>
      <td>Vice President, Sales</td>
      <td>North America</td>
    </tr>
    <tr>
      <td>2</td>
      <td>3</td>
      <td>Leverling</td>
      <td>Janet</td>
      <td>Sales Representative</td>
      <td>North America</td>
    </tr>
    <tr>
      <td>3</td>
      <td>4</td>
      <td>Peacock</td>
      <td>Margaret</td>
      <td>Sales Representative</td>
      <td>North America</td>
    </tr>
    <tr>
      <td>4</td>
      <td>5</td>
      <td>Buchanan</td>
      <td>Steven</td>
      <td>Sales Manager</td>
      <td>British Isles</td>
    </tr>
    <tr>
      <td>5</td>
      <td>6</td>
      <td>Suyama</td>
      <td>Michael</td>
      <td>Sales Representative</td>
      <td>British Isles</td>
    </tr>
    <tr>
      <td>6</td>
      <td>7</td>
      <td>King</td>
      <td>Robert</td>
      <td>Sales Representative</td>
      <td>British Isles</td>
    </tr>
    <tr>
      <td>7</td>
      <td>8</td>
      <td>Callahan</td>
      <td>Laura</td>
      <td>Inside Sales Coordinator</td>
      <td>North America</td>
    </tr>
    <tr>
      <td>8</td>
      <td>9</td>
      <td>Dodsworth</td>
      <td>Anne</td>
      <td>Sales Representative</td>
      <td>British Isles</td>
    </tr>
  </tbody>
</table>
</div>




```python
reps = {}
for rep in dfr['EmployeeId'].unique():
    reps[str(rep)] = dfr.groupby('EmployeeId').get_group(rep)['SaleRev']

```


```python
fig, ax = plt.subplots(figsize=(10,5))
for k,v in reps.items():
    sns.distplot(v,label=v)

plt.title('Sales Revenue By Distribution by Rep')
print('Distributions appear roughly equal and there appears to be outliers')
```

    Distributions appear roughly equal and there appears to be outliers
    


![png](output_131_1.png)


#### Initial Observations:
Datatype is numeric in this 2155 order sample.

There are 9 employees in this company associated with sales information

The avarage revenue generated by a sales representative is $629.00. 

Initial visual inspection indicates roughly uniform distribution in sales revenue, more than half of the sales representatives achieve the average.  Additional testing will demonstrate if it is significant.

Since we are comparing multiple discounts to inspect it's impact on quantity ordered an AVNOVA test will be run:
Assumptions for ANOVA Testing: 

1) No significant outliers 
    Upon a quick visual inspection, there appears to be some outliers that could be removed

2) Equal variance
    


3) Normality (if n>15)
      Not required for samples greater than 15

### Assumption 1: Outliers


```python
for rep, rep_data in reps.items():
    idx_outs = fn.find_outliers_Z(rep_data)
    print(f'Found {idx_outs.sum()} outliers in Employee # {rep}')
    reps[rep] = rep_data[~idx_outs]
print('\n All of these outliers were removed')


```

    Found 3 outliers in Employee # 5
    Found 3 outliers in Employee # 6
    Found 7 outliers in Employee # 4
    Found 4 outliers in Employee # 3
    Found 2 outliers in Employee # 9
    Found 4 outliers in Employee # 1
    Found 5 outliers in Employee # 8
    Found 5 outliers in Employee # 2
    Found 5 outliers in Employee # 7
    
     All of these outliers were removed
    


```python
fig, ax = plt.subplots(figsize=(10,5))
for k,v in reps.items():
    sns.distplot(v,label=v)

plt.title('Revised: Sales Revenue Distribution by Rep')
print('Distributions appear roughly equal and outliers are visibly removed in comparisson with other visual')
```

    Distributions appear roughly equal and outliers are visibly removed in comparisson with other visual
    


![png](output_135_1.png)


###  Asumption 2: Equal Variance

Results are NOT equal variance for this group


```python
#from functions import test_equal_variance
import scipy.stats as stats
```


```python
datas = []
for k,v in reps.items():
    datas.append(v)
    
```


```python
stat,p = stats.levene(*datas)
print(f'Lavene test for equal variance results are {round(p,4)}')
sig = 'do NOT' if p < .05 else 'DO'

print(f'The groups {sig} have equal variance')
      
          
```

    Lavene test for equal variance results are 0.0143
    The groups do NOT have equal variance
    

### Assumption 3:  Normality
The lengths of these samples are >15 so normality criteria is met.


```python
n = []

for rep,samples in reps.items():
    print(f'There are {len(samples)} samples in the data set for Employee #{rep}.')
    n.append(len(samples)>15)
if all(n):
    print('\nAll samples are >15: Normality Assumption Criterion is met.')
    




```

    There are 114 samples in the data set for Employee #5.
    There are 165 samples in the data set for Employee #6.
    There are 413 samples in the data set for Employee #4.
    There are 317 samples in the data set for Employee #3.
    There are 105 samples in the data set for Employee #9.
    There are 341 samples in the data set for Employee #1.
    There are 255 samples in the data set for Employee #8.
    There are 236 samples in the data set for Employee #2.
    There are 171 samples in the data set for Employee #7.
    
    All samples are >15: Normality Assumption Criterion is met.
    


```python
stat, p = stats.kruskal(*datas)
print(f"Kruskal test p value: {round(p,4)}")
```

    Kruskal test p value: 0.2968
    


```python
stat, p = stats.f_oneway(*datas)
print(stat,p)
```

    2.180626766904163 0.026222185205141618
    


```python
clean_data = fn.prep_data_for_tukeys(reps)
clean_data
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>data</th>
      <th>group</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>168.000</td>
      <td>5</td>
    </tr>
    <tr>
      <td>1</td>
      <td>98.000</td>
      <td>5</td>
    </tr>
    <tr>
      <td>2</td>
      <td>174.000</td>
      <td>5</td>
    </tr>
    <tr>
      <td>17</td>
      <td>45.900</td>
      <td>5</td>
    </tr>
    <tr>
      <td>18</td>
      <td>342.720</td>
      <td>5</td>
    </tr>
    <tr>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <td>2077</td>
      <td>390.000</td>
      <td>7</td>
    </tr>
    <tr>
      <td>2103</td>
      <td>52.350</td>
      <td>7</td>
    </tr>
    <tr>
      <td>2104</td>
      <td>386.400</td>
      <td>7</td>
    </tr>
    <tr>
      <td>2105</td>
      <td>490.000</td>
      <td>7</td>
    </tr>
    <tr>
      <td>2123</td>
      <td>232.085</td>
      <td>7</td>
    </tr>
  </tbody>
</table>
<p>2117 rows × 2 columns</p>
</div>



### Hypothesis 3: A Clean Visualization:


```python
f, ax = plt.subplots(figsize=(8,4))
sns.set(style="whitegrid")
sns.barplot(data=clean_data, x='group', y='data', ci=68)
plt.xlabel('Employee Id')
plt.ylabel('Average Revenue Generated')
plt.axhline(clean_data['data'].mean(), linestyle="--", color='darkgray')

plt.title('Average Revenue Generated by Sales Representative', fontsize=20)

```




    Text(0.5, 1.0, 'Average Revenue Generated by Sales Representative')




![png](output_146_1.png)


Observation:
The plot above is misleading since it goes off of means it skews the data.  Further testing indicates there are no statistical differences between representatives in terms of revenue generated over this time span.  The subsequent plot reveals a more accurate depiction of what testing demonstrates.


```python
mu = clean_data['data'].mean()

sns.catplot(data=clean_data, x='group', y='data', 
            kind='swarm', height=6, aspect=1.5)
formatter = ticker.FormatStrFormatter('$%1.2f')
plt.axhline(mu, color='k', linestyle="-", lw=2)
plt.xlabel('Employee Id')
plt.ylabel('Average Total Revenue in US Dollars')
plt.title('Average Total Revenue by Sales Representaitve', fontsize=20)
print(f'Average revenue across all sales representatives: ${round(mu,2)}')
```

    Average revenue across all sales representatives: $494.72
    


![png](output_148_1.png)



```python
#datacleaning for additional testing:
clean_data['data'] = clean_data['data'].astype(float)
clean_data['group'] = clean_data['group'].astype(str)
```


```python
clean_data
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>data</th>
      <th>group</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>168.000</td>
      <td>5</td>
    </tr>
    <tr>
      <td>1</td>
      <td>98.000</td>
      <td>5</td>
    </tr>
    <tr>
      <td>2</td>
      <td>174.000</td>
      <td>5</td>
    </tr>
    <tr>
      <td>17</td>
      <td>45.900</td>
      <td>5</td>
    </tr>
    <tr>
      <td>18</td>
      <td>342.720</td>
      <td>5</td>
    </tr>
    <tr>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <td>2077</td>
      <td>390.000</td>
      <td>7</td>
    </tr>
    <tr>
      <td>2103</td>
      <td>52.350</td>
      <td>7</td>
    </tr>
    <tr>
      <td>2104</td>
      <td>386.400</td>
      <td>7</td>
    </tr>
    <tr>
      <td>2105</td>
      <td>490.000</td>
      <td>7</td>
    </tr>
    <tr>
      <td>2123</td>
      <td>232.085</td>
      <td>7</td>
    </tr>
  </tbody>
</table>
<p>2117 rows × 2 columns</p>
</div>



## The table below illustrates to accept the null hypothesis.


```python
tukeys = sms.stats.multicomp.pairwise_tukeyhsd(clean_data['data'], clean_data['group'])
tukeys.summary()
```




<table class="simpletable">
<caption>Multiple Comparison of Means - Tukey HSD, FWER=0.05</caption>
<tr>
  <th>group1</th> <th>group2</th> <th>meandiff</th>   <th>p-adj</th>   <th>lower</th>     <th>upper</th>  <th>reject</th>
</tr>
<tr>
     <td>1</td>      <td>2</td>    <td>70.6795</td>  <td>0.7896</td> <td>-67.9146</td>  <td>209.2736</td>  <td>False</td>
</tr>
<tr>
     <td>1</td>      <td>3</td>    <td>62.1979</td>  <td>0.8328</td> <td>-65.5036</td>  <td>189.8995</td>  <td>False</td>
</tr>
<tr>
     <td>1</td>      <td>4</td>    <td>-2.0207</td>    <td>0.9</td>  <td>-121.7839</td> <td>117.7426</td>  <td>False</td>
</tr>
<tr>
     <td>1</td>      <td>5</td>    <td>2.7041</td>     <td>0.9</td>  <td>-174.3746</td> <td>179.7827</td>  <td>False</td>
</tr>
<tr>
     <td>1</td>      <td>6</td>   <td>-81.4678</td>  <td>0.7616</td> <td>-236.6872</td>  <td>73.7517</td>  <td>False</td>
</tr>
<tr>
     <td>1</td>      <td>7</td>    <td>68.5247</td>    <td>0.9</td>  <td>-84.8486</td>  <td>221.8981</td>  <td>False</td>
</tr>
<tr>
     <td>1</td>      <td>8</td>   <td>-24.7293</td>    <td>0.9</td>  <td>-160.2376</td>  <td>110.779</td>  <td>False</td>
</tr>
<tr>
     <td>1</td>      <td>9</td>   <td>101.7408</td>  <td>0.7013</td> <td>-80.9369</td>  <td>284.4186</td>  <td>False</td>
</tr>
<tr>
     <td>2</td>      <td>3</td>    <td>-8.4815</td>    <td>0.9</td>  <td>-149.2052</td> <td>132.2421</td>  <td>False</td>
</tr>
<tr>
     <td>2</td>      <td>4</td>   <td>-72.7002</td>   <td>0.725</td> <td>-206.2617</td>  <td>60.8614</td>  <td>False</td>
</tr>
<tr>
     <td>2</td>      <td>5</td>   <td>-67.9754</td>    <td>0.9</td>  <td>-254.6631</td> <td>118.7123</td>  <td>False</td>
</tr>
<tr>
     <td>2</td>      <td>6</td>   <td>-152.1472</td> <td>0.1034</td> <td>-318.2452</td>  <td>13.9507</td>  <td>False</td>
</tr>
<tr>
     <td>2</td>      <td>7</td>    <td>-2.1547</td>    <td>0.9</td>  <td>-166.5288</td> <td>162.2193</td>  <td>False</td>
</tr>
<tr>
     <td>2</td>      <td>8</td>   <td>-95.4088</td>  <td>0.5349</td> <td>-243.2531</td>  <td>52.4356</td>  <td>False</td>
</tr>
<tr>
     <td>2</td>      <td>9</td>    <td>31.0613</td>    <td>0.9</td>  <td>-160.9455</td> <td>223.0682</td>  <td>False</td>
</tr>
<tr>
     <td>3</td>      <td>4</td>   <td>-64.2186</td>  <td>0.7606</td> <td>-186.4399</td>  <td>58.0027</td>  <td>False</td>
</tr>
<tr>
     <td>3</td>      <td>5</td>   <td>-59.4939</td>    <td>0.9</td>  <td>-238.2441</td> <td>119.2564</td>  <td>False</td>
</tr>
<tr>
     <td>3</td>      <td>6</td>   <td>-143.6657</td> <td>0.1049</td> <td>-300.7895</td>  <td>13.4581</td>  <td>False</td>
</tr>
<tr>
     <td>3</td>      <td>7</td>    <td>6.3268</td>     <td>0.9</td>  <td>-148.9735</td> <td>161.6271</td>  <td>False</td>
</tr>
<tr>
     <td>3</td>      <td>8</td>   <td>-86.9273</td>  <td>0.5613</td> <td>-224.6128</td>  <td>50.7583</td>  <td>False</td>
</tr>
<tr>
     <td>3</td>      <td>9</td>    <td>39.5429</td>    <td>0.9</td>  <td>-144.7557</td> <td>223.8415</td>  <td>False</td>
</tr>
<tr>
     <td>4</td>      <td>5</td>    <td>4.7247</td>     <td>0.9</td>  <td>-168.4434</td> <td>177.8929</td>  <td>False</td>
</tr>
<tr>
     <td>4</td>      <td>6</td>   <td>-79.4471</td>  <td>0.7575</td>  <td>-230.19</td>   <td>71.2959</td>  <td>False</td>
</tr>
<tr>
     <td>4</td>      <td>7</td>    <td>70.5454</td>  <td>0.8574</td> <td>-78.2959</td>  <td>219.3867</td>  <td>False</td>
</tr>
<tr>
     <td>4</td>      <td>8</td>   <td>-22.7086</td>    <td>0.9</td>  <td>-153.0653</td>  <td>107.648</td>  <td>False</td>
</tr>
<tr>
     <td>4</td>      <td>9</td>   <td>103.7615</td>  <td>0.6578</td> <td>-75.1282</td>  <td>282.6512</td>  <td>False</td>
</tr>
<tr>
     <td>5</td>      <td>6</td>   <td>-84.1718</td>    <td>0.9</td>  <td>-283.5134</td> <td>115.1697</td>  <td>False</td>
</tr>
<tr>
     <td>5</td>      <td>7</td>    <td>65.8207</td>    <td>0.9</td>  <td>-132.0867</td> <td>263.7281</td>  <td>False</td>
</tr>
<tr>
     <td>5</td>      <td>8</td>   <td>-27.4334</td>    <td>0.9</td>  <td>-211.8418</td>  <td>156.975</td>  <td>False</td>
</tr>
<tr>
     <td>5</td>      <td>9</td>    <td>99.0368</td>    <td>0.9</td>  <td>-122.3569</td> <td>320.4304</td>  <td>False</td>
</tr>
<tr>
     <td>6</td>      <td>7</td>   <td>149.9925</td>  <td>0.1837</td> <td>-28.6232</td>  <td>328.6082</td>  <td>False</td>
</tr>
<tr>
     <td>6</td>      <td>8</td>    <td>56.7384</td>    <td>0.9</td>  <td>-106.7935</td> <td>220.2704</td>  <td>False</td>
</tr>
<tr>
     <td>6</td>      <td>9</td>   <td>183.2086</td>  <td>0.1211</td> <td>-21.1229</td>  <td>387.5401</td>  <td>False</td>
</tr>
<tr>
     <td>7</td>      <td>8</td>   <td>-93.2541</td>  <td>0.6646</td> <td>-255.0348</td>  <td>68.5267</td>  <td>False</td>
</tr>
<tr>
     <td>7</td>      <td>9</td>    <td>33.2161</td>    <td>0.9</td>  <td>-169.7166</td> <td>236.1487</td>  <td>False</td>
</tr>
<tr>
     <td>8</td>      <td>9</td>   <td>126.4701</td>  <td>0.4952</td> <td>-63.3213</td>  <td>316.2616</td>  <td>False</td>
</tr>
</table>



### Effect Size Testing:


```python
tukeyrepdf = fn.tukey_df(tukeys)
```


```python
tukeyrepdf
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>group1</th>
      <th>group2</th>
      <th>meandiff</th>
      <th>p-adj</th>
      <th>lower</th>
      <th>upper</th>
      <th>reject</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>1</td>
      <td>2</td>
      <td>70.6795</td>
      <td>0.7896</td>
      <td>-67.9146</td>
      <td>209.2736</td>
      <td>False</td>
    </tr>
    <tr>
      <td>1</td>
      <td>1</td>
      <td>3</td>
      <td>62.1979</td>
      <td>0.8328</td>
      <td>-65.5036</td>
      <td>189.8995</td>
      <td>False</td>
    </tr>
    <tr>
      <td>2</td>
      <td>1</td>
      <td>4</td>
      <td>-2.0207</td>
      <td>0.9000</td>
      <td>-121.7839</td>
      <td>117.7426</td>
      <td>False</td>
    </tr>
    <tr>
      <td>3</td>
      <td>1</td>
      <td>5</td>
      <td>2.7041</td>
      <td>0.9000</td>
      <td>-174.3746</td>
      <td>179.7827</td>
      <td>False</td>
    </tr>
    <tr>
      <td>4</td>
      <td>1</td>
      <td>6</td>
      <td>-81.4678</td>
      <td>0.7616</td>
      <td>-236.6872</td>
      <td>73.7517</td>
      <td>False</td>
    </tr>
    <tr>
      <td>5</td>
      <td>1</td>
      <td>7</td>
      <td>68.5247</td>
      <td>0.9000</td>
      <td>-84.8486</td>
      <td>221.8981</td>
      <td>False</td>
    </tr>
    <tr>
      <td>6</td>
      <td>1</td>
      <td>8</td>
      <td>-24.7293</td>
      <td>0.9000</td>
      <td>-160.2376</td>
      <td>110.7790</td>
      <td>False</td>
    </tr>
    <tr>
      <td>7</td>
      <td>1</td>
      <td>9</td>
      <td>101.7408</td>
      <td>0.7013</td>
      <td>-80.9369</td>
      <td>284.4186</td>
      <td>False</td>
    </tr>
    <tr>
      <td>8</td>
      <td>2</td>
      <td>3</td>
      <td>-8.4815</td>
      <td>0.9000</td>
      <td>-149.2052</td>
      <td>132.2421</td>
      <td>False</td>
    </tr>
    <tr>
      <td>9</td>
      <td>2</td>
      <td>4</td>
      <td>-72.7002</td>
      <td>0.7250</td>
      <td>-206.2617</td>
      <td>60.8614</td>
      <td>False</td>
    </tr>
    <tr>
      <td>10</td>
      <td>2</td>
      <td>5</td>
      <td>-67.9754</td>
      <td>0.9000</td>
      <td>-254.6631</td>
      <td>118.7123</td>
      <td>False</td>
    </tr>
    <tr>
      <td>11</td>
      <td>2</td>
      <td>6</td>
      <td>-152.1472</td>
      <td>0.1034</td>
      <td>-318.2452</td>
      <td>13.9507</td>
      <td>False</td>
    </tr>
    <tr>
      <td>12</td>
      <td>2</td>
      <td>7</td>
      <td>-2.1547</td>
      <td>0.9000</td>
      <td>-166.5288</td>
      <td>162.2193</td>
      <td>False</td>
    </tr>
    <tr>
      <td>13</td>
      <td>2</td>
      <td>8</td>
      <td>-95.4088</td>
      <td>0.5349</td>
      <td>-243.2531</td>
      <td>52.4356</td>
      <td>False</td>
    </tr>
    <tr>
      <td>14</td>
      <td>2</td>
      <td>9</td>
      <td>31.0613</td>
      <td>0.9000</td>
      <td>-160.9455</td>
      <td>223.0682</td>
      <td>False</td>
    </tr>
    <tr>
      <td>15</td>
      <td>3</td>
      <td>4</td>
      <td>-64.2186</td>
      <td>0.7606</td>
      <td>-186.4399</td>
      <td>58.0027</td>
      <td>False</td>
    </tr>
    <tr>
      <td>16</td>
      <td>3</td>
      <td>5</td>
      <td>-59.4939</td>
      <td>0.9000</td>
      <td>-238.2441</td>
      <td>119.2564</td>
      <td>False</td>
    </tr>
    <tr>
      <td>17</td>
      <td>3</td>
      <td>6</td>
      <td>-143.6657</td>
      <td>0.1049</td>
      <td>-300.7895</td>
      <td>13.4581</td>
      <td>False</td>
    </tr>
    <tr>
      <td>18</td>
      <td>3</td>
      <td>7</td>
      <td>6.3268</td>
      <td>0.9000</td>
      <td>-148.9735</td>
      <td>161.6271</td>
      <td>False</td>
    </tr>
    <tr>
      <td>19</td>
      <td>3</td>
      <td>8</td>
      <td>-86.9273</td>
      <td>0.5613</td>
      <td>-224.6128</td>
      <td>50.7583</td>
      <td>False</td>
    </tr>
    <tr>
      <td>20</td>
      <td>3</td>
      <td>9</td>
      <td>39.5429</td>
      <td>0.9000</td>
      <td>-144.7557</td>
      <td>223.8415</td>
      <td>False</td>
    </tr>
    <tr>
      <td>21</td>
      <td>4</td>
      <td>5</td>
      <td>4.7247</td>
      <td>0.9000</td>
      <td>-168.4434</td>
      <td>177.8929</td>
      <td>False</td>
    </tr>
    <tr>
      <td>22</td>
      <td>4</td>
      <td>6</td>
      <td>-79.4471</td>
      <td>0.7575</td>
      <td>-230.1900</td>
      <td>71.2959</td>
      <td>False</td>
    </tr>
    <tr>
      <td>23</td>
      <td>4</td>
      <td>7</td>
      <td>70.5454</td>
      <td>0.8574</td>
      <td>-78.2959</td>
      <td>219.3867</td>
      <td>False</td>
    </tr>
    <tr>
      <td>24</td>
      <td>4</td>
      <td>8</td>
      <td>-22.7086</td>
      <td>0.9000</td>
      <td>-153.0653</td>
      <td>107.6480</td>
      <td>False</td>
    </tr>
    <tr>
      <td>25</td>
      <td>4</td>
      <td>9</td>
      <td>103.7615</td>
      <td>0.6578</td>
      <td>-75.1282</td>
      <td>282.6512</td>
      <td>False</td>
    </tr>
    <tr>
      <td>26</td>
      <td>5</td>
      <td>6</td>
      <td>-84.1718</td>
      <td>0.9000</td>
      <td>-283.5134</td>
      <td>115.1697</td>
      <td>False</td>
    </tr>
    <tr>
      <td>27</td>
      <td>5</td>
      <td>7</td>
      <td>65.8207</td>
      <td>0.9000</td>
      <td>-132.0867</td>
      <td>263.7281</td>
      <td>False</td>
    </tr>
    <tr>
      <td>28</td>
      <td>5</td>
      <td>8</td>
      <td>-27.4334</td>
      <td>0.9000</td>
      <td>-211.8418</td>
      <td>156.9750</td>
      <td>False</td>
    </tr>
    <tr>
      <td>29</td>
      <td>5</td>
      <td>9</td>
      <td>99.0368</td>
      <td>0.9000</td>
      <td>-122.3569</td>
      <td>320.4304</td>
      <td>False</td>
    </tr>
    <tr>
      <td>30</td>
      <td>6</td>
      <td>7</td>
      <td>149.9925</td>
      <td>0.1837</td>
      <td>-28.6232</td>
      <td>328.6082</td>
      <td>False</td>
    </tr>
    <tr>
      <td>31</td>
      <td>6</td>
      <td>8</td>
      <td>56.7384</td>
      <td>0.9000</td>
      <td>-106.7935</td>
      <td>220.2704</td>
      <td>False</td>
    </tr>
    <tr>
      <td>32</td>
      <td>6</td>
      <td>9</td>
      <td>183.2086</td>
      <td>0.1211</td>
      <td>-21.1229</td>
      <td>387.5401</td>
      <td>False</td>
    </tr>
    <tr>
      <td>33</td>
      <td>7</td>
      <td>8</td>
      <td>-93.2541</td>
      <td>0.6646</td>
      <td>-255.0348</td>
      <td>68.5267</td>
      <td>False</td>
    </tr>
    <tr>
      <td>34</td>
      <td>7</td>
      <td>9</td>
      <td>33.2161</td>
      <td>0.9000</td>
      <td>-169.7166</td>
      <td>236.1487</td>
      <td>False</td>
    </tr>
    <tr>
      <td>35</td>
      <td>8</td>
      <td>9</td>
      <td>126.4701</td>
      <td>0.4952</td>
      <td>-63.3213</td>
      <td>316.2616</td>
      <td>False</td>
    </tr>
  </tbody>
</table>
</div>



### Hypothesis 3 Results Table:


```python
fn.mult_Cohn_d(tukeyrepdf, reps)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>g1</th>
      <th>g2</th>
      <th>padj</th>
      <th>d</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>1</td>
      <td>2</td>
      <td>0.7896</td>
      <td>-0.130744</td>
    </tr>
    <tr>
      <td>1</td>
      <td>1</td>
      <td>3</td>
      <td>0.8328</td>
      <td>-0.114624</td>
    </tr>
    <tr>
      <td>2</td>
      <td>1</td>
      <td>4</td>
      <td>0.9000</td>
      <td>0.004144</td>
    </tr>
    <tr>
      <td>3</td>
      <td>1</td>
      <td>5</td>
      <td>0.9000</td>
      <td>-0.005335</td>
    </tr>
    <tr>
      <td>4</td>
      <td>1</td>
      <td>6</td>
      <td>0.7616</td>
      <td>0.170314</td>
    </tr>
    <tr>
      <td>5</td>
      <td>1</td>
      <td>7</td>
      <td>0.9000</td>
      <td>-0.120978</td>
    </tr>
    <tr>
      <td>6</td>
      <td>1</td>
      <td>8</td>
      <td>0.9000</td>
      <td>0.052428</td>
    </tr>
    <tr>
      <td>7</td>
      <td>1</td>
      <td>9</td>
      <td>0.7013</td>
      <td>-0.176757</td>
    </tr>
    <tr>
      <td>8</td>
      <td>2</td>
      <td>3</td>
      <td>0.9000</td>
      <td>0.014775</td>
    </tr>
    <tr>
      <td>9</td>
      <td>2</td>
      <td>4</td>
      <td>0.7250</td>
      <td>0.143003</td>
    </tr>
    <tr>
      <td>10</td>
      <td>2</td>
      <td>5</td>
      <td>0.9000</td>
      <td>0.123877</td>
    </tr>
    <tr>
      <td>11</td>
      <td>2</td>
      <td>6</td>
      <td>0.1034</td>
      <td>0.298368</td>
    </tr>
    <tr>
      <td>12</td>
      <td>2</td>
      <td>7</td>
      <td>0.9000</td>
      <td>0.003517</td>
    </tr>
    <tr>
      <td>13</td>
      <td>2</td>
      <td>8</td>
      <td>0.5349</td>
      <td>0.192116</td>
    </tr>
    <tr>
      <td>14</td>
      <td>2</td>
      <td>9</td>
      <td>0.9000</td>
      <td>-0.049137</td>
    </tr>
    <tr>
      <td>15</td>
      <td>3</td>
      <td>4</td>
      <td>0.7606</td>
      <td>0.124941</td>
    </tr>
    <tr>
      <td>16</td>
      <td>3</td>
      <td>5</td>
      <td>0.9000</td>
      <td>0.108117</td>
    </tr>
    <tr>
      <td>17</td>
      <td>3</td>
      <td>6</td>
      <td>0.1049</td>
      <td>0.277284</td>
    </tr>
    <tr>
      <td>18</td>
      <td>3</td>
      <td>7</td>
      <td>0.9000</td>
      <td>-0.010479</td>
    </tr>
    <tr>
      <td>19</td>
      <td>3</td>
      <td>8</td>
      <td>0.5613</td>
      <td>0.171933</td>
    </tr>
    <tr>
      <td>20</td>
      <td>3</td>
      <td>9</td>
      <td>0.9000</td>
      <td>-0.063944</td>
    </tr>
    <tr>
      <td>21</td>
      <td>4</td>
      <td>5</td>
      <td>0.9000</td>
      <td>-0.010070</td>
    </tr>
    <tr>
      <td>22</td>
      <td>4</td>
      <td>6</td>
      <td>0.7575</td>
      <td>0.178198</td>
    </tr>
    <tr>
      <td>23</td>
      <td>4</td>
      <td>7</td>
      <td>0.8574</td>
      <td>-0.133375</td>
    </tr>
    <tr>
      <td>24</td>
      <td>4</td>
      <td>8</td>
      <td>0.9000</td>
      <td>0.051141</td>
    </tr>
    <tr>
      <td>25</td>
      <td>4</td>
      <td>9</td>
      <td>0.6578</td>
      <td>-0.194860</td>
    </tr>
    <tr>
      <td>26</td>
      <td>5</td>
      <td>6</td>
      <td>0.9000</td>
      <td>0.193965</td>
    </tr>
    <tr>
      <td>27</td>
      <td>5</td>
      <td>7</td>
      <td>0.9000</td>
      <td>-0.110550</td>
    </tr>
    <tr>
      <td>28</td>
      <td>5</td>
      <td>8</td>
      <td>0.9000</td>
      <td>0.063274</td>
    </tr>
    <tr>
      <td>29</td>
      <td>5</td>
      <td>9</td>
      <td>0.9000</td>
      <td>-0.159411</td>
    </tr>
    <tr>
      <td>30</td>
      <td>6</td>
      <td>7</td>
      <td>0.1837</td>
      <td>-0.275056</td>
    </tr>
    <tr>
      <td>31</td>
      <td>6</td>
      <td>8</td>
      <td>0.9000</td>
      <td>-0.140752</td>
    </tr>
    <tr>
      <td>32</td>
      <td>6</td>
      <td>9</td>
      <td>0.1211</td>
      <td>-0.329617</td>
    </tr>
    <tr>
      <td>33</td>
      <td>7</td>
      <td>8</td>
      <td>0.6646</td>
      <td>0.178140</td>
    </tr>
    <tr>
      <td>34</td>
      <td>7</td>
      <td>9</td>
      <td>0.9000</td>
      <td>-0.048048</td>
    </tr>
    <tr>
      <td>35</td>
      <td>8</td>
      <td>9</td>
      <td>0.4952</td>
      <td>-0.239676</td>
    </tr>
  </tbody>
</table>
</div>



### Findings and recommendations: 


#### Findings:
Both parametric and non parametric tests were conducted, despite indications for non-parametric tests as the dataset(s) did not meet the assupmtion of equal variance. A visual inspection after outlier removal suggested there could be significant variance in the mean and the parametric was run for comparison.  The parametric test indicated that the null hypothesis could be rejected.  However, post-hoc testing validated the efficacy of the non-parametric test to **accept the null hypothesis**, with the smallest probability that the outcome was due to chance was well over the accepted rate of .05. 

The Hypothesis 3 Results Table above provides details on how each representative compares with one another and is itemized by the adjusted p values and d is the result of a Cohen D illustrating the effect size of each comparison.


#### Recommendation:    
If there is no statistical difference, and effect size is small at best, best practices can still be shared by those who have a higher average revenue, examples 2,3 and 9 still have higher than average sales.
    
Perhaps a little healthy, insentivised competition might spur increased revenues if not by one, by many.  Also, building on knowledge of smaller discounts yielding larger quantities, sales team could increase revenue by being conservative with discount rates.
   
    

# HYPOTHESIS 4:

> ***Where are our customers from that spend the most money?***

$H0$: Customers spend equal amounts regardless of region.

$H1$: Region has an effect on total amount spent.


    

#### Importing and inspecting data from  OrderDetail and Order

These table includes information on:

    1) Sales total information 
    2) Regions where orders shipped to indicating the location of customers


```python
cur.execute("""SELECT 
                ShipRegion, 
                OrderID, 
                ProductID, 
                UnitPrice,
                Quantity, 
                Discount
                FROM `Order` AS o
                JOIN OrderDetail AS od
                on o.ID = od.OrderId ;""")
dfreg = pd.DataFrame(cur.fetchall(), columns=[x[0] for x in cur.description])
dfreg.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ShipRegion</th>
      <th>OrderId</th>
      <th>ProductId</th>
      <th>UnitPrice</th>
      <th>Quantity</th>
      <th>Discount</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>Western Europe</td>
      <td>10248</td>
      <td>11</td>
      <td>14.0</td>
      <td>12</td>
      <td>0.0</td>
    </tr>
    <tr>
      <td>1</td>
      <td>Western Europe</td>
      <td>10248</td>
      <td>42</td>
      <td>9.8</td>
      <td>10</td>
      <td>0.0</td>
    </tr>
    <tr>
      <td>2</td>
      <td>Western Europe</td>
      <td>10248</td>
      <td>72</td>
      <td>34.8</td>
      <td>5</td>
      <td>0.0</td>
    </tr>
    <tr>
      <td>3</td>
      <td>Western Europe</td>
      <td>10249</td>
      <td>14</td>
      <td>18.6</td>
      <td>9</td>
      <td>0.0</td>
    </tr>
    <tr>
      <td>4</td>
      <td>Western Europe</td>
      <td>10249</td>
      <td>51</td>
      <td>42.4</td>
      <td>40</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
dfreg['Amount_Spent'] = ((dfreg['UnitPrice'])*(1 - dfreg['Discount']))*dfreg['Quantity']
```

### Hypothesis 4 Preliminary Visualizations:


```python
fig, ax = plt.subplots()
spend_mu = dfreg['Amount_Spent'].mean()
sns.distplot(dfreg['Amount_Spent'], ax=ax)
plt.axvline(spend_mu, color='lightgreen')
plt.title('Average Total Spend')
print(f'The average total spend is ${round(spend_mu,2)}')
print(f'The distribution indicates there may be outliers.')
```

    The average total spend is $587.37
    The distribution indicates there may be outliers.
    


![png](output_164_1.png)



```python

```


```python
regs = {}
for reg in dfreg['ShipRegion'].unique():
    regs[reg] = dfreg.groupby('ShipRegion').get_group(reg)['Amount_Spent']

```


```python
regions = list(dfreg['ShipRegion'].unique())
regions
print(f'There are {len(regions)} regions, they are {regions}.')
```

    There are 9 regions, they are ['Western Europe', 'South America', 'Central America', 'North America', 'Northern Europe', 'Scandinavia', 'Southern Europe', 'British Isles', 'Eastern Europe'].
    


```python
fig, ax = plt.subplots(figsize=(10,5))
for k,v in regs.items():
    sns.distplot(v,label=v)


plt.title('Sales Revenue Distribution')
plt.ylabel('Distribution')
print('Distributions appear roughly equal, although there appears to be outliers')
```

    Distributions appear roughly equal, although there appears to be outliers
    


![png](output_168_1.png)



```python
@interact
def plt_discounts(d=regions):
    sns.distplot(dfreg.groupby('ShipRegion').get_group(d)['Amount_Spent'])
    plt.axvline(spend_mu, color='purple')
    plt.gca()
```


    interactive(children=(Dropdown(description='d', options=('Western Europe', 'South America', 'Central America',…



```python
fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(data=dfreg, x='ShipRegion', y='Amount_Spent', ci=68, palette="rocket", ax=ax)
plt.title('Total Spend by Region', fontsize=16)
plt.axhline(spend_mu,linestyle="--", color='orange', linewidth=.6 )
plt.xlabel('Region')
plt.xticks(rotation=45)
plt.ylabel('Total Spend')
plt.show()
```


![png](output_170_0.png)



```python

```

#### Hypothesis 4 Initial Observations:
Datatype is numeric in this 2155 order sample.

There are 9 regions in reflected in this dataset

The avarage of total spent is $587.37.

Initial visual inspection indicates skewed, but roughly uniform distribution in total sales, more than half of the sales representatives achieve the average. Additional testing will demonstrate if it is significant.

Since we are comparing multiple regions to inspect it's impact on quantity ordered an AVNOVA test will be run: Assumptions for ANOVA Testing:

1) Upon a quick visual inspection, there appears to be some outliers that could be removed

2) Equal variance

3) Normality (if n>15) Not required for samples greater than 15

### Hypothesis 4 Assumption 1: Outlier 
Outliers were identified and removed via z-score testing.  Details are below:


```python
regs = {}
for reg in dfreg['ShipRegion'].unique():
    regs[reg] = dfreg.groupby('ShipRegion').get_group(reg)['Amount_Spent']

```


```python
for reg, reg_data in regs.items():
    idx_outs = fn.find_outliers_Z(reg_data)
    print(f'Found {idx_outs.sum()} outliers in the {reg}')
    regs[reg] = reg_data[~idx_outs]
print('\n All of these outliers were removed')
```

    Found 11 outliers in the Western Europe
    Found 2 outliers in the South America
    Found 1 outliers in the Central America
    Found 9 outliers in the North America
    Found 2 outliers in the Northern Europe
    Found 1 outliers in the Scandinavia
    Found 3 outliers in the Southern Europe
    Found 4 outliers in the British Isles
    Found 0 outliers in the Eastern Europe
    
     All of these outliers were removed
    

### Hypothesis 4 Assumption 2: Equal Variance


```python
data = []
labels = []
for k,v in regs.items():
    data.append(v)
    labels.append(k)
```


```python
stat,p = stats.levene(*data, center = 'median')
print(f'Lavene test for equal variance results are {round(p,4)}')
sig = 'do NOT' if p < .05 else 'DO'

print(f'The groups {sig} have equal variance')
      
```

    Lavene test for equal variance results are 0.0
    The groups do NOT have equal variance
    

### Hypothesis 4 Assumption 3: Normality


```python
n =[]
for reg, samples in regs.items():
    print(f'There are {len(samples)} samples in the data set for Regions #{reg}.')
    n.append(len(samples)>15)
if all(n):
    print('\nAll samples are >15: Normality Assumption Criterion is met.')
```

    There are 734 samples in the data set for Regions #Western Europe.
    There are 353 samples in the data set for Regions #South America.
    There are 71 samples in the data set for Regions #Central America.
    There are 418 samples in the data set for Regions #North America.
    There are 141 samples in the data set for Regions #Northern Europe.
    There are 69 samples in the data set for Regions #Scandinavia.
    There are 134 samples in the data set for Regions #Southern Europe.
    There are 186 samples in the data set for Regions #British Isles.
    There are 16 samples in the data set for Regions #Eastern Europe.
    
    All samples are >15: Normality Assumption Criterion is met.
    

#### Using non-parametric Kruskal since the data set was not of equal variance:


```python
stat, p = stats.kruskal(*data)
print(f"Kruskal test p value: {round(p,6)}")
```

    Kruskal test p value: 0.0
    


```python
cregs = fn.prep_data_for_tukeys(regs)  
cregs
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>data</th>
      <th>group</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>168.0</td>
      <td>Western Europe</td>
    </tr>
    <tr>
      <td>1</td>
      <td>98.0</td>
      <td>Western Europe</td>
    </tr>
    <tr>
      <td>2</td>
      <td>174.0</td>
      <td>Western Europe</td>
    </tr>
    <tr>
      <td>3</td>
      <td>167.4</td>
      <td>Western Europe</td>
    </tr>
    <tr>
      <td>4</td>
      <td>1696.0</td>
      <td>Western Europe</td>
    </tr>
    <tr>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <td>1933</td>
      <td>54.0</td>
      <td>Eastern Europe</td>
    </tr>
    <tr>
      <td>1934</td>
      <td>199.5</td>
      <td>Eastern Europe</td>
    </tr>
    <tr>
      <td>1935</td>
      <td>200.0</td>
      <td>Eastern Europe</td>
    </tr>
    <tr>
      <td>1936</td>
      <td>232.5</td>
      <td>Eastern Europe</td>
    </tr>
    <tr>
      <td>2054</td>
      <td>591.6</td>
      <td>Eastern Europe</td>
    </tr>
  </tbody>
</table>
<p>2122 rows × 2 columns</p>
</div>




```python
mu = cregs['data'].mean()
mu
```




    500.12534142318566




```python
cregs['data']=cregs['data'].astype(float)
cregs['group']=cregs['group'].astype(str)
```


```python
tukeyr = sms.stats.multicomp.pairwise_tukeyhsd(cregs['data'],cregs['group'])
tukeyr.summary()
```




<table class="simpletable">
<caption>Multiple Comparison of Means - Tukey HSD, FWER=0.05</caption>
<tr>
      <th>group1</th>          <th>group2</th>      <th>meandiff</th>   <th>p-adj</th>   <th>lower</th>     <th>upper</th>   <th>reject</th>
</tr>
<tr>
   <td>British Isles</td>  <td>Central America</td> <td>-185.8522</td> <td>0.2271</td> <td>-415.6671</td>  <td>43.9628</td>   <td>False</td>
</tr>
<tr>
   <td>British Isles</td>  <td>Eastern Europe</td>  <td>-241.5782</td> <td>0.6901</td> <td>-670.7752</td> <td>187.6188</td>   <td>False</td>
</tr>
<tr>
   <td>British Isles</td>   <td>North America</td>  <td>108.0077</td>  <td>0.3368</td> <td>-37.1939</td>  <td>253.2093</td>   <td>False</td>
</tr>
<tr>
   <td>British Isles</td>  <td>Northern Europe</td>  <td>48.1291</td>    <td>0.9</td>  <td>-135.8232</td> <td>232.0814</td>   <td>False</td>
</tr>
<tr>
   <td>British Isles</td>    <td>Scandinavia</td>   <td>-137.1482</td> <td>0.6379</td> <td>-369.3612</td>  <td>95.0647</td>   <td>False</td>
</tr>
<tr>
   <td>British Isles</td>   <td>South America</td>  <td>-38.1848</td>    <td>0.9</td>  <td>-187.4464</td> <td>111.0767</td>   <td>False</td>
</tr>
<tr>
   <td>British Isles</td>  <td>Southern Europe</td> <td>-172.9738</td> <td>0.0946</td> <td>-359.6391</td>  <td>13.6914</td>   <td>False</td>
</tr>
<tr>
   <td>British Isles</td>  <td>Western Europe</td>  <td>124.6055</td>  <td>0.0989</td> <td>-10.6288</td>  <td>259.8398</td>   <td>False</td>
</tr>
<tr>
  <td>Central America</td> <td>Eastern Europe</td>   <td>-55.726</td>    <td>0.9</td>  <td>-511.6242</td> <td>400.1721</td>   <td>False</td>
</tr>
<tr>
  <td>Central America</td>  <td>North America</td>  <td>293.8599</td>   <td>0.001</td>  <td>82.3968</td>  <td>505.3229</td>   <td>True</td> 
</tr>
<tr>
  <td>Central America</td> <td>Northern Europe</td> <td>233.9812</td>  <td>0.0623</td>  <td>-5.7511</td>  <td>473.7136</td>   <td>False</td>
</tr>
<tr>
  <td>Central America</td>   <td>Scandinavia</td>    <td>48.7039</td>    <td>0.9</td>  <td>-229.7849</td> <td>327.1927</td>   <td>False</td>
</tr>
<tr>
  <td>Central America</td>  <td>South America</td>  <td>147.6673</td>  <td>0.4491</td> <td>-66.6039</td>  <td>361.9385</td>   <td>False</td>
</tr>
<tr>
  <td>Central America</td> <td>Southern Europe</td>  <td>12.8783</td>    <td>0.9</td>  <td>-228.942</td>  <td>254.6986</td>   <td>False</td>
</tr>
<tr>
  <td>Central America</td> <td>Western Europe</td>  <td>310.4577</td>   <td>0.001</td> <td>105.7104</td>   <td>515.205</td>   <td>True</td> 
</tr>
<tr>
  <td>Eastern Europe</td>   <td>North America</td>  <td>349.5859</td>  <td>0.1926</td> <td>-70.0708</td>  <td>769.2426</td>   <td>False</td>
</tr>
<tr>
  <td>Eastern Europe</td>  <td>Northern Europe</td> <td>289.7073</td>  <td>0.4947</td> <td>-144.8807</td> <td>724.2953</td>   <td>False</td>
</tr>
<tr>
  <td>Eastern Europe</td>    <td>Scandinavia</td>    <td>104.43</td>     <td>0.9</td>  <td>-352.6817</td> <td>561.5417</td>   <td>False</td>
</tr>
<tr>
  <td>Eastern Europe</td>   <td>South America</td>  <td>203.3934</td>  <td>0.8404</td> <td>-217.6853</td>  <td>624.472</td>   <td>False</td>
</tr>
<tr>
  <td>Eastern Europe</td>  <td>Southern Europe</td>  <td>68.6044</td>    <td>0.9</td>  <td>-367.1389</td> <td>504.3476</td>   <td>False</td>
</tr>
<tr>
  <td>Eastern Europe</td>  <td>Western Europe</td>  <td>366.1837</td>  <td>0.1372</td> <td>-50.1293</td>  <td>782.4968</td>   <td>False</td>
</tr>
<tr>
   <td>North America</td>  <td>Northern Europe</td> <td>-59.8786</td>    <td>0.9</td>  <td>-220.316</td>  <td>100.5588</td>   <td>False</td>
</tr>
<tr>
   <td>North America</td>    <td>Scandinavia</td>   <td>-245.1559</td> <td>0.0115</td> <td>-459.2227</td> <td>-31.0892</td>   <td>True</td> 
</tr>
<tr>
   <td>North America</td>   <td>South America</td>  <td>-146.1925</td> <td>0.0045</td> <td>-265.2754</td> <td>-27.1097</td>   <td>True</td> 
</tr>
<tr>
   <td>North America</td>  <td>Southern Europe</td> <td>-280.9815</td>  <td>0.001</td> <td>-444.5224</td> <td>-117.4406</td>  <td>True</td> 
</tr>
<tr>
   <td>North America</td>  <td>Western Europe</td>   <td>16.5978</td>    <td>0.9</td>  <td>-84.3478</td>  <td>117.5435</td>   <td>False</td>
</tr>
<tr>
  <td>Northern Europe</td>   <td>Scandinavia</td>   <td>-185.2773</td> <td>0.2974</td> <td>-427.3094</td>  <td>56.7548</td>   <td>False</td>
</tr>
<tr>
  <td>Northern Europe</td>  <td>South America</td>  <td>-86.3139</td>  <td>0.7597</td> <td>-250.4349</td>  <td>77.807</td>    <td>False</td>
</tr>
<tr>
  <td>Northern Europe</td> <td>Southern Europe</td> <td>-221.1029</td> <td>0.0164</td> <td>-419.8505</td> <td>-22.3554</td>   <td>True</td> 
</tr>
<tr>
  <td>Northern Europe</td> <td>Western Europe</td>   <td>76.4764</td>  <td>0.7992</td> <td>-74.9996</td>  <td>227.9525</td>   <td>False</td>
</tr>
<tr>
    <td>Scandinavia</td>    <td>South America</td>   <td>98.9634</td>  <td>0.8905</td> <td>-117.8778</td> <td>315.8046</td>   <td>False</td>
</tr>
<tr>
    <td>Scandinavia</td>   <td>Southern Europe</td> <td>-35.8256</td>    <td>0.9</td>  <td>-279.926</td>  <td>208.2748</td>   <td>False</td>
</tr>
<tr>
    <td>Scandinavia</td>   <td>Western Europe</td>  <td>261.7538</td>   <td>0.003</td>  <td>54.3185</td>   <td>469.189</td>   <td>True</td> 
</tr>
<tr>
   <td>South America</td>  <td>Southern Europe</td> <td>-134.789</td>  <td>0.2306</td> <td>-301.9451</td>  <td>32.3671</td>   <td>False</td>
</tr>
<tr>
   <td>South America</td>  <td>Western Europe</td>  <td>162.7904</td>   <td>0.001</td>  <td>56.0873</td>  <td>269.4934</td>   <td>True</td> 
</tr>
<tr>
  <td>Southern Europe</td> <td>Western Europe</td>  <td>297.5794</td>   <td>0.001</td>  <td>142.82</td>   <td>452.3387</td>   <td>True</td> 
</tr>
</table>




```python
tukeyr.plot_simultaneous();
```


![png](output_187_0.png)


** Noting that the sample size of Eastern Europe is relatively small and the confidence interval is much greater to accomodate for it, possibly skewing the results of the table below.


```python
tukeyr_df = fn.tukey_df(tukeyr)
```


```python
tukeyr_false = tukeyr_df[tukeyr_df['reject']==False]
tukeyr_false
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>group1</th>
      <th>group2</th>
      <th>meandiff</th>
      <th>p-adj</th>
      <th>lower</th>
      <th>upper</th>
      <th>reject</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>British Isles</td>
      <td>Central America</td>
      <td>-185.8522</td>
      <td>0.2271</td>
      <td>-415.6671</td>
      <td>43.9628</td>
      <td>False</td>
    </tr>
    <tr>
      <td>1</td>
      <td>British Isles</td>
      <td>Eastern Europe</td>
      <td>-241.5782</td>
      <td>0.6901</td>
      <td>-670.7752</td>
      <td>187.6188</td>
      <td>False</td>
    </tr>
    <tr>
      <td>2</td>
      <td>British Isles</td>
      <td>North America</td>
      <td>108.0077</td>
      <td>0.3368</td>
      <td>-37.1939</td>
      <td>253.2093</td>
      <td>False</td>
    </tr>
    <tr>
      <td>3</td>
      <td>British Isles</td>
      <td>Northern Europe</td>
      <td>48.1291</td>
      <td>0.9000</td>
      <td>-135.8232</td>
      <td>232.0814</td>
      <td>False</td>
    </tr>
    <tr>
      <td>4</td>
      <td>British Isles</td>
      <td>Scandinavia</td>
      <td>-137.1482</td>
      <td>0.6379</td>
      <td>-369.3612</td>
      <td>95.0647</td>
      <td>False</td>
    </tr>
    <tr>
      <td>5</td>
      <td>British Isles</td>
      <td>South America</td>
      <td>-38.1848</td>
      <td>0.9000</td>
      <td>-187.4464</td>
      <td>111.0767</td>
      <td>False</td>
    </tr>
    <tr>
      <td>6</td>
      <td>British Isles</td>
      <td>Southern Europe</td>
      <td>-172.9738</td>
      <td>0.0946</td>
      <td>-359.6391</td>
      <td>13.6914</td>
      <td>False</td>
    </tr>
    <tr>
      <td>7</td>
      <td>British Isles</td>
      <td>Western Europe</td>
      <td>124.6055</td>
      <td>0.0989</td>
      <td>-10.6288</td>
      <td>259.8398</td>
      <td>False</td>
    </tr>
    <tr>
      <td>8</td>
      <td>Central America</td>
      <td>Eastern Europe</td>
      <td>-55.7260</td>
      <td>0.9000</td>
      <td>-511.6242</td>
      <td>400.1721</td>
      <td>False</td>
    </tr>
    <tr>
      <td>10</td>
      <td>Central America</td>
      <td>Northern Europe</td>
      <td>233.9812</td>
      <td>0.0623</td>
      <td>-5.7511</td>
      <td>473.7136</td>
      <td>False</td>
    </tr>
    <tr>
      <td>11</td>
      <td>Central America</td>
      <td>Scandinavia</td>
      <td>48.7039</td>
      <td>0.9000</td>
      <td>-229.7849</td>
      <td>327.1927</td>
      <td>False</td>
    </tr>
    <tr>
      <td>12</td>
      <td>Central America</td>
      <td>South America</td>
      <td>147.6673</td>
      <td>0.4491</td>
      <td>-66.6039</td>
      <td>361.9385</td>
      <td>False</td>
    </tr>
    <tr>
      <td>13</td>
      <td>Central America</td>
      <td>Southern Europe</td>
      <td>12.8783</td>
      <td>0.9000</td>
      <td>-228.9420</td>
      <td>254.6986</td>
      <td>False</td>
    </tr>
    <tr>
      <td>15</td>
      <td>Eastern Europe</td>
      <td>North America</td>
      <td>349.5859</td>
      <td>0.1926</td>
      <td>-70.0708</td>
      <td>769.2426</td>
      <td>False</td>
    </tr>
    <tr>
      <td>16</td>
      <td>Eastern Europe</td>
      <td>Northern Europe</td>
      <td>289.7073</td>
      <td>0.4947</td>
      <td>-144.8807</td>
      <td>724.2953</td>
      <td>False</td>
    </tr>
    <tr>
      <td>17</td>
      <td>Eastern Europe</td>
      <td>Scandinavia</td>
      <td>104.4300</td>
      <td>0.9000</td>
      <td>-352.6817</td>
      <td>561.5417</td>
      <td>False</td>
    </tr>
    <tr>
      <td>18</td>
      <td>Eastern Europe</td>
      <td>South America</td>
      <td>203.3934</td>
      <td>0.8404</td>
      <td>-217.6853</td>
      <td>624.4720</td>
      <td>False</td>
    </tr>
    <tr>
      <td>19</td>
      <td>Eastern Europe</td>
      <td>Southern Europe</td>
      <td>68.6044</td>
      <td>0.9000</td>
      <td>-367.1389</td>
      <td>504.3476</td>
      <td>False</td>
    </tr>
    <tr>
      <td>20</td>
      <td>Eastern Europe</td>
      <td>Western Europe</td>
      <td>366.1837</td>
      <td>0.1372</td>
      <td>-50.1293</td>
      <td>782.4968</td>
      <td>False</td>
    </tr>
    <tr>
      <td>21</td>
      <td>North America</td>
      <td>Northern Europe</td>
      <td>-59.8786</td>
      <td>0.9000</td>
      <td>-220.3160</td>
      <td>100.5588</td>
      <td>False</td>
    </tr>
    <tr>
      <td>25</td>
      <td>North America</td>
      <td>Western Europe</td>
      <td>16.5978</td>
      <td>0.9000</td>
      <td>-84.3478</td>
      <td>117.5435</td>
      <td>False</td>
    </tr>
    <tr>
      <td>26</td>
      <td>Northern Europe</td>
      <td>Scandinavia</td>
      <td>-185.2773</td>
      <td>0.2974</td>
      <td>-427.3094</td>
      <td>56.7548</td>
      <td>False</td>
    </tr>
    <tr>
      <td>27</td>
      <td>Northern Europe</td>
      <td>South America</td>
      <td>-86.3139</td>
      <td>0.7597</td>
      <td>-250.4349</td>
      <td>77.8070</td>
      <td>False</td>
    </tr>
    <tr>
      <td>29</td>
      <td>Northern Europe</td>
      <td>Western Europe</td>
      <td>76.4764</td>
      <td>0.7992</td>
      <td>-74.9996</td>
      <td>227.9525</td>
      <td>False</td>
    </tr>
    <tr>
      <td>30</td>
      <td>Scandinavia</td>
      <td>South America</td>
      <td>98.9634</td>
      <td>0.8905</td>
      <td>-117.8778</td>
      <td>315.8046</td>
      <td>False</td>
    </tr>
    <tr>
      <td>31</td>
      <td>Scandinavia</td>
      <td>Southern Europe</td>
      <td>-35.8256</td>
      <td>0.9000</td>
      <td>-279.9260</td>
      <td>208.2748</td>
      <td>False</td>
    </tr>
    <tr>
      <td>33</td>
      <td>South America</td>
      <td>Southern Europe</td>
      <td>-134.7890</td>
      <td>0.2306</td>
      <td>-301.9451</td>
      <td>32.3671</td>
      <td>False</td>
    </tr>
  </tbody>
</table>
</div>




```python
tukeyr_trues = tukeyr_df[tukeyr_df['reject']==True]
tukeyr_trues
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>group1</th>
      <th>group2</th>
      <th>meandiff</th>
      <th>p-adj</th>
      <th>lower</th>
      <th>upper</th>
      <th>reject</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>9</td>
      <td>Central America</td>
      <td>North America</td>
      <td>293.8599</td>
      <td>0.0010</td>
      <td>82.3968</td>
      <td>505.3229</td>
      <td>True</td>
    </tr>
    <tr>
      <td>14</td>
      <td>Central America</td>
      <td>Western Europe</td>
      <td>310.4577</td>
      <td>0.0010</td>
      <td>105.7104</td>
      <td>515.2050</td>
      <td>True</td>
    </tr>
    <tr>
      <td>22</td>
      <td>North America</td>
      <td>Scandinavia</td>
      <td>-245.1559</td>
      <td>0.0115</td>
      <td>-459.2227</td>
      <td>-31.0892</td>
      <td>True</td>
    </tr>
    <tr>
      <td>23</td>
      <td>North America</td>
      <td>South America</td>
      <td>-146.1925</td>
      <td>0.0045</td>
      <td>-265.2754</td>
      <td>-27.1097</td>
      <td>True</td>
    </tr>
    <tr>
      <td>24</td>
      <td>North America</td>
      <td>Southern Europe</td>
      <td>-280.9815</td>
      <td>0.0010</td>
      <td>-444.5224</td>
      <td>-117.4406</td>
      <td>True</td>
    </tr>
    <tr>
      <td>28</td>
      <td>Northern Europe</td>
      <td>Southern Europe</td>
      <td>-221.1029</td>
      <td>0.0164</td>
      <td>-419.8505</td>
      <td>-22.3554</td>
      <td>True</td>
    </tr>
    <tr>
      <td>32</td>
      <td>Scandinavia</td>
      <td>Western Europe</td>
      <td>261.7538</td>
      <td>0.0030</td>
      <td>54.3185</td>
      <td>469.1890</td>
      <td>True</td>
    </tr>
    <tr>
      <td>34</td>
      <td>South America</td>
      <td>Western Europe</td>
      <td>162.7904</td>
      <td>0.0010</td>
      <td>56.0873</td>
      <td>269.4934</td>
      <td>True</td>
    </tr>
    <tr>
      <td>35</td>
      <td>Southern Europe</td>
      <td>Western Europe</td>
      <td>297.5794</td>
      <td>0.0010</td>
      <td>142.8200</td>
      <td>452.3387</td>
      <td>True</td>
    </tr>
  </tbody>
</table>
</div>




```python
mult_Cohn_d(tukeyr_trues, regs)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>g1</th>
      <th>g2</th>
      <th>padj</th>
      <th>d</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
      <td>Central America</td>
      <td>North America</td>
      <td>0.0010</td>
      <td>-0.485386</td>
    </tr>
    <tr>
      <td>1</td>
      <td>Central America</td>
      <td>Western Europe</td>
      <td>0.0010</td>
      <td>-0.548229</td>
    </tr>
    <tr>
      <td>2</td>
      <td>North America</td>
      <td>Scandinavia</td>
      <td>0.0115</td>
      <td>0.402484</td>
    </tr>
    <tr>
      <td>3</td>
      <td>North America</td>
      <td>South America</td>
      <td>0.0045</td>
      <td>0.262021</td>
    </tr>
    <tr>
      <td>4</td>
      <td>North America</td>
      <td>Southern Europe</td>
      <td>0.0010</td>
      <td>0.485062</td>
    </tr>
    <tr>
      <td>5</td>
      <td>Northern Europe</td>
      <td>Southern Europe</td>
      <td>0.0164</td>
      <td>0.481990</td>
    </tr>
    <tr>
      <td>6</td>
      <td>Scandinavia</td>
      <td>Western Europe</td>
      <td>0.0030</td>
      <td>-0.460358</td>
    </tr>
    <tr>
      <td>7</td>
      <td>South America</td>
      <td>Western Europe</td>
      <td>0.0010</td>
      <td>-0.300535</td>
    </tr>
    <tr>
      <td>8</td>
      <td>Southern Europe</td>
      <td>Western Europe</td>
      <td>0.0010</td>
      <td>-0.539438</td>
    </tr>
  </tbody>
</table>
</div>




```python
for reg, rev in regs.items():
    print(f'The average revenue for {reg} is ${round(rev.mean(),2)}')
```

    The average revenue for Western Europe is $586.93
    The average revenue for South America is $424.14
    The average revenue for Central America is $276.47
    The average revenue for North America is $570.33
    The average revenue for Northern Europe is $510.45
    The average revenue for Scandinavia is $325.18
    The average revenue for Southern Europe is $289.35
    The average revenue for British Isles is $462.33
    The average revenue for Eastern Europe is $220.75
    

### Hypothesis 4 Observations and Recommendations:

#### Obeservations 
The average spend for this dataset accross all regions was $500.

Regional averages were found to be what is reported in the table below: 

Region | Average Revenue
 -- | --|
Western Europe | `$586.93`
North America | `$570.33`
Northern Europe | `$510.45`
British Isles | `$462.33`
South America | `$424.14`
Scandinavia | `$325.18`
Southern Europe | `$289.35`
Central America | `$276.47`
Eastern Europe | `$220.75

For each group, the assumption for equal variance was not met and a Kruksal test was conducted.  The p value for the nonparametric kruskal test was singificant, which can reject the null hypothesis that all regions spend the same amounts with a 5% degree of error that this is due to chance.

Orders shipped to Western Europe, and North America and Northern Europe generated the highest amount of revenue, statistically these regions are equal:  

Region 1 | Region 2 |  MeanDiff | Adj P | Reject Null
 -- | -- | --| --| --|
North America | Northern Europe	| -59.8786	| 0.9000 | False
North America | Western Europe | 16.5978 | 0.9000	|	False
Northern Europe	| Western Europe | 76.4764 | 0.7992	| False


For bottom performers that had enough data:

Region 1 | Region 2 | Adj P 
 -- | -- | --|
South America |	Southern Europe	| 0.2306		

#### Recommendations:
Explore best practices from regions that are top performers.  
Market analysis for regions that need to be developed. 
Leverage knowledge gained regarding categories and discounts.



```python
indexr = list(cregs.groupby('group').mean().sort_values('data', ascending=False).index)
indexr
```




    ['Western Europe',
     'North America',
     'Northern Europe',
     'British Isles',
     'South America',
     'Scandinavia',
     'Southern Europe',
     'Central America',
     'Eastern Europe']




```python
avspend = cregs['data'].mean()
avspend
fig, ax = plt.subplots(figsize=(12,8))
sns.barplot(data=cregs, x='group', y='data', ci=68,order=indexr, palette="rocket", ax=ax)
plt.title('Average Revenue by Region', fontsize=20)
plt.axhline(avspend,linestyle="--", color='orange', linewidth=.6 )
plt.xlabel('Region')
plt.xticks(rotation=45)
plt.ylabel('Average Revenue')
plt.show()
```


![png](output_196_0.png)


# In Closing:

Since the data provided did not include purchase prices of merchandise, ways were examined to maximize revenues.
The datasets were all multi group comparisons and none of the groups met all the assupmtions for parametric testing.  All groups called for Kruskal-Wallis and post-hoc testing detailed in this notebook.

It was discovered through hypothesis testing and data analysis, various ways to achieve this through: 
    Minimizing discounts
    Broadening Revenue Generating Categories
    **add alllll the recommendations)
    
In addition, future analysis and testeing could provide insight to: 
    Develop Regional Markets
    Develop Sales Staff
    
   


```python

```
