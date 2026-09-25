![CustomAnalytics2_cropped.png](8e70f867-dab2-4034-8b25-3f87dbac1498.png)

# MintClassics Warehouse Elimination Study

### Imports


```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
```


```python
data_file = 'CSV_Files/productLinesInfo.csv'
```


```python
df = pd.read_csv(data_file)
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
      <th>warehouseCode</th>
      <th>productCode</th>
      <th>productLine</th>
      <th>productVendor</th>
      <th>buyPrice</th>
      <th>quantityInStock</th>
      <th>investmentValue</th>
      <th>priceEach</th>
      <th>quantitySold</th>
      <th>lineRevenue</th>
      <th>grossRevenue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>a</td>
      <td>S10_1678</td>
      <td>Motorcycles</td>
      <td>Min Lin Diecast</td>
      <td>48.81</td>
      <td>7933</td>
      <td>387209.73</td>
      <td>81.35</td>
      <td>124</td>
      <td>244.05</td>
      <td>30262.20</td>
    </tr>
    <tr>
      <th>1</th>
      <td>a</td>
      <td>S10_1678</td>
      <td>Motorcycles</td>
      <td>Min Lin Diecast</td>
      <td>48.81</td>
      <td>7933</td>
      <td>387209.73</td>
      <td>86.13</td>
      <td>34</td>
      <td>86.13</td>
      <td>2928.42</td>
    </tr>
    <tr>
      <th>2</th>
      <td>a</td>
      <td>S10_1678</td>
      <td>Motorcycles</td>
      <td>Min Lin Diecast</td>
      <td>48.81</td>
      <td>7933</td>
      <td>387209.73</td>
      <td>90.92</td>
      <td>82</td>
      <td>181.84</td>
      <td>14910.88</td>
    </tr>
    <tr>
      <th>3</th>
      <td>a</td>
      <td>S10_1678</td>
      <td>Motorcycles</td>
      <td>Min Lin Diecast</td>
      <td>48.81</td>
      <td>7933</td>
      <td>387209.73</td>
      <td>76.56</td>
      <td>118</td>
      <td>306.24</td>
      <td>36136.32</td>
    </tr>
    <tr>
      <th>4</th>
      <td>a</td>
      <td>S10_1678</td>
      <td>Motorcycles</td>
      <td>Min Lin Diecast</td>
      <td>48.81</td>
      <td>7933</td>
      <td>387209.73</td>
      <td>94.74</td>
      <td>77</td>
      <td>189.48</td>
      <td>14589.96</td>
    </tr>
  </tbody>
</table>
</div>



## Initial inspection of stock on hand by warehouse location

- The first thing to check is the distribution of product stock according to which warehouse location the stock is being stored.


```python
warehouse_data = df.groupby('warehouseCode')[['quantityInStock', 'investmentValue']].sum().reset_index()
warehouse_data
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
      <th>warehouseCode</th>
      <th>quantityInStock</th>
      <th>investmentValue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>a</td>
      <td>2035676</td>
      <td>1.033236e+08</td>
    </tr>
    <tr>
      <th>1</th>
      <td>b</td>
      <td>3265557</td>
      <td>2.125878e+08</td>
    </tr>
    <tr>
      <th>2</th>
      <td>c</td>
      <td>1941757</td>
      <td>8.882738e+07</td>
    </tr>
    <tr>
      <th>3</th>
      <td>d</td>
      <td>1264110</td>
      <td>6.573173e+07</td>
    </tr>
  </tbody>
</table>
</div>




