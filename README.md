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
...

### Code

The code folder contains two subfolders: 
* "comparative_method" contains the code of all comparative methods.
* "data_sampling" contains the code of our degree-based sampling method.

#### Dependencies
* Python 3
* Tensorflow
* Scipy
* Numpy
* sklearn

### Experimental Results
The file results.xlsx contains our detailed experimental results.

> If you have any difficulty or question in running code and reproducing expriment results, please email to zqsun.nju@gmail.com and whu@nju.edu.cn.
