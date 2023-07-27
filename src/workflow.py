import time

import numpy as np
import pandas as pd
import streamlit as st
import pyopenms as oms

@st.cache_data
def generate_random_table(x, y):
    """Example for a cached table"""
    df = pd.DataFrame(np.random.randn(x, y))
    time.sleep(2)
    return df


def run_example_filter(in_file, out_file):
    exp = oms.MSExperiment()
    oms.MzMLFile().load(in_file, exp)
    oms.NLargest().filterPeakMap(exp)
    oms.MzMLFile().store(out_file, exp)
    return
    
def run_OPXLLF(in_mzML, in_fasta, out_file):
    # load files
    exp = oms.MSExperiment()
    oms.MzMLFile().load(in_mzML, exp)
    fasta_DB = []
    oms.FASTAFile().load(in_fasta, fasta_DB)
    
    # prep empty containers, that are filled up by OPXL
    pep_ids = []
    prot_ids = []
    prot_ids.append(oms.ProteinIdentification())
    all_top_csms = []
    res_exp = oms.MSExperiment()
    
    # set parameters from UI fields
    opxlAlgo = oms.OpenPepXLLFAlgorithm()
    
    opxl_params = opxlAlgo.getParameters()
    opxl_params.setValue("threads", 4)
    opxl_params.setValue("decoy_string", st.session_state["decoy-string"])
    
    if (st.session_state["decoy-pos"] == "suffix"):
        opxl_params.setValue("decoy_prefix", "false")
        
    opxl_params.setValue("precursor:mass_tolerance", st.session_state["precursor-tol"])
    opxl_params.setValue("fragment:mass_tolerance", st.session_state["fragment-tol"])
    opxl_params.setValue("peptide:enzyme", st.session_state["enzyme"])
    opxl_params.setValue("cross_linker:residue1", st.session_state["resA"].split(","))
    opxl_params.setValue("cross_linker:residue2", st.session_state["resB"].split(","))
    opxl_params.setValue("cross_linker:mass", st.session_state["xl-mass"])
    
    mono_masses = []
    for mono_mass in st.session_state["xl-mono-masses"].split(","):
        mono_masses.append(float(mono_mass))
    opxl_params.setValue("cross_linker:mass_mono_link", mono_masses)
    
    opxl_params.setValue("cross_linker:name", st.session_state["xl-name"])
    
    opxlAlgo.setParameters(opxl_params)
    
    # run OpenPepXLLF
    opxlAlgo.run(exp, fasta_DB, prot_ids, pep_ids, all_top_csms, res_exp)
    
    # write idXML output
    oms.IdXMLFile().store(out_file, prot_ids, pep_ids);
    return