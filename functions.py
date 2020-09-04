
def Cohen_d(group1, group2, correction = False):
    """Compute Cohen's d
    d = (group1.mean()-group2.mean())/pool_variance.
    pooled_variance= (n1 * var1 + n2 * var2) / (n1 + n2)

    Args:
        group1 (Series or NumPy array): group 1 for calculating d
        group2 (Series or NumPy array): group 2 for calculating d
        correction (bool): Apply equation correction if N<50. Default is False. 
            - Url with small ncorrection equation: 
                - https://www.statisticshowto.datasciencecentral.com/cohens-d/ 
    Returns:
        d (float): calculated d value
         
    INTERPRETATION OF COHEN's D: 
    > Small effect = 0.2
    > Medium Effect = 0.5
    > Large Effect = 0.8
    
    """    
    import scipy.stats as stats
    import scipy   
    import numpy as np
    N = len(group1)+len(group2)
    diff = group1.mean() - group2.mean()

    n1, n2 = len(group1), len(group2)
    var1 = group1.var()
    var2 = group2.var()

    # Calculate the pooled threshold as shown earlier
    pooled_var = (n1 * var1 + n2 * var2) / (n1 + n2)
    
    # Calculate Cohen's d statistic
    d = diff / np.sqrt(pooled_var)
    
    ## Apply correction if needed
    if (N < 50) & (correction==True):
        d=d * ((N-3)/(N-2.25))*np.sqrt((N-2)/N)
    
    return d

#Your code here
def find_outliers_Z(data,col=None):
    """Use scipy to calcualte absoliute Z-scores 
    and return boolean series where True indicates it is an outlier

    Args:
        data (DataFrame,Series,or ndarray): data to test for outliers.
        col (str): If passing a DataFrame, must specify column to use.

    Returns:
        [boolean Series]: A True/False for each row use to slice outliers.
        
    EXAMPLE USE: 
    >> idx_outs = find_outliers_df(df,col='AdjustedCompensation')
    >> good_data = data[~idx_outs].copy()
    """
    
    from scipy import stats
    import numpy as np
    import pandas as pd

    if isinstance(data, pd.DataFrame):
        if col is None:
            raise Exception('If passing a DataFrame, must provide col=')
        else:
            data = data[col]
    elif isinstance(data,np.ndarray):
        data= pd.Series(data)

    elif isinstance(data,pd.Series):
        pass
    else:
        raise Exception('data must be a DataFrame, Series, or np.ndarray')
    
    z = np.abs(stats.zscore(data))
    idx_outliers = np.where(z>3,True,False)
    return idx_outliers

    
    
def find_outliers_IQR(data):
    """Use Tukey's Method of outlier removal AKA InterQuartile-Range Rule
    and return boolean series where True indicates it is an outlier.
    - Calculates the range between the 75% and 25% quartiles
    - Outliers fall outside upper and lower limits, using a treshold of  1.5*IQR the 75% and 25% quartiles.

    IQR Range Calculation:    
        res = df.describe()
        IQR = res['75%'] -  res['25%']
        lower_limit = res['25%'] - 1.5*IQR
        upper_limit = res['75%'] + 1.5*IQR

    Args:
        data (Series,or ndarray): data to test for outliers.

    Returns:
        [boolean Series]: A True/False for each row use to slice outliers.
        
    EXAMPLE USE: 
    >> idx_outs = find_outliers_df(df['AdjustedCompensation'])
    >> good_data = df[~idx_outs].copy()
    
    """
    import pandas as pd
    df_b=data
    res= df_b.describe()

    IQR = res['75%'] -  res['25%']
    lower_limit = res['25%'] - 1.5*IQR
    upper_limit = res['75%'] + 1.5*IQR

    idx_outs = (df_b>upper_limit) | (df_b<lower_limit)

    return idx_outs

def test_equal_variance(grp1,grp2, alpha=.05):
    stat,p = stats.levene(grp1,grp2)
    if p<alpha:
        print(f"Levene's test p value of {np.round(p,3)} is < {alpha}, therefore groups do NOT have equal variance.")
    else:
        print(f"Normal test p value of {np.round(p,3)} is > {alpha},  therefore groups DOES have equal variance.")
    return p

def test_normality(grp_control,col='BL',alpha=0.05):
    import scipy.stats as stats
    stat,p =stats.normaltest(grp_control[col])
    if p<alpha:
        print(f"Normal test p value of {np.round(p,3)} is < {alpha}, therefore data is NOT normal.")
    else:
        print(f"Normal test p value of {np.round(p,3)} is > {alpha}, therefore data IS normal.")
    return p

def test_assumptions(**kwargs):
    import scipy.stats as stats
    res= [['Test','Group','Stat','p','p<.05']]
    
    all_data = []
    for k,v in kwargs.items():
        try:
            all_data.append(v)
            stat,p =stats.normaltest(v)
            res.append(['Normality',k,stat,p,p<.05])
        except:
            res.append(['Normality',k,'err','err','err'])
        
    stat,p = stats.levene(*all_data)
    res.append(['Equal Variance','All',stat,p,p<.05]) 
    
    res=pd.DataFrame(res[1:],columns=res[0]).round(3)
    
    return res

def prep_data_for_tukeys(reps):
    """Accepts a dictionary with group names as the keys 
    and pandas series as the values. 
    
    Returns a dataframe ready for tukeys test:
    - with a 'data' column and a 'group' column for sms.stats.multicomp.pairwise_tukeyhsd 
    
    Example Use:
    df_tukey = prep_data_for_tukeys(grp_data)
    tukey = sms.stats.multicomp.pairwise_tukeyhsd(df_tukey['data'], df_tukey['group'])
    tukey.summary()"""
    import pandas as pd
    df_tukey = pd.DataFrame(columns=['data','group'])
    for k,v in  reps.items():
        grp_df = v.rename('data').to_frame() 
        grp_df['group'] = k
        df_tukey=pd.concat([df_tukey,grp_df],axis=0)
        df_tukey['group']=df_tukey['group'].astype(str)
        df_tukey['data']=df_tukey['data'].astype(float)
    return df_tukey

def tukey_df(tukey_results):
    '''Creates a DataFrame from the .stats Tukey test
    output can be sliced/manipulated accordingly
    
    Example use: building a dataframe for slicing out 
    the samples that are statistically not equal and 
    return a True value on Tukey test.
    
    tukeycdf = tukey_df(tukeyc)
    
    tukeyctrues  = tukeycdf.loc[tukeycdf['reject']==True]
    tukeyctrues '''
    import pandas as pd
    tukey_df = pd.DataFrame(data=tukey_results._results_table.data[1:], columns=tukey_results._results_table.data[0])
    return tukey_df

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
        d = Cohen_d(df_dict[g1], df_dict[g2])

        res.append([g1, g2,padj, d])

    mdc = pd.DataFrame(res[1:], columns=res[0])
    return mdc

def sort_index(df):
    ''' Tool for sorting an index, 
    
    Example use:
    sns.barplot(data=dg, x='group', y='data', ci=68,order=index, palette="rocket", ax=ax) '''
    
    index = list(df.groupby('group').mean().sort_values('data', ascending=False).index)
    return index
     


