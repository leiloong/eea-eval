## Experimental analysis of knowledge graph embedding for entity alignment
> We developed a degree-based sampling method to generate 42 alignment-oriented datasets from real-world large-scale KGs, representing different heterogeneities of the original KGs. We selected three state-of-the-art embedding-based entity alignment methods for evaluation and comparison. Furthermore, we observed that multi-mapping relations and literal embedding are the two main obstacles for embedding-based entity alignment and some preliminary solutions were attempted. Specifically, we leveraged several enhanced KG embedding models to handle multi-mapping relations and used word2vec to incorporate literal similarities into embeddings. Our findings indicate that the performance of existing embedding-based methods is influenced by the characteristics of datasets and not all KG embedding models are suitable for entity alignment. Alignment-oriented KG embedding remains to be explored.

### Dataset
Our datasets can be found here _ . It contains three folders namely "_1", "_2" and "_3", denoting our three samples.

For each dataset, we have xx files:
* file1:
* file2:
* filex:
...

The statistics of the 100K datasets are shown below.

<table style="text-align:center;font-size:10px" align="center">
    <tr>
        <th style="text-align:center"  colspan="21">DBP-WD-100K</th>
    </tr>
    <tr>
        <td colspan="2" rowspan="2"></td>
        <td style="text-align:center" colspan="3">V1</td>
        <td style="text-align:center" colspan="3">V2</td>
    </tr>
    <tr>
        <td style="text-align:center">MTransE</td>
        <td style="text-align:center">IPTransE</td>
        <td style="text-align:center">JAPE</td>
        <td style="text-align:center">MTransE</td>
        <td style="text-align:center">IPTransE</td>
        <td style="text-align:center">JAPE</td>
    </tr>
    <tr>
	<td style="text-align:center;valign:middle" rowspan=5>Hits@1</td>
	<td style="text-align:center">S1</td>
	<td style="text-align:center">22.05</td>
	<td style="text-align:center">21.84</td>
	<td style="text-align:center">22.67</td>
	<td style="text-align:center">25.4</td>
	<td style="text-align:center">30.71</td>
	<td style="text-align:center">21.1</td></tr>
	</tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">20.94</td>
	<td style="text-align:center">22.12</td>
	<td style="text-align:center">20.88</td>
	<td style="text-align:center">24.33</td>
	<td style="text-align:center">29.16</td>
	<td style="text-align:center">24.85</td>
</tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">23.24</td>
	<td style="text-align:center">25.78</td>
	<td style="text-align:center">24.17</td>
	<td style="text-align:center">23.1</td>
	<td style="text-align:center">27.81</td>
	<td style="text-align:center">23.23</td>
</tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">22.08</td>
	<td style="text-align:center">23.25</td>
	<td style="text-align:center">22.57</td>
	<td style="text-align:center">24.28</td>
	<td style="text-align:center">29.23</td>
	<td style="text-align:center">23.06</td>
</tr>
<tr>
	<td style="text-align:center">STDEV</td>
	<td style="text-align:center">1.15</td>
	<td style="text-align:center">2.2</td>
	<td style="text-align:center">1.65</td>
	<td style="text-align:center">1.15</td>
	<td style="text-align:center">1.45</td>
	<td style="text-align:center">1.88</td>
</tr>
    
<tr>
	<td style="text-align:center;valign:middle" rowspan=5>Hits@10</td>
	<td style="text-align:center">S1</td>
	<td style="text-align:center">41.38</td>
	<td style="text-align:center">40.13</td>
	<td style="text-align:center">43.32</td>
	<td style="text-align:center">49.3</td>
	<td style="text-align:center">59.2</td>
	<td style="text-align:center">43.57</td>
</tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">40.31</td>
	<td style="text-align:center">42.52</td>
	<td style="text-align:center">40.92</td>
	<td style="text-align:center">46.15</td>
	<td style="text-align:center">54.91</td>
	<td style="text-align:center">47.55</td>
</tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">44.14</td>
	<td style="text-align:center">48.57</td>
	<td style="text-align:center">46.16</td>
	<td style="text-align:center">45.5</td>
	<td style="text-align:center">53.74</td>
	<td style="text-align:center">46.47</td>
</tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">41.94</td>
	<td style="text-align:center">43.74</td>
	<td style="text-align:center">43.47</td>
	<td style="text-align:center">46.98</td>
	<td style="text-align:center">55.95</td>
	<td style="text-align:center">45.86</td>
