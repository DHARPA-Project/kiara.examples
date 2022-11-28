---
jupyter:
  jupytext:
    cell_markers: region,endregion
    formats: "ipynb,.pct.py:percent,.lgt.py:light,.spx.py:sphinx,md,Rmd,.pandoc.md:pandoc"
    text_representation:
      extension: .md
      format_name: pandoc
      format_version: 2.19.2
      jupytext_version: 1.14.1
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
  nbformat: 4
  nbformat_minor: 5
---

::: {#bcaefdc9 .cell .code}
``` python
%env CONSOLE_WIDTH=140

from kiara.interfaces.python_api.workflow import Workflow
from kiara.utils.jupyter import graph_to_image
from kiara.utils.cli import terminal_print_model
```
:::

::: {#20db7f5d .cell .markdown}
# Creating the workflow object `<a class="anchor" id="create_workflow_obj">`{=html}`</a>`{=html} {#creating-the-workflow-object-}

As the first step we create a [`Workflow`](https://dharpa.org/kiara/latest/reference/kiara/interfaces/python_api/workflow/) object, which is a convenience class that manages workflow state, internal consistency and history for us:
:::

::: {#00c618e1 .cell .code}
``` python
doc = """Onboard network data"""
workflow = Workflow.create("create_network_graph", doc=doc, replace_existing_alias=True)
```
:::

::: {#7f59e37d .cell .markdown}
# Assembling the workflow `<a class="anchor" id="assembly">`{=html}`</a>`{=html} {#assembling-the-workflow-}

The first step in the creation of our workflow is to create the individual steps from the available *kiara* modules.

A list of available modules and their aliases can be found here: TODO

## Creating the steps of the workflow `<a class="anchor" id="creating_steps">`{=html}`</a>`{=html} {#creating-the-steps-of-the-workflow-}
:::

::: {#1cb1fc64 .cell .code}
``` python
# Creating step: import_edges_file
workflow.add_step(operation="import.file", step_id="import_edges_file")
```
:::

::: {#54199b1c .cell .code}
``` python
# Creating step: import_nodes_file
workflow.add_step(operation="import.file", step_id="import_nodes_file")
```
:::

::: {#fcac77e1 .cell .code}
``` python
# Creating step: create_edges_table
step_create_edges_table_config = {'constants': {}, 'defaults': {}, 'source_type': 'csv_file', 'target_type': 'table', 'ignore_errors': False}
workflow.add_step(
    operation="create.table",
    module_config=step_create_edges_table_config,
    step_id="create_edges_table")
```
:::

::: {#4107fc62 .cell .code}
``` python
# Connecting input(s) of step 'create_edges_table'
workflow.connect_fields("create_edges_table.csv_file", "import_edges_file.file")
```
:::

::: {#84f98096 .cell .code}
``` python
# Creating step: create_nodes_table
step_create_nodes_table_config = {'constants': {}, 'defaults': {}, 'source_type': 'csv_file', 'target_type': 'table', 'ignore_errors': False}
workflow.add_step(
    operation="create.table",
    module_config=step_create_nodes_table_config,
    step_id="create_nodes_table")
```
:::

::: {#382bc081 .cell .code}
``` python
# Connecting input(s) of step 'create_nodes_table'
workflow.connect_fields("create_nodes_table.csv_file", "import_nodes_file.file")
```
:::

::: {#ba8b8aa5 .cell .code}
``` python
# Creating step: assemble_network_data
workflow.add_step(operation="create.network_data.from.tables", step_id="assemble_network_data")
```
:::

::: {#91a78860 .cell .code}
``` python
# Connecting input(s) of step 'assemble_network_data'
workflow.connect_fields("assemble_network_data.edges", "create_edges_table.table")
workflow.connect_fields("assemble_network_data.nodes", "create_nodes_table.table")
```
:::

::: {#28411083 .cell .markdown}
## Setting workflow input/output names (optional)

To make our workflow nicer to use, we can set aliases for its inputs and outputs.
:::

::: {#e140e8ea .cell .code}
``` python
workflow.set_input_alias(input_field="import_edges_file.path", alias="edges_file")
workflow.set_input_alias(input_field="import_nodes_file.path", alias="nodes_file")
workflow.set_input_alias(input_field="assemble_network_data.source_column_name", alias="source_column_name")
workflow.set_input_alias(input_field="assemble_network_data.target_column_name", alias="target_column_name")
workflow.set_input_alias(input_field="assemble_network_data.edges_column_map", alias="edges_column_map")
workflow.set_input_alias(input_field="assemble_network_data.id_column_name", alias="id_column_name")
workflow.set_input_alias(input_field="assemble_network_data.label_column_name", alias="label_column_name")
workflow.set_input_alias(input_field="assemble_network_data.nodes_column_map", alias="nodes_column_map")


workflow.set_output_alias(output_field="assemble_network_data.network_data", alias="network_data")
```
:::

::: {#17af77c7 .cell .markdown}
# Workflow information `<a class="anchor" id="pipeline_info">`{=html}`</a>`{=html} {#workflow-information-}

After our workflow is wired up, we look can look at its structure, and other properties.
:::

::: {#f61c3dc1 .cell .markdown}
## Workflow status

A workflow consists of a series of \'states\', the most relevant is always the most recent one. We can investigate
that latest states details like so:
:::

::: {#f91ef819 .cell .code}
``` python
workflow.current_state
```
:::

::: {#7c4d18ca .cell .markdown}
## Pipeline execution graph

Let\'s look at the current execution graph for the current workflow pipeline:
:::

::: {#11f29cf8 .cell .code}
``` python
graph_to_image(workflow.pipeline.execution_graph)
```
:::

::: {#f5493a9e .cell .markdown}
# Workflow inputs `<a class="anchor" id="pipeline_inputs">`{=html}`</a>`{=html} {#workflow-inputs-}

Once a workflow has an assembled pipeline, we can set it\'s inputs. We use the input field
names that we got from the result of the `workflow.current_state` call.
:::

::: {#575e76c8 .cell .code}
``` python
workflow.set_input("edges_file", "/home/markus/projects/kiara/dev/kiara.examples/examples/pipelines/network_analysis/../../data/journals/JournalEdges1902.csv")
workflow.set_input("nodes_file", "/home/markus/projects/kiara/dev/kiara.examples/examples/pipelines/network_analysis/../../data/journals/JournalNodes1902.csv")
workflow.set_input("source_column_name", "Source")
workflow.set_input("target_column_name", "Target")
workflow.set_input("edges_column_map", None)
workflow.set_input("id_column_name", "Id")
workflow.set_input("label_column_name", "Label")
workflow.set_input("nodes_column_map", None)


# process all workflow steps that can be processed
workflow.process_steps()

# print the current state, after we set our inputs
workflow.current_state
```
:::

::: {#d185fa68 .cell .markdown}
# Workflow outputs `<a class="anchor" id="pipeline_outputs">`{=html}`</a>`{=html} {#workflow-outputs-}

To print the actual data of the workflows\' current outputs, we call the `current_output_values` property of the workflow object:
:::

::: {#1771ad23 .cell .code}
``` python
workflow.current_output_values
```
:::

::: {#dfd51891 .cell .markdown}
# Workflow snapshot `<a class="anchor" id="snapshot">`{=html}`</a>`{=html} {#workflow-snapshot-}

So far, our workflow only exists in memory. If we want to save it so we can have a look at it again at a later stage, we can snapshot the current state, which will save the current structure of the internal pipeline, as well as all inputs that are currently used. In addition, this will register the workflow under the alias we specified on top of this file when creating the `Workflow` object (in our case: `create_network_graph`).

If we would not not specify `save=True`, the structure of the pipeline and inputs would still be frozen and kept, but only in memory, and we\'d only be able to access it in our current session.
:::

::: {#fd0c8385 .cell .code}
``` python
workflow.snapshot(save=True)
```
:::

::: {#15d0501f .cell .markdown}
Now, we can access our workflow in other environments, for example from the commandline:
:::

::: {#aa1f42dc .cell .code}
``` python
! kiara workflow list
```
:::

::: {#13ca06b5 .cell .code}
``` python
! kiara workflow explain create_network_graph
```
:::