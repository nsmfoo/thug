#!/usr/bin/env python
from __future__ import with_statement

import sys, re, string

from HTML import BeautifulSoup
import PyV8

from DOMException import DOMException
from Node import Node

class Attr(Node):
    _value = ""
    
    def __init__(self, parent, attr):
        self.parent = parent
        self.attr   = attr

        self._value = self.getValue()
        
    def __repr__(self):
        return "<Attr object %s%s at 0x%08X>" % ("%s." % self.parent.tagName if self.parent else "", self.attr, id(self))
        
    def __eq__(self, other):
        return hasattr(other, "parent") and self.parent == other.parent and \
               hasattr(other, "attr") and self.attr == other.attr
        
    @property
    def nodeType(self):
        return Node.ATTRIBUTE_NODE
       
    @property        
    def nodeName(self):
        return self.attr
    
    def getNodeValue(self):
        return self.getValue()
    
    def setNodeValue(self, value):
        return self.setValue(value)
        
    nodeValue = property(getNodeValue, setNodeValue)
    
    @property
    def childNodes(self):
        from NodeList import NodeList

        return NodeList(self.parent.doc, [])
    
    @property
    def parentNode(self):
        return self.parent

    # Introduced in DOM Level 2
    @property
    def ownerElement(self):
        if self.parent: 
            if self.parent.nodeType == Node.ELEMENT_NODE:
                return self.parent
        
        return None
        
    @property
    def ownerDocument(self):
        return self.parent.doc
    
    @property
    def name(self):
        return self.attr
    
    def specified(self):
        return self.parent.has_key(self.attr)
    
    def getValue(self):
        if self.parent:
            if self.parent.tag.has_key(self.attr):
                return self.parent.tag[self.attr]
            
        return self._value 
        
    def setValue(self, value):
        self._value = value
        
        if self.parent:
            self.parent.tag[self.attr] = value
        
    value = property(getValue, setValue)
