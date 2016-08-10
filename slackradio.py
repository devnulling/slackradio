#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Slackradio
# Generated: Thu Aug  4 16:16:55 2016
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import math
import rds
import time


class slackradio(gr.top_block):

    def __init__(self, freq=88.5e6, gain=30, input_gain=.3, pilot_gain=.09, ps="DEFCON", rds_gain=.1, stereo_gain=.3, wavfile=""):
        gr.top_block.__init__(self, "Slackradio")

        ##################################################
        # Parameters
        ##################################################
        self.freq = freq
        self.gain = gain
        self.input_gain = input_gain
        self.pilot_gain = pilot_gain
        self.ps = ps
        self.rds_gain = rds_gain
        self.stereo_gain = stereo_gain
        self.wavfile = wavfile

        ##################################################
        # Variables
        ##################################################
        self.usrp_rate = usrp_rate = 19e3*20
        self.outbuffer = outbuffer = 1024
        self.fm_max_dev = fm_max_dev = 80e3

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_sink = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink.set_samp_rate(1e6)
        self.uhd_usrp_sink.set_center_freq(freq, 0)
        self.uhd_usrp_sink.set_gain(gain, 0)
        self.uhd_usrp_sink.set_antenna("TX/RX", 0)
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=100,
                decimation=38,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_fff(
                interpolation=380,
                decimation=48,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=380,
                decimation=48,
                taps=None,
                fractional_bw=None,
        )
        self.low_pass_filter_0_0_0 = filter.interp_fir_filter_fff(1, firdes.low_pass(
        	1, usrp_rate, 15e3, 2e3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0 = filter.interp_fir_filter_fff(1, firdes.low_pass(
        	1, usrp_rate, 15e3, 2e3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0 = filter.interp_fir_filter_fff(1, firdes.low_pass(
        	1, usrp_rate, 2.5e3, .5e3, firdes.WIN_HAMMING, 6.76))
        (self.low_pass_filter_0).set_max_output_buffer(1024)
        self.gr_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(2)
        (self.gr_unpack_k_bits_bb_0).set_max_output_buffer(4096)
        self.gr_sub_xx_0 = blocks.sub_ff(1)
        self.gr_sig_source_x_0_1 = analog.sig_source_f(usrp_rate, analog.GR_SIN_WAVE, 19e3, 1, 0)
        self.gr_sig_source_x_0_0 = analog.sig_source_f(usrp_rate, analog.GR_SIN_WAVE, 57e3, 1, 0)
        self.gr_sig_source_x_0 = analog.sig_source_f(usrp_rate, analog.GR_SIN_WAVE, 38e3, 1, 0)
        self.gr_rds_encoder_0 = rds.encoder(1, 8, True, ps, 89.8e6,
        			True, False, 13, 3,
        			147, "CYBERSPECTRUM")
        	
        (self.gr_rds_encoder_0).set_max_output_buffer(4096)
        self.gr_multiply_xx_1 = blocks.multiply_vff(1)
        self.gr_multiply_xx_0 = blocks.multiply_vff(1)
        (self.gr_multiply_xx_0).set_max_output_buffer(1024)
        self.gr_map_bb_1 = digital.map_bb(([1,2]))
        (self.gr_map_bb_1).set_max_output_buffer(4096)
        self.gr_map_bb_0 = digital.map_bb(([-1,1]))
        (self.gr_map_bb_0).set_max_output_buffer(4096)
        self.gr_frequency_modulator_fc_0 = analog.frequency_modulator_fc(2*math.pi*fm_max_dev/usrp_rate)
        (self.gr_frequency_modulator_fc_0).set_max_output_buffer(1024)
        self.gr_diff_encoder_bb_0 = digital.diff_encoder_bb(2)
        (self.gr_diff_encoder_bb_0).set_max_output_buffer(4096)
        self.gr_char_to_float_0 = blocks.char_to_float(1, 1)
        (self.gr_char_to_float_0).set_max_output_buffer(1024)
        self.gr_add_xx_1 = blocks.add_vff(1)
        (self.gr_add_xx_1).set_max_output_buffer(1024)
        self.gr_add_xx_0 = blocks.add_vff(1)
        self.blocks_wavfile_source_0 = blocks.wavfile_source(wavfile, True)
        self.blocks_socket_pdu_0 = blocks.socket_pdu("TCP_SERVER", "", "52001", 10000, False)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_float*1, 160)
        self.blocks_multiply_const_vxx_0_1 = blocks.multiply_const_vff((input_gain, ))
        self.blocks_multiply_const_vxx_0_0_1 = blocks.multiply_const_vff((pilot_gain, ))
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vff((rds_gain, ))
        (self.blocks_multiply_const_vxx_0_0).set_max_output_buffer(1024)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((input_gain, ))

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_socket_pdu_0, 'pdus'), (self.gr_rds_encoder_0, 'rds in'))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.gr_add_xx_1, 0))    
        self.connect((self.blocks_multiply_const_vxx_0_0_1, 0), (self.gr_add_xx_1, 1))    
        self.connect((self.blocks_multiply_const_vxx_0_1, 0), (self.rational_resampler_xxx_0_0, 0))    
        self.connect((self.blocks_repeat_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.blocks_wavfile_source_0, 1), (self.blocks_multiply_const_vxx_0_1, 0))    
        self.connect((self.gr_add_xx_0, 0), (self.low_pass_filter_0_0, 0))    
        self.connect((self.gr_add_xx_1, 0), (self.gr_frequency_modulator_fc_0, 0))    
        self.connect((self.gr_char_to_float_0, 0), (self.blocks_repeat_0, 0))    
        self.connect((self.gr_diff_encoder_bb_0, 0), (self.gr_map_bb_1, 0))    
        self.connect((self.gr_frequency_modulator_fc_0, 0), (self.rational_resampler_xxx_1, 0))    
        self.connect((self.gr_map_bb_0, 0), (self.gr_char_to_float_0, 0))    
        self.connect((self.gr_map_bb_1, 0), (self.gr_unpack_k_bits_bb_0, 0))    
        self.connect((self.gr_multiply_xx_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))    
        self.connect((self.gr_multiply_xx_1, 0), (self.gr_add_xx_1, 2))    
        self.connect((self.gr_rds_encoder_0, 0), (self.gr_diff_encoder_bb_0, 0))    
        self.connect((self.gr_sig_source_x_0, 0), (self.gr_multiply_xx_1, 0))    
        self.connect((self.gr_sig_source_x_0_0, 0), (self.gr_multiply_xx_0, 0))    
        self.connect((self.gr_sig_source_x_0_1, 0), (self.blocks_multiply_const_vxx_0_0_1, 0))    
        self.connect((self.gr_sub_xx_0, 0), (self.low_pass_filter_0_0_0, 0))    
        self.connect((self.gr_unpack_k_bits_bb_0, 0), (self.gr_map_bb_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.gr_multiply_xx_0, 1))    
        self.connect((self.low_pass_filter_0_0, 0), (self.gr_add_xx_1, 3))    
        self.connect((self.low_pass_filter_0_0_0, 0), (self.gr_multiply_xx_1, 1))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.gr_add_xx_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.gr_sub_xx_0, 0))    
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.gr_add_xx_0, 1))    
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.gr_sub_xx_0, 1))    
        self.connect((self.rational_resampler_xxx_1, 0), (self.uhd_usrp_sink, 0))    

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_sink.set_center_freq(self.freq, 0)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.uhd_usrp_sink.set_gain(self.gain, 0)
        	

    def get_input_gain(self):
        return self.input_gain

    def set_input_gain(self, input_gain):
        self.input_gain = input_gain
        self.blocks_multiply_const_vxx_0.set_k((self.input_gain, ))
        self.blocks_multiply_const_vxx_0_1.set_k((self.input_gain, ))

    def get_pilot_gain(self):
        return self.pilot_gain

    def set_pilot_gain(self, pilot_gain):
        self.pilot_gain = pilot_gain
        self.blocks_multiply_const_vxx_0_0_1.set_k((self.pilot_gain, ))

    def get_ps(self):
        return self.ps

    def set_ps(self, ps):
        self.ps = ps
        self.gr_rds_encoder_0.set_ps(self.ps)

    def get_rds_gain(self):
        return self.rds_gain

    def set_rds_gain(self, rds_gain):
        self.rds_gain = rds_gain
        self.blocks_multiply_const_vxx_0_0.set_k((self.rds_gain, ))

    def get_stereo_gain(self):
        return self.stereo_gain

    def set_stereo_gain(self, stereo_gain):
        self.stereo_gain = stereo_gain

    def get_wavfile(self):
        return self.wavfile

    def set_wavfile(self, wavfile):
        self.wavfile = wavfile

    def get_usrp_rate(self):
        return self.usrp_rate

    def set_usrp_rate(self, usrp_rate):
        self.usrp_rate = usrp_rate
        self.gr_frequency_modulator_fc_0.set_sensitivity(2*math.pi*self.fm_max_dev/self.usrp_rate)
        self.gr_sig_source_x_0.set_sampling_freq(self.usrp_rate)
        self.gr_sig_source_x_0_0.set_sampling_freq(self.usrp_rate)
        self.gr_sig_source_x_0_1.set_sampling_freq(self.usrp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.usrp_rate, 2.5e3, .5e3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.usrp_rate, 15e3, 2e3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0_0.set_taps(firdes.low_pass(1, self.usrp_rate, 15e3, 2e3, firdes.WIN_HAMMING, 6.76))

    def get_outbuffer(self):
        return self.outbuffer

    def set_outbuffer(self, outbuffer):
        self.outbuffer = outbuffer

    def get_fm_max_dev(self):
        return self.fm_max_dev

    def set_fm_max_dev(self, fm_max_dev):
        self.fm_max_dev = fm_max_dev
        self.gr_frequency_modulator_fc_0.set_sensitivity(2*math.pi*self.fm_max_dev/self.usrp_rate)


def argument_parser():
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option(
        "", "--freq", dest="freq", type="eng_float", default=eng_notation.num_to_str(88.5e6),
        help="Set freq [default=%default]")
    parser.add_option(
        "", "--gain", dest="gain", type="eng_float", default=eng_notation.num_to_str(30),
        help="Set gain [default=%default]")
    parser.add_option(
        "", "--input-gain", dest="input_gain", type="eng_float", default=eng_notation.num_to_str(.3),
        help="Set input_gain [default=%default]")
    parser.add_option(
        "", "--pilot-gain", dest="pilot_gain", type="eng_float", default=eng_notation.num_to_str(.09),
        help="Set pilot_gain [default=%default]")
    parser.add_option(
        "", "--ps", dest="ps", type="string", default="DEFCON",
        help="Set ps [default=%default]")
    parser.add_option(
        "", "--rds-gain", dest="rds_gain", type="eng_float", default=eng_notation.num_to_str(.1),
        help="Set rds_gain [default=%default]")
    parser.add_option(
        "", "--stereo-gain", dest="stereo_gain", type="eng_float", default=eng_notation.num_to_str(.3),
        help="Set stereo_gain [default=%default]")
    parser.add_option(
        "", "--wavfile", dest="wavfile", type="string", default="",
        help="Set wavfile [default=%default]")
    return parser


def main(top_block_cls=slackradio, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(freq=options.freq, gain=options.gain, input_gain=options.input_gain, pilot_gain=options.pilot_gain, ps=options.ps, rds_gain=options.rds_gain, stereo_gain=options.stereo_gain, wavfile=options.wavfile)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
