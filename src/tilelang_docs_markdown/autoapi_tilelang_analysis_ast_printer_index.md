# tilelang.analysis.ast_printerÂ¶

## FunctionsÂ¶

`ASTPrinter`() | A visitor pass that renders the TileLang AST hierarchy in a visual tree format.  
---|---  
  
## Module ContentsÂ¶

tilelang.analysis.ast_printer.ASTPrinter()Â¶
    

A visitor pass that renders the TileLang AST hierarchy in a visual tree format.

Comparing with TL script, this printer is more suitable for debugging and understanding the internal structure of TensorIR, like the class structure of each node and their connections.

This printer generates a human-readable, tree-structured representation of the Abstract Syntax Tree (AST). It uses ASCII/Unicode connectors to visualize parent-child relationships, making it easier to inspect nested structures (e.g., loops, blocks, scopes) and verify compiler transformations.
