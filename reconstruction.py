import reconstruct_picture
import reconstruct_gob
import reconstruct_macro_block
import reconstruct_block
import reconstruct_base
import block
import macroblock
import gob
import picture
import ref_picture


class Reconstruction:

    @staticmethod
    def reconstruct_pic(pic: picture.Picture):
        print("--------------------------------reconstruction: total start-----------------------------------")

        ref_picture.RefPicInterpreter.record_current_processing_pic(ref_picture.CurrentProcessInfo(pic, ref_picture.RefPicInterpreter.current_ref_pic))
        reconstruct_pic = reconstruct_picture.ReconstructPicture(pic)
        for gob in pic.gobs:
            ref_picture.RefPicInterpreter.record_current_process_gop(ref_picture.CurrentProcessInfo(current_proc_ele=gob, ref_li=ref_picture.RefPicInterpreter.current_ref_gop))
            reconstruct_gob_ = reconstruct_gob.ReconstructGOB(gob)
            for mb in gob.macroblocks:
                ref_picture.RefPicInterpreter.record_current_process_mb(ref_picture.CurrentProcessInfo(current_proc_ele=mb, ref_li=ref_picture.RefPicInterpreter.current_ref_macroblock))
                real_mb: macroblock.Macroblock = mb
                reconstruct_mb = reconstruct_macro_block.ReconstructMacroBlock(real_mb)
                reconstruct_blk = None
                if real_mb.block_data is not None:
                    for index, blk in enumerate(real_mb.block_data):
                        ref_picture.RefPicInterpreter.record_current_process_blk(ref_picture.CurrentProcessInfo(current_proc_ele=blk, ref_li=ref_picture.RefPicInterpreter.current_ref_block))
                        if blk is None:
                            reconstruct_mb.go_reconstruction_with_motion_compensation(real_mb.mba, index)

                        real_blk: block.Block = blk
                        reconstruct_blk = reconstruct_block.ReconstructBlock(real_blk, index)
                        reconstruct_blk.go_reconstruction()
                        reconstruct_mb.go_reconstruction_macro_block(reconstruct_blk)
                else:
                    reconstruct_mb.go_reconstruction_with_motion_compensation(
                        ref_picture.RefPicInterpreter.get_current_ref_pic().frame, real_mb)

                reconstruct_gob_.go_reconstruction_gob(reconstruct_mb)
                ref_picture.RefPicInterpreter.record_current_ref_macroblock(reconstruct_mb)
                ref_picture.RefPicInterpreter.walk_through_a_mb()

            reconstruct_pic.go_reconstruction_gob(reconstruct_gob_)
            ref_picture.RefPicInterpreter.record_current_ref_gop(reconstruct_gob_)
        print("--------------------------------reconstruction: total end-----------------------------------")

        ref_picture.RefPicInterpreter.record_current_ref_pic(reconstruct_pic)
        ref_picture.RefPicInterpreter.clear_walkthrough_bytes()
        return reconstruct_pic
