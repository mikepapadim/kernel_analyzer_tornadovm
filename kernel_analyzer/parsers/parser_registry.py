from typing import Dict, Type, Optional
import os

class ParserRegistry:
    """Registry to manage different kernel parsers based on file extensions"""
    
    _parsers: Dict[str, Type] = {}
    
    @classmethod
    def register_parser(cls, extension: str, parser_class: Type) -> None:
        """Register a parser class for a specific file extension"""
        cls._parsers[extension] = parser_class
        
    @classmethod
    def get_parser(cls, file_path: str) -> Optional[Type]:
        """Get the appropriate parser class based on file extension"""
        _, ext = os.path.splitext(file_path)
        return cls._parsers.get(ext.lower())
        
    @classmethod
    def get_all_parsers(cls) -> Dict[str, Type]:
        """Get all registered parsers"""
        return cls._parsers.copy() 