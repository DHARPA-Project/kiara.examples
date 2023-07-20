# kiara examples

A repository containing example data and pipelines for kiara.

## Prepare environment

### Using pixi (recommended)

#### macOS and Linux
To install Pixi on macOS and Linux, open a terminal and run the following command:
```bash
curl -fsSL https://raw.githubusercontent.com/prefix-dev/pixi/main/install/install.sh | bash
# or with brew
brew install pixi
```
The script will also update your ~/.bash_profile to include ~/.pixi/bin in your PATH, allowing you to invoke the pixi command from anywhere.
You might need to restart your terminal or source your shell for the changes to take effect.

#### Windows
To install Pixi on Windows, open a PowerShell terminal (you may need to run it as an administrator) and run the following command:

```powershell
iwr -useb https://raw.githubusercontent.com/prefix-dev/pixi/main/install/install.ps1 | iex
```
The script will inform you once the installation is successful and add the ~/.pixi/bin directory to your PATH, which will allow you to run the pixi command from any location.

## Check-out examples repo

```
git clone https://github.com/DHARPA-Project/kiara.examples.git
cd kiara.examples
```

## Run tasks

Pre-defined tasks can be run via the `pixi` command. If you want to run `kiara` directly, you'll need to use the full 
path to it, something like:

```
.pixi/env/bin/kiara --version
```

### Predefined tasks

#### Display kiara and kiara plugin versions

```
pixi run show-version
```


#### Delete the current kiara context

```
pixi run delete-context
```

To delete all contexts, use:

```
pixi run delete-context -a
```

#### Run a kiara command

```
pixi run kiara <sub-command> <options>
```

For example, to run the example [`create_network_graph`](./examples/pipelines/network_analysis/create_network_data.yaml) pipeline, you can do:

```
pixi run kiara run examples/pipelines/network_analysis/create_network_data.yaml edges_file=examples/data/network_analysis/journals/JournalEdges1902.csv nodes_file=examples/data/network_analysis/journals/JournalNodes1902.csv
```

#### Run a streamlit app

Streamlit apps can be found under `examples/streamlit`. Use the path to the app you want to run as argument to:

```
pixi run streamlit examples/streamlit/<app_name>.py
```

For example:

```
pixi run streamlit examples/streamlit/analyze_network_data.py
```


