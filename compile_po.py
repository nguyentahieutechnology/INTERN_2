import struct
import array
import os

def make(po_path, mo_path):
    MESSAGES = {}
    with open(po_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    msgid = ""
    msgstr = ""
    in_msgid = False
    in_msgstr = False
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('msgid '):
            in_msgid = True
            in_msgstr = False
            msgid = line[6:].strip().strip('"')
        elif line.startswith('msgstr '):
            in_msgid = False
            in_msgstr = True
            msgstr = line[7:].strip().strip('"')
        elif line.startswith('"') and line.endswith('"'):
            val = line.strip('"')
            if in_msgid:
                msgid += val
            elif in_msgstr:
                msgstr += val
        
        # When we hit a new statement or end of line, save the previous if completed
        # Actually a simpler PO parser:
    
    # Let's write a robust parser
    MESSAGES = {}
    with open(po_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    entries = content.split('\n\n')
    for entry in entries:
        lines = entry.strip().split('\n')
        cur_id = None
        cur_str = None
        mode = None # 'id' or 'str'
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('msgid '):
                cur_id = line[6:].strip().strip('"')
                cur_id = cur_id.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"').replace('\\\\', '\\')
                mode = 'id'
            elif line.startswith('msgstr '):
                cur_str = line[7:].strip().strip('"')
                cur_str = cur_str.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"').replace('\\\\', '\\')
                mode = 'str'
            elif line.startswith('"'):
                val = line.strip('"')
                val = val.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"').replace('\\\\', '\\')
                if mode == 'id':
                    cur_id += val
                elif mode == 'str':
                    cur_str += val
        if cur_id is not None and cur_str is not None:
            MESSAGES[cur_id] = cur_str

    # Write MO file
    keys = sorted(MESSAGES.keys())
    offsets = []
    ids = b''
    strs = b''
    for key in keys:
        offsets.append((len(ids), len(key.encode('utf-8')), len(strs), len(MESSAGES[key].encode('utf-8'))))
        ids += key.encode('utf-8') + b'\0'
        strs += MESSAGES[key].encode('utf-8') + b'\0'
        
    keystart = 7 * 4 + len(offsets) * 16
    valstart = keystart + len(ids)
    
    koffsets = []
    voffsets = []
    for idoff, idlen, stroff, strlen in offsets:
        koffsets.append(idlen)
        koffsets.append(keystart + idoff)
        voffsets.append(strlen)
        voffsets.append(valstart + stroff)
        
    # Magic number: 0x950412de
    output = struct.pack('<Iiiiiii',
                         0x950412de,  # magic
                         0,            # file format revision
                         len(keys),    # number of strings
                         7 * 4,        # offset of key table
                         7 * 4 + len(keys) * 8, # offset of value table
                         0,            # size of hashing table
                         0)            # offset of hashing table
    
    output += array.array('i', koffsets).tobytes()
    output += array.array('i', voffsets).tobytes()
    output += ids
    output += strs
    
    os.makedirs(os.path.dirname(mo_path), exist_ok=True)
    with open(mo_path, 'wb') as f:
        f.write(output)

if __name__ == '__main__':
    make('locale/en/LC_MESSAGES/django.po', 'locale/en/LC_MESSAGES/django.mo')
    print("Compiled successfully!")
