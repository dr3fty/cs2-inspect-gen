import econ_pb2
import zlib

import sys
import struct

# All you need to generate a gen code
def generate_inspect(proto):
    # Needs to be prefixed with a null byte
    buffer = bytearray([0]) 
    buffer.extend(proto.SerializeToString())

    # calculate the checksum
    crc = zlib.crc32(buffer)
    xored_crc = (crc & 0xFFFF) ^ (proto.ByteSize() * crc)
    
    buffer.extend((xored_crc & 0xFFFFFFFF).to_bytes(length=4, byteorder='big'))

    # Must be upper case
    return buffer.hex().upper()

# Very primitive arg parsing
class ArgParser:
    def __init__(self) -> None:
        self.args = sys.argv[1:]

    @property
    def count(self):
        return len(self.args)

    def pop_string(self, default_value=None):
        if len(self.args) > 0:
            return self.args.pop(0)
        return default_value
    
    def pop_int(self, default_value=None):
        if len(self.args) > 0:
            try:
                return int(self.args.pop(0))
            except:
                return default_value
        return default_value
    
    def pop_float(self, default_value=None):
        if len(self.args) > 0:
            try:
                return float(self.args.pop(0))
            except:
                return default_value
        return default_value

ALLOWED_COMMANDS = ["gen", "gengl", "genrarity"]

def main():
    args = ArgParser()

    # Not too proud of this
    command_name = args.pop_string()
    if command_name and len(command_name) > 1 and command_name[0] == "!":
        command_name = command_name[1:]

    if command_name and command_name.lower() not in ALLOWED_COMMANDS:
        print("Invalid or no command name")
        return
    
    if args.count < 1:
        print("Not enough arguments")
        return

    command_name = command_name.lower()
    is_weapon_gen = command_name == "gen" or command_name == "genrarity"

    # You can modify other parameters to your liking (check econ.proto for all variables)
    proto = econ_pb2.CEconItemPreviewDataBlock()

    if command_name == "genrarity":
        proto.rarity = args.pop_int(0)
    elif command_name == "gengl":
        # Always set the quality to red on gloves
        proto.rarity = 6

    proto.defindex = args.pop_int(1)
    proto.paintindex = args.pop_int(0)
    proto.paintseed = args.pop_int(0)

    paint_wear = args.pop_float(0)
    # Is there a better way to do it in python? 
    proto.paintwear = int.from_bytes(struct.pack(">f", paint_wear))

    if is_weapon_gen:
        for slot in range(0, 5):
            sticker_id = args.pop_int()
            sticker_wear = args.pop_float(0)
            if not sticker_id:
                break

            sticker = proto.stickers.add()
            sticker.slot = slot
            sticker.sticker_id = sticker_id
            sticker.wear = sticker_wear

    generated_payload = generate_inspect(proto)

    print(f"steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20{generated_payload}")

if __name__ == "__main__":
    main()