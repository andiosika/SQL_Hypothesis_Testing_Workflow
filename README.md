# Hypothesis Testing to Inform Business Intelligence

___
## Main Files:

student.ipynb - Notebook inclues data, methodologies and modeling around hypothesis testing

Mod_3_preso.pdf - presentation summarizing findings for a non-technical audience

Additional Files
Blog Post: [All Data Is NOT Created Normal](https://andiosika.github.io/statistics_hypothesis_testing_alert_not_all_data_is_created_nomal)
____

## Description
***SQL Querying was performed for data extraction** for conducting A/B Testing to inform buisiness decisions making for global retailer. 

__

## Background

A two year sales history was examined in a series of tables stored in an SQL database.  The data provided focused primarly on sales information and did not include cost of goods, so ways were examined to maximize revenues in an effort to improve margins.  Several theories were developed and hypothesis were formed around ways to improve revenues.

# Questions to be answered through hypothesis a/b testing:

> 1) ***Does discount amount have a statistically significant effect on the quantity of a product in an order? If so, at what level(s) of discount?***

> 2) ***Do some categories generate more revenue than others ??*** 
     **Which ones?**
     
> 3) ***Do certain sales representatives sell more than others?  Who are the top sellers?***

> 4) ***Where are the customers from that spend the most money?***


___
### SQL Database Table Schematic Layout:

<img src="https://raw.githubusercontent.com/jirvingphd/dsc-mod-3-project-online-ds-ft-100719/master/Northwind_ERD_updated.png">


# HYPOTHESIS 1

> ***Does discount amount have a statistically significant effect on the quantity of a product in an order? If so, at what level(s) of discount?***

- $H_0$:There is no statistcally significant effect on the quantity of a product in an order in relation to a discount amount.
- $H_1$:Discounts have a statistically significant effect on the quantiy of a product in an order.
- $H_1a$:Certain discount values have a greater effect than others.


To begin, in taking a look at the **OrderDetail table**, the data required was made available: quantity and discount.  
Once imported, the data was grouped by discount level and the means of the quantity sold for each were compared against each other to evaluate if they were statistically significantly different.  The results can suggest if the null hypothesis can be rejected with a probability of 5% error in reporting a false negative.

### Some initial information was gathered:

From this dataset of 2155 line items that span 830 orders, it was discovered the average quantity ordered is 24 regardless of discount, the minimum ordered is 0 and max ordered is 130, although the IQR is between 10 and 30.  Pricing ranges from `$2` - `$263` with an average price of `$26.21` 

Discounts were distributed as follows:

    0.00    1317
    0.05     185
    0.10     173
    0.15     157
    0.20     161
    0.25     154

### Since we are comparing multiple discounts to inspect it's impact on quantity ordered an AVNOVA or Kruksal test will be run depending on how assumptions are met: 
   
Assumptions for ANOVA Testing were evaluated - Outliers were evaluated using Z-Score Testing and removed. Lavines Testing was conducted on the cleaned dataset and demonstrated that it was not equal variance so Kruksal Wallace testing was conducted.  All sample sizes were greater than 15 so the assumption of normality was met.  
  

### Post-Hoc Testing: Tukeys testing was conducted

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


Visual on distributions and potential remaining outliers to get a cleaner view:

```python
#boxen plot
sns.catplot(data=disc_df, x='group', y='data', kind='boxen')
ax.axhline(26.75, color='k')
plt.gca()
plt.show()
```

<img src="https://github.com/andiosika/SQL_Hypothesis_Testing_Workflow/blob/master/imgs/output_68_0.png">

This plot may not best suit non-technical audience with the additional information potentially could cause confusion.  However, the above boxen plot clearly illustrates distributions as well as remaining potential outliers in the .05, .15, .2 and .25 groups.  These outliers will not be removed at the present moment with the intention to preserve as much of the initial dataset as possible.  
    

## Hypothesis 1 Findings and Recommendation:

