## Large Gephi file for testing

This is a gephi file in an old file format that networkX should be able to deal with (GEXF 1.2). 
It has been modified to meet some other networkX requirements: 
- All edges have been converted to undirected, because networkX does not support a mix of directed and undirected edges in one dataset.
- This line has been added (ln12):  ```<attribute id="n@nationality" title="nationality" type="string"/>``` to avoid another error


The original source of this file is here:

https://github.com/mbingenheimer/ChineseBuddhism_SNA

The resulting graph will be an undirected multigraph with
- 18130 Nodes
- 33976 Edges
