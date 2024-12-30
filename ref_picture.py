import gob
import macroblock
import block
import linked_frame_list


class CurrentProcessInfo:
    def __init__(self, current_proc_ele, ref_li):
        self.current_process_element = current_proc_ele
        self.ref_list = ref_li


class RefPicInterpreter:
    current_ref_pic = linked_frame_list.LinkedFrameList()
    current_ref_gop = linked_frame_list.LinkedFrameList()
    current_ref_macroblock = linked_frame_list.LinkedFrameList()
    current_ref_block = linked_frame_list.LinkedFrameList()
    current_proc_pic = None
    current_proc_gop = None
    current_proc_macroblock = None
    current_proc_block = None
    current_walkthrough_bytes_y = 0
    current_walkthrough_bytes_u = 0
    current_walkthrough_bytes_v = 0

    def __init__(self, picture_struct):
        self.pic_interpreter = picture_struct

    @staticmethod
    def clear_walkthrough_bytes():
        RefPicInterpreter.current_walkthrough_bytes_y = 0
        RefPicInterpreter.current_walkthrough_bytes_u = 0
        RefPicInterpreter.current_walkthrough_bytes_v = 0

    @staticmethod
    def walk_through_a_mb():
        RefPicInterpreter.current_walkthrough_bytes_y += 64 * 4
        RefPicInterpreter.current_walkthrough_bytes_u += 64 * 2
        RefPicInterpreter.current_walkthrough_bytes_v += 64 * 2

    @staticmethod
    def get_current_corresponding_mb_data_start_index_y():
        return RefPicInterpreter.current_walkthrough_bytes_y

    @staticmethod
    def get_current_corresponding_mb_data_start_index_u():
        return RefPicInterpreter.current_walkthrough_bytes_u

    @staticmethod
    def get_current_corresponding_mb_data_start_index_v():
        return RefPicInterpreter.current_walkthrough_bytes_v

    @staticmethod
    def work_out_current_global_mb_index_in_2d_form():
        mb_global = RefPicInterpreter.current_walkthrough_bytes_y / 4 / 64
        y = int(mb_global // 16)  # Row index (y)
        x = int(mb_global % 16)  # Column index (x)
        return [x, y]

    def get_gop_at_index(self, index):
        return self.pic_interpreter.gobs[index]

    @staticmethod
    def get_current_process_gop():
        return RefPicInterpreter.current_proc_gop

    @staticmethod
    def record_current_process_gop(group_of_pics):
        RefPicInterpreter.current_proc_gop = group_of_pics

    @staticmethod
    def get_current_process_mb():
        return RefPicInterpreter.current_proc_macroblock

    @staticmethod
    def record_current_process_mb(mb):
        RefPicInterpreter.current_proc_macroblock = mb

    @staticmethod
    def get_current_process_blk():
        return RefPicInterpreter.current_proc_block

    @staticmethod
    def record_current_process_blk(blk):
        RefPicInterpreter.current_proc_block = blk

    @staticmethod
    def get_current_processing_pic():
        return RefPicInterpreter.current_proc_pic

    @staticmethod
    def record_current_processing_pic(current_pic):
        RefPicInterpreter.current_proc_pic = current_pic

    @staticmethod
    def get_current_ref_pic():
        return RefPicInterpreter.current_ref_pic.get_latest_one()

    @staticmethod
    def record_current_ref_pic(ref_pic):
        RefPicInterpreter.current_ref_pic.add_frame(ref_pic)

    @staticmethod
    def get_current_ref_gop():
        return RefPicInterpreter.current_ref_gop.get_latest_one()

    @staticmethod
    def record_current_ref_gop(ref_gop):
        RefPicInterpreter.current_ref_gop.add_frame(ref_gop)

    @staticmethod
    def get_current_ref_macroblock():
        return RefPicInterpreter.current_ref_macroblock.get_latest_one()

    @staticmethod
    def record_current_ref_macroblock(ref_mb):
        RefPicInterpreter.current_ref_macroblock.add_frame(ref_mb)

    @staticmethod
    def get_current_ref_blk():
        return RefPicInterpreter.current_ref_block.get_latest_one()

    @staticmethod
    def record_current_ref_blk(ref_blk):
        RefPicInterpreter.current_ref_block.add_frame(ref_blk)