```python
fig, ax = plt.subplots(1, 2, figsize=(16, 7))

labels = ['Warehouse A', 'Warehouse B', 'Warehouse C', 'Warehouse D']

wedges0, texts0, autotexts0 = ax[0].pie(
    warehouse_data.quantityInStock, 
    labels=labels, 
    autopct='%1.1f%%', 
    wedgeprops={'edgecolor': 'black', 'linewidth': 1.5}
)
ax[0].set_title('Stock Quantity by Warehouse', fontsize=22, weight='bold')
plt.setp(autotexts0, size=16, weight="bold", color="white")
plt.setp(texts0, size=15, weight="bold")

wedges1, texts1, autotexts1 = ax[1].pie(
        warehouse_data.investmentValue,
        labels=labels,
        autopct='%1.1f%%',
        wedgeprops={'edgecolor': 'black', 'linewidth': 1.5}
         )
ax[1].set_title('Investment Value by Warehouse', fontsize=22, weight='bold')
plt.setp(autotexts1, size=16, weight="bold", color="white")
plt.setp(texts1, size=15, weight="bold")

plt.tight_layout()
plt.show()
plt.close('all')


```


    
![png](output_9_0.png)
    


- The majority of product stock is stored in Warehouse A.
- The cost of the stock in Warehouse A is comparatively higher than the cost of the stock stored in any of the other warehouses as demonstrated by the 'Investment Value' being 6% higher than the 'Stock Quantity'

## Check Customer Locations

- Where does each warehouse ship it's products?
- Does each warehouse service it's own geographic location?

![MintClassicsMap.png](9cd8f22a-1241-4222-9e36-da9f3df30ceb.png)

- The map shows that each of the four warehouses ship to all customer regions.

## Check Warehouse Sales & Overhead

- What does the overall product overhead look like?
- How much overhead investment cost is in each warehouse?


```python
df_OH = df.groupby(['productCode', 'investmentValue'])['grossRevenue'].sum().sort_values().reset_index()
df_OH.head()
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
      <th>productCode</th>
      <th>investmentValue</th>
      <th>grossRevenue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>S24_2840</td>
      <td>40443.22</td>
      <td>57481.15</td>
    </tr>
    <tr>
      <th>1</th>
      <td>S32_2206</td>
      <td>223077.74</td>
      <td>69291.41</td>
    </tr>
    <tr>
      <th>2</th>
      <td>S24_3969</td>
      <td>45261.75</td>
      <td>73419.21</td>
    </tr>
    <tr>
      <th>3</th>
      <td>S24_1937</td>
      <td>165483.24</td>
      <td>74553.29</td>
    </tr>
    <tr>
      <th>4</th>
      <td>S18_2248</td>
      <td>17982.00</td>
      <td>83767.75</td>
    </tr>
  </tbody>
</table>
</div>




```python
fig, ax = plt.subplots(figsize=(10, 4))

ax.bar(df_OH['productCode'], df_OH['grossRevenue'], color='steelblue').set_label('Gross Revenue')
ax.bar(df_OH['productCode'], df_OH['investmentValue'], bottom=df_OH['grossRevenue'], color='orange').set_label('Investment Value')
ax.legend()

ax.set_xticks([])
ax.set_title('Investment Overhead / Sales Revenue', fontsize=13, pad=15)
ax.set_xlabel('All Products', fontsize=11)
ax.set_ylabel('In Dollars', fontsize=11)

plt.tight_layout()
plt.show()
plt.close('all')
```


    
![png](output_18_0.png)
    


- Overall, sales look reasonable across all product codes with no serious problems in terms of extreme poor sales performance.
- The amount of inventory for each product code is fairly inconsistent.
- Several products show extremely low inventory on hand.

### Sort Products by Warehouse


```python
df_WH = df.groupby(['warehouseCode', 'productCode', 'investmentValue'])['grossRevenue'].sum().sort_values().reset_index()
df_WH.head()
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
      <th>warehouseCode</th>
      <th>productCode</th>
      <th>investmentValue</th>
      <th>grossRevenue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>b</td>
      <td>S24_2840</td>
      <td>40443.22</td>
      <td>57481.15</td>
    </tr>
    <tr>
      <th>1</th>
      <td>a</td>
      <td>S32_2206</td>
      <td>223077.74</td>
      <td>69291.41</td>
    </tr>
    <tr>
      <th>2</th>
      <td>c</td>
      <td>S24_3969</td>
      <td>45261.75</td>
      <td>73419.21</td>
    </tr>
    <tr>
      <th>3</th>
      <td>c</td>
      <td>S24_1937</td>
      <td>165483.24</td>
      <td>74553.29</td>
    </tr>
    <tr>
      <th>4</th>
      <td>c</td>
      <td>S18_2248</td>
      <td>17982.00</td>
      <td>83767.75</td>
    </tr>
  </tbody>
