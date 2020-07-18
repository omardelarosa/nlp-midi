import argparse

from midi_server import serve, print_midi_ports
from train import train


SUPPORTED_MODES = [
    'printPorts',
    'midi',
    'train'
]


parser = argparse.ArgumentParser(
    description='NLP tools for MIDI')

parser.add_argument('--mode', type=str,
                    help='supported modes: {}'.format(SUPPORTED_MODES))

parser.add_argument('--corpusPath', type=str, help='path to training corpus')
parser.add_argument('--octaveOffset', type=int,
                    help='offset output notes by +n octaves')
parser.add_argument('--spread', type=float,
                    help='randomly spread out the notes across octaves')
parser.add_argument('--modelIn',
                    type=str,
                    help='language embedding model used for input')
parser.add_argument('--inPort',
                    type=str,
                    help='midi input port name')
parser.add_argument('--outPort',
                    type=str,
                    help='midi output port name')

args = parser.parse_args()


if args.mode == 'printPorts':
    print_midi_ports()
elif args.mode == 'midi':
    serve(args.modelIn, args.inPort, args.outPort,
          args.octaveOffset, args.spread)
elif args.mode == 'train':
    train(args.modelIn, args.modelOut)
else:
    print("please specify one of the supported modes: {}".format(SUPPORTED_MODES))