### Findings:
**Rejecting the null hypothesis :**
*   𝐻0 :There is no statistcally significant effect on the quantity of a product in an order in relation to a discount amount.

**Alternative hypothesese:**

    *  𝐻1 :Discounts have a statistically significant effect on the quantiy of a product in an order.
    *  𝐻1𝑎 :Certain discount values have a greater effect than others.(see below for findings)

A 10% discount had no statistical significance on the quantiy purchased.

Discounts extended at 5%, 15%, 20%, and 25% statistically are equal on quantity sold when compared to none offered, with a p-value of .001 meaning there is a .01 percent chance of classifying them as such due to chance. Each have varying effect sizes in compared to orders placed with no discount extended.
 
Discount |AvQty | Effect Size | Effect
 -- | -- | -- | --|
5 % | 27| .1982 | Small
15 % | 27| .454 | Medium
20 % |26| .3751 | Medium
25 % |27 | .454 | Medium

Additional notes:
- For discounts 1%,2%,3%,4%, and 6% that were included in the original dataset, the amount of data provided was relatively small to evaluate the impact on the whole. This data was removed from further testing
- With additional outliers removed for each of the discount groups, the revised average qty purchased was 23 overall.
 
###  Recommendation:

While larger discounts did deomonstrate significant effect on quantity purchased, smaller discounts held a statistically equal effect.  **To recognize the effect of driving higher quantities purchased and realize larger profit margins, offer the smaller discount(s).**

____
# HYPOTHESIS 2:

> ***Do some categories generate more revenue than others ??*** 
  **Which ones?**

- $𝐻0$ : All categories generate equal revenues.
- $𝐻1$ : Certain categories sell at statistically higher rates of revneu than others.
- $𝐻1𝑎$ : 

For this round of testing the **Product** and **OrderDetail** tables were queried using SQL.  These tables includes product information data including: categories, pricing, and discount information to generate revenues.


### Background Observations after Initial Inspection:

There are 8 different categories sold in this company that represent 77 products, and the average revenue generated across all categories is `$587.00`

Visually, it appears that there are three categories that significantly generate higher revenues than others, additional testing will demonstrate their siginficance and effect.

<img src='https://github.com/andiosika/SQL_Hypothesis_Testing_Workflow/blob/master/imgs/output_83_0.png' width=400>

```python
cats = {}
for cat in catavs['CategoryName'].unique():
    cats[cat] = catavs.groupby('CategoryName').get_group(cat)['Revenue']
```
In each of the different categories, the products align as such: 

    There are 10 products in the Dairy Products Category
    There are 7 products in the Grains/Cereals Category
    There are 5 products in the Produce Category
    There are 12 products in the Seafood Category
    There are 12 products in the Condiments Category
    There are 13 products in the Confections Category
    There are 12 products in the Beverages Category
    There are 6 products in the Meat/Poultry Category

### Outliers were identified and removed via z-score testing, Levene's testing revealed the data was not of equal variance so Kruksal Wallance was conducted.  All sample sizes were greater than 15 so the assumption of normality was met.  

 Kruksal Testing yielded a p-value of 0.0 so we can reject the null hypothesis. However, since there are multiple products compared to each other, further testing is required.   
