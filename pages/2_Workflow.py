
import streamlit as st
import subprocess
import threading

from src.common import *
from src.workflow import *



# Page name "workflow" will show mzML file selector in sidebar
params = page_setup(page="workflow")
st.title("Workflow")



# Define two widgets with values from paramter file
# To save them as parameters use the same key as in the json file

# We access the x-dimension via local variable
#xdimension = st.number_input(
#    label="x dimension", min_value=1, max_value=20, value=params["example-x-dimension"], step=1, key="example-x-dimension")

#st.number_input(label="y dimension", min_value=1, max_value=20,
#                value=params["example-y-dimension"], step=1, key="example-y-dimension")

#input_mzML_file = st.text_input(label="input mzML file", key="input-mzML-file")
#input_fasta_file = st.text_input(label="input FASTA file", key="input-fasta-file")
#output_file = st.text_input(label="output file", key="output-file")

cols = st.columns(5)

# TODO: Add selectbox for file inputs, instead of left border stuff
#params["selected-mzML-files"] = 
#params["selected-fasta-file"]

params["decoy-string"] = cols[0].text_input(label="Decoy identifier string", value=params["decoy-string"], key="decoy-string")
params["decoy-pos"] = cols[1].selectbox(label="Decoy string position", options=("prefix", "suffix"), index=0, key="decoy-pos")

params["precursor-tol"] = cols[2].number_input(label="precursor mass tolerance (ppm)", value=params["precursor-tol"], min_value=1., max_value=50., step=1., key="precursor-tol")
params["fragment-tol"] = cols[3].number_input(label="fragment mass tolerance (ppm)", value=params["fragment-tol"], min_value=1., max_value=200., step=1., key="fragment-tol")

enzymes = ('Trypsin', 'Chymotrypsin', 'Lys-C','Asp-N/B', 'Arg-C', 'Chymotrypsin/P', 'CNBr', 'TrypChymo', 'PepsinA', 'Trypsin/P', 'Formic_acid', 'Asp-N', 'Asp-N_ambic', 'Lys-N', 'Lys-C/P', 'V8-DE', 'Arg-C/P','V8-E', 'leukocyte elastase', 'proline endopeptidase', 'glutamylendopeptidase', 'Glu-C+P', 'unspecific cleavage', 'staphylococcalprotease/D', 'PepsinA + P', '2-iodobenzoate', 'Alpha-lytic protease', 'Clostripain/P', 'iodosobenzoate', 'no cleavage', 'elastase-trypsin-chymotrypsin', 'proline-endopeptidase/HKR', 'cyanogen-bromide')
params["enzyme"] = cols[4].selectbox(label="Digestion enzyme", index=0, options=enzymes, key="enzyme")

params["resA"] = cols[0].text_input(label="Cross-linkable residue 1 (comma separated list)", value=params["resA"], key="resA")
params["resB"] = cols[1].text_input(label="Cross-linkable residue 2 (comma separated list)", value=params["resB"], key="resB")
params["xl-mass"] = cols[2].number_input(label="Cross-linker mass", value=params["xl-mass"], min_value=0.0, max_value=9999., step=0.1, key="xl-mass")
params["xl-mono-masses"] = cols[3].text_input(label="Mono-link masses (comma separated list)", value=params["xl-mono-masses"], key="xl-mono-masses")
params["xl-name"] = cols[4].text_input(label="Cross-linker name", value=params["xl-name"], key="xl-name")

if st.button('Run OpenPepXLLF'):
    st.write('Running OpenPepXLLF...')
    for mzML_file in params["selected-mzML-files"]:
        run_OPXLLF(Path(st.session_state.workspace, "mzML-files", mzML_file+".mzML").__str__(), 
                        Path(st.session_state.workspace, "fasta-files", params["selected-fasta-file"][0]+".fasta").__str__(),
                        Path(st.session_state.workspace, "idXML-files", mzML_file+".idXML").__str__())
    st.write('Finished!')
else:
    st.write('Waiting')



# At the end of each page, always save parameters (including any changes via widgets with key)
save_params(params)