</table>
</div>




```python
df_WHa = df_WH[(df_WH['warehouseCode'] == 'a')].sort_values('grossRevenue')
df_WHb = df_WH[(df_WH['warehouseCode'] == 'b')].sort_values('grossRevenue')
df_WHc = df_WH[(df_WH['warehouseCode'] == 'c')].sort_values('grossRevenue')
df_WHd = df_WH[(df_WH['warehouseCode'] == 'd')].sort_values('grossRevenue')
```


```python
fig, ax = plt.subplots(1, 4, figsize=(12, 4))

fig.suptitle('Investment Overhead / Sales Revenue\nBy Warehouse', fontsize=20, y=1.02)

ax[0].bar(df_WHa['productCode'], df_WHa['grossRevenue'], color='steelblue').set_label('Gross Revenue')
ax[0].bar(df_WHa['productCode'], df_WHa['investmentValue'], bottom=df_WHa['grossRevenue'], color='orange').set_label('Investment Value')
ax[0].set_xlabel("Warehouse A")
ax[0].set_xticks([])

ax[1].bar(df_WHb['productCode'], df_WHb['grossRevenue'], color='steelblue')
ax[1].bar(df_WHb['productCode'], df_WHb['investmentValue'], bottom=df_WHb['grossRevenue'], color='orange')
ax[1].set_xlabel("Warehouse B")
ax[1].set_xticks([])

ax[2].bar(df_WHc['productCode'], df_WHc['grossRevenue'], color='steelblue')
ax[2].bar(df_WHc['productCode'], df_WHc['investmentValue'], bottom=df_WHc['grossRevenue'], color='orange')
ax[2].set_xlabel("Warehouse C")
ax[2].set_xticks([])

ax[3].bar(df_WHd['productCode'], df_WHd['grossRevenue'], color='steelblue')
ax[3].bar(df_WHd['productCode'], df_WHd['investmentValue'], bottom=df_WHd['grossRevenue'], color='orange')
ax[3].set_xlabel("Warehouse D")
ax[3].set_xticks([])

fig.legend()

ax[1].sharey(ax[0])
ax[2].sharey(ax[0])
ax[3].sharey(ax[0])

plt.tight_layout()
plt.show()
plt.close('all')
```


    
![png](output_23_0.png)
    


- All warehouses are selling inventory with reasonable distributions.
- All warehouses contain some products which appear to contain insufficient stock levels based on previous sales.
- Depending on the resons behind the low inventory of certain products it may be advisable to discontinue those particular products.

## Check Low-Stock by Manufacturer

- Check for low stock by the current investment in inventory by product code.
- Inspect whether there is any correlation between low-stock items and any particular manufacturer.