### Post-Hoc Testing: This got complicated since we are comparing each product to every other product individually.
The comarison becomes complicated as each product needs to be compared against the other.  This was solved by creating a dataframe that compared group 1 (g1) to group 2 (g2) and results of [Tukey Testing](https://en.wikipedia.org/wiki/Tukey%27s_range_test) to determine if there was significant difference were collected. Subsequently Cohen's D was determined for each pair separately to examine individual effect size.

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

The table below illustrates those categories that can reject the null hypothesis that states all categories generate equal revenue.  The adjusted probabplity value (padj) reflects probability and the d column illustrates the outcome of the Cohens D test or the effect size. 

```python
mult_Cohn_d(tukeyctrues, cats)
```
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

<img src='https://github.com/andiosika/SQL_Hypothesis_Testing_Workflow/blob/master/imgs/output_109_1.png' width=400>

another look:

<img src="https://github.com/andiosika/SQL_Hypothesis_Testing_Workflow/blob/master/imgs/output_110_1.png" width=400>

Statistically, Meat/Poultry & Produce were statistically equivalent and ranked as top sellers, Dairy & Produce were statiscally equal. 
(Definition of statistically equal: they returned false value from Tukey test, indicating they had a simliar mean and therefore statiticaly equal with a .05 chance of falsely being classified as such)
 
Category | Average Revenue
-- | -- |
Meat/Poultry | `$810.81`
Produce | `$695.87`
Dairy Products | `$593.86`
Condiments | `$455.54`
Confections | `$426.83`
Grains/Cereals | `$421.17`
Beverages | `$399.77`
Seafood | `$353.61`

The table(s) above outlines how the various categories compare to each other.  If the adjusted p-value in column padj is >.05, they are statistically equal.  Conversely of the adjusted p-value 'adjp' is <.05 the two samples are statistically not-equal.  This is further examined by the effect size illustrated in column d.   d=0.2 be considered a 'small' effect size, 0.5 represents a 'medium' effect size and 0.8 a 'large' effect size. 

Notes:
Revenue is calculated by subtracting any extended discounts from the salesprice and multiplying that by quantity sold.


### Recommendation: 

1) If there are additional products that align with the higher revenue generating categories, that category could be broadened to maximize revenue generating potential.  

Example: Meat/Poultry currently has 6 products, this could be expanded.  Conversely, the seafood category carries 12 products which could be narrowed.  Additional analysis could demonstrate which seafood are the best sellers which would be preserved.

2) Knowing what revenue each category generates could potentially influence the ability to appropriately categorize discounts.  However, not knowing profit margins - we'd need to take this into consideration.

_______________
# HYPOTHESIS 3

> ***Do certain sales representatives sell more than others?  Who are the top sellers?***

$H0$: All sales representatives generate equal revenue.

$H1$: Some sales representatives generate more than others in revenue.

__
For this test sql queries were conducted on Product, OrderDetail, Order and Employee Tables
These table includes information on:

    1) Product information including SalesPrice, Discount and Quantity Sold
    2) Sales Representative Information

A dataframe was compiled and a few calculations were made:
```
#Sales Revenue is calculated by multiplying the adjusted price (accounting for any discounts) times quantity
dfr['SaleRev'] = (dfr['SalesPrice'] * (1-dfr['Discount'])) * dfr['Quantity']
```
    
#### Initial Observations:

There are 9 employees in this company associated with sales information and the avarage revenue generated by a sales representative is $629.00. 

Initial visual inspection indicates roughly uniform distribution in sales revenue, more than half of the sales representatives achieve the average.  Additional testing will demonstrate if it is significant.

Since we are comparing multiple discounts to inspect it's impact on quantity ordered an AVNOVA test will be run:
Testing revealed again that equal variance did not exist, outliers were removed via z-scores and since sample sizes were greater than 15 these assumptions were met. 

<img src="https://github.com/andiosika/SQL_Hypothesis_Testing_Workflow/blob/master/imgs/output_135_1.png" width=400>

### Visualization:


<img src="https://github.com/andiosika/SQL_Hypothesis_Testing_Workflow/blob/master/imgs/output_146_1.png" width=400>

**Observation:**
The plot above proved to be misleading since it goes off the mean, it skews the data.  Further testing indicates there are no statistical differences between representatives in terms of revenue generated over this time span.  The subsequent plot reveals a more accurate depiction of what testing demonstrates.

With some outliers removed, the adjusted average revenue across all sales representatives: $494.72
    
<img src="https://github.com/andiosika/SQL_Hypothesis_Testing_Workflow/blob/master/imgs/output_148_1.png" width = 400>

### Findings and recommendations: 

