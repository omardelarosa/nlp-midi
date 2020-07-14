from mido import Message
import mido
from pychord import Chord, note_to_chord

from generate import load_mdl, get_next_chord, MODEL_OUT_PATH, rand_octave_shift
from proll import INT_TO_NOTE, NOTE_TO_INT

mdl = load_mdl(MODEL_OUT_PATH)


# msg = Message('note_on', note=60)

# outport = mido.open_output()

# outport.send(msg)

def generate_notes_from_chord(chord, octave):
    spread = 0.0
    OCTAVE = octave
    notes = [(OCTAVE + rand_octave_shift(spread)) * 12 + NOTE_TO_INT[c]
             for c in chord.components()]
    return notes


def main():
    mdl = load_mdl(MODEL_OUT_PATH)

    input_names = mido.get_input_names()
    print(input_names)

    # mid = mido.MidiFile('test.mid')

    DEVICE_NAME = 'CASIO USB-MIDI'

    print('Using device: {}'.format(DEVICE_NAME))
    port = mido.open_output(DEVICE_NAME)
    inport = mido.open_input(DEVICE_NAME)

    current_ai_notes = set()
    current_human_played_notes = set()
    current_human_played_note = None
    current_human_vel = 0
    last_human_played_note = None

    while True:
        r_msg = inport.receive()
        if r_msg.type in ['note_on', 'note_off']:
            note_num = INT_TO_NOTE[r_msg.note % 12]
            if r_msg.type == 'note_on':
                current_human_played_notes.add(r_msg.note)
                last_human_played_note = current_human_played_note
                current_human_played_note = r_msg.note
                current_human_vel = r_msg.velocity
            else:
                if r_msg.note in current_human_played_notes:
                    current_human_played_notes.remove(r_msg.note)
                current_human_played_note = None
                current_human_vel = 0

        # print(current_human_played_notes)
        # print(current_human_played_note, "vel: ", current_human_vel)

        if not current_human_played_notes:
            stop_all_ai_notes(port, list(current_ai_notes))
            current_ai_notes = set()
        elif current_human_played_note and current_human_played_note != last_human_played_note:
            chrd_notes = [current_human_played_note]
            human_octave = int(max(current_human_played_notes) / 12)
            if len(current_human_played_notes) == 1:
                # chrd = Chord(chrd_notes[0])
                chrd_str = INT_TO_NOTE[chrd_notes[0] % 12]
                human_notes_names = [chrd_str]
            else:
                human_notes = list(current_human_played_notes)
                human_notes_names = [INT_TO_NOTE[n % 12] for n in human_notes]
                chrd = note_to_chord(human_notes_names)
                if not chrd:
                    chrd_str = ''
                else:
                    chrd_str = str(chrd[0])
            if not chrd_str:
                continue
            try:
                next_chord = get_next_chord(
                    mdl, chrd_str, random_neighbors=True)
                print("notes: {}, chord_suggestion: {}".format(
                    human_notes_names, next_chord))
                next_chord_notes = generate_notes_from_chord(
                    next_chord, human_octave)
                # if len(current_ai_notes) == 0:
                start_all_ai_notes(port, next_chord_notes, current_human_vel)
                for note in next_chord_notes:
                    current_ai_notes.add(note)
            except:
                print("unparsable chrd_str: '{}'".format(chrd_str))

        # if not current_human_played_notes:
        #     stop_all_ai_notes(port, list(current_ai_notes))
        #     current_ai_notes = set()


def stop_all_ai_notes(port, notes):
    messages = [mido.Message('note_off', note=note) for note in notes]
    for msg in messages:
        port.send(msg)


def start_all_ai_notes(port, notes, human_vel):
    vel = human_vel
    time = 0.0
    messages = [mido.Message('note_on', note=note,
                             velocity=vel, time=time) for note in notes]
    for msg in messages:
        port.send(msg)

# for msg in mid.play():
#     port.send(msg)
# while True:


if __name__ == '__main__':
    main()
