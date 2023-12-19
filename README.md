# kiara examples

A repository containing example data and pipelines for kiara.

## Prepare environment

### Using pixi (recommended)

It's easiest to use [pixi](https://github.com/prefix-dev/pixi) to setup the environment. Check out [their install instructions](https://github.com/prefix-dev/pixi#installation), the following might or might not be out of date:

#### macOS and Linux
To install Pixi on macOS and Linux, open a terminal and run the following command:
```bash
curl -fsSL https://pixi.sh/install.sh | bash
# or with brew
brew install pixi
```
The script will also update your ~/.bash_profile to include ~/.pixi/bin in your PATH, allowing you to invoke the pixi command from anywhere.
You might need to restart your terminal or source your shell for the changes to take effect.

#### Windows
To install Pixi on Windows, open a PowerShell terminal (you may need to run it as an administrator) and run the following command:

```powershell
iwr -useb https://pixi.sh/install.ps1 | iex
```
The script will inform you once the installation is successful and add the ~/.pixi/bin directory to your PATH, which will allow you to run the pixi command from any location.

## Check-out examples repo

```
git clone https://github.com/DHARPA-Project/kiara.examples.git
cd kiara.examples
```
## Run `kiara` directly

If you want to run `kiara` directly (instead of using a `pixi` predefined task, you can use the full 
path to the `kiara` executable:

```
.pixi/env/bin/kiara --version
```

## Run pre-defined tasks via pixi

Pre-defined tasks can be run via the `pixi` command. 

### Predefined tasks

Check the `pixi.toml` file for the full list of tasks. The most important ones are listed below.

#### Run a kiara command

```
pixi run kiara <sub-command> <options>
```

#### Examples of `kiara` commands to run

##### Display kiara and kiara plugin versions

```
pixi run show-versions
```

##### Delete the current kiara context

```
pixi run delete-context
```

To delete all contexts, use:

```
pixi run delete-context -a
```

##### List all available operations

```
pixi run kiara operation list
```

##### Run a pipeline defined in a yaml file

This command runs the example pipeline ['`create_network_graph`'](./examples/pipelines/network_analysis/create_network_data.yaml), with some inputs that lives under `examples/data`:

```
pixi run kiara run examples/pipelines/network_analysis/create_network_data.yaml edges_file=examples/data/network_analysis/journals/JournalEdges1902.csv nodes_file=examples/data/network_analysis/journals/JournalNodes1902.csv
```

##### List all available renderers

```
pixi run kiara render list-renderers
```

##### Render a jupyter notebook from a registered pipeline

```
pixi run kiara render --source-type pipeline --target-type jupyter_notebook item logic.xor inputs='{"a": true, "b": true}' > xor.ipynb
pixi run jupyter lab xor.ipynb
```

##### Render a jupyter notebook from a pipeline file
```
pixi run kiara render --source-type pipeline --target-type jupyter_notebook item examples/pipelines/topic_modeling/topic_modeling.yaml inputs='{"text_corpus_folder_path": "examples/data/language_processing/text_corpus/data"}' > topic_modeling.ipynb
pixi run jupyter lab topic_modeling.ipynb
```

#### Run a streamlit app

Streamlit apps can be found under [`examples/streamlit`](https://github.com/DHARPA-Project/kiara.examples/tree/main/examples/streamlit). Use the path to the app you want to run as argument to:

```
pixi run streamlit examples/streamlit/<app_name>.py
```

#### Examples of streamlit apps to run

##### A streamlit version of the workshop getting started notebook
```
pixi run streamlit examples/streamlit/workshop.py
```

##### A development helper mini-app to display kiara operations and streamlit components

```
pixi run streamlit examples/streamlit/info/dev_helper.py
```

##### A proof-of-concept streamlit app to onboard network data

```
pixi run streamlit examples/streamlit/analyze_network_data.py
```

(this one might or might not make sense to you, as it's a proof-of-concept to demonstrate and help discussion around onboarding of complex data types like for example the 'network_data' one)

