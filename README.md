## DVC DL TF

## Commands

## Create & activate the Environment
```bash
conda create --prefix ./env python=3.7 -y
conda activate ./env
```

## Initialize the Git
```bash
git init
dvc init
```

## Add Files 
```bash
touch requirements.txt setup.py .gitignore dvc.yaml params.yaml
```

## Add Directory
```bash
mkdir -p config/config.yaml
mkdir -p src/utils/all_utils.py
touch  src/stage_01_load_save_data.py
```