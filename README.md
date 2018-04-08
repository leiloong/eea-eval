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
        <td style="text-align:center" colspan="2">V1</td>
        <td style="text-align:center" colspan="2">V2</td>
    </tr>
    <tr>
        <td style="text-align:center">DBpedia</td>
        <td style="text-align:center">Wikidata</td>
        <td style="text-align:center">DBpedia</td>
        <td style="text-align:center">Wikidata</td>
    </tr>
    <tr>
	<td style="text-align:center;valign:middle" rowspan=4>Relationships</td>
	<td style="text-align:center">S1</td>
	<td style="text-align:center">22.05</td>
	<td style="text-align:center">21.84</td>
	<td style="text-align:center">22.67</td>
	<td style="text-align:center">25.4</td>
	</tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">20.94</td>
	<td style="text-align:center">22.12</td>
	<td style="text-align:center">20.88</td>
	<td style="text-align:center">24.33</td>
</tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">23.24</td>
	<td style="text-align:center">25.78</td>
	<td style="text-align:center">24.17</td>
	<td style="text-align:center">23.1</td>
</tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">22.08</td>
	<td style="text-align:center">23.25</td>
	<td style="text-align:center">22.57</td>
	<td style="text-align:center">24.28</td>
</tr>
    
<tr>
	<td style="text-align:center;valign:middle" rowspan=4>Attributes</td>
	<td style="text-align:center">S1</td>
	<td style="text-align:center">41.38</td>
	<td style="text-align:center">40.13</td>
	<td style="text-align:center">43.32</td>
	<td style="text-align:center">49.3</td>
</tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">40.31</td>
	<td style="text-align:center">42.52</td>
	<td style="text-align:center">40.92</td>
	<td style="text-align:center">46.15</td>
</tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">44.14</td>
	<td style="text-align:center">48.57</td>
	<td style="text-align:center">46.16</td>
	<td style="text-align:center">45.5</td>
</tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">41.94</td>
	<td style="text-align:center">43.74</td>
	<td style="text-align:center">43.47</td>
	<td style="text-align:center">46.98</td>
</tr>	
<tr>
	<td style="text-align:center;valign:middle" rowspan=4>Rel. triples</td>
	<td style="text-align:center">S1</td>
	<td style="text-align:center">1111.74</td>
	<td style="text-align:center">876.47</td>
	<td style="text-align:center">790.99</td>
	<td style="text-align:center">628.08</td>
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
</tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">1101.57</td>
	<td style="text-align:center">899.08</td>
	<td style="text-align:center">860.03</td>
	<td style="text-align:center">816.48</td>
</tr>
<tr>
	<td style="text-align:center;valign:middle" rowspan=4>Attr. triples</td>
	<td style="text-align:center">S1</td>
	<td style="text-align:center">0.29</td>
	<td style="text-align:center">0.28</td>
	<td style="text-align:center">0.3</td>
	<td style="text-align:center">0.34</td>
</tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">0.28</td>
	<td style="text-align:center">0.29</td>
	<td style="text-align:center">0.28</td>
	<td style="text-align:center">0.32</td>
</tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">0.31</td>
	<td style="text-align:center">0.34</td>
	<td style="text-align:center">0.32</td>
	<td style="text-align:center">0.31</td>
</tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">0.29</td>
	<td style="text-align:center">0.3</td>
	<td style="text-align:center">0.3</td>
	<td style="text-align:center">0.32</td>
</tr>
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


