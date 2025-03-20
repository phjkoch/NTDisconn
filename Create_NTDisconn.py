#!/usr/bin/env python
# -*- coding: utf-8 -*-


#### Population based Tractogram: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10474320/


from __future__ import division
import argparse
import nibabel as nib
import numpy as np
from dipy.tracking._utils import _mapping_to_voxel, _to_voxel_coordinates
import subprocess
from scipy.stats import zscore
import os
import ants
from tqdm import tqdm
import pandas as pd
import requests
def buildArgsParser():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter)


    #p.add_argument('in_neurotrans',
    #               help='Input Neurotransmitter system (Specific name can be found in HCP_NT folder')
    p.add_argument('ID',
                   help='Subject ID')
    p.add_argument('in_lesion',
                   help='Input individual Lesionmask in MNI152 (1mm iso)')
    p.add_argument('output_dir',
                   help='Specify output directory')
    p.add_argument('--discStreamlines', default='y',
                   help='Create disconnected streamline output? [y|n]')
    p.add_argument('--Connectome', default='y',
                   help='Create Connectome output? [y|n]')


    return p


def main():
    parser = buildArgsParser()
    args = parser.parse_args()


    reference = "HCPA422-T1w-500um-norm.nii.gz"
    out_NT_disc = os.path.join(args.output_dir, args.ID +"_NT_Diconnect.csv")

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    def define_streamlines(streamlines, lesion, reference):#, NT_weights_SUM):#, weights):
        metric_tractrogram = []
        metric_tractogram_preserved = []

        les = lesion.get_fdata()
        affine = reference.affine
        lin_T, offset = _mapping_to_voxel(affine)

        for s in tqdm(range(2000000), desc="Evaluate streamlines"):
            streamline = streamlines[s]
            ### location
            x_ind_2 = _to_voxel_coordinates(streamline[:], lin_T, offset)[:, 0]
            y_ind_2 = _to_voxel_coordinates(streamline[:], lin_T, offset)[:, 1]
            z_ind_2 = _to_voxel_coordinates(streamline[:], lin_T, offset)[:, 2]

            if np.sum(les[x_ind_2, y_ind_2, z_ind_2]) > 0:
                metric_tractrogram.append(1)
                #metric_tractogram_preserved.append(0)
            else:
                metric_tractrogram.append(0)
            #    metric_tractogram_preserved.append(a[s])

        return(metric_tractrogram)

    tck_file = "HCP422_2_million.tck"
    if os.path.isfile(tck_file)
        print("Tactogram exisitng")
    else:
        print("Downloading Tractogram...........")
        osf_url = "https://osf.io/download/nduwc/"
        response = requests.get(osf_url, stream=True)
        total_size = int(response.headers.get("content-length", 0))
        with open(tck_file, "wb") as file, tqdm(desc=tck_file, total=total_size, unit="B", unit_scale=True) as bar:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                bar.update(len(chunk))
        print("Download complete!")
       

    
    if os.path.isfile(out_NT_disc) == True:
        print("disc sl already calculated")
    else:

        print("Loading streamlines ##########################################")
        tractogram = nib.streamlines.load(tck_file)
        streamlines = tractogram.streamlines
        header_sl = tractogram.header

        ### Bring Input Lesion (MNI) in HCPA MNI
        standard = "HCPA422-T1w-500um-norm.nii.gz"
        listtransf = ['MNI_to_HCPA_Warp.nii.gz', "MNI_to_HCPA.mat"]
        fi = ants.image_read(standard)
        movmap = ants.image_read(args.in_lesion)
        mywarpedimage = ants.apply_transforms(fixed=fi, moving=movmap,
                                              transformlist=listtransf, interpolator='multiLabel')

        output = mywarpedimage.numpy()
        ref = nib.load(standard)
        lesion = nib.Nifti1Image(output, ref.affine, ref.header)
        nib.save(lesion, "tmp_les.nii.gz")

        weights_tractogram = define_streamlines(streamlines, lesion, nib.load(reference))

        out_weights_tractogram_disc = os.path.join(args.output_dir,
                                                   args.ID + "_Disc_Streamlines.txt")
        if args.discStreamlines == 'y':
            np.savetxt(out_weights_tractogram_disc, weights_tractogram)

        d = {}
        d["ID"] = args.ID
        d["Disc_SL"] = np.sum(weights_tractogram)
        print("Evaluate NT systems......................")
        for neurotrans in ["5HT1a_way_hc36_savli", "5HT1b_p943_hc65_gallezot", "5HT2a_cimbi_hc29_beliveau", "5HT4_sb20_hc59_beliveau", "5HT6_gsk_hc30_radhakrishnan", "5HTT_dasb_hc100_beliveau", "D1_SCH23390_hc13_kaller", "D2_flb457_hc37_smith", "DAT_fpcit_hc174_dukart_spect", "A4B2_flubatine_hc30_hillmer", "VAChT_feobv_hc18_aghourian_sum", "mGluR5_abp_hc22_rosaneto", "GABAa-bz_flumazenil_hc16_norgaard", "NAT_MRB_hc77_ding", "H3_cban_hc8_gallezot", "M1_lsn_hc24_naganawa", "CB1_omar_hc77_normandin", "NMDA_ge179_hc29_galovic", "MU_carfentanil_hc204_kantonen"]:
            print(neurotrans)
            in_neurotrans_weights = os.path.join("HCP_NT", neurotrans,
                                                 "GT_" + neurotrans + "_weights_disc_Tractogram.txt")
            out_connect = os.path.join(args.output_dir, args.ID + "_" + neurotrans + "_Diconnectome.csv")
            #out_connect_pres = os.path.join(args.output_dir, args.in_neurotrans + "_Preserved_Connectome.csv")

            nt_weights = weights_tractogram * np.loadtxt(in_neurotrans_weights)
            np.savetxt("tmp_disc.txt", nt_weights)
            d[neurotrans] = np.sum(nt_weights)



            if args.Connectome == 'y':
                print("Creating Connectomes #########################")
                #tck2connectome_cmd = "tck2connectome HCP422_2_million.tck BN_Atlas_277_05mm_HCPA.nii.gz " + out_connect_pres + " -tck_weights_in "+out_weights_tractogram_pres+" --assignment_radial_search 4 -symmetric -f"  # -zero_diagonal
                #subprocess.call(tck2connectome_cmd, shell=True)

                tck2connectome_cmd = "tck2connectome HCP422_2_million.tck BN_Atlas_277_05mm_HCPA.nii.gz " + out_connect + " -tck_weights_in tmp_disc.txt --assignment_radial_search 4 -symmetric -f"  # -zero_diagonal
                subprocess.call(tck2connectome_cmd, shell=True)

        df = pd.DataFrame(d, index=[0])
        df.to_csv(out_NT_disc)

if __name__ == "__main__":
    main()

# %%
