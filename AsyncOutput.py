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
from server import PromptServer




MAIN_CATEGORY = "AsyncOutput"

ASYNC_OUTPUT_STORAGE_DATA = {}
ASYNC_OUTPUT_COUNTER = {}
ASYNC_OUTPUT_MULTI_LINE_TEXT_YIELD_ID_DECT = {}


ASYNC_OUTPUT_EXTRA_KEY = "ASYNC_OUTPUT"
ASYNC_OUTPUT_INIT_SINGAL_KEY = "INIT_SIGNAL"

def onprompt(json_data):

    if ASYNC_OUTPUT_EXTRA_KEY not in json_data.extra:
        json_data.extra[ASYNC_OUTPUT_EXTRA_KEY] = {}

    ASYNC_OUTPUT_EXTRA_DICT = json_data.extra[ASYNC_OUTPUT_EXTRA_KEY]

    if ASYNC_OUTPUT_INIT_SINGAL_KEY not in ASYNC_OUTPUT_EXTRA_DICT:
        ASYNC_OUTPUT_EXTRA_DICT[ASYNC_OUTPUT_INIT_SINGAL_KEY] = False
    json_data.extra[ASYNC_OUTPUT_EXTRA_KEY][ASYNC_OUTPUT_INIT_SINGAL_KEY] = False

    return json_data

PromptServer.instance.on_prompt_handlers.append(onprompt)

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
                "join_word": ("STRING", { "default": "" }),
                "is_escape_char": ("BOOLEAN", { "default": False, "tooltip": "if use ascii escape char, must enable" })
            }
        }
    
    RETURN_TYPES = ("STRING", )
    RETURN_NAMES = ("strings", )
    
    CATEGORY = f'{MAIN_CATEGORY}/Utils'
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
    
    def convert_string_list_to_string(self, input_string_list=[], join_word="", is_escape_char=False):
        
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
            
class AsyncOutputMultiLineTextWithBatchNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "touch": ("BOOLEAN", { "forceInput": True }),
                "eof_size": ("INT", { "forceInput": True }),
                "text": ("STRING", { "multiline": True }),
                "remove_words": ("*", { "forceInput": True }),
                "delimiter": ("STRING", { "multiline": False, "default": "\n" }),
                "skip_empty": ("BOOLEAN", { "default": True }),
            },
            "optional": {
                "remove_words": ("*", { "forceInput": True })
            },
            "hidden": {
                "unique_id": "UNIQUE_ID"
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text_line",)
    CATEGORY = f'{MAIN_CATEGORY}/WorkFlowTool'
    FUNCTION = "batch_text_yield"
    
    def batch_text_yield(self, touch, eof_size, text, delimiter="\n", skip_empty=True, remove_words=[], unique_id=0):
        
        global ASYNC_OUTPUT_MULTI_LINE_TEXT_YIELD_ID_DECT

        if touch != True:
            return (comfy_execution.graph.ExecutionBlocker(None), )
        

        if unique_id not in ASYNC_OUTPUT_MULTI_LINE_TEXT_YIELD_ID_DECT:
            ASYNC_OUTPUT_MULTI_LINE_TEXT_YIELD_ID_DECT[unique_id] = 0
        
        current_line_index = ASYNC_OUTPUT_MULTI_LINE_TEXT_YIELD_ID_DECT[unique_id]
        ASYNC_OUTPUT_MULTI_LINE_TEXT_YIELD_ID_DECT[unique_id] += 1

        prompts = text.split(delimiter)

        if skip_empty:
            prompts = [p.strip() for p in prompts if p.strip()]
        else:
            prompts = [p.strip() for p in prompts]
        
        
        if ASYNC_OUTPUT_MULTI_LINE_TEXT_YIELD_ID_DECT[unique_id] == eof_size:
            del ASYNC_OUTPUT_MULTI_LINE_TEXT_YIELD_ID_DECT[unique_id]

        current_line_promts = prompts[current_line_index]
        
        if isinstance(remove_words, list):
            for word in remove_words:
                if isinstance(word, str):
                    current_line_promts = current_line_promts.replace(word, "")

        return (current_line_promts,)
    
    @classmethod
    def IS_CHANGED(s, touch, eof_size, text, delimiter="\n", skip_empty=True, remove_words=[], unique_id=0):
	    return float('nan')

class AsyncOutputInitSignalOutputNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "always_output": ("BOOLEAN", { "default": False, "tooltip": "if false, only emit once. else every runtime loop tick send." })
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO",
            }
        }
    
    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("init_signal",)
    CATEGORY = f'{MAIN_CATEGORY}/WorkFlowTool'
    FUNCTION = "init_signal"
    
    def init_signal(self, always_output, unique_id, prompt, extra_pnginfo):

        WORKFLOW = "workflow"
        EXTRA = "extra"
        if WORKFLOW in extra_pnginfo:
            if EXTRA in extra_pnginfo[WORKFLOW]:
                if ASYNC_OUTPUT_EXTRA_KEY in extra_pnginfo[WORKFLOW][EXTRA]:
                    if ASYNC_OUTPUT_INIT_SINGAL_KEY in extra_pnginfo[WORKFLOW][EXTRA][ASYNC_OUTPUT_EXTRA_KEY]:
                        if extra_pnginfo[WORKFLOW][EXTRA][ASYNC_OUTPUT_EXTRA_KEY][ASYNC_OUTPUT_INIT_SINGAL_KEY] == False:
                            extra_pnginfo[WORKFLOW][EXTRA][ASYNC_OUTPUT_EXTRA_KEY][ASYNC_OUTPUT_INIT_SINGAL_KEY] = True
                            return (True, )
                        else:
                            if always_output == True:
                                return (False, )
    
        return (comfy_execution.graph.ExecutionBlocker(None), )

        
    
    @classmethod
    def IS_CHANGED(s, always_output, unique_id, prompt, extra_pnginfo):
	    return float('nan')