```python
df_LS = df.groupby([ 'productVendor', 'productCode', 'warehouseCode', 'investmentValue'])['grossRevenue'].sum().reset_index()
df_LS = df_LS.sort_values('investmentValue')
df_LS.head(10)
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
      <th>productVendor</th>
      <th>productCode</th>
      <th>warehouseCode</th>
      <th>investmentValue</th>
      <th>grossRevenue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>48</th>
      <td>Highway 66 Mini Classics</td>
      <td>S24_2000</td>
      <td>a</td>
      <td>559.80</td>
      <td>184872.72</td>
    </tr>
    <tr>
      <th>50</th>
      <td>Highway 66 Mini Classics</td>
      <td>S32_4289</td>
      <td>c</td>
      <td>4490.72</td>
      <td>116846.98</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Autoart Studio Design</td>
      <td>S12_1099</td>
      <td>b</td>
      <td>6483.12</td>
      <td>405790.13</td>
    </tr>
    <tr>
      <th>35</th>
      <td>Exoto Designs</td>
      <td>S32_1374</td>
      <td>a</td>
      <td>11911.76</td>
      <td>184494.69</td>
    </tr>
    <tr>
      <th>100</th>
      <td>Unimax Art Galleries</td>
      <td>S72_3212</td>
      <td>d</td>
      <td>13786.20</td>
      <td>115385.28</td>
    </tr>
    <tr>
      <th>63</th>
      <td>Motor City Art Classics</td>
      <td>S18_2248</td>
      <td>c</td>
      <td>17982.00</td>
      <td>83767.75</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Autoart Studio Design</td>
      <td>S50_4713</td>
      <td>a</td>
      <td>20502.00</td>
      <td>147570.78</td>
    </tr>
    <tr>
      <th>75</th>
      <td>Red Start Diecast</td>
      <td>S32_3522</td>
      <td>d</td>
      <td>27358.54</td>
      <td>139560.92</td>
    </tr>
    <tr>
      <th>68</th>
      <td>Motor City Art Classics</td>
      <td>S700_3167</td>
      <td>a</td>
      <td>29974.40</td>
      <td>177948.80</td>
    </tr>
    <tr>
      <th>92</th>
      <td>Studio M Art Models</td>
      <td>S700_1938</td>
      <td>d</td>
      <td>31912.10</td>
      <td>149632.93</td>
    </tr>
  </tbody>
</table>
</div>



- Seven out of 13 product vendors are represented in the Top10 lowest inventory query.

## Reinspect the Overhead Graphs Sorted by Product Vendor


```python
vendors = df_LS['productVendor'].unique()
vendor_dfs = []

for vendor in vendors:
    df_temp = df_LS[(df_LS['productVendor'] == vendor)].sort_values('grossRevenue')
    vendor_dfs.append(df_temp)


fig, axes = plt.subplots(2, 7, figsize=(12, 6))
ax = axes.flatten()

fig.suptitle('Investment Overhead / Sales Revenue\nBy Manufacturer', fontsize=20, y=1.02)

for i in range(len(vendors)):
    Vendor = vendors[i]
    df_temp = vendor_dfs[i]

    ax[i].bar(df_temp['productCode'],
          df_temp['grossRevenue'],
          color='steelblue'
         )

    ax[i].bar(df_temp['productCode'],
          df_temp['investmentValue'],
          color='orange',
          bottom=df_temp['grossRevenue']
         )

    ax[i].set_xlabel(vendors[i])
    ax[i].set_xticks([])
    ax[i].sharey(ax[0])

ax[13].set_axis_off()
plt.tight_layout()
plt.show()
plt.close('all')
```


    
![png](output_30_0.png)
    


- Clearly now, issues regarding low-stock inventory are with respect to individual products and not the fault of any single suppier.
- Low stock levels are not directly correlated to high sales volumes in most cases.
- The dataset lacks the necessary product supply information required to investigate any further at this time.

## Check Warehouse Volumes

- Actual packaging volume information was not available.
- A list of the approximate product volumes has been generated based on product names and scale for the purpose of analysis.


```python
df_cap = pd.read_csv('CSV_Files/capacityInfo.csv')
df_cap['warehouseCode'] = df_cap['warehouseCode'].str.upper()
df_cap
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
      <th>warehouseCode</th>
      <th>warehousePctCap</th>
      <th>stockVolume</th>
      <th>warehouseCapacity</th>
      <th>spaceRemaining</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>A</td>
      <td>72</td>
      <td>13288.2293</td>
      <td>18455.874028</td>
      <td>5167.644728</td>
    </tr>
    <tr>
      <th>1</th>
      <td>B</td>
      <td>67</td>
      <td>23207.0423</td>
      <td>34637.376567</td>
      <td>11430.334267</td>
    </tr>
    <tr>
      <th>2</th>
      <td>C</td>
      <td>50</td>
      <td>6936.7398</td>
      <td>13873.479600</td>
      <td>6936.739800</td>
    </tr>
    <tr>
      <th>3</th>
      <td>D</td>
      <td>75</td>
      <td>7891.7998</td>
      <td>10522.399733</td>
      <td>2630.599933</td>
    </tr>
  </tbody>
