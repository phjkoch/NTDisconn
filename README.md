# NTDisconn
Create Neurotransmitter Network Damage

This work is based on 
Population based Tractogram Xiao et al. 2023: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10474320/
Neurotransmitter Density maps Hansen et al. 2022: https://pubmed.ncbi.nlm.nih.gov/36303070/


1. Required repositories   
&nbsp;&nbsp;&nbsp;&nbsp;nibabel  
&nbsp;&nbsp;&nbsp;&nbsp;scipy  
&nbsp;&nbsp;&nbsp;&nbsp;dipy  
&nbsp;&nbsp;&nbsp;&nbsp;antspyx  
&nbsp;&nbsp;&nbsp;&nbsp;pandas  

2. Clone the repository
```bash
git clone https://github.com/phjkoch/NTDisconn.git
cd NTDisconn
```


3. Usage

```bash
python Create_NTDisconn.py --help
```
&nbsp;&nbsp;&nbsp;&nbsp;Usage:  
&nbsp;&nbsp;&nbsp;&nbsp;Create_NTDisconn.py [-h] [--discStreamlines DISCSTREAMLINES]
                       ID in_lesion output_dir

&nbsp;&nbsp;&nbsp;&nbsp;positional arguments:  
&nbsp;&nbsp;&nbsp;&nbsp;ID:                    Subject ID  
&nbsp;&nbsp;&nbsp;&nbsp;in_lesion:             Input individual Lesionmask in MNI152 (1mm iso)  
&nbsp;&nbsp;&nbsp;&nbsp;output_dir:            Specify output directory

&nbsp;&nbsp;&nbsp;&nbsp;optional arguemnts:  
&nbsp;&nbsp;&nbsp;-h, --help            show this help message and exit  
&nbsp;&nbsp;&nbsp;--discStreamlines DISCSTREAMLINES
                    Create disconnected streamline output? [y|n]

4. Output
IN the output_dir a directory with the ID is created containing
1. A csv file with the estimated Neurotransmitter network damage of the individual lesion map for all the Neurotransmitter receptors and transporters from Hansen et al. 2022
2. A txt file with 2 Millionen entries indicating which streamlines of the HCP-aging tractogram is passing through the individual lesion mask [1] and which are sparsed [0] (optional)


5. Test_MNI_lesion.nii.gz
This is a test lesion when used correctly like:
```bash
python Create_NT_Disconn.py Test Test_MNI_lesion.nii.gz output_test
```

Creates the individual Neurotransmitter network damage:


