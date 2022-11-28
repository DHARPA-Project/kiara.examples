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

::: {#2516fede .cell .code}
``` python
%env CONSOLE_WIDTH=140

from kiara.interfaces.python_api.workflow import Workflow
from kiara.utils.jupyter import graph_to_image
from kiara.utils.cli import terminal_print_model
```
:::

::: {#45953319 .cell .markdown}
# Creating the workflow object `<a class="anchor" id="create_workflow_obj">`{=html}`</a>`{=html} {#creating-the-workflow-object-}

As the first step we create a [`Workflow`](https://dharpa.org/kiara/latest/reference/kiara/interfaces/python_api/workflow/) object, which is a convenience class that manages workflow state, internal consistency and history for us:
:::

::: {#9b66f52b .cell .code}
``` python
doc = """Example topic-modeling end-to-end workflow."""
workflow = Workflow.create("topic_modeling", doc=doc, replace_existing_alias=True)
```
:::

::: {#e059e77c .cell .markdown}
# Assembling the workflow `<a class="anchor" id="assembly">`{=html}`</a>`{=html} {#assembling-the-workflow-}

The first step in the creation of our workflow is to create the individual steps from the available *kiara* modules.

A list of available modules and their aliases can be found here: TODO

## Creating the steps of the workflow `<a class="anchor" id="creating_steps">`{=html}`</a>`{=html} {#creating-the-steps-of-the-workflow-}
:::

::: {#2b2b2c9f .cell .code}
``` python
# Creating step: import_text_corpus
workflow.add_step(operation="import.file_bundle", step_id="import_text_corpus")
```
:::

::: {#e9393171 .cell .code}
``` python
# Creating step: create_stopwords_list
workflow.add_step(operation="create.stopwords_list", step_id="create_stopwords_list")
```
:::

::: {#82a2cd88 .cell .code}
``` python
# Creating step: create_text_corpus
step_create_text_corpus_config = {'constants': {}, 'defaults': {}, 'source_type': 'text_file_bundle', 'target_type': 'table', 'ignore_errors': False}
workflow.add_step(
    operation="create.table",
    module_config=step_create_text_corpus_config,
    step_id="create_text_corpus")
```
:::

::: {#bd431dfe .cell .code}
``` python
# Connecting input(s) of step 'create_text_corpus'
workflow.connect_fields("create_text_corpus.text_file_bundle", "import_text_corpus.file_bundle")
```
:::

::: {#a1be9445 .cell .code}
``` python
# Creating step: extract_texts_column
workflow.add_step(operation="table.cut_column", step_id="extract_texts_column")
```
:::

::: {#f9eff334 .cell .code}
``` python
# Connecting input(s) of step 'extract_texts_column'
workflow.connect_fields("extract_texts_column.table", "create_text_corpus.table")
```
:::

::: {#67bdf739 .cell .code}
``` python
# Creating step: extract_filename_column
workflow.add_step(operation="table.cut_column", step_id="extract_filename_column")
```
:::

::: {#321cd92c .cell .code}
``` python
# Connecting input(s) of step 'extract_filename_column'
workflow.connect_fields("extract_filename_column.table", "create_text_corpus.table")
```
:::

::: {#1062ce19 .cell .code}
``` python
# Creating step: create_date_array
workflow.add_step(operation="parse.date_array", step_id="create_date_array")
```
:::

::: {#a7b64660 .cell .code}
``` python
# Connecting input(s) of step 'create_date_array'
workflow.connect_fields("create_date_array.array", "extract_filename_column.array")
```
:::

::: {#94034477 .cell .code}
``` python
# Creating step: tokenize_content
workflow.add_step(operation="tokenize.texts_array", step_id="tokenize_content")
```
:::

::: {#50a94780 .cell .code}
``` python
# Connecting input(s) of step 'tokenize_content'
workflow.connect_fields("tokenize_content.texts_array", "extract_texts_column.array")
```
:::

::: {#cb9e922b .cell .code}
``` python
# Creating step: preprocess_corpus
workflow.add_step(operation="preprocess.tokens_array", step_id="preprocess_corpus")
```
:::

::: {#9d90f4b3 .cell .code}
``` python
# Connecting input(s) of step 'preprocess_corpus'
workflow.connect_fields("preprocess_corpus.tokens_array", "tokenize_content.tokens_array")
workflow.connect_fields("preprocess_corpus.remove_stopwords", "create_stopwords_list.stopwords_list")
```
:::

::: {#c89b5b0a .cell .code}
``` python
# Creating step: generate_lda
workflow.add_step(operation="generate.LDA.for.tokens_array", step_id="generate_lda")
```
:::

::: {#206e06c6 .cell .code}
``` python
# Connecting input(s) of step 'generate_lda'
workflow.connect_fields("generate_lda.tokens_array", "preprocess_corpus.tokens_array")
```
:::

::: {#e52f9dd8 .cell .markdown}
## Setting workflow input/output names (optional)

To make our workflow nicer to use, we can set aliases for its inputs and outputs.
:::

::: {#b30ffb28 .cell .code}
``` python
workflow.set_input_alias(input_field="extract_texts_column.column_name", alias="content_column_name")
workflow.set_input_alias(input_field="extract_filename_column.column_name", alias="filename_column_name")
workflow.set_input_alias(input_field="import_text_corpus.path", alias="text_corpus_folder_path")
workflow.set_input_alias(input_field="create_date_array.min_index", alias="date_parse_min")
workflow.set_input_alias(input_field="create_date_array.max_index", alias="date_parse_max")
workflow.set_input_alias(input_field="create_date_array.force_non_null", alias="date_force_non_null")
workflow.set_input_alias(input_field="create_date_array.remove_tokens", alias="date_remove_tokensl")
workflow.set_input_alias(input_field="tokenize_content.tokenize_by_word", alias="tokenize_by_word")
workflow.set_input_alias(input_field="generate_lda.num_topics_min", alias="num_topics_min")
workflow.set_input_alias(input_field="generate_lda.num_topics_max", alias="num_topics_max")
workflow.set_input_alias(input_field="generate_lda.compute_coherence", alias="compute_coherence")
workflow.set_input_alias(input_field="generate_lda.words_per_topic", alias="words_per_topic")
workflow.set_input_alias(input_field="create_stopwords_list.languages", alias="languages")
workflow.set_input_alias(input_field="create_stopwords_list.stopword_lists", alias="stopword_lists")
workflow.set_input_alias(input_field="preprocess_corpus.to_lowercase", alias="to_lowercase")
workflow.set_input_alias(input_field="preprocess_corpus.remove_alphanumeric", alias="remove_alphanumeric")
workflow.set_input_alias(input_field="preprocess_corpus.remove_non_alpha", alias="remove_non_alpha")
workflow.set_input_alias(input_field="preprocess_corpus.remove_all_numeric", alias="remove_all_numeric")
workflow.set_input_alias(input_field="preprocess_corpus.remove_short_tokens", alias="remove_short_tokens")
workflow.set_input_alias(input_field="preprocess_corpus.remove_stopwords", alias="remove_stopwords")


workflow.set_output_alias(output_field="import_text_corpus.file_bundle", alias="text_corpus_file_bundle")
workflow.set_output_alias(output_field="create_text_corpus.table", alias="text_corpus_table")
workflow.set_output_alias(output_field="extract_texts_column.array", alias="content_array")
workflow.set_output_alias(output_field="tokenize_content.tokens_array", alias="tokenized_corpus")
workflow.set_output_alias(output_field="preprocess_corpus.tokens_array", alias="preprocessed_corpus")
workflow.set_output_alias(output_field="generate_lda.topic_models", alias="topic_models")
workflow.set_output_alias(output_field="generate_lda.coherence_map", alias="coherence_map")
workflow.set_output_alias(output_field="generate_lda.coherence_table", alias="coherence_table")
workflow.set_output_alias(output_field="create_date_array.date_array", alias="date_array")
```
:::

::: {#41cf2333 .cell .markdown}
# Workflow information `<a class="anchor" id="pipeline_info">`{=html}`</a>`{=html} {#workflow-information-}

After our workflow is wired up, we look can look at its structure, and other properties.
:::

::: {#23c37789 .cell .markdown}
## Workflow status

A workflow consists of a series of \'states\', the most relevant is always the most recent one. We can investigate
that latest states details like so:
:::

::: {#dfb61aff .cell .code}
``` python
workflow.current_state
```
:::

::: {#daec93d7 .cell .markdown}
## Pipeline execution graph

Let\'s look at the current execution graph for the current workflow pipeline:
:::

::: {#6f7aeca9 .cell .code}
``` python
graph_to_image(workflow.pipeline.execution_graph)
```
:::

::: {#f9cd45fe .cell .markdown}
# Workflow inputs `<a class="anchor" id="pipeline_inputs">`{=html}`</a>`{=html} {#workflow-inputs-}

Once a workflow has an assembled pipeline, we can set it\'s inputs. We use the input field
names that we got from the result of the `workflow.current_state` call.
:::

::: {#20bad9b7 .cell .code}
``` python
workflow.set_input("text_corpus_folder_path", "/home/markus/projects/kiara/dev/kiara.examples/examples/pipelines/topic_modeling/../../data/text_corpus/data")
workflow.set_input("content_column_name", "content")
workflow.set_input("filename_column_name", "file_name")
workflow.set_input("date_force_non_null", None)
workflow.set_input("date_parse_min", 11)
workflow.set_input("date_parse_max", 21)
workflow.set_input("date_remove_tokensl", None)
workflow.set_input("tokenize_by_word", None)
workflow.set_input("languages", ['italian'])
workflow.set_input("stopword_lists", [])
workflow.set_input("to_lowercase", None)
workflow.set_input("remove_alphanumeric", None)
workflow.set_input("remove_non_alpha", None)
workflow.set_input("remove_all_numeric", None)
workflow.set_input("remove_short_tokens", None)
workflow.set_input("num_topics_min", 7)
workflow.set_input("num_topics_max", 9)
workflow.set_input("compute_coherence", True)
workflow.set_input("words_per_topic", None)


# process all workflow steps that can be processed
workflow.process_steps()

# print the current state, after we set our inputs
workflow.current_state
```
:::

::: {#44cad78e .cell .markdown}
# Workflow outputs `<a class="anchor" id="pipeline_outputs">`{=html}`</a>`{=html} {#workflow-outputs-}

To print the actual data of the workflows\' current outputs, we call the `current_output_values` property of the workflow object:
:::

::: {#968de9c6 .cell .code}
``` python
workflow.current_output_values
```
:::

::: {#1e80af5e .cell .markdown}
# Workflow snapshot `<a class="anchor" id="snapshot">`{=html}`</a>`{=html} {#workflow-snapshot-}

So far, our workflow only exists in memory. If we want to save it so we can have a look at it again at a later stage, we can snapshot the current state, which will save the current structure of the internal pipeline, as well as all inputs that are currently used. In addition, this will register the workflow under the alias we specified on top of this file when creating the `Workflow` object (in our case: `topic_modeling`).

If we would not not specify `save=True`, the structure of the pipeline and inputs would still be frozen and kept, but only in memory, and we\'d only be able to access it in our current session.
:::

::: {#c7f38904 .cell .code}
``` python
workflow.snapshot(save=True)
```
:::

::: {#0eb83f14 .cell .markdown}
Now, we can access our workflow in other environments, for example from the commandline:
:::

::: {#a601a5ce .cell .code}
``` python
! kiara workflow list
```
:::

::: {#c3c2c4e5 .cell .code}
``` python
! kiara workflow explain topic_modeling
```
:::