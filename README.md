# NTDisconn
Create Neurotransmitter Network Damage

This work is based on 
Population based Tractogram Xiao et al. 2023: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10474320/
Neurotransmitter Density maps Hansen et al. 2022: https://pubmed.ncbi.nlm.nih.gov/36303070/


1. Required repositories 
nibabel
scipy
dipy
antspyx
pandas

To create the Disconnectomes, currently the installation of mrtrix3 (https://www.mrtrix.org/) is required, this will be changed in the future.

2. Clone the repository

git clone https://github.com/phjkoch/NTDisconn.git
cd NTDisconn


3. Usage

python Create_NTDisconn.py --help
usage: Create_NTDisconn.py [-h] [--discStreamlines DISCSTREAMLINES]
                           [--Connectome CONNECTOME]
                           ID in_lesion output_dir

positional arguments:
  ID                    Subject ID
  in_lesion             Input individual Lesionmask in MNI152 (1mm iso)
  output_dir            Specify output directory

options:
  -h, --help            show this help message and exit
  --discStreamlines DISCSTREAMLINES
                        Create disconnected streamline output? [y|n]
  --Connectome CONNECTOME
                        Create Connectome output? [y|n]
 
4. Output
IN the output_dir a directory with the ID is created containing
1. A csv file with the estimated Neurotransmitter network damage of the individual lesion map for all the Neurotransmitter receptors and transporters from Hansen et al. 2022
2. A txt file with 2 Millionen entries indicating which streamlines of the HCP-aging tractogram is passing through the individual lesion mask [1] and which are sparsed [0] (optional)
3. A Disconnectome of the individual lesion for each Neurotransmitter receptor or transporter (optional)

5. Test_MNI_lesion.nii.gz
This is a test lesion when used correctly like: 
python Create_NT_Disconn.py Test Test_MNI_lesion.nii.gz output_test

Creates the individual Neurotransmitter network damage:


