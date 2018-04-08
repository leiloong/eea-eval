## Experimental analysis of knowledge graph embedding for entity alignment
> We developed a degree-based sampling method to generate 42 alignment-oriented datasets from real-world large-scale KGs, representing different heterogeneities of the original KGs. We selected three state-of-the-art embedding-based entity alignment methods for evaluation and comparison. Furthermore, we observed that multi-mapping relations and literal embedding are the two main obstacles for embedding-based entity alignment and some preliminary solutions were attempted. Specifically, we leveraged several enhanced KG embedding models to handle multi-mapping relations and used word2vec to incorporate literal similarities into embeddings. Our findings indicate that the performance of existing embedding-based methods is influenced by the characteristics of datasets and not all KG embedding models are suitable for entity alignment. Alignment-oriented KG embedding remains to be explored.

### Dataset
All datasets can be downloaded from [here](https://www.dropbox.com/s/jmkumdyv6etx4hn/iswc2018-dataset.7z?dl=0), in which three folders named "_1", "_2" and "_3" denote our three samples.

For each dataset, we have five files:
* ent_links: reference entity alignmet
* triples_1: relation triples of sampled entities in KG1
* triples_2: relation triples of sampled entities in KG2
* attr_triples_1: attribute triples of sampled entities in KG1
* attr_triples_2: attribute triples of sampled entities in KG2

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
	<td style="text-align:center;valign:middle" rowspan=4>Relations</td>
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
	<td style="text-align:center">S1</td>
	<td style="text-align:center">463</td>
	<td style="text-align:center">807</td>
	<td style="text-align:center">349</td>
	<td style="text-align:center">740</td></tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">486</td>
	<td style="text-align:center">791</td>
	<td style="text-align:center">390</td>
	<td style="text-align:center">731</td></tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">466</td>
	<td style="text-align:center">783</td>
	<td style="text-align:center">402</td>
	<td style="text-align:center">756</td></tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">472</td>
	<td style="text-align:center">794</td>
	<td style="text-align:center">380</td>
	<td style="text-align:center">742</td></tr>
<tr>
	<td style="text-align:center;valign:middle" rowspan=4>Rel. triples</td>
	<td style="text-align:center">S1</td>
	<td style="text-align:center">257,398</td>
	<td style="text-align:center">226,585</td>
	<td style="text-align:center">497,241</td>
	<td style="text-align:center">503,836</td></tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">259,100</td>
	<td style="text-align:center">224,863</td>
	<td style="text-align:center">493,865</td>
	<td style="text-align:center">484,209</td></tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">269,471</td>
	<td style="text-align:center">237,846</td>
	<td style="text-align:center">519,713</td>
	<td style="text-align:center">517,948</td></tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">261,990</td>
	<td style="text-align:center">229,765</td>
	<td style="text-align:center">503,606</td>
	<td style="text-align:center">501,998</td></tr>
<tr>
	<td style="text-align:center;valign:middle" rowspan=4>Attr. triples</td>
	<td style="text-align:center">S1</td>
	<td style="text-align:center">399,424</td>
	<td style="text-align:center">593,332</td>
	<td style="text-align:center">385,004</td>
	<td style="text-align:center">838,155</td></tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">398,373</td>
	<td style="text-align:center">587,581</td>
	<td style="text-align:center">397,852</td>
	<td style="text-align:center">830,654</td></tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">397,787</td>
	<td style="text-align:center">619,950</td>
	<td style="text-align:center">389,973</td>
	<td style="text-align:center">856,447</td></tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">398,528</td>
	<td style="text-align:center">600,288</td>
	<td style="text-align:center">390,943</td>
	<td style="text-align:center">841,752</td></tr>
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
	<td style="text-align:center;valign:middle" rowspan=4>Relations</td>
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
	<td style="text-align:center">S1</td>
	<td style="text-align:center">404</td>
	<td style="text-align:center">24</td>
	<td style="text-align:center">347</td>
	<td style="text-align:center">24</td></tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">415</td>
	<td style="text-align:center">24</td>
	<td style="text-align:center">335</td>
	<td style="text-align:center">23</td></tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">402</td>
	<td style="text-align:center">24</td>
	<td style="text-align:center">343</td>
	<td style="text-align:center">23</td></tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">407</td>
	<td style="text-align:center">24</td>
	<td style="text-align:center">342</td>
	<td style="text-align:center">23</td></tr>
<tr>
	<td style="text-align:center;valign:middle" rowspan=4>Rel. triples</td>
	<td style="text-align:center">S1</td>
	<td style="text-align:center">261,038</td>
	<td style="text-align:center">277,779</td>
	<td style="text-align:center">457,197</td>
	<td style="text-align:center">535,106</td></tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">281,143</td>
	<td style="text-align:center">318,434</td>
	<td style="text-align:center">443,115</td>
	<td style="text-align:center">522,817</td></tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">280,904</td>
	<td style="text-align:center">313,147</td>
	<td style="text-align:center">457,888</td>
	<td style="text-align:center">529,100</td></tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">274,362</td>
	<td style="text-align:center">303,120</td>
	<td style="text-align:center">452,733</td>
	<td style="text-align:center">529,008</td></tr>
<tr>
	<td style="text-align:center;valign:middle" rowspan=4>Attr. triples</td>
	<td style="text-align:center">S1</td>
	<td style="text-align:center">425,648</td>
	<td style="text-align:center">141,936</td>
	<td style="text-align:center">442,973</td>
	<td style="text-align:center">108,338</td></tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">413,532</td>
	<td style="text-align:center">131,411</td>
	<td style="text-align:center">442,122</td>
	<td style="text-align:center">111,467</td></tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">420,947</td>
	<td style="text-align:center">136,464</td>
	<td style="text-align:center">448,000</td>
	<td style="text-align:center">105,639</td></tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">420,042</td>
	<td style="text-align:center">136,604</td>
	<td style="text-align:center">444,365</td>
	<td style="text-align:center">108,481</td></tr>
</table>

<table style="text-align:center;font-size:10px" align="center">
    <tr>
        <td colspan="2" rowspan="2"></td>
        <th style="text-align:center" colspan="2">DBP(en_fr)-100K-V1</th>
        <th style="text-align:center" colspan="2">DBP(en_de)-100K-V1</th>
    </tr>
    <tr>
        <td style="text-align:center">en</td>
        <td style="text-align:center">fr</td>
        <td style="text-align:center">en</td>
        <td style="text-align:center">de</td>
    </tr>
    <tr>
	<td style="text-align:center;valign:middle" rowspan=4>Relations</td>
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
	<td style="text-align:center">332</td>
	<td style="text-align:center">469</td>
        <td style="text-align:center">S1</td>
	<td style="text-align:center">360</td>
	<td style="text-align:center">494</td>
	</tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">331</td>
	<td style="text-align:center">478</td>
	<td style="text-align:center">361</td>
	<td style="text-align:center">494</td>
</tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">331</td>
	<td style="text-align:center">480</td>
	<td style="text-align:center">357</td>
	<td style="text-align:center">489</td>
</tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">221</td>
	<td style="text-align:center">476</td>
	<td style="text-align:center">359</td>
	<td style="text-align:center">492</td>
</tr>
<tr>
	<td style="text-align:center;valign:middle" rowspan=4>Rel. triples</td>
	<td style="text-align:center">S1</td>
	<td style="text-align:center">367,096</td>
	<td style="text-align:center">294,440</td>
	<td style="text-align:center">273,093</td>
	<td style="text-align:center">230,586</td></tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">367,190</td>
	<td style="text-align:center">294,378</td>
	<td style="text-align:center">274,256</td>
	<td style="text-align:center">232,439</td></tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">367,328</td>
	<td style="text-align:center">294,471</td>
	<td style="text-align:center">275,022</td>
	<td style="text-align:center">232,364</td></tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">367,205</td>
	<td style="text-align:center">294,430</td>
	<td style="text-align:center">274,124</td>
	<td style="text-align:center">231,796</td></tr>
<tr>
	<td style="text-align:center;valign:middle" rowspan=4>Attr. triples</td>
	<td style="text-align:center">S1</td>
	<td style="text-align:center">403,321</td>
	<td style="text-align:center">361,330</td>
	<td style="text-align:center">437,144</td>
	<td style="text-align:center">684,663</td>
</tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">402,443</td>
	<td style="text-align:center">361,648</td>
	<td style="text-align:center">436,472</td>
	<td style="text-align:center">685,318</td>
</tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">402,764</td>
	<td style="text-align:center">361,788</td>
        <td style="text-align:center">439,633</td>
	<td style="text-align:center">689,150</td>
</tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">402,843</td>
	<td style="text-align:center">361,589</td>
	<td style="text-align:center">437,750</td>
	<td style="text-align:center">686,377</td>
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


