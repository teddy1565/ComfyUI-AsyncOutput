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
    "AsyncOutputConvertStringListToString": AsyncOutput.AsyncOutputConvertStringListToStringNode,
    "AsyncOutputMultiLineTextWithBatch": AsyncOutput.AsyncOutputMultiLineTextWithBatchNode,
    "AsyncOutputInitSignalOutput": AsyncOutput.AsyncOutputInitSignalOutputNode,
    "AsyncOutputRemoteCollection": AsyncOutput.AsyncOutputRemoteCollectionNode,
    "AsyncOutputRemoteTrigger": AsyncOutput.AsyncOutputRemoteTriggerNode,
    "AsyncOutputGlobalAutoReset": AsyncOutput.AsyncOutputGlobalAutoResetNode,
    "AsyncOutputGlobalManualReset": AsyncOutput.AsyncOutputGlobalManualResetNode,
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
}

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS"
]