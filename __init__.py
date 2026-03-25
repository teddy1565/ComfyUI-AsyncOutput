"""
@Author: teddy1565
@Description: Async Output Initializer
@Title: AsyncOutputUtils
@Nickname: AsyncOutputUtils
"""

from . import AsyncOutput

NODE_CLASS_MAPPINGS = {
    "AsyncOutputCollect": AsyncOutput.AsyncOutputCollectionNode,
    "AsyncOutputEmitter": AsyncOutput.AsyncOutputEmitterNode,
    "AsyncOutputCallback": AsyncOutput.AsyncOutputCallbackNode,
    "AsyncOutputConvertStringListToString": AsyncOutput.AsyncOutputConvertStringListToStringNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AsyncOutputCollect": "Collection",
    "AsyncOutputEmitter": "Conditions",
    "AsyncOutputCallback": "Output",
    "AsyncOutputConvertStringListToString": "String List To String",
}

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS"
]