</table>
</div>




```python
fig, ax = plt.subplots(figsize=(10, 5))

rects1 = ax.bar(df_cap['warehouseCode'],
           df_cap['stockVolume'],
           color='red',
           edgecolor='black',
           label ='Stock Volume')

rects2 = ax.bar(df_cap['warehouseCode'],
           df_cap['spaceRemaining'],
           bottom=df_cap['stockVolume'],
           color='yellow',
           edgecolor='black',
           label='Space Remaining')

ax.bar_label(rects1, fmt='%.0f', label_type='center', color='white')
ax.bar_label(rects2, fmt='%.0f', label_type='center')

ax.set_title('Warehouse Stock Information', fontsize=20, pad=15)
ax.legend()

plt.tight_layout()
plt.show()
plt.close('all')
```


    
![png](output_35_0.png)
    


- The largest warehouse, Warehouse B, shows enough space remaining to hold the stock from either Warehouse C or Warehouse D.
- Considering that Warehouse C is half-empty, this may a good candidate for closure.


```python
df_PL = pd.read_csv('CSV_Files/avgProductLineVolume.csv')
df_PL = df_PL.sort_values(by='warehouseCode')
df_PL
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
      <th>warehouseCode</th>
      <th>productLine</th>
      <th>averageProductVolume</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>a</td>
      <td>Planes</td>
      <td>0.016425</td>
    </tr>
    <tr>
      <th>5</th>
      <td>a</td>
      <td>Motorcycles</td>
      <td>0.136623</td>
    </tr>
    <tr>
      <th>4</th>
      <td>b</td>
      <td>Classic Cars</td>
      <td>0.113468</td>
    </tr>
    <tr>
      <th>3</th>
      <td>c</td>
      <td>Vintage Cars</td>
      <td>0.054325</td>
    </tr>
    <tr>
      <th>0</th>
      <td>d</td>
      <td>Ships</td>
      <td>0.011333</td>
    </tr>
    <tr>
      <th>2</th>
      <td>d</td>
      <td>Trains</td>
      <td>0.021433</td>
    </tr>
    <tr>
      <th>6</th>
      <td>d</td>
      <td>Trucks and Buses</td>
      <td>0.150755</td>
    </tr>
  </tbody>
</table>
</div>



- It can be seen that the large warehouse "B" contains only 'Classic Cars'.
- The warehouse which is a candidate for closure, "C", contains only 'Vintage Cars'.
- Merging the contents of warehouses B and C would allow for the full stock of 'Cars' to be housed in a single location.

## Look into Warehouse Shipping Efficiency

- Check the amount of time each warehouse requires to ship an order.
- Look for shipping delays from each warehouse.
- Determine if shipping delays are incidental or a systemic issue.


```python
df_SI = pd.read_csv('CSV_Files/shippingInfo.csv')
df_SI.head()
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
      <th>orderNumber</th>
      <th>warehouseCode</th>
      <th>productCode</th>
      <th>daysToShipping</th>
      <th>lineTotal</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>10210</td>
      <td>a</td>
      <td>S10_2016</td>
      <td>8</td>
      <td>2598.77</td>
    </tr>
    <tr>
      <th>1</th>
      <td>10210</td>
      <td>a</td>
      <td>S10_4698</td>
      <td>8</td>
      <td>6452.86</td>
    </tr>
    <tr>
      <th>2</th>
      <td>10210</td>
      <td>a</td>
      <td>S18_1662</td>
      <td>8</td>
      <td>4399.52</td>
    </tr>
    <tr>
      <th>3</th>
      <td>10210</td>
      <td>a</td>
      <td>S18_2581</td>
      <td>8</td>
      <td>3421.50</td>
    </tr>
    <tr>
      <th>4</th>
      <td>10210</td>
      <td>a</td>
      <td>S18_2625</td>
      <td>8</td>
      <td>2059.20</td>
    </tr>
  </tbody>
