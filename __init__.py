"""
@Author: teddy1565
@Description: Async Output Initializer
@Title: AsyncOutputUtils
@Nickname: AsyncOutputUtils
"""

from . import AsyncOutput
from . import BatchIterator
from . import Utils

NODE_CLASS_MAPPINGS = {
    "AsyncOutputCollect": AsyncOutput.AsyncOutputCollectionNode,
    "AsyncOutputEmitter": AsyncOutput.AsyncOutputEmitterNode,
    "AsyncOutputCallback": AsyncOutput.AsyncOutputCallbackNode,
    "AsyncOutputConvertStringListToString": AsyncOutput.AsyncOutputConvertStringListToStringNode,
    "AsyncOutputMultiLineTextWithBatch": AsyncOutput.AsyncOutputMultiLineTextWithBatchNode,
    "AsyncOutputInitSignalOutput": AsyncOutput.AsyncOutputInitSignalOutputNode,
    "AsyncOutputRemoteCollection": AsyncOutput.AsyncOutputRemoteCollectionNode,
    "AsyncOutputRemoteTrigger": AsyncOutput.AsyncOutputRemoteTriggerNode,
    "AsyncOutputGlobalAutoReset": AsyncOutput.AsyncOutputGlobalAutoResetNode,
    "AsyncOutputGlobalManualReset": AsyncOutput.AsyncOutputGlobalManualResetNode,

    "BatchIteratorMultiLine": BatchIterator.BatchIteratorMultiLineNode,
    "BatchIteratorGlobalCacheClear": BatchIterator.BatchIteratorGlobalCacheClearNode,
    "BatchIteratorStringCollection": BatchIterator.BatchIteratorStringCollectionNode,
    "BatchIteratorStringEmitter": BatchIterator.BatchIteratorStringEmitterNode,
    "BatchIteratorStringCallback": BatchIterator.BatchIteratorStringCallbackNode,

    "UtilsConvertStringListToStringNode": Utils.AsyncOutputUtilsConvertStringListToStringNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AsyncOutputCollect": "Collection",
    "AsyncOutputEmitter": "Conditions",
    "AsyncOutputCallback": "Output",
    "AsyncOutputConvertStringListToString": "String List To String",
    "AsyncOutputMultiLineTextWithBatch": "Batch Text Yield With Batch",
    "AsyncOutputInitSignalOutput": "Init Singal Output",
    "AsyncOutputRemoteCollection": "Remote Collect",
    "AsyncOutputRemoteTrigger": "Remote Trigger",
    "AsyncOutputGlobalAutoReset": "AsyncOutput[module_config] Global Auto Reset",
    "AsyncOutputGlobalManualReset": "AsyncOutput[module_config] Global Memory Reset",

    "BatchIteratorMultiLine": "Multiline Text Iterator",
    "BatchIteratorGlobalCacheClear": "BatchIterator GlobalCache Clear",
    "BatchIteratorStringCollection": "BatchIterator String Collection",
    "BatchIteratorStringEmitter": "BatchIterator String Emitter",
    "BatchIteratorStringCallback": "BatchIterator String Callback",

    "UtilsConvertStringListToStringNode": "StringList To String",
}

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS"
]