import os
import time
import json
import math
import random

import nodes
import folder_paths
import comfy.utils
import comfy_execution
from server import PromptServer

MAIN_CATEGORY = "AsyncOutput/Utils"

class AsyncOutputUtilsConvertStringListToStringNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_string_list": ("LIST", { "forceInput": True }),
                "join_word": ("STRING", { "default": "" }),
                "is_escape_char": ("BOOLEAN", { "default": False, "tooltip": "if use ascii escape char, must enable" })
            }
        }
    
    RETURN_TYPES = ("STRING", )
    RETURN_NAMES = ("strings", )
    
    CATEGORY = f'{MAIN_CATEGORY}/String'
    FUNCTION = "convert_string_list_to_string"
    DESCRIPTION = \
    """
    If use `\n` or others escape_char, must enable `is_escape_char`, or not, module will receive `\\n`, that not expected

    support list:
    - `\n`
    - `\t`
    - `\r`
    - `\'`
    - `\"`
    - `\\`
    """
    
    def convert_string_list_to_string(self, input_string_list=None, join_word="", is_escape_char=False):
        
        if isinstance(input_string_list, list) == False:
            raise Exception("ERROR: input_string_list not a list.")
        
        result = join_word

        if is_escape_char == True:
            escape_map = {
                "\\n": "\n",
                "\\t": "\t",
                "\\r": "\r",
                "\\\"": "\"",
                "\\\'": "\'",
                "\\\\": "\\"
            }
            
            for escaped, real in escape_map.items():
                result = result.replace(escaped, real)

        
        result = result.join(input_string_list)

        return (result, )