</table>
</div>




```python
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

# 1. Setup data
x = df_SI["daysToShipping"]

# 2. Set up a spacious canvas
plt.figure(figsize=(12, 6))

plt.hist(x, bins=8, color='teal', edgecolor='black', alpha=0.7)

plt.title('Overall Days to Shipping', fontsize=20, pad=15)
plt.xlabel('Days to Shipping', fontsize=12)
plt.ylabel('Number of Orders', fontsize=12)

plt.tight_layout()
plt.show()
plt.close('all')
```


    
![png](output_42_0.png)
    


#### Orders shipped from multiple warehouses DO NOT differentiate their date of shipment from each warehouse individually, THEREFORE the aggregated totals for each will only show a difference if a given warehouse is performing differently than average.


```python
warehouses = sorted(df_SI['warehouseCode'].unique())
num = len(warehouses)
warehouse_list = []

colors = ['#970afa', '#ff9c00', '#ef0000', '#fdff08']

fig, ax = plt.subplots(1, num, figsize=(12, 4))

for warehouse in warehouses:
    df_temp = df_SI[df_SI['warehouseCode'] == warehouse]['daysToShipping']
    warehouse_list.append(df_temp)

for i, warehouse in enumerate(warehouses):
    ax[i].hist(warehouse_list[i], bins=8, color=colors[i % len(colors)], edgecolor='black', alpha=0.7)
    ax[i].set_xlabel(f'Warehouse \'{warehouse.upper()}\'\nDays to Shipping', fontsize=10)
    

fig.suptitle('Days to Shipping by Warehouse', fontsize=20, y=0.95)
plt.tight_layout()
plt.show()
plt.close('all')

```


    
![png](output_44_0.png)
    


#### After splitting the shipping delays into occurances by location, normalized to maximum orders per bin:

- Warehouse 'B' has proportionally more One-Day shipping delays than the other warehouses.
- If warehouse 'C' were to be moved into warehouse 'B' then warehouse 'B' must be able to accomodate an extra 100 orders worth of source/process/ship per day.
- If the One-Day and Two-Day shipping delays associated with warehouse 'B' are the result of order volume, staffing, or warehouse operations efficiency, then these potential bottlenecks should be rectified prior to moving extra inventory into warehouse 'B'.

## Next Steps:

#### - Compare the actual volumes of Warehouse B and Warehouse C against the estimated model

- It is extremely important to remember that the amount of space that any given portion of inventory shall occupy has been estimated here without the spacial burden of the items' packaging.
- It would be unsurprising to discover that the smaller scale models of current Warehouse C have proportionally more packaging than the somewhat larger models currently occupying Warehouse B.
- Both Warehouse B and Warehouse C will, in reality, be much larger than the generated volumes which were used to compare warehouse capacities.  Comparing the ratio of (Actual:Estimated) warehouse volume for each warehouse could possibly be used in lieu of ascertaining complete product packaging size information.

#### - Look into the reasons why some items have incredibly low inventory stock

- Are any of these items no longer availible or difficult to acquire from the manufacturer?
- If so, consider dropping those products from the Mint Classics products catalogue.
- This method could be useful in warehouse reorganization more storage volume might be achieved from the same square footage with less individual product codes to keep organized and accessible.

#### - Consider the ability to handle the logistics of increased shipping from Warehouse B

- At the outset of this analysis, Mint Classics expressed an interest in being able to ship products within 24 hours of recieving a purchase order.
- The warehouse to which the inventory of the proposed closure would be moved has a higher proportion of 2-3 day delays than the other warehouses.
- Ensure that warehouse staffing and logistics in Warehouse B will be capable of accomodating the estimated 100 extra line items of orders per day after ammalgamation.
- Condense the existing inventory in Warehouse B creating a completely seperate and empty space for the inventory of Warehouse C prior to shutting down Warehouse.

### Please feel free to come back with any other more specific questions regarding any aspect of this ongoing project.

# Thank You for choosing BCPMcustom Analytics!
