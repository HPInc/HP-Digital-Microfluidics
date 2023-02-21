from __future__ import annotations
from mpam.exerciser import Exerciser
from support.pcr import Prepare, MixPrep, CombSynth, Test
from argparse import Namespace, _ArgumentGroup, ArgumentParser
from mpam.device import Board
from quantities.dimensions import Time
from typing import Optional, Sequence
from mpam.pipettor import Pipettor
from devices.opentrons import OT2
from devices import joey
from devices.joey import HeaterType
from mpam.cmd_line import time_arg

class JoeyPCRDriver(Exerciser):
    default_off_on_delay = Time.ZERO
    
    def __init__(self) -> None:
        super().__init__(description=f"Mockup of PCR tasks on Joey board")
        self.add_task(Prepare())
        self.add_task(MixPrep())
        self.add_task(CombSynth())
        self.add_task(Test())

    def make_board(self, args:Namespace)->Board: 
        pipettor: Optional[Pipettor] = None
        if args.ot_ip is not None:
            assert args.ot_config is not None, f"Opentrons IP address given, but no config file"
            pipettor = OT2(robot_ip_addr = args.ot_ip,
                           config = args.ot_config,
                           reagents = args.ot_reagents)
        off_on_delay: Time = args.off_on_delay
        return joey.Board(pipettor=pipettor,
                          heater_type=HeaterType.from_name(args.heaters),
                          off_on_delay=off_on_delay,
                          extraction_point_splash_radius=args.extraction_point_splash_radius)

    def available_wells(self)->Sequence[int]:
        return range(8)

    def add_device_specific_common_args(self,
                                        group: _ArgumentGroup,
                                        parser: ArgumentParser  # @UnusedVariable
                                        ) -> None:
        super().add_device_specific_common_args(group, parser)
        group.add_argument('-ps', '--pipettor-speed', type=float, metavar='MULT',
                           help="A speed-up factor for dummy pipettor operations.")
        group.add_argument("-ip", "--ot-ip", metavar="IP",
                           help="The IP address of the Opentrons robot")
        group.add_argument("-otc", "--ot-config", metavar="FILE",
                           help="The config file for the the Opentrons robot")
        group.add_argument("-otr", "--ot-reagents", metavar="FILE",
                           help=f"The reagents JSON file for the the Opentrons robot")
        group.add_argument('-ood','--off-on-delay', type=time_arg, metavar='TIME', 
                           default=self.default_off_on_delay,
                           help=f'''
                            The amount of time to wait between turning pads off
                            and turning pads on in a clock tick.  0ms is no
                            delay.  Negative values means pads are turned on
                            before pads are turned off. Default is
                            {self.fmt_time(self.default_off_on_delay)}.
                            ''')


if __name__ == '__main__':
    exerciser = JoeyPCRDriver()
    exerciser.parse_args_and_run()