</tr>
<tr>
	<td style="text-align:center">STDEV</td>
	<td style="text-align:center">1.98</td>
	<td style="text-align:center">4.35</td>
	<td style="text-align:center">2.62</td>
	<td style="text-align:center">2.03</td>
	<td style="text-align:center">2.87</td>
	<td style="text-align:center">2.06</td>
</tr>    
	
<tr>
	<td style="text-align:center;valign:middle" rowspan=5>MR</td>
	<td style="text-align:center">S1</td>
	<td style="text-align:center">1111.74</td>
	<td style="text-align:center">876.47</td>
	<td style="text-align:center">790.99</td>
	<td style="text-align:center">628.08</td>
	<td style="text-align:center">243.95</td>
	<td style="text-align:center">534.53</td>
</tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">1041.4</td>
	<td style="text-align:center">935.78</td>
	<td style="text-align:center">842.33</td>
	<td style="text-align:center">985.74</td>
	<td style="text-align:center">480.58</td>
	<td style="text-align:center">754.94</td>
</tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">1151.58</td>
	<td style="text-align:center">884.98</td>
	<td style="text-align:center">946.76</td>
	<td style="text-align:center">835.63</td>
	<td style="text-align:center">440.26</td>
	<td style="text-align:center">579.05</td>
</tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">1101.57</td>
	<td style="text-align:center">899.08</td>
	<td style="text-align:center">860.03</td>
	<td style="text-align:center">816.48</td>
	<td style="text-align:center">388.26</td>
	<td style="text-align:center">622.84</td>
</tr>
<tr>
	<td style="text-align:center">STDEV</td>
	<td style="text-align:center">55.79</td>
	<td style="text-align:center">32.07</td>
	<td style="text-align:center">79.38</td>
	<td style="text-align:center">179.6</td>
	<td style="text-align:center">126.59</td>
	<td style="text-align:center">116.55</td>
</tr>
<tr>
	<td style="text-align:center;valign:middle" rowspan=5>MRR</td>
	<td style="text-align:center">S1</td>
	<td style="text-align:center">0.29</td>
	<td style="text-align:center">0.28</td>
	<td style="text-align:center">0.3</td>
	<td style="text-align:center">0.34</td>
	<td style="text-align:center">0.4</td>
	<td style="text-align:center">0.29</td>
</tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">0.28</td>
	<td style="text-align:center">0.29</td>
	<td style="text-align:center">0.28</td>
	<td style="text-align:center">0.32</td>
	<td style="text-align:center">0.38</td>
	<td style="text-align:center">0.33</td>
</tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">0.31</td>
	<td style="text-align:center">0.34</td>
	<td style="text-align:center">0.32</td>
	<td style="text-align:center">0.31</td>
	<td style="text-align:center">0.37</td>
	<td style="text-align:center">0.31</td>
</tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">0.29</td>
	<td style="text-align:center">0.3</td>
	<td style="text-align:center">0.3</td>
	<td style="text-align:center">0.32</td>
	<td style="text-align:center">0.38</td>
	<td style="text-align:center">0.31</td>
</tr>
<tr>
	<td style="text-align:center">STDEV</td>
	<td style="text-align:center">0.01</td>
	<td style="text-align:center">0.03</td>
	<td style="text-align:center">0.02</td>
	<td style="text-align:center">0.01</td>
	<td style="text-align:center">0.02</td>
	<td style="text-align:center">0.02</td>
</tr>
</table>

<table style="text-align:center;font-size:10px" align="center">
    <tr>
        <th style="text-align:center"  colspan="21">DBP-YG-100K</th>
    </tr>
    <tr>
        <td colspan="2" rowspan="2"></td>
        <td style="text-align:center" colspan="3">V1</td>
        <td style="text-align:center" colspan="3">V2</td>
    </tr>
    <tr>
        <td style="text-align:center">MTransE</td>
        <td style="text-align:center">IPTransE</td>
        <td style="text-align:center">JAPE</td>
        <td style="text-align:center">MTransE</td>
        <td style="text-align:center">IPTransE</td>
        <td style="text-align:center">JAPE</td>
    </tr>
    <tr>
	<td style="text-align:center;valign:middle" rowspan=5>Hits@1</td>
	<td style="text-align:center">S1</td>
	<td style="text-align:center">19.96</td>
	<td style="text-align:center">20.05</td>
	<td style="text-align:center">18.36</td>
	<td style="text-align:center">22.43</td>
	<td style="text-align:center">25.66</td>
	<td style="text-align:center">23.76</td></tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">20.43</td>
	<td style="text-align:center">22.04</td>
	<td style="text-align:center">17.3</td>
	<td style="text-align:center">20.43</td>
	<td style="text-align:center">27.07</td>
	<td style="text-align:center">27.19</td></tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">17.85</td>
	<td style="text-align:center">18.93</td>
	<td style="text-align:center">18.22</td>
	<td style="text-align:center">22.68</td>
	<td style="text-align:center">25.69</td>
	<td style="text-align:center">24.69</td></tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">19.41</td>
	<td style="text-align:center">20.34</td>
	<td style="text-align:center">17.96</td>
	<td style="text-align:center">21.85</td>
	<td style="text-align:center">26.14</td>
	<td style="text-align:center">25.21</td></tr>
