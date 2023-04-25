# ---
# jupyter:
#   jupytext:
#     cell_markers: region,endregion
#     formats: ipynb,.pct.py:percent,.lgt.py:light,.spx.py:sphinx,md,Rmd,.pandoc.md:pandoc
#     text_representation:
#       extension: .py
#       format_name: sphinx
#       format_version: '1.1'
#       jupytext_version: 1.14.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %env CONSOLE_WIDTH=140

from kiara.interfaces.python_api.workflow import Workflow
from kiara.utils.jupyter import graph_to_image
from kiara.utils.cli import terminal_print_model


"""
# Creating the workflow object <a class="anchor" id="create_workflow_obj"></a>

As the first step we create a [`Workflow`](https://dharpa.org/kiara/latest/reference/kiara/interfaces/python_api/workflow/) object, which is a convenience class that manages workflow state, internal consistency and history for us:
"""

doc = """Onboard network data"""
workflow = Workflow.create("create_network_graph", doc=doc, replace_existing_alias=True)

###############################################################################
# # Assembling the workflow <a class="anchor" id="assembly"></a>
#
# The first step in the creation of our workflow is to create the individual steps from the available *kiara* modules.
#
# A list of available modules and their aliases can be found here: TODO
#
# ## Creating the steps of the workflow <a class="anchor" id="creating_steps"></a>

# Creating step: import_edges_file
workflow.add_step(operation="import.file", step_id="import_edges_file")
""
# Creating step: import_nodes_file
workflow.add_step(operation="import.file", step_id="import_nodes_file")
""
# Creating step: create_edges_table
step_create_edges_table_config = {'constants': {}, 'defaults': {}, 'source_type': 'csv_file', 'target_type': 'table', 'ignore_errors': False}
workflow.add_step(
    operation="create.table",
    module_config=step_create_edges_table_config,
    step_id="create_edges_table")
""
# Connecting input(s) of step 'create_edges_table'
workflow.connect_fields("create_edges_table.csv_file", "import_edges_file.file")
""
# Creating step: create_nodes_table
step_create_nodes_table_config = {'constants': {}, 'defaults': {}, 'source_type': 'csv_file', 'target_type': 'table', 'ignore_errors': False}
workflow.add_step(
    operation="create.table",
    module_config=step_create_nodes_table_config,
    step_id="create_nodes_table")
""
# Connecting input(s) of step 'create_nodes_table'
workflow.connect_fields("create_nodes_table.csv_file", "import_nodes_file.file")
""
# Creating step: assemble_network_data
workflow.add_step(operation="create.network_data.from.tables", step_id="assemble_network_data")
""
# Connecting input(s) of step 'assemble_network_data'
workflow.connect_fields("assemble_network_data.edges", "create_edges_table.table")
workflow.connect_fields("assemble_network_data.nodes", "create_nodes_table.table")
###############################################################################
# ## Setting workflow input/output names (optional)
#
# To make our workflow nicer to use, we can set aliases for its inputs and outputs.
workflow.set_input_alias(input_field="import_edges_file.path", alias="edges_file")
workflow.set_input_alias(input_field="import_nodes_file.path", alias="nodes_file")
workflow.set_input_alias(input_field="assemble_network_data.source_column_name", alias="source_column_name")
workflow.set_input_alias(input_field="assemble_network_data.target_column_name", alias="target_column_name")
workflow.set_input_alias(input_field="assemble_network_data.edges_column_map", alias="edges_column_map")
workflow.set_input_alias(input_field="assemble_network_data.id_column_name", alias="id_column_name")
workflow.set_input_alias(input_field="assemble_network_data.label_column_name", alias="label_column_name")
workflow.set_input_alias(input_field="assemble_network_data.nodes_column_map", alias="nodes_column_map")


workflow.set_output_alias(output_field="assemble_network_data.network_data", alias="network_data")
###############################################################################
# # Workflow information <a class="anchor" id="pipeline_info"></a>
#
# After our workflow is wired up, we look can look at its structure, and other properties.

###############################################################################
#
# ## Workflow status
#
# A workflow consists of a series of 'states', the most relevant is always the most recent one. We can investigate
# that latest states details like so:

workflow.current_state

###############################################################################
# ## Pipeline execution graph
#
# Let's look at the current execution graph for the current workflow pipeline:

graph_to_image(workflow.pipeline.execution_graph)

###############################################################################
# # Workflow inputs <a class="anchor" id="pipeline_inputs"></a>
#
# Once a workflow has an assembled pipeline, we can set it's inputs. We use the input field
# names that we got from the result of the `workflow.current_state` call.

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

###############################################################################
# # Workflow outputs <a class="anchor" id="pipeline_outputs"></a>
#
# To print the actual data of the workflows' current outputs, we call the `current_output_values` property of the workflow object:

workflow.current_output_values

###############################################################################
# # Workflow snapshot <a class="anchor" id="snapshot"></a>
#
# So far, our workflow only exists in memory. If we want to save it so we can have a look at it again at a later stage, we can snapshot the current state, which will save the current structure of the internal pipeline, as well as all inputs that are currently used. In addition, this will register the workflow under the alias we specified on top of this file when creating the `Workflow` object (in our case: `create_network_graph`).
#
# If we would not not specify `save=True`, the structure of the pipeline and inputs would still be frozen and kept, but only in memory, and we'd only be able to access it in our current session.

workflow.snapshot(save=True)

###############################################################################
# Now, we can access our workflow in other environments, for example from the commandline:

# ! kiara workflow list

""
# ! kiara workflow explain create_network_graph