#### Findings:
Both parametric and non parametric tests were conducted, despite indications for non-parametric tests as the dataset(s) did not meet the assupmtion of equal variance. A visual inspection after outlier removal suggested there could be significant variance in the mean and the parametric was run for comparison.  The parametric test indicated that the null hypothesis could be rejected.  However, post-hoc testing validated the efficacy of the non-parametric test to **accept the null hypothesis**, with the smallest probability that the outcome was due to chance was well over the accepted rate of .05. 


#### Recommendation:    
If there is no statistical difference, and effect size is small at best, best practices can still be shared by those who have a higher average revenue, examples 2,3 and 9 still have higher than average sales.
    
Perhaps a little healthy, insentivised competition might spur increased revenues if not by one, by many.  Also, building on knowledge of smaller discounts yielding larger quantities, sales team could increase revenue by being conservative with discount rates.
   
___    
# HYPOTHESIS 4:

> ***Where are the customers from that spend the most money?***

$H0$: Customers spend equal amounts regardless of region.

$H1$: Region has an effect on total amount spent.
   

An SQL query was executed on the OrderDetail and Order tables.  These table includes information on:

    1) Sales total information 
    2) Regions where orders shipped to indicating the location of customers


The amount spent takes into account any discounts that were applied:
```python
dfreg['Amount_Spent'] = ((dfreg['UnitPrice'])*(1 - dfreg['Discount']))*dfreg['Quantity']
```

### Hypothesis 4 Preliminary Observations:

     There are 9 regions, they are Western Europe, South America, Central America, North America, Northern Europe, Scandinavia, Southern Europe, British Isles, and Eastern Europe'.
    The average total spend is $587.37
    The distribution indicates there may be outliers.

<src img="https://github.com/andiosika/SQL_Hypothesis_Testing_Workflow/blob/master/imgs/output_164_1.png" width=400>


<img src="https://github.com/andiosika/SQL_Hypothesis_Testing_Workflow/blob/master/imgs/output_170_0.png" width=400>

#### Hypothesis 4 Initial Observations:


There are 9 regions in reflected in this dataset

The avarage of total spent is $587.37.


Since we are comparing multiple regions to inspect it's impact on quantity ordered an AVNOVA test will be run: Assumptions for ANOVA Testing were examined. 
Testing revealed again that equal variance did not exist, outliers were removed via z-scores and since sample sizes were greater than 15 these assumptions were met. It should be noted that one region was only slightly over the minimum sample size (n>15) and contained 16 samples.

#### Kruskal Wallace testing was conducted once again since the data set was not of equal variance and revealed that we could reject the null hypothesis indicating that some regions generated significantly more revenue than others.


** Noting that the sample size of Eastern Europe is relatively small and the confidence interval is much greater to accomodate for it, possibly skewing the results.

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

### Visualization

<img src="https://github.com/andiosika/SQL_Hypothesis_Testing_Workflow/blob/master/imgs/output_196_0.png" width=400>

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

** Noting that the sample size of Eastern Europe is relatively small and the confidence interval is much greater to accomodate for it, possibly skewing the results.

```python
tukeyr.plot_simultaneous();
```

<img src="https://github.com/andiosika/SQL_Hypothesis_Testing_Workflow/blob/master/imgs/output_187_0.png" width = 400>

#### Recommendations:
Explore best practices from regions that are top performers.  
Market analysis for regions that need to be developed. 
Leverage knowledge gained regarding categories and discounts.

________
# In Closing:

Since the data provided did not include purchase prices of merchandise, ways were examined to maximize revenues.
The datasets were all multi group comparisons and none of the groups met all the assupmtions for parametric testing.  All groups called for Kruskal-Wallis and post-hoc testing detailed in this notebook.

It was discovered through hypothesis testing and data analysis, various ways to achieve this through: 
    Minimizing discounts
    Broadening Revenue Generating Categories
    Explore best practices from top performing regions: North America, Northern Europe, and Western Europe
    Conduct market analysis on regions that need to be developed: South America, Southern Europe as well as Eastern Europe
    
In addition, future analysis and testing could provide insight to: 
    Develop Regional Markets
    Develop Sales Staff
    
    
   