<tr>
	<td style="text-align:center">STDEV</td>
	<td style="text-align:center">1.37</td>
	<td style="text-align:center">1.58</td>
	<td style="text-align:center">0.58</td>
	<td style="text-align:center">1.23</td>
	<td style="text-align:center">0.81</td>
	<td style="text-align:center">1.77</td></tr>
    
<tr>
	<td style="text-align:center;valign:middle" rowspan=5>Hits@10</td>
	<td style="text-align:center">S1</td>
	<td style="text-align:center">45.31</td>
	<td style="text-align:center">44.24</td>
	<td style="text-align:center">42.5</td>
	<td style="text-align:center">45.42</td>
	<td style="text-align:center">50.19</td>
	<td style="text-align:center">48.01</td></tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">43.51</td>
	<td style="text-align:center">45.64</td>
	<td style="text-align:center">39.92</td>
	<td style="text-align:center">43.51</td>
	<td style="text-align:center">52.11</td>
	<td style="text-align:center">52.09</td></tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">40.07</td>
	<td style="text-align:center">41.48</td>
	<td style="text-align:center">40.99</td>
	<td style="text-align:center">46.09</td>
	<td style="text-align:center">50.87</td>
	<td style="text-align:center">49.41</td></tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">42.96</td>
	<td style="text-align:center">43.79</td>
	<td style="text-align:center">41.14</td>
	<td style="text-align:center">45.01</td>
	<td style="text-align:center">51.06</td>
	<td style="text-align:center">49.84</td></tr>
<tr>
	<td style="text-align:center">STDEV</td>
	<td style="text-align:center">2.66</td>
	<td style="text-align:center">2.12</td>
	<td style="text-align:center">1.3</td>
	<td style="text-align:center">1.34</td>
	<td style="text-align:center">0.97</td>
	<td style="text-align:center">2.07</td></tr>   
	
<tr>
	<td style="text-align:center;valign:middle" rowspan=5>MR</td>
	<td style="text-align:center">S1</td>
	<td style="text-align:center">750.2</td>
	<td style="text-align:center">488.05</td>
	<td style="text-align:center">580.95</td>
	<td style="text-align:center">581.65</td>
	<td style="text-align:center">228.87</td>
	<td style="text-align:center">224.63</td></tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">931.2</td>
	<td style="text-align:center">440.13</td>
	<td style="text-align:center">589.61</td>
	<td style="text-align:center">931.2</td>
	<td style="text-align:center">169.06</td>
	<td style="text-align:center">207.39</td></tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">839.28</td>
	<td style="text-align:center">514.45</td>
	<td style="text-align:center">639.12</td>
	<td style="text-align:center">417.02</td>
	<td style="text-align:center">185.29</td>
	<td style="text-align:center">232.47</td></tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">840.22</td>
	<td style="text-align:center">480.88</td>
	<td style="text-align:center">603.23</td>
	<td style="text-align:center">643.29</td>
	<td style="text-align:center">194.41</td>
	<td style="text-align:center">221.5</td></tr>
<tr>
	<td style="text-align:center">STDEV</td>
	<td style="text-align:center">90.5</td>
	<td style="text-align:center">37.68</td>
	<td style="text-align:center">31.38</td>
	<td style="text-align:center">262.57</td>
	<td style="text-align:center">30.93</td>
	<td style="text-align:center">12.83</td></tr>
<tr>
	<td style="text-align:center;valign:middle" rowspan=5>MRR</td>
	<td style="text-align:center">S1</td>
	<td style="text-align:center">0.29</td>
	<td style="text-align:center">0.28</td>
	<td style="text-align:center">0.27</td>
	<td style="text-align:center">0.3</td>
	<td style="text-align:center">0.34</td>
	<td style="text-align:center">0.32</td></tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">0.28</td>
	<td style="text-align:center">0.3</td>
	<td style="text-align:center">0.25</td>
	<td style="text-align:center">0.28</td>
	<td style="text-align:center">0.36</td>
	<td style="text-align:center">0.36</td></tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">0.25</td>
	<td style="text-align:center">0.27</td>
	<td style="text-align:center">0.26</td>
	<td style="text-align:center">0.31</td>
	<td style="text-align:center">0.34</td>
	<td style="text-align:center">0.33</td></tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">0.27</td>
	<td style="text-align:center">0.28</td>
	<td style="text-align:center">0.26</td>
	<td style="text-align:center">0.3</td>
	<td style="text-align:center">0.35</td>
	<td style="text-align:center">0.34</td></tr>
