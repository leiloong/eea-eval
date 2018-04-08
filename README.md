## Experimental analysis of knowledge graph embedding for entity alignment
> We developed a degree-based sampling method to generate 42 alignment-oriented datasets from real-world large-scale KGs, representing different heterogeneities of the original KGs. We selected three state-of-the-art embedding-based entity alignment methods for evaluation and comparison. Furthermore, we observed that multi-mapping relations and literal embedding are the two main obstacles for embedding-based entity alignment and some preliminary solutions were attempted. Specifically, we leveraged several enhanced KG embedding models to handle multi-mapping relations and used word2vec to incorporate literal similarities into embeddings. Our findings indicate that the performance of existing embedding-based methods is influenced by the characteristics of datasets and not all KG embedding models are suitable for entity alignment. Alignment-oriented KG embedding remains to be explored.

### Dataset
Our datasets can be found [here](https://www.dropbox.com/s/jmkumdyv6etx4hn/iswc2018-dataset.7z?dl=0). It contains three folders namely "_1", "_2" and "_3", denoting our three samples.

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
	<td style="text-align:center">257398</td>
	<td style="text-align:center">226585</td>
	<td style="text-align:center">497241</td>
	<td style="text-align:center">503836</td></tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">259100</td>
	<td style="text-align:center">224863</td>
	<td style="text-align:center">493865</td>
	<td style="text-align:center">484209</td></tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">269471</td>
	<td style="text-align:center">237846</td>
	<td style="text-align:center">519713</td>
	<td style="text-align:center">517948</td></tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">261990</td>
	<td style="text-align:center">229765</td>
	<td style="text-align:center">503606</td>
	<td style="text-align:center">501998</td></tr>
<tr>
	<td style="text-align:center;valign:middle" rowspan=4>Attr. triples</td>
	<td style="text-align:center">S1</td>
	<td style="text-align:center">399424</td>
	<td style="text-align:center">593332</td>
	<td style="text-align:center">385004</td>
	<td style="text-align:center">838155</td></tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">398373</td>
	<td style="text-align:center">587581</td>
	<td style="text-align:center">397852</td>
	<td style="text-align:center">830654</td></tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">397787</td>
	<td style="text-align:center">619950</td>
	<td style="text-align:center">389973</td>
	<td style="text-align:center">856447</td></tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">398528</td>
	<td style="text-align:center">600288</td>
	<td style="text-align:center">390943</td>
	<td style="text-align:center">841752</td></tr>
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
	<td style="text-align:center">261038</td>
	<td style="text-align:center">277779</td>
	<td style="text-align:center">457197</td>
	<td style="text-align:center">535106</td></tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">281143</td>
	<td style="text-align:center">318434</td>
	<td style="text-align:center">443115</td>
	<td style="text-align:center">522817</td></tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">280904</td>
	<td style="text-align:center">313147</td>
	<td style="text-align:center">457888</td>
	<td style="text-align:center">529100</td></tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">274362</td>
	<td style="text-align:center">303120</td>
	<td style="text-align:center">452733</td>
	<td style="text-align:center">529008</td></tr>
<tr>
	<td style="text-align:center;valign:middle" rowspan=4>Attr. triples</td>
	<td style="text-align:center">S1</td>
	<td style="text-align:center">425648</td>
	<td style="text-align:center">141936</td>
	<td style="text-align:center">442973</td>
	<td style="text-align:center">108338</td></tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">413532</td>
	<td style="text-align:center">131411</td>
	<td style="text-align:center">442122</td>
	<td style="text-align:center">111467</td></tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">420947</td>
	<td style="text-align:center">136464</td>
	<td style="text-align:center">448000</td>
	<td style="text-align:center">105639</td></tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">420042</td>
	<td style="text-align:center">136604</td>
	<td style="text-align:center">444365</td>
	<td style="text-align:center">108481</td></tr>
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
	<td style="text-align:center">S1</td>
	<td style="text-align:center">360</td>
	<td style="text-align:center">494</td>
	<td style="text-align:center">332</td>
	<td style="text-align:center">469</td></tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">361</td>
	<td style="text-align:center">494</td>
	<td style="text-align:center">331</td>
	<td style="text-align:center">478</td></tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">357</td>
	<td style="text-align:center">489</td>
	<td style="text-align:center">0</td>
	<td style="text-align:center">480</td></tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">359</td>
	<td style="text-align:center">492</td>
	<td style="text-align:center">221</td>
	<td style="text-align:center">476</td></tr>
<tr>
	<td style="text-align:center;valign:middle" rowspan=4>Rel. triples</td>
	<td style="text-align:center">S1</td>
	<td style="text-align:center">367096</td>
	<td style="text-align:center">294440</td>
	<td style="text-align:center">273093</td>
	<td style="text-align:center">230586</td></tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">367190</td>
	<td style="text-align:center">294378</td>
	<td style="text-align:center">274256</td>
	<td style="text-align:center">232439</td></tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">367328</td>
	<td style="text-align:center">294471</td>
	<td style="text-align:center">275022</td>
	<td style="text-align:center">232364</td></tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">367205</td>
	<td style="text-align:center">294430</td>
	<td style="text-align:center">274124</td>
	<td style="text-align:center">231796</td></tr>
<tr>
	<td style="text-align:center;valign:middle" rowspan=4>Attr. triples</td>
	<td style="text-align:center">S1</td>
	<td style="text-align:center">445878</td>
	<td style="text-align:center">386557</td>
	<td style="text-align:center">403321</td>
	<td style="text-align:center">361330</td></tr>
<tr>
	<td style="text-align:center">S2</td>
	<td style="text-align:center">443409</td>
	<td style="text-align:center">381795</td>
	<td style="text-align:center">402443</td>
	<td style="text-align:center">361648</td></tr>
<tr>
	<td style="text-align:center">S3</td>
	<td style="text-align:center">444744</td>
	<td style="text-align:center">382894</td>
	<td style="text-align:center">402764</td>
	<td style="text-align:center">361788</td></tr>
<tr>
	<td style="text-align:center">AVG</td>
	<td style="text-align:center">444677</td>
	<td style="text-align:center">383749</td>
	<td style="text-align:center">402843</td>
	<td style="text-align:center">361589</td></tr>
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


