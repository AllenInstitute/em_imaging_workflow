#!/bin/bash
SOURCE_ENV=/data/aibstemp/timf/example_data/blue_sky_27
DEST_ENV=/data/aibstemp/timf/example_data/blue_sky_27_copy
WORK_DIR=`pwd`

# see https://github.com/conda/conda/issues/1935
cd ${SOURCE_ENV}/..
source activate ${SOURCE_ENV_DIR}
cd ${WORK_DIR}

# The yml needs to be hand-edited to remove conda package
conda env export > source_conda_environment.yml

# other export options:
conda list --explicit > source_conda_requirements.txt
pip freeze > source_pip_freeze.txt

conda env create --prefix=${DEST_ENV} --file=source_conda_environment.yml