<tr>
	<td style="text-align:center">STDEV</td>
	<td style="text-align:center">0.02</td>
	<td style="text-align:center">0.02</td>
	<td style="text-align:center">0.01</td>
	<td style="text-align:center">0.01</td>
	<td style="text-align:center">0.01</td>
	<td style="text-align:center">0.02</td></tr>
</table>

<table style="text-align:center;font-size:10px" align="center">
    <tr>
        <th style="text-align:center"  colspan="21">DBP(en-fr)-100K-V1</th>
    </tr>
    <tr>
	<td colspan="2"></td>
        <td style="text-align:center">MTransE</td>
        <td style="text-align:center">IPTransE</td>
        <td style="text-align:center">JAPE</td>
        <td style="text-align:center">MTransE</td>
        <td style="text-align:center">IPTransE</td>
        <td style="text-align:center">JAPE</td>
    </tr>
    <tr>
	<td style="text-align:center;valign:middle" rowspan=5>Hits@1</td>
    	<td style="text-align:center">S1</td>
	<td style="text-align:center">21.77</td>
	<td style="text-align:center">25.68</td>
	<td style="text-align:center">23.95</td></tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">22.57</td>
	<td style="text-align:center">25.93</td>
	<td style="text-align:center">24.06</td></tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">22.77</td>
	<td style="text-align:center">25.78</td>
	<td style="text-align:center">24.23</td></tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">22.37</td>
	<td style="text-align:center">25.8</td>
	<td style="text-align:center">24.08</td></tr>
<tr>
	<td style="text-align:center">STDEV</td>
	<td style="text-align:center">0.53</td>
	<td style="text-align:center">0.13</td>
	<td style="text-align:center">0.14</td></tr>
<tr>
	<td style="text-align:center;valign:middle" rowspan=5>Hits@10</td>
	<td style="text-align:center">S1</td>
	<td style="text-align:center">42.72</td>
	<td style="text-align:center">49.74</td>
	<td style="text-align:center">46.03</td></tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">43.83</td>
	<td style="text-align:center">50.36</td>
	<td style="text-align:center">46.21</td></tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">44.48</td>
	<td style="text-align:center">50.17</td>
	<td style="text-align:center">46.09</td></tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">43.68</td>
	<td style="text-align:center">50.09</td>
	<td style="text-align:center">46.11</td></tr>
<tr>
	<td style="text-align:center">STDEV</td>
	<td style="text-align:center">0.89</td>
	<td style="text-align:center">0.32</td>
	<td style="text-align:center">0.09</td></tr>
<tr>
	<td style="text-align:center;valign:middle" rowspan=5>MR</td>
	<td style="text-align:center">S1</td>
	<td style="text-align:center">786.23</td>
	<td style="text-align:center">458.14</td>
	<td style="text-align:center">517.07</td></tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">690.31</td>
	<td style="text-align:center">495.25</td>
	<td style="text-align:center">506.02</td></tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">707.15</td>
	<td style="text-align:center">483.05</td>
	<td style="text-align:center">509.85</td></tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">727.89</td>
	<td style="text-align:center">478.81</td>
	<td style="text-align:center">510.98</td></tr>
<tr>
	<td style="text-align:center">STDEV</td>
	<td style="text-align:center">51.22</td>
	<td style="text-align:center">18.91</td>
	<td style="text-align:center">5.61</td></tr>
<tr>
	<td style="text-align:center;valign:middle" rowspan=5>MRR</td>
	td style="text-align:center">S1</td>
	<td style="text-align:center">0.289</td>
	<td style="text-align:center">0.339</td>
	<td style="text-align:center">0.315</td></tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">0.299</td>
	<td style="text-align:center">0.34</td>
	<td style="text-align:center">0.32</td></tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">0.302</td>
	<td style="text-align:center">0.341</td>
	<td style="text-align:center">0.318</td></tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">0.3</td>
	<td style="text-align:center">0.34</td>
	<td style="text-align:center">0.32</td></tr>
