"""
@Author: teddy1565
@Description: Custom nodes for ComfyUI to Convert AsyncOutput
@Nickname: AsyncOutput
@Version: 0.0.1 ALPHA
@URL: https://github.com/teddy1565/ComfyUI-AsyncOutput
"""

import os
import time
import json
import math
import random

import nodes
import folder_paths
import comfy.utils
import comfy_execution



MAIN_CATEGORY = "AsyncOutput"

ASYNC_OUTPUT_STORAGE_DATA = {}
ASYNC_OUTPUT_COUNTER = {}

class AsyncOutputCollectionNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "incoming_input": ("STRING", { "forceInput": True }),
                "key_id": ("STRING", {})
            },
            "hidden": {
                "unique_id": "UNIQUE_ID"
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("passthough_output",)
    CATEGORY = f'{MAIN_CATEGORY}/String'
    FUNCTION = "collect"
    
    def collect(self, incoming_input, key_id, unique_id):
        global ASYNC_OUTPUT_STORAGE_DATA
        
        if key_id == "":
            raise Exception("ERROR: key_id property not set.")
        
        if key_id not in ASYNC_OUTPUT_STORAGE_DATA:
            ASYNC_OUTPUT_STORAGE_DATA[key_id] = []
        
        ASYNC_OUTPUT_STORAGE_DATA[key_id].append(incoming_input)
        
        return (incoming_input,)
    
    @classmethod
    def IS_CHANGED(s, incoming_input, key_id, unique_id):
	    return float('nan')
    
class AsyncOutputEmitterNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "touch": ("BOOLEAN", { "forceInput": True }),
                
                "mode": (["exact", "greater_than_or_equal"], {"default": "exact"}),
                "key_id": ("STRING", {}),
                "step": ("INT", { "default": 1, "min": 1 }),
                "conditions": ("INT", { "min": 0, "default": 1 }),
            },
            "optional": {
                "reset": ("BOOLEAN", { "defaultInput": False })
            },
            "hidden": {
                "unique_id": "UNIQUE_ID"
            }
        }
    
    RETURN_TYPES = ("INT", "BOOLEAN",)
    RETURN_NAMES = ("count", "emit_result",)
    OUTPUT_TOOLTIPS = ("Current Count Value", "if count == conditions, return true. then remove this record")
    CATEGORY = f'{MAIN_CATEGORY}/String'
    FUNCTION = "emit"
    
    def emit(self, touch, mode, key_id, step=1, conditions=1, reset=False, unique_id=0):
        global ASYNC_OUTPUT_COUNTER

        if isinstance(step, int) == False:
            step = int(step)
        if isinstance(conditions, int) == False:
            conditions = int(conditions)
        
        if math.isnan(step) or math.isnan(conditions):
            raise Exception(f'ERROR: step or conditions data type not int. step: {type(step)}, conditions: {type(conditions)}')

        if key_id not in ASYNC_OUTPUT_COUNTER:
            ASYNC_OUTPUT_COUNTER[key_id] = 0
        k = ASYNC_OUTPUT_COUNTER[key_id]

        if reset == True:
            ASYNC_OUTPUT_COUNTER[key_id] = 0
            return (k, False)

        if touch == False:
            return (k, False)
        else:
            if key_id not in ASYNC_OUTPUT_COUNTER:
                ASYNC_OUTPUT_COUNTER[key_id] = 0
            ASYNC_OUTPUT_COUNTER[key_id] += step
        
       
        emit_result = False

        if mode == "exact" and ASYNC_OUTPUT_COUNTER[key_id] == conditions:
            if key_id in ASYNC_OUTPUT_COUNTER:
                del ASYNC_OUTPUT_COUNTER[key_id]
            emit_result = True
        elif mode == "greater_than_or_equal" and ASYNC_OUTPUT_COUNTER[key_id] >= conditions:
            if key_id in ASYNC_OUTPUT_COUNTER:
                    del ASYNC_OUTPUT_COUNTER[key_id]
            emit_result = True
        
        return (k, emit_result)
    
    @classmethod
    def IS_CHANGED(s, touch, step, conditions, mode, key_id, reset=False, unique_id=0):
	    return float('nan')
            

   
class AsyncOutputCallbackNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "emitter_result": ("BOOLEAN", { "forceInput": True }),
                "key_id": ("STRING", {  })
            },
            "optional": {
                "reset": ("BOOLEAN", { "defaultInput": False })
            },
            "hidden": {
                "unique_id": "UNIQUE_ID"
            }
        }
    
    RETURN_TYPES = ("LIST", )
    RETURN_NAMES = ("output_list", )
    
    CATEGORY = f'{MAIN_CATEGORY}/String'
    FUNCTION = "get_collection"
    
    def get_collection(self, emitter_result, key_id, reset=False, unique_id=0):
        global ASYNC_OUTPUT_STORAGE_DATA

        if reset == True:
            if key_id in ASYNC_OUTPUT_STORAGE_DATA:
                del ASYNC_OUTPUT_STORAGE_DATA[key_id]
            return (comfy_execution.graph.ExecutionBlocker(None), )
        
        if emitter_result == False:
            return (comfy_execution.graph.ExecutionBlocker(None), )
        
        if emitter_result == True:
            if key_id not in ASYNC_OUTPUT_STORAGE_DATA:
                return (comfy_execution.graph.ExecutionBlocker(None), )
        
            data = ASYNC_OUTPUT_STORAGE_DATA[key_id]
            del ASYNC_OUTPUT_STORAGE_DATA[key_id]
            return (data, )
        
        return (comfy_execution.graph.ExecutionBlocker(None), )
                
    @classmethod
    def IS_CHANGED(s, emitter_result, key_id, reset=False, unique_id=0):
	    return float('nan')
            


class AsyncOutputConvertStringListToStringNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_string_list": ("LIST", { "forceInput": True }),
                "join_word": ("STRING", { "default": "\n" })
            }
        }
    
    RETURN_TYPES = ("STRING", )
    RETURN_NAMES = ("strings", )
    
    CATEGORY = f'{MAIN_CATEGORY}/Utils'
    FUNCTION = "convert_string_list_to_string"
    
    def convert_string_list_to_string(self, input_string_list=[], join_word="\n"):
        
        if isinstance(input_string_list, list) == False:
            raise Exception("ERROR: input_string_list not a list.")
        
        result = join_word
        result.join(input_string_list)
        
        return result
            

