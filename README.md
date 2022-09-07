# kiara examples

A repository containing example data and pipelines for kiara.

## Prepare Python environment

### Using conda (recommended)

```
conda create -n kiara_examples python=3.9
conda activate kiara_examples
conda install -c conda-forge mamba   # this is optional, but makes everything install related much faster, if you don't use it, replace 'mamba' with 'conda' below
mamba install -c conda-forge -c dharpa kiara kiara_plugin.core_types kiara_plugin.tabular kiara_plugin.network_analysis kiara_plugin.language_processing
```

## Check-out examples repo

```
git clone https://github.com/DHARPA-Project/kiara.examples.git
cd kiara.examples
```

## Run included pipelines

Networking analysis examples:

```
# explain the create network pipeline
kiara operation explain examples/pipelines/network_analysis/create_network_graph.yaml

# display some internal pipeline details
kiara pipeline explain examples/pipelines/network_analysis/create_network_graph.yaml

# run the create network pipeline with the example data
kiara run examples/pipelines/network_analysis/create_network_graph.yaml

# run the create network pipeline with the example data and save the 'network_data' result field as alias 'journals_network' 
kiara run examples/pipelines/network_analysis/create_network_graph.yaml --save network_data=journals_network

# 'explain' the result network (basically display it's metadata)
kiara data explain -p alias:journals_network
```


Topic modeling examples:

```
# explain the topic modeling pipeline
kiara operation explain examples/pipelines/topic_modeling/topic_modeling.yaml

# print the execution graph
kiara pipeline execution-graph examples/pipelines/topic_modeling/topic_modeling.yaml

# run the topic modeling pipeline with the default example values
kiara run examples/pipelines/topic_modeling/topic_modeling.yaml

# run the topic modeling pipeline with the default example values and save all results (and intermediate results)
kiara run examples/pipelines/topic_modeling/topic_modeling.yaml --save tm

# run the topic modeling pipeline with some additional inputs to augment the defaults and save all results:
kiara run examples/pipelines/topic_modeling/topic_modeling.yaml compute_coherence=true num_topics_min=4 num_topics_max=6 --save tm_coherence

# 'load' the topic model data
kiara data load alias:tm_coherence.topic_models
```

