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
        <th style="text-align:center" colspan=21>DBP-WD-V1</th>
    </tr>
    <tr>
        <td style="text-align:center" rowspan=2></td>
        <td style="text-align:center" colspan=5>Hits@1</td>
        <td style="text-align:center" colspan=5>Hits@10</td>
        <td style="text-align:center" colspan=5>MR</td>
        <td style="text-align:center" colspan=5>MRR</td>
    </tr>
    <tr>
        <td style="text-align:center">S1</td>
        <td style="text-align:center">S2</td>
        <td style="text-align:center">S3</td>
        <td style="text-align:center">AVG</td>
        <td style="text-align:center">STDEV</td>
        <td style="text-align:center">S1</td>
        <td style="text-align:center">S2</td>
        <td style="text-align:center">S3</td>
        <td style="text-align:center">AVG</td>
        <td style="text-align:center">STDEV</td>
        <td style="text-align:center">S1</td>
        <td style="text-align:center">S2</td>
        <td style="text-align:center">S3</td>
        <td style="text-align:center">AVG</td>
        <td style="text-align:center">STDEV</td>
        <td style="text-align:center">S1</td>
        <td style="text-align:center">S2</td>
        <td style="text-align:center">S3</td>
        <td style="text-align:center">AVG</td>
        <td style="text-align:center">STDEV</td>
    </tr>
    <tr>
        <td style="text-align:center">MTransE</td>
        <td style="text-align:center">22.05</td>
        <td style="text-align:center">20.94</td>
        <td style="text-align:center">23.24</td>
        <td style="text-align:center">22.08</td>
        <td style="text-align:center">1.15</td>
        <td style="text-align:center">41.38</td>
        <td style="text-align:center">40.31</td>
        <td style="text-align:center">44.14</td>
        <td style="text-align:center">41.94</td>
        <td style="text-align:center">1.98</td>
        <td style="text-align:center">1111.74</td>
        <td style="text-align:center">1041.40</td>
        <td style="text-align:center"></td>
        <td style="text-align:center"></td>
        <td style="text-align:center"></td>
        <td style="text-align:center"></td>
        <td style="text-align:center"></td>
        <td style="text-align:center"></td>
        <td style="text-align:center"></td>
        <td style="text-align:center"></td>
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


