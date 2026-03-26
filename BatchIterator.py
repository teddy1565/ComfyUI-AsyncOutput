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

MAIN_CATEGORY = "AsyncOutput/BatchIterator"

ASYNC_OUTPUT_BATCH_ITERATOR_GLOBAL_AUTO_RESET = True

ASYNC_OUTPUT_BATCH_ITERATOR_MULTILINE_TEXT_ITERATOR_DICT = {}
ASYNC_OUTPUT_BATCH_ITERATOR_STORAGE_DATA_DICT = {}
ASYNC_OUTPUT_BATCH_ITERATOR_STORAGE_DATA_COUNTER_DICT = {}

class BatchIteratorMultiLineNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "persistence_memory_key_id": ("STRING", {
                    "tootip": "the key id in global memory dict, must not empty string"
                }),
                "text": ("STRING", { "multiline": True }),
                "delimiter": ("STRING", { "multiline": False, "default": "\n" }),
                "skip_empty": ("BOOLEAN", { "default": True }),
            },
            "optional": {
                "mode": (["fixed", "overflow"], {
                    "default": "fixed",
                    "tooltip": \
                    """
                    - fixed:
                        if iterate count >= len(promts):
                            return (comfy_execution.graph.ExecutionBlocker(None), )
                    - overflow:
                        if iterate count >= len(promts):
                            current_index = current_index mod len(promts)
                    """
                }),
                "force_reset": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "If enabled, will force_reset data in global memory"
                }),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID"
            }
        }

    RETURN_TYPES = ("STRING", "INT", )
    RETURN_NAMES = ("text_line", "count", )
    CATEGORY = f'{MAIN_CATEGORY}/String'
    FUNCTION = "text_yield"
    DESCRIPTION = \
    """
    Each Run Task (Prompt),  Will Iterator Once, Output Single String.
    """

    def text_yield(self, persistence_memory_key_id, text, delimiter="\n", skip_empty=True, mode="fixed", force_reset=False, unique_id=0):
        global ASYNC_OUTPUT_BATCH_ITERATOR_MULTILINE_TEXT_ITERATOR_DICT

        if force_reset == True:
            if persistence_memory_key_id in ASYNC_OUTPUT_BATCH_ITERATOR_MULTILINE_TEXT_ITERATOR_DICT:
                del ASYNC_OUTPUT_BATCH_ITERATOR_MULTILINE_TEXT_ITERATOR_DICT[persistence_memory_key_id]
            (comfy_execution.graph.ExecutionBlocker(None), comfy_execution.graph.ExecutionBlocker(None), )
        
        if persistence_memory_key_id not in ASYNC_OUTPUT_BATCH_ITERATOR_MULTILINE_TEXT_ITERATOR_DICT:
            ASYNC_OUTPUT_BATCH_ITERATOR_MULTILINE_TEXT_ITERATOR_DICT[persistence_memory_key_id] = 0

        prompts = text.split(delimiter)

        if skip_empty:
            prompts = [p.strip() for p in prompts if p.strip()]
        else:
            prompts = [p.strip() for p in prompts]

        current_index = ASYNC_OUTPUT_BATCH_ITERATOR_MULTILINE_TEXT_ITERATOR_DICT[persistence_memory_key_id]
        text_line_count = len(prompts)
        
        if current_index >= text_line_count:
            if mode == "fixed":
                return (comfy_execution.graph.ExecutionBlocker(None), comfy_execution.graph.ExecutionBlocker(None), )
            if mode == "overflow":
                current_index = current_index % text_line_count
        else:
            ASYNC_OUTPUT_BATCH_ITERATOR_MULTILINE_TEXT_ITERATOR_DICT[persistence_memory_key_id] += 1
        
        text_ln = prompts[current_index]

        return (text_ln, text_line_count, )

    @classmethod
    def IS_CHANGED(self, persistence_memory_key_id, text, delimiter="\n", mode="fixed", skip_empty=True, force_reset=False, unique_id=0):
	    return float('nan')

class BatchIteratorGlobalCacheClearNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "silent_mode": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "If True, Node Never raise Error, inturrept thread. but not recommend, because you forget it. will be disaster."
                }),
                "force_clear": ("BOOLEAN", {
                    "default": True
                })
            },
            "hidden": {
                "unique_id": "UNIQUE_ID"
            }
        }

    RETURN_TYPES = ("BOOLEAN", )
    RETURN_NAMES = ("void", )
    CATEGORY = f'{MAIN_CATEGORY}/SystemTools'
    FUNCTION = "clear_cache"
    OUTPUT_NODE = True
    DESCRIPTION = \
    """
    Remove BatchIterator All GlobalCache
    """

    def clear_cache(self, silent_mode=False, force_clear=True, unique_id=0):
        global ASYNC_OUTPUT_BATCH_ITERATOR_MULTILINE_TEXT_ITERATOR_DICT
        global ASYNC_OUTPUT_BATCH_ITERATOR_STORAGE_DATA_DICT
        global ASYNC_OUTPUT_BATCH_ITERATOR_STORAGE_DATA_COUNTER_DICT
        
        if force_clear == True:
            for k in list(ASYNC_OUTPUT_BATCH_ITERATOR_MULTILINE_TEXT_ITERATOR_DICT.keys()):
                del ASYNC_OUTPUT_BATCH_ITERATOR_MULTILINE_TEXT_ITERATOR_DICT[k]
            for k in list(ASYNC_OUTPUT_BATCH_ITERATOR_STORAGE_DATA_DICT.keys()):
                del ASYNC_OUTPUT_BATCH_ITERATOR_STORAGE_DATA_DICT[k]
            for k in list(ASYNC_OUTPUT_BATCH_ITERATOR_STORAGE_DATA_COUNTER_DICT.keys()):
                del ASYNC_OUTPUT_BATCH_ITERATOR_STORAGE_DATA_COUNTER_DICT[k]
            
            if silent_mode == False:
                raise Exception("WARRNING: Module AsyncOutput.BatchIterator All GlobalCache are reset, please remove the CacheClear Node or Disable force_clear.")
            else:
                print("WARRNING: Module AsyncOutput.BatchIterator All GlobalCache are reset, please remove the CacheClear Node or Disable force_clear.")
                return (comfy_execution.graph.ExecutionBlocker(None), )
        
        return (comfy_execution.graph.ExecutionBlocker(None), )
        

    @classmethod
    def IS_CHANGED(self, silent_mode=False, force_clear=True, unique_id=0):
	    return float('nan')
    
