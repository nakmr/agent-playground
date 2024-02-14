from typing import Dict, List
from semantic_kernel import Kernel
from semantic_kernel.plugin_definition.kernel_plugin import KernelPlugin

plugins_directory = "../plugins"

class SKPluginConfiguration:

    def add_semantic_plugin(pluginNames: List[str], kernel: Kernel) -> Dict[str, KernelPlugin]:
        plugins = {}

        for pluginName in pluginNames:
            plugin = kernel.import_semantic_plugin_from_directory(plugins_directory, pluginName)
            plugins[pluginName] = plugin
        
        return plugins

    def add_native_plugin(pluginNames: List[str], kernel: Kernel) -> Dict[str, KernelPlugin]:
        plugins = {}

        for pluginName in pluginNames:
            plugin = kernel.import_plugin(SlackPlugin(), "SlackPlugin")
            plugins[pluginName] = plugin
        
        return plugins