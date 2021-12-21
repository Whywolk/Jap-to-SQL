# This file is part of Jap-to-SQL source code.
# Copyright (C) 2021  Author: Alex Shirshov <https://github.com/Whywolk>
#
# Jap-to-SQL is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <https://www.gnu.org/licenses/>.


import xml.etree.ElementTree as ET


class Version:

    def __init__(self, ver_root: ET.Element):
        for el in ver_root:
            if (el.tag == 'file_version'):
                self.file_version = el.text

            elif (el.tag == 'database_version'):
                self.db_version = el.text

            elif (el.tag == 'date_of_creation'):
                self.date_creation = el.text

    def print(self):
        print(f'File version: {self.file_version}\n'
              f'Database version: {self.db_version}\n'
              f'Date of creation: {self.date_creation}')


class Character:

    def __init__(self, char_root: ET.Element):

        self.codepoint = dict.fromkeys(['jis208', 'jis212', 'jis213', 'ucs'])
        self.radical = dict.fromkeys(['classical', 'nelson_c'])
        self.misc = dict.fromkeys(['grade', 'stroke_count', 'variant', 'freq', 'rad_name', 'jlpt'])
        self.dic_number = dict.fromkeys(['nelson_c', 'nelson_n', 'halpern_njecd', 'halpern_kkd', 'halpern_kkld',
                                         'halpern_kkld_2ed', 'heisig', 'heisig6', 'gakken', 'oneill_names', 'oneill_kk',
                                         'moro', 'henshall', 'sh_kk', 'sh_kk2', 'sakade', 'jf_cards', 'henshall3',
                                         'tutt_cards', 'crowley', 'kanji_in_context', 'busy_people', 'kodansha_compact',
                                         'maniette'])
        self.query_code = dict.fromkeys(['skip', 'sh_desc', 'four_corner', 'deroo', 'misclass'])
        self.query_code['misclass'] = []
        self.reading_meaning = {
                                'reading': dict.fromkeys(['pinyin', 'korean_r', 'korean_h', 'ja_on', 'ja_kun'], None),
                                'meaning': dict.fromkeys(['en', 'fr', 'es', 'pt'], []),
                                'nanori': []
                                }

        for el in char_root:
            if (el.tag == 'literal'):
                self.literal = el.text

            elif (el.tag == 'codepoint'):
                for cp_value in el:
                    self.codepoint.update({cp_value.attrib['cp_type']: cp_value.text})

            elif (el.tag == 'radical'):
                for rad_value in el:
                    self.radical.update({rad_value.attrib['rad_type']: int(rad_value.text)})

            elif (el.tag == 'misc'):
                variant = {}
                for misc in el:
                    if (misc.tag == 'grade'
                            or misc.tag == 'stroke_count'
                            or misc.tag == 'freq'
                            or misc.tag == 'jlpt'):
                        self.misc.update({misc.tag: int(misc.text)})

                    elif (misc.tag == 'rad_name'):
                        self.misc.update({'rad_name': misc.text})

                    elif (misc.tag == 'variant'):
                        variant.update({misc.attrib['var_type']: misc.text})

                self.misc.update({'variant': variant})

            elif (el.tag == 'dic_number'):
                for dic_ref in el:
                    if (dic_ref.attrib['dr_type'] == 'moro'):
                        self.dic_number.update({dic_ref.attrib['dr_type']: {
                            'number': dic_ref.text,
                            'place': dict.fromkeys(['m_vol', 'm_page'])}
                        })

                        attribs = list(dic_ref.attrib.keys())
                        for attr in attribs[1:]:
                            self.dic_number['moro']['place'][attr] = dic_ref.attrib[attr]

                    else:
                        self.dic_number.update({dic_ref.attrib['dr_type']: dic_ref.text})

            elif (el.tag == 'query_code'):
                for q_code in el:
                    if 'skip_misclass' in q_code.attrib.keys():
                        misclass = dict.fromkeys(['posn', 'stroke_count', 'stroke_and_posn', 'stroke_diff'])
                        misclass.update({q_code.attrib['skip_misclass']: q_code.text})
                        self.query_code['misclass'].append(misclass)
                    else:
                        self.query_code.update({q_code.attrib['qc_type']: q_code.text})

            elif (el.tag == 'reading_meaning'):
                for group in el:
                    if (group.tag == 'rmgroup'):
                        for rm in group:
                            if (rm.tag == 'reading'):
                                self.reading_meaning['reading'][list(rm.attrib.keys())[0]] = rm.text
                            elif (rm.tag == 'meaning'):
                                if not rm.attrib:
                                    self.reading_meaning['meaning']['en'].append(rm.text)
                                else:
                                    self.reading_meaning['meaning'][rm.attrib['m_lang']].append(rm.text)
                    elif (group.tag == 'nanori'):
                        self.reading_meaning['nanori'].append(group.text)

    def print(self):
        print(f'---------- {self.literal} ----------\n'
              f'Codepoint:{self.codepoint}\n'
              f'Radical: {self.radical}\n'
              f'Misc: {self.misc}\n'
              f'Dic number: {self.dic_number}\n'
              f'Query code: {self.query_code}\n'
              f'Reading Meaning: {self.reading_meaning}\n')


if __name__ == "__main__":
    tree = ET.parse('src_data/kanjidic2.xml')
    root = tree.getroot()
    childrens = list(root)

    version = Version(childrens[0])
    version.print()

    characters = childrens[1:]

    kanjis = []
    for char in characters:
        kanjis.append(Character(char))

    for kanji in kanjis:
        kanji.print()
