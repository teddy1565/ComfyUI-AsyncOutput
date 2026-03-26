"""
@Author: teddy1565
@Description: Custom nodes for ComfyUI to Convert AsyncOutput
@Nickname: AsyncOutput
@Version: 0.0.1 ALPHA
@URL: https://github.com/teddy1565/ComfyUI-AsyncOutput


NOT RECOMMENDED USE, Because ComfyUI not real support change status in upstream on a workflow.

So Many Design not real match this scheduler(scope), it't not a real Turing complete.
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




MAIN_CATEGORY = "AsyncOutput/Deprecated(ComfyUI NOT Turing complete)"
ASYNC_OUTPUT_GLOBAL_AUTO_RESET = True

ASYNC_OUTPUT_STORAGE_DATA = {}
ASYNC_OUTPUT_COUNTER = {}
ASYNC_OUTPUT_MULTI_LINE_TEXT_YIELD_ID_DECT = {}
ASYNC_OUTPUT_MULTI_LINE_TEXT_YIELD_TICK_DICT = {}

ASYNC_OUTPUT_REMOTE_CONTROL_DATA = {}
ASYNC_OUTPUT_REMOTE_CONTROL_TICK_DICT = {}
ASYNC_OUTPUT_REMOTE_CONTROL_WITH_MULTI_LINE_TEXT_TICK_ID_DICT = {}

ASYNC_OUTPUT_EXTRA_KEY = "ASYNC_OUTPUT"
ASYNC_OUTPUT_INIT_SINGAL_KEY = "INIT_SIGNAL"
ASYNC_OUTPUT_INIT_REMOTE_CONTROL_KEY = "REMOTE_CONTROL_DATA_INITED"

def onprompt(json_data):
    # print(list(json_data.keys()))
    # print(list(json_data["extra_data"].keys()))
    # print(list(json_data["extra_data"]["extra_pnginfo"].keys()))
    # print(list(json_data["extra_data"]["extra_pnginfo"]["workflow"].keys()))
    # print(list(json_data["extra_data"]["extra_pnginfo"]["workflow"]["extra"].keys()))
    data_info = json_data["extra_data"]["extra_pnginfo"]["workflow"]["extra"]

    if ASYNC_OUTPUT_EXTRA_KEY not in data_info:
        data_info[ASYNC_OUTPUT_EXTRA_KEY] = {}

    ASYNC_OUTPUT_EXTRA_DICT = data_info[ASYNC_OUTPUT_EXTRA_KEY]

    if ASYNC_OUTPUT_INIT_SINGAL_KEY not in ASYNC_OUTPUT_EXTRA_DICT:
        ASYNC_OUTPUT_EXTRA_DICT[ASYNC_OUTPUT_INIT_SINGAL_KEY] = False
    ASYNC_OUTPUT_EXTRA_DICT[ASYNC_OUTPUT_INIT_SINGAL_KEY] = False

    if ASYNC_OUTPUT_GLOBAL_AUTO_RESET == True:
        remote_control_data_keys = list(ASYNC_OUTPUT_REMOTE_CONTROL_DATA.keys())
        remote_control_tick_keys = list(ASYNC_OUTPUT_REMOTE_CONTROL_TICK_DICT.keys())
        remote_control_with_multiline_text_tick_keys = list(ASYNC_OUTPUT_REMOTE_CONTROL_WITH_MULTI_LINE_TEXT_TICK_ID_DICT.keys())
        async_output_storage_data = list(ASYNC_OUTPUT_STORAGE_DATA.keys())
        async_output_counter_data = list(ASYNC_OUTPUT_COUNTER.keys())
        async_output_multiline_yield_id_data = list(ASYNC_OUTPUT_MULTI_LINE_TEXT_YIELD_ID_DECT.keys())
        async_output_multiline_yield_tick_data = list(ASYNC_OUTPUT_MULTI_LINE_TEXT_YIELD_TICK_DICT.keys())

        for k in remote_control_data_keys:
            del ASYNC_OUTPUT_REMOTE_CONTROL_DATA[k]
        for k in remote_control_tick_keys:
            del ASYNC_OUTPUT_REMOTE_CONTROL_TICK_DICT[k]
        for k in remote_control_with_multiline_text_tick_keys:
            del ASYNC_OUTPUT_REMOTE_CONTROL_WITH_MULTI_LINE_TEXT_TICK_ID_DICT[k]
        for k in async_output_storage_data:
            del ASYNC_OUTPUT_STORAGE_DATA[k]
        for k in async_output_counter_data:
            del ASYNC_OUTPUT_COUNTER[k]
        for k in async_output_multiline_yield_id_data:
            del ASYNC_OUTPUT_MULTI_LINE_TEXT_YIELD_ID_DECT[k]
        for k in async_output_multiline_yield_tick_data:
            del ASYNC_OUTPUT_MULTI_LINE_TEXT_YIELD_TICK_DICT[k]


    if ASYNC_OUTPUT_INIT_REMOTE_CONTROL_KEY not in ASYNC_OUTPUT_EXTRA_DICT:
        ASYNC_OUTPUT_EXTRA_DICT[ASYNC_OUTPUT_INIT_REMOTE_CONTROL_KEY] = True

    return json_data

PromptServer.instance.on_prompt_handlers.append(onprompt)

# ======================================================== Global Config Node ========================================

class AsyncOutputGlobalAutoResetNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "global_auto_reset": ("BOOLEAN", { "default": True })
            },
            "hidden": {
                "unique_id": "UNIQUE_ID"
            }
        }
    
    OUTPUT_NODE = True
    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("AsyncOutputModule_AutoReset",)
    CATEGORY = f'{MAIN_CATEGORY}/Global'
    FUNCTION = "auto_reset"
    
    def auto_reset(self, global_auto_reset, unique_id):
        global ASYNC_OUTPUT_GLOBAL_AUTO_RESET

        if isinstance(global_auto_reset, bool):
            ASYNC_OUTPUT_GLOBAL_AUTO_RESET = global_auto_reset
            return (ASYNC_OUTPUT_GLOBAL_AUTO_RESET, )
        else:
            return (comfy_execution.graph.ExecutionBlocker(None), )
    
    @classmethod
    def IS_CHANGED(s, global_auto_reset, unique_id):
	    return float('nan')
class AsyncOutputGlobalManualResetNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "reset_all_memory": ("BOOLEAN", { "default": False })
            },
            "hidden": {
                "unique_id": "UNIQUE_ID"
            }
        }
    
    OUTPUT_NODE = True
    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("reset result",)
    CATEGORY = f'{MAIN_CATEGORY}/Global/ManualOperation'
    FUNCTION = "manual_reset"
    
    def manual_reset(self, reset_all_memory, unique_id):
        global ASYNC_OUTPUT_GLOBAL_AUTO_RESET

        global ASYNC_OUTPUT_STORAGE_DATA
        global ASYNC_OUTPUT_COUNTER
        global ASYNC_OUTPUT_MULTI_LINE_TEXT_YIELD_ID_DECT
        global ASYNC_OUTPUT_REMOTE_CONTROL_DATA
        global ASYNC_OUTPUT_REMOTE_CONTROL_TICK_DICT
        global ASYNC_OUTPUT_MULTI_LINE_TEXT_YIELD_TICK_DICT
        global ASYNC_OUTPUT_REMOTE_CONTROL_WITH_MULTI_LINE_TEXT_TICK_ID_DICT

        ASYNC_OUTPUT_STORAGE_DATA = {}
        ASYNC_OUTPUT_COUNTER = {}
        ASYNC_OUTPUT_MULTI_LINE_TEXT_YIELD_ID_DECT = {}
        ASYNC_OUTPUT_REMOTE_CONTROL_DATA = {}
        ASYNC_OUTPUT_REMOTE_CONTROL_TICK_DICT = {}
        ASYNC_OUTPUT_MULTI_LINE_TEXT_YIELD_TICK_DICT = {}
        ASYNC_OUTPUT_REMOTE_CONTROL_WITH_MULTI_LINE_TEXT_TICK_ID_DICT = {}

        print(f'[AsyncOutput]: Current AUTO_RESET on {"`Enabled`" if ASYNC_OUTPUT_GLOBAL_AUTO_RESET == True else "`Disabled`"}')
        print(f'[AsyncOutput]: Enabled -> each Run Batch auto Reset | Disabled -> Never Auto Reset, Until ComfyUI process exit')

        if isinstance(reset_all_memory, bool):
            ASYNC_OUTPUT_GLOBAL_AUTO_RESET = reset_all_memory
            return (ASYNC_OUTPUT_GLOBAL_AUTO_RESET, )
        else:
            return (comfy_execution.graph.ExecutionBlocker(None), )
    
    @classmethod
    def IS_CHANGED(s, reset_all_memory, unique_id):
	    return float('nan')

# ============================================================================================================

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

class AsyncOutputRemoteCollectionNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "touch": ("BOOLEAN", { "forceInput": True }),
                "key_id": ("STRING", {}),
                "with_AsyncOutput_multiline_prompt_batch": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "if want sync multiline prompt batch, need enable this."
                }),
            },
            "optional": {
                "multiline_trigger_control_unique_id": ("STRING", {
                    "forceInput": True,
                    "tooltip": "should input a unique_id, AsyncOutput multi text node will reference this id."
                }),
                "multiline_tick_index": ("INT", {
                    "default": -1,
                    "tooltip": "a group shared reference same tick. sync this group tick"
                }),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID"
            }
        }
    
    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("passthough_output",)
    CATEGORY = f'{MAIN_CATEGORY}/RemoteControl'
    FUNCTION = "collect"
    
    def collect(self, touch, key_id, with_AsyncOutput_multiline_prompt_batch=False, multiline_trigger_control_unique_id="", multiline_tick_index=-1, unique_id=0):
        global ASYNC_OUTPUT_REMOTE_CONTROL_DATA
        global ASYNC_OUTPUT_REMOTE_CONTROL_WITH_MULTI_LINE_TEXT_TICK_ID_DICT

        
        
        if with_AsyncOutput_multiline_prompt_batch == True:
            # 等待實作
            if isinstance(multiline_tick_index, int) == False:
                multiline_tick_index = int(multiline_tick_index)
            if multiline_trigger_control_unique_id == None:
                raise Exception("ERROR: (in remote control collect) with_AsyncOutput_multiline_prompt_batch enabled, must input a vaild string")
            elif isinstance(multiline_trigger_control_unique_id, str) == False:
                multiline_trigger_control_unique_id = str(multiline_trigger_control_unique_id)
            if multiline_trigger_control_unique_id == "":
                raise Exception("ERROR: multiline_trigger_control_unique_id must a not empty string.")
            
            if multiline_trigger_control_unique_id not in ASYNC_OUTPUT_REMOTE_CONTROL_WITH_MULTI_LINE_TEXT_TICK_ID_DICT:
                ASYNC_OUTPUT_REMOTE_CONTROL_WITH_MULTI_LINE_TEXT_TICK_ID_DICT[multiline_trigger_control_unique_id] = 0
            ASYNC_OUTPUT_REMOTE_CONTROL_WITH_MULTI_LINE_TEXT_TICK_ID_DICT[multiline_trigger_control_unique_id] += 1

        if key_id == "":
            raise Exception("ERROR: key_id property not set.")
        
        if key_id not in ASYNC_OUTPUT_REMOTE_CONTROL_DATA:
            ASYNC_OUTPUT_REMOTE_CONTROL_DATA[key_id] = 0
        
        ASYNC_OUTPUT_REMOTE_CONTROL_DATA[key_id] += 1
        
        return (touch,)
    
    @classmethod
    def IS_CHANGED(s, touch, key_id, with_AsyncOutput_multiline_prompt_batch=False, multiline_trigger_control_unique_id=-1, multiline_tick_index=-1, unique_id=0):
	    return float('nan')

class AsyncOutputRemoteTriggerNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "key_id": ("STRING", {  }),
                "conditions": ("INT", { "default": 1, "min": 0 }),
                "mode": (["==", "<", ">", "<=", ">=", "!="], {"default": "=="})
            },
            "optional": {
                "tick_output": ("BOOLEAN", { "defaultInput": False }),
                "reset": ("BOOLEAN", { "defaultInput": False })
            },
            "hidden": {
                "unique_id": "UNIQUE_ID"
            }
        }
    
    RETURN_TYPES = ("BOOLEAN", "INT", )
    RETURN_NAMES = ("bool", "tick_index", )
    OUTPUT_NODE = True
    CATEGORY = f'{MAIN_CATEGORY}/RemoteControl'
    FUNCTION = "remote_trigger"
    DESCRIPTION = \
    """
    Remote Trigger, If conditions true, return true else false
    """
    
    def remote_trigger(self, key_id, conditions, mode, tick_output=False, reset=False, unique_id=0):
        global ASYNC_OUTPUT_REMOTE_CONTROL_DATA
        global ASYNC_OUTPUT_REMOTE_CONTROL_TICK_DICT

        if isinstance(conditions, int) == False:
            conditions = int(conditions)

        if reset == True:
            if key_id in ASYNC_OUTPUT_REMOTE_CONTROL_DATA:
                del ASYNC_OUTPUT_REMOTE_CONTROL_DATA[key_id]
            if key_id in ASYNC_OUTPUT_REMOTE_CONTROL_TICK_DICT:
                del ASYNC_OUTPUT_REMOTE_CONTROL_TICK_DICT[key_id]
            return (False, -1, )
        
        if tick_output == True:
            if key_id not in ASYNC_OUTPUT_REMOTE_CONTROL_DATA:
                ASYNC_OUTPUT_REMOTE_CONTROL_TICK_DICT[key_id] = -1
                ASYNC_OUTPUT_REMOTE_CONTROL_DATA[key_id] = 0
            elif key_id not in ASYNC_OUTPUT_REMOTE_CONTROL_TICK_DICT:
                ASYNC_OUTPUT_REMOTE_CONTROL_TICK_DICT[key_id] = -1
                

        if key_id not in ASYNC_OUTPUT_REMOTE_CONTROL_DATA:
            return (False, -1, )
        
        
        res = False
        tick_index = -1
        if mode == "==":
            res = (conditions == ASYNC_OUTPUT_REMOTE_CONTROL_DATA[key_id])
        elif mode == "!=":
            res = (conditions != ASYNC_OUTPUT_REMOTE_CONTROL_DATA[key_id])
        elif mode == ">":
            res = (conditions > ASYNC_OUTPUT_REMOTE_CONTROL_DATA[key_id])
        elif mode == "<":
            res = (conditions < ASYNC_OUTPUT_REMOTE_CONTROL_DATA[key_id])
        elif mode == ">=":
            res = (conditions >= ASYNC_OUTPUT_REMOTE_CONTROL_DATA[key_id])
        elif mode == "<=":
            res = (conditions <= ASYNC_OUTPUT_REMOTE_CONTROL_DATA[key_id])

        if tick_output == True:
            count = ASYNC_OUTPUT_REMOTE_CONTROL_DATA[key_id]
            tick_count = ASYNC_OUTPUT_REMOTE_CONTROL_TICK_DICT[key_id]
            if tick_count == -1 and tick_count < count:
                ASYNC_OUTPUT_REMOTE_CONTROL_TICK_DICT[key_id] += 1
                return (True, -1, )
            elif tick_count < count:
                tick_index = ASYNC_OUTPUT_REMOTE_CONTROL_TICK_DICT[key_id]
                ASYNC_OUTPUT_REMOTE_CONTROL_TICK_DICT[key_id] += 1
                return (res, tick_index, )
            else:
                return (False, -1, )


        return (res, tick_index, )
                
    @classmethod
    def IS_CHANGED(s, key_id, conditions, mode, tick_output=False, reset=False, unique_id=0):
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
                "with_tick": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Recommend use false, else maybe blocking downstream"
                }),
                "delimiter": ("STRING", { "multiline": False, "default": "\n" }),
                "skip_empty": ("BOOLEAN", { "default": True }),
            },
            "optional": {
                "tick_index": ("INT", { "forceInput": True }),
                "remove_words": ("*", { "forceInput": True }),
                "with_remote_control_collect": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "If want control a loop, enable this, it will sync with a remote control collect node"
                }),
                "multiline_trigger_control_unique_id": ("STRING", {
                    "forceInput": True,
                    "tooltip": "must use same unique_id with othter multiline trigger and remote control collect node"
                }),
                "after_init_loop": ("BOOLEAN", {
                    "forceInput": True,
                    "lazy": True,
                    "default": False,
                    "tooltip": "If enable with_remote_control_collect, must with this singal index"
                }),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID"
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text_line",)
    CATEGORY = f'{MAIN_CATEGORY}/WorkFlowTool'
    FUNCTION = "batch_text_yield"
    DESCRIPTION = \
    """
    Async Output Multi Line Text With Batch,

    it can output first line, then wait unit prev workflow loop done, trigger next loop
    """
    
    def batch_text_yield(self, touch, eof_size, text, with_tick=False, delimiter="\n", skip_empty=True, tick_index=-1, remove_words=None, with_remote_control_collect=False, multiline_trigger_control_unique_id="", after_init_loop=False, unique_id=0):
        
        global ASYNC_OUTPUT_MULTI_LINE_TEXT_YIELD_ID_DECT
        global ASYNC_OUTPUT_MULTI_LINE_TEXT_YIELD_TICK_DICT

        if touch != True:
            return (comfy_execution.graph.ExecutionBlocker(None), )
        
        if isinstance(with_tick, bool) == False:
            with_tick = bool(with_tick)
        
        if with_tick == True:
            if isinstance(tick_index, int) == False:
                tick_index = int(tick_index)

            if unique_id not in ASYNC_OUTPUT_MULTI_LINE_TEXT_YIELD_TICK_DICT:
                ASYNC_OUTPUT_MULTI_LINE_TEXT_YIELD_TICK_DICT[unique_id] = 0
            if tick_index >= ASYNC_OUTPUT_MULTI_LINE_TEXT_YIELD_TICK_DICT[unique_id]:
                return (comfy_execution.graph.ExecutionBlocker(None), )
            if tick_index < ASYNC_OUTPUT_MULTI_LINE_TEXT_YIELD_TICK_DICT[unique_id]:
                ASYNC_OUTPUT_MULTI_LINE_TEXT_YIELD_TICK_DICT[unique_id] += 1
            
        

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

        if current_line_index >= len(prompts):
            current_line_index = current_line_index % len(prompts)
        current_line_promts = prompts[current_line_index]
        
        if isinstance(remove_words, list):
            for word in remove_words:
                if isinstance(word, str):
                    current_line_promts = current_line_promts.replace(word, "")

        return (current_line_promts,)
    
    # special method with comfyUI
    def check_lazy_status(self, touch, eof_size, text, with_tick=False, delimiter="\n", skip_empty=True, tick_index=-1, remove_words=[], with_remote_control_collect=False, multiline_trigger_control_unique_id="", after_init_loop=False, unique_id=0):
        global ASYNC_OUTPUT_REMOTE_CONTROL_WITH_MULTI_LINE_TEXT_TICK_ID_DICT

        needed = []
        if with_remote_control_collect == True:
            if multiline_trigger_control_unique_id == None:
                raise Exception("ERROR: with_remote_control_collect enabled, must input a vaild string")
            elif isinstance(multiline_trigger_control_unique_id, str) == False:
                multiline_trigger_control_unique_id = str(multiline_trigger_control_unique_id)
            if multiline_trigger_control_unique_id == "":
                raise Exception(f"ERROR: (in batch_text_yield)[unique_id: {unique_id}] multiline_trigger_control_unique_id must a not empty string.")
            if multiline_trigger_control_unique_id in ASYNC_OUTPUT_REMOTE_CONTROL_WITH_MULTI_LINE_TEXT_TICK_ID_DICT and ASYNC_OUTPUT_REMOTE_CONTROL_WITH_MULTI_LINE_TEXT_TICK_ID_DICT[multiline_trigger_control_unique_id] > 0:
                needed.append("after_init_loop")
        
        return needed
        
    
    @classmethod
    def IS_CHANGED(self, touch, eof_size, text, with_tick=False, delimiter="\n", skip_empty=True, tick_index=-1, remove_words=[], with_remote_control_collect=False, multiline_trigger_control_unique_id="", after_init_loop=False, unique_id=0):
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
        print(list(extra_pnginfo.keys()))
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