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
                "force_clear": ("BOOLEAN", { "default": True })
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

    def clear_cache(self, force_clear=True, unique_id=0):
        global ASYNC_OUTPUT_BATCH_ITERATOR_MULTILINE_TEXT_ITERATOR_DICT
        
        if force_clear == True:
            for k in list(ASYNC_OUTPUT_BATCH_ITERATOR_MULTILINE_TEXT_ITERATOR_DICT.keys()):
                del ASYNC_OUTPUT_BATCH_ITERATOR_MULTILINE_TEXT_ITERATOR_DICT[k]
            raise Exception("WARRNING: Module AsyncOutput.BatchIterator All GlobalCache are reset, please remove the CacheClear Node or Disable force_clear.")
        
        return (comfy_execution.graph.ExecutionBlocker(None), )
        

    @classmethod
    def IS_CHANGED(self, force_clear=True, unique_id=0):
	    return float('nan')