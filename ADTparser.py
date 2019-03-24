"""
Parses dpf file in search for certain data
"""
# Data required: filename, date, ligandname, Estimated Free Energy of Binding, Number of non-hydrogen atoms in ligand, RMSD TABLE
import re
import pandas as pd



def parse(filename):
    #Patterns for parsing dlg files
    free_energy_pattern=re.compile(r"DOCKED: USER    Estimated Free Energy of Binding")
    model_pattern=re.compile(r"DOCKED: MODEL")
    ligand_file_pattern=re.compile(r"Ligand PDBQT file = ")
    creation_date_pattern=re.compile(r"This file was created at")
    macromolecule_pattern=re.compile(r"Macromolecule file used to create Grid Maps =")
    nonhydrogen_count_pattern=re.compile(r"Number of non-hydrogen atoms in ligand:")
    ranking_pattern=re.compile(r'RANKING')
    dpf_greater_than_pop_size_pattern=re.compile(r"DPF> ga_pop_size")
    dpf_greater_than_num_evals_pattern = re.compile(r"DPF> ga_num_evals")

    #Tables for data storage
    energy_values = []
    runs = []
    ligands = []
    datetime = []
    protname = []
    ligeff = []
    rawrmsdt = []
    pop_size = []
    eval_num = []

    with open(filename,'rt') as in_file:
        for line in in_file:
            if dpf_greater_than_num_evals_pattern.search(line) != None:
                eval=re.findall(r"\b\d+\b",line)
                eval=list(map(int,eval))
                eval_num.append(eval)
            if dpf_greater_than_pop_size_pattern.search(line) != None:
                pop=re.findall(r"\b\d+\b",line)
                pop=list(map(int,pop))
                pop_size.append(pop)
            if ranking_pattern.search(line) != None:
                rawrmsd=re.findall(r"\s*(-?[\d+\.]+)",line)
                rawrmsd=list(map(float,rawrmsd))
                rawrmsdt.append(rawrmsd)
            if nonhydrogen_count_pattern.search(line) != None:
                hbonds=re.findall(r"\b\d+\b",line)
                hbonds=int(hbonds[0])
            if macromolecule_pattern.search(line) != None:
                protein=re.findall(r"\=\s(.*)\.pdbqt", line)
                protname.append(protein)
            if creation_date_pattern.search(line) != None:
                date=re.findall(r"\,\s(.*)", line)
                datetime.append(date)
            if ligand_file_pattern.search(line) != None:
                ligand=re.findall(r"\"(.*)\.pdbqt\"", line)
                ligands.append(ligand)
            if model_pattern.search(line) != None:
                run = re.findall(r"\b\d+\b",line)
                runs.append(run)
            if free_energy_pattern.search(line) != None:
                energy = re.findall(r"=\s*(-?[\d+\.]+)", line)
                energy=list(map(float, energy))
                energy_values.append(energy)
    # RMSD table tidying
    if len(rawrmsdt) != 0:
        rawrmsdt=pd.DataFrame(rawrmsdt)
        # Naming columns for further processing in pandas module
        rawrmsdt.columns=['A','B','C','D','Cluster RMSD','Reference RMSD']
        df_run=rawrmsdt['C']
        df_be=rawrmsdt['D']
        # Naming the ones that are needed
        df_cr=rawrmsdt['Cluster RMSD']
        df_rr=rawrmsdt['Reference RMSD']
        # Merging data and processing
        calcdf=pd.concat([df_run,df_be,df_cr,df_rr], axis=1)
        calcdf=calcdf.sort_values(by=['C'])
        clusterdf = calcdf['Cluster RMSD']
        referencedf = calcdf['Reference RMSD']
    else:
        clusterdf=[0]
        clusterdf=pd.DataFrame(clusterdf)
        referencedf=[0]
        referencedf=pd.DataFrame(referencedf)
    #Data conversion into DataFrame
    energy_values=pd.DataFrame(energy_values)
    runs=pd.DataFrame(runs)
    ligands=pd.DataFrame(ligands)
    datetime=pd.DataFrame(datetime)
    protname=pd.DataFrame(protname)
    pop_size=pd.DataFrame(pop_size)
    eval_num=pd.DataFrame(eval_num)
    eval_num = pd.DataFrame(eval_num/1000)
    # Ligand efficiency calculation
    ligeff=pd.DataFrame(round(energy_values/hbonds,3))
    # Data prep for export
    data=pd.concat([datetime,protname,runs,energy_values,ligeff,ligands,clusterdf,referencedf,pop_size,eval_num], axis=1)
    # Filling missing columns
    data.fillna(method='ffill', inplace=True)
    data.columns=['Date','Protein','Run','Energy','Ligand eff','Ligand','Cluster_RMSD','Reference_RMSD','Pop_size','eval_num[k]']
    return data