<tr>
	<td style="text-align:center">STDEV</td>
	<td style="text-align:center">0.01</td>
	<td style="text-align:center">0</td>
	<td style="text-align:center">0</td></tr>
</table>

<table style="text-align:center;font-size:10px" align="center">
    <tr>
        <th style="text-align:center"  colspan="21">DBP(en-de)-100K-V1</th>
    </tr>
    <tr>
	<td colspan="2"></td>
        <td style="text-align:center">MTransE</td>
        <td style="text-align:center">IPTransE</td>
        <td style="text-align:center">JAPE</td>
        <td style="text-align:center">MTransE</td>
        <td style="text-align:center">IPTransE</td>
        <td style="text-align:center">JAPE</td>
    </tr>
    <tr>
	<td style="text-align:center;valign:middle" rowspan=5>Hits@1</td>
	<td style="text-align:center">S1</td>
	<td style="text-align:center">20.28</td>
	<td style="text-align:center">22.07</td>
	<td style="text-align:center">22.06</td></tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">20.83</td>
	<td style="text-align:center">23.48</td>
	<td style="text-align:center">22.5</td></tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">20.48</td>
	<td style="text-align:center">22.95</td>
	<td style="text-align:center">22.76</td></tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">20.53</td>
	<td style="text-align:center">22.83</td>
	<td style="text-align:center">22.44</td></tr>
<tr>
	<td style="text-align:center">STDEV</td>
	<td style="text-align:center">0.28</td>
	<td style="text-align:center">0.71</td>
	<td style="text-align:center">0.35</td></tr>
<tr>
	<td style="text-align:center;valign:middle" rowspan=5>Hits@10</td>
	<td style="text-align:center">S1</td>
	<td style="text-align:center">40.48</td>
	<td style="text-align:center">42.96</td>
	<td style="text-align:center">43.43</td></tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">41.47</td>
	<td style="text-align:center">45.45</td>
	<td style="text-align:center">44.03</td></tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">40.92</td>
	<td style="text-align:center">45.56</td>
	<td style="text-align:center">44.36</td></tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">40.96</td>
	<td style="text-align:center">44.66</td>
	<td style="text-align:center">43.94</td></tr>
<tr>
	<td style="text-align:center">STDEV</td>
	<td style="text-align:center">0.5</td>
	<td style="text-align:center">1.47</td>
	<td style="text-align:center">0.47</td></tr>
<tr>
	<td style="text-align:center;valign:middle" rowspan=5>MR</td>
	<td style="text-align:center">S1</td>
	<td style="text-align:center">1911.12</td>
	<td style="text-align:center">1322.36</td>
	<td style="text-align:center">1188.68</td></tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">1838.08</td>
	<td style="text-align:center">1003.97</td>
	<td style="text-align:center">1171.12</td></tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">2024.47</td>
	<td style="text-align:center">962.2</td>
	<td style="text-align:center">1202.8</td></tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">1924.56</td>
	<td style="text-align:center">1096.18</td>
	<td style="text-align:center">1187.53</td></tr>
<tr>
	<td style="text-align:center">STDEV</td>
	<td style="text-align:center">93.92</td>
	<td style="text-align:center">196.99</td>
	<td style="text-align:center">15.87</td></tr>
<tr>
	<td style="text-align:center;valign:middle" rowspan=5>MRR</td>
	<td style="text-align:center">S1</td>
	<td style="text-align:center">0.272</td>
	<td style="text-align:center">0.292</td>
	<td style="text-align:center">0.293</td></tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">0.279</td>
	<td style="text-align:center">0.31</td>
	<td style="text-align:center">0.3</td></tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">0.275</td>
	<td style="text-align:center">0.306</td>
	<td style="text-align:center">0.302</td></tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">0.28</td>
	<td style="text-align:center">0.3</td>
	<td style="text-align:center">0.3</td></tr>
<tr>
	<td style="text-align:center">STDEV</td>
	<td style="text-align:center">0</td>
	<td style="text-align:center">0.01</td>
	<td style="text-align:center">0</td></tr>
</table>

### Code

Folder "code" contains two subfolders: 
* "comparative_method" contains the code of all comparative methods.
* "data_handler" contains the code of our degree-based sampling method.

#### Dependencies
* Python 3
* Tensorflow
* Scipy
* Numpy
* sklearn

### Experimental Results
The file results.xlsx contains our detailed experimental results. 
Folder "figure" contains some figures about our experimental results.

> If you have any difficulty or question about our datasets, source code or reproducing expriment results, please email to qhzhang.nju@gmail.com, zqsun.nju@gmail.com or whu@nju.edu.cn.


