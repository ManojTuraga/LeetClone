class Node:
    def __init__( self, val ):
        self.val = val
        self.left : Node = None
        self.right : Node = None

class LinkedList:
    def __init__( self ):
        self._head : Node = Node( None )
        self._tail : Node = Node( None )
        self._head.right = self._tail
        self._tail.left = self._head
        self._length : int = 0

    def push( self, val, index ):
        assert( 0 <= index <= self._length )
        
        new_node = Node( val )
        jumper_a = self._head
        
        for _ in range( index ):
            jumper_a = jumper_a.right

        jumper_b = jumper_a.right
        jumper_a.right = new_node
        new_node.left = self._head
        new_node.right = jumper_b
        jumper_b.left = new_node
        
        self._length += 1

    def pop( self, index ):
        assert( 0 <= index < self._length )

        jumper_a = self._head
        
        for _ in range( index ):
            jumper_a = jumper_a.right

        node = jumper_a.right
        jumper_b = node.right
        jumper_a.right = jumper_b
        jumper_b.left = jumper_a
        node.left = None
        node.right = None

        self._length -= 1
        return node.val
    
    def get( self, index ):
        assert( 0 <= index < self._length )

        jumper_a = self._head.right
        
        for _ in range( index ):
            jumper_a = jumper_a.right

        return jumper_a.val
    
    def length( self ):
        return self._length
    
    def reverse( self ):
        for i in range( self.length() ):
            self.push( self.pop( i ), 0 )
    
    def _debug_print( self ):
        for i in range( self.length() ):
            print( self.get( i ), sep=", " )