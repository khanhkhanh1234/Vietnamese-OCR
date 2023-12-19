import sys
import json
import re
if "../" not in sys.path:
    sys.path.append("../")


import json
from modules.Base import Base
class FontPage:
    def __init__(self, name, year_of_birth, cmnd, address):
        self._name = name
        self._year_of_birth = year_of_birth
        self._cmnd = cmnd
        self._address = address

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def year_of_birth(self):
        return self._year_of_birth

    @year_of_birth.setter
    def year_of_birth(self, value):
        self._year_of_birth = value

    @property
    def cmnd(self):
        return self._cmnd

    @cmnd.setter
    def cmnd(self, value):
        self._cmnd = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

    def to_json(self):
        return json.dumps(self.data)
    
class InnerLeftPage:
    def __init__(self, terrain_non, address, superficie, usage_pattern, expiration_date, origin_of_use, map_sheet, purpose_of_use):
        self._terrain_non = terrain_non
        self._address = address
        self._superficie = superficie
        self._usage_pattern = usage_pattern
        self._expiration_date = expiration_date
        self._origin_of_use = origin_of_use
        self._map_sheet = map_sheet
        self._purpose_of_use = purpose_of_use

    # Getter và Setter cho terrain_non
    def get_terrain_non(self):
        return self._terrain_non

    def set_terrain_non(self, terrain_non):
        self._terrain_non = terrain_non

    # Getter và Setter cho address
    def get_address(self):
        return self._address

    def set_address(self, address):
        self._address = address

    # Getter và Setter cho superficie
    def get_superficie(self):
        return self._superficie

    def set_superficie(self, superficie):
        self._superficie = superficie

    # Getter và Setter cho usage_pattern
    def get_usage_pattern(self):
        return self._usage_pattern

    def set_usage_pattern(self, usage_pattern):
        self._usage_pattern = usage_pattern

    # Getter và Setter cho expiration_date
    def get_expiration_date(self):
        return self._expiration_date

    def set_expiration_date(self, expiration_date):
        self._expiration_date = expiration_date

    # Getter và Setter cho origin_of_use
    def get_origin_of_use(self):
        return self._origin_of_use

    def set_origin_of_use(self, origin_of_use):
        self._origin_of_use = origin_of_use

    # Getter và Setter cho map_sheet
    def get_map_sheet(self):
        return self._map_sheet

    def set_map_sheet(self, map_sheet):
        self._map_sheet = map_sheet

    # Getter và Setter cho purpose_of_use
    def get_purpose_of_use(self):
        return self._purpose_of_use

    def set_purpose_of_use(self, purpose_of_use):
        self._purpose_of_use = purpose_of_use


        






class InformationExtraction(Base):
    def __init__(self):
        pass

    def inner_left_extract(self, content):
        data = {}
        lines = content.split("\n");
        innerLeftPage = InnerLeftPage("","","","","","","","")
        innerLeftPage.set_terrain_non(lines[2][lines[2].find(":"):])
        innerLeftPage.set_map_sheet(lines[3][lines[3].find(":")+1:])
        innerLeftPage.set_address(lines[4][lines[4].find(":") +1 :])
        innerLeftPage.set_superficie(lines[6][lines[6].find(":"):lines[6].find(",")] +"M3")
        innerLeftPage.set_usage_pattern(lines[7])
        innerLeftPage.set_purpose_of_use(lines[9])
        innerLeftPage.set_expiration_date(lines[11])
        innerLeftPage.set_origin_of_use(lines[12] + " " + lines[14])
        
        return vars(innerLeftPage)

  
    
    def front_extract(self, content):
        lines = content.splitlines()
        fontPage = FontPage("","","","")
        name = ""
        while ":" not in lines[0]:
            name = lines[0]
            del lines[0]
            
        if name:
            fontPage.name = name
           
        fontPage.year_of_birth = lines[0][lines[0].find(":") + 1:lines[0].find(",")]
        fontPage.address = lines[1][(lines[1].find(":") +1):] + " " + lines[2]
        fontPage.cmnd = re.findall(r'\d+', lines[0][lines[1].rfind(":"):])
      
        return vars(fontPage)

    def __call__(self, 
                 front: str=None, 
                 inner_left: str=None, 
                 inner_right: str=None, 
                 back: str=None,
                 is_debug: bool=False):
        data = {}
        if front is not None:
            try:
                front_data = self.front_extract(front)
                data["Thông tin về chủ sở hữu"] = front_data
            except Exception as e:
                print(front)
                print(e)

        if inner_left is not None:
            try:
                inner_left_data = self.inner_left_extract(inner_left)
                data["Thửa đất, nhà ở và tài sản khác gắn liền với đất"] = inner_left_data
            except Exception as e:
                print(inner_left)
                print(e)

        if is_debug:
            print(json.dumps(data, indent=4, ensure_ascii=False))
        return data