class PassIn:
    @classmethod
    def pass_in_gui_final_inputs_object(cls,gui_final_inputs_object):
        cls.gui_final_inputs_object = gui_final_inputs_object
    
    @classmethod
    def pass_in_gui_peak_clicks_object(cls,gui_peak_clicks_object):
        cls.gui_peak_clicks_object = gui_peak_clicks_object

    @classmethod
    def pass_in_gui_record_force_object(cls,gui_record_force_object):
        cls.gui_record_force_object = gui_record_force_object

    @classmethod
    def pass_in_gui_initial_inputs_object(cls,gui_initial_inputs_object):
        cls.gui_initial_inputs_object = gui_initial_inputs_object
    
    @classmethod
    def pass_in_gui_calibrate_object(cls,gui_calibrate_object):
        cls.gui_calibrate_object = gui_calibrate_object

    @classmethod
    def pass_in_gui_stem_count_classic_object(cls,gui_stem_count_classic_object):
        cls.gui_stem_count_classic_object = gui_stem_count_classic_object

    @classmethod
    def pass_in_gui_guide_object(cls,gui_guide_object):
        cls.gui_guide_object = gui_guide_object

    @classmethod
    def pass_in_gui_error_report_object(cls,gui_error_report_object):
        cls.gui_error_report_object = gui_error_report_object

    def __init__(self):
        self.gui_initial_inputs_object = object()
        self.gui_record_force_object = object()
        self.gui_final_inputs_object = object()
        self.gui_peak_clicks_object = object()
        self.gui_error_report_object = object()
        self.gui_calibrate_object = object()