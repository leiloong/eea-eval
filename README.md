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
	<td style="text-align:center">358</td>
	<td style="text-align:center">216</td>
	<td style="text-align:center">333</td>
	<td style="text-align:center">221</td></tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">364</td>
	<td style="text-align:center">211</td>
	<td style="text-align:center">333</td>
	<td style="text-align:center">226</td></tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">368</td>
	<td style="text-align:center">217</td>
	<td style="text-align:center">347</td>
	<td style="text-align:center">221</td></tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">363</td>
	<td style="text-align:center">215</td>
	<td style="text-align:center">338</td>
	<td style="text-align:center">223</td></tr>
<tr>
	<td style="text-align:center;valign:middle" rowspan=4>Attributes</td>
	
<tr>
	<td style="text-align:center;valign:middle" rowspan=4>Rel. triples</td>
	
<tr>
	<td style="text-align:center;valign:middle" rowspan=4>Attr. triples</td>
	
</table>

<table style="text-align:center;font-size:10px" align="center">
    <tr>
        <th style="text-align:center"  colspan="21">DBP-YG-100K</th>
    </tr>
    <tr>
        <td colspan="2" rowspan="2"></td>
        <td style="text-align:center" colspan="2">V1</td>
        <td style="text-align:center" colspan="2">V2</td>
    </tr>
    <tr>
        <td style="text-align:center">DBpedia</td>
        <td style="text-align:center">YAGO</td>
        <td style="text-align:center">DBpedia</td>
        <td style="text-align:center">YAGO</td>
    </tr>
    <tr>
	<td style="text-align:center;valign:middle" rowspan=4>Relationships</td>
	<td style="text-align:center">S1</td>
	<td style="text-align:center">326</td>
	<td style="text-align:center">30</td>
	<td style="text-align:center">311</td>
	<td style="text-align:center">31</td></tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">358</td>
	<td style="text-align:center">31</td>
	<td style="text-align:center">320</td>
	<td style="text-align:center">31</td></tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">337</td>
	<td style="text-align:center">30</td>
	<td style="text-align:center">303</td>
	<td style="text-align:center">31</td></tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">340</td>
	<td style="text-align:center">30</td>
	<td style="text-align:center">311</td>
	<td style="text-align:center">31</td></tr>
<tr>
	<td style="text-align:center;valign:middle" rowspan=4>Attributes</td>
	
<tr>
	<td style="text-align:center;valign:middle" rowspan=4>Rel. triples</td>
	
<tr>
	<td style="text-align:center;valign:middle" rowspan=4>Attr. triples</td>
	
</table>

<table style="text-align:center;font-size:10px" align="center">
    <tr>
        <td colspan="2" rowspan="2"></td>
        <th style="text-align:center" colspan="2">DBP(en_fr)-100K-V1</th>
        <th style="text-align:center" colspan="2">DBP(en_fr)-100K-V1</th>
    </tr>
    <tr>
        <td style="text-align:center">en</td>
        <td style="text-align:center">fr</td>
        <td style="text-align:center">en</td>
        <td style="text-align:center">de</td>
    </tr>
    <tr>
	<td style="text-align:center;valign:middle" rowspan=4>Relationships</td>
	<td style="text-align:center">S1</td>
	<td style="text-align:center">329</td>
	<td style="text-align:center">257</td>
	<td style="text-align:center">305</td>
	<td style="text-align:center">163</td></tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">331</td>
	<td style="text-align:center">254</td>
	<td style="text-align:center">310</td>
	<td style="text-align:center">167</td></tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">331</td>
	<td style="text-align:center">256</td>
	<td style="text-align:center">305</td>
	<td style="text-align:center">169</td></tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">330</td>
	<td style="text-align:center">256</td>
	<td style="text-align:center">307</td>
	<td style="text-align:center">166</td></tr>
<tr>
	<td style="text-align:center;valign:middle" rowspan=4>Attributes</td>
	
<tr>
	<td style="text-align:center;valign:middle" rowspan=4>Rel. triples</td>
	
<tr>
	<td style="text-align:center;valign:middle" rowspan=4>Attr. triples</td>
	
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


