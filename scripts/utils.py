# test_script.py
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "tomllib"
# ]
# ///

import tomllib


def read_toml():
    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)

    if data is None:
        print("No data found")
    else:
        print(data)
    return data


DEFAULT = """
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(0, 1, 1, 1),
    prodvers=(0, 1, 1, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        '040904B0',
        [StringStruct(u'CompanyName', 'Dottorlink'),
        StringStruct(u'FileDescription', 'Description of my script'),
        StringStruct(u'FileVersion', '0.1.1'),
        StringStruct(u'InternalName', 'new-certificazione-770'),
        StringStruct(u'LegalCopyright', u'Dottorlink. All rights reserved.'),
        StringStruct(u'ProductName', u'New Certificazione 770'),
        StringStruct(u'ProductVersion', '0.1.1')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [0, 0])])
  ]
)
"""


def write_version_file():
    """Write file version.rc"""

    data = read_toml()
    if data is None:
        return

    company_name = data["project"]["authors"]["name"]
    print(company_name)

    file_description = data["project"]["description"]
    print(file_description)


read_toml()
