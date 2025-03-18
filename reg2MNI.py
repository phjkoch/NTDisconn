#!/usr/bin/env python
# -*- coding: utf-8 -*-


#### Population based Tractogram: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10474320/


from __future__ import division
import argparse
import nibabel as nib
import shutil
import os
import ants

def buildArgsParser():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter)

    p.add_argument('in_anat',
                   help='Input anat')
    p.add_argument('in_mask',
                   help='Input individual mask (e.g.Lesionmask) to transfer to MNI ')
    p.add_argument('output_dir',
                   help='Specify output directory')


    return p


def main():
    parser = buildArgsParser()
    args = parser.parse_args()


    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    ### fi= fixed, mi=moving
    mi = ants.image_read(args.in_anat)
    fi = ants.image_read("MNI152_T1_1mm.nii.gz")


    tx = ants.registration(fixed=fi, moving=mi, type_of_transform='SyN')

    Warped = tx['warpedmovout']
    warpnib = Warped.numpy()
    ref = nib.load("MNI152_T1_1mm.nii.gz")
    warpnib = nib.Nifti1Image(warpnib, ref.affine, ref.header)
    nib.save(warpnib, os.path.join(args.output_dir, "anat_in_MNI.nii.gz"))

    ##################
    ###################

    t12mni_mat = os.path.join(args.output_dir, "t12mni.mat")
    t12mni_warp = os.path.join(args.output_dir, "t12mni_warp.nii.gz")
    t12mni_invwarp = os.path.join(args.output_dir, "t12mni_invwarp.nii.gz")

    forwardtrans = tx['fwdtransforms']
    invtrans = tx['invtransforms']
    #### maybe include ants.tonibabel
    shutil.copyfile(forwardtrans[1], t12mni_mat)
    shutil.copyfile(forwardtrans[0], t12mni_warp)
    shutil.copyfile(invtrans[0], t12mni_invwarp)


    #### Apply registration

    listtransf2 = [str(t12mni_mat), str(t12mni_warp)]
    apply = ants.apply_transforms(fixed=ants.image_read("MNI152_T1_1mm.nii.gz"),
                                  moving=ants.image_read(args.in_mask),
                                  transformlist=listtransf2, whichtoinvert=(False, False),
                                  interpolator="multiLabel")

    warpnib = apply.numpy()
    warpnib = nib.Nifti1Image(warpnib, ref.affine, ref.header)
    nib.save(warpnib, os.path.join(args.output_dir, "mask_in_MNI.nii.gz"))


if __name__ == "__main__":
    main()

# %%