class BatchIteratorStringCollectionNode:
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
        global ASYNC_OUTPUT_BATCH_ITERATOR_STORAGE_DATA_DICT
        
        if key_id == "":
            raise Exception("ERROR: key_id property not set.")
        
        if key_id not in ASYNC_OUTPUT_BATCH_ITERATOR_STORAGE_DATA_DICT:
            ASYNC_OUTPUT_BATCH_ITERATOR_STORAGE_DATA_DICT[key_id] = []
        
        ASYNC_OUTPUT_BATCH_ITERATOR_STORAGE_DATA_DICT[key_id].append(incoming_input)
        
        return (incoming_input,)
    
    @classmethod
    def IS_CHANGED(s, incoming_input, key_id, unique_id):
	    return float('nan')
    
class BatchIteratorStringEmitterNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "touch": ("BOOLEAN", { "forceInput": True }),
                
                "mode": (["==", ">="], {"default": "=="}),
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
        global ASYNC_OUTPUT_BATCH_ITERATOR_STORAGE_DATA_COUNTER_DICT

        if isinstance(step, int) == False:
            step = int(step)
        if isinstance(conditions, int) == False:
            conditions = int(conditions)
        
        if math.isnan(step) or math.isnan(conditions):
            raise Exception(f'ERROR: step or conditions data type not int. step: {type(step)}, conditions: {type(conditions)}')

        if key_id not in ASYNC_OUTPUT_BATCH_ITERATOR_STORAGE_DATA_COUNTER_DICT:
            ASYNC_OUTPUT_BATCH_ITERATOR_STORAGE_DATA_COUNTER_DICT[key_id] = 0
        k = ASYNC_OUTPUT_BATCH_ITERATOR_STORAGE_DATA_COUNTER_DICT[key_id]

        if reset == True:
            ASYNC_OUTPUT_BATCH_ITERATOR_STORAGE_DATA_COUNTER_DICT[key_id] = 0
            return (k, False)

        if touch == False:
            return (k, False)
        else:
            if key_id not in ASYNC_OUTPUT_BATCH_ITERATOR_STORAGE_DATA_COUNTER_DICT:
                ASYNC_OUTPUT_BATCH_ITERATOR_STORAGE_DATA_COUNTER_DICT[key_id] = 0
            ASYNC_OUTPUT_BATCH_ITERATOR_STORAGE_DATA_COUNTER_DICT[key_id] += step
        
       
        emit_result = False

        if mode == "==" and ASYNC_OUTPUT_BATCH_ITERATOR_STORAGE_DATA_COUNTER_DICT[key_id] == conditions:
            emit_result = True
        elif mode == ">=" and ASYNC_OUTPUT_BATCH_ITERATOR_STORAGE_DATA_COUNTER_DICT[key_id] >= conditions:
            emit_result = True
        
        return (k, emit_result)
    
    @classmethod
    def IS_CHANGED(s, touch, step, conditions, mode, key_id, reset=False, unique_id=0):
	    return float('nan')

class BatchIteratorStringCallbackNode:
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
        global ASYNC_OUTPUT_BATCH_ITERATOR_STORAGE_DATA_DICT

        if reset == True:
            if key_id in ASYNC_OUTPUT_BATCH_ITERATOR_STORAGE_DATA_DICT:
                del ASYNC_OUTPUT_BATCH_ITERATOR_STORAGE_DATA_DICT[key_id]
            return (comfy_execution.graph.ExecutionBlocker(None), )
        
        if emitter_result == False:
            return (comfy_execution.graph.ExecutionBlocker(None), )
        
        if emitter_result == True:
            if key_id not in ASYNC_OUTPUT_BATCH_ITERATOR_STORAGE_DATA_DICT:
                return (comfy_execution.graph.ExecutionBlocker(None), )
        
            data = ASYNC_OUTPUT_BATCH_ITERATOR_STORAGE_DATA_DICT[key_id]
            return (data, )
        
        return (comfy_execution.graph.ExecutionBlocker(None), )
                
    @classmethod
    def IS_CHANGED(s, emitter_result, key_id, reset=False, unique_id=0):
	    return float('nan')