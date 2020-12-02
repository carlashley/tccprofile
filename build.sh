#!/bin/zsh

# Constants
ROOT=$(/usr/bin/cd "."; /bin/pwd)
PYTHON_PKG_SRC_DIR=${ROOT}/src
VERS_FILE=${PYTHON_PKG_SRC_DIR}/tcclib/vers.py
VERSION=$(/usr/bin/awk -F ' ' '/^VER = / {print $NF}' ${VERS_FILE})

TCCPROFILE_ZIP_FILE=${ROOT}/tccprofile
TCCPROFILE_PKG_ROOT=${PKG_ROOT}

PYTHON_SHEBANG=/usr/local/bin/python3

TPM_DIR=${ROOT}/src/tcclib/tpm

# Clean
/bin/rm ${TCCPROFILE_ZIP_FILE} &> /dev/null

if [ $? -eq 0 ]; then
    echo "Cleaned up prior builds..."
fi

/bin/rm -rf ${TPM_DIR}

if [ $? -eq 0 ]; then
    echo "Cleaned up third party packages..."
fi

# Install PyYAML for portability
/usr/local/bin/pip3 install --target=${TPM_DIR} pyyaml

# To provide your own python path, just add '/path/to/python' after './build'
# For example: ./build.sh /usr/bin/env python3.7
# or           ./build.sh /usr/local/munki/python
if [[ ! -z ${1} ]]; then
    PYTHON_SHEBANG=${1}
fi

# Build the zipapp version of the python package
/usr/local/bin/python3 -m zipapp "${PYTHON_PKG_SRC_DIR}" \
    --compress \
    --output "${TCCPROFILE_ZIP_FILE}" \
    --python="${PYTHON_SHEBANG}"

if [ $? -eq 0 ]; then
    echo "Built '${TCCPROFILE_ZIP_FILE}' version ${VERSION}..."
    /bin/chmod 755 ${TCCPROFILE_ZIP_FILE}
fi
