#ifndef LINKED_LIST_H
#define LINKED_LIST_H

#include <stdlib.h>
#include <assert.h>

typedef struct node_t
    {
    void *                 val;
    struct node_t *        left;
    struct node_t *        right;
    } node_t;

typedef struct linked_list_t
    {
    node_t *        head;
    node_t *        tail;
    int             length;

    void ( * linked_list_push )( struct linked_list_t *, void *, int );
    void * ( * linked_list_pop )( struct linked_list_t *, int );
    void ( * linked_list_reverse )( struct linked_list_t * );

    } linked_list_t;

void linked_list_init( linked_list_t * list );
void * linked_list_get( linked_list_t * list, int index );
int linked_list_length( linked_list_t * list);
void linked_list_destroy( linked_list_t * list );

void linked_list_push_dflt( linked_list_t * list, void * val , int index );
void * linked_list_pop_dflt( linked_list_t * list, int index );
void linked_list_reverse_dflt( linked_list_t * list );

void linked_list_init( linked_list_t * list )
    {
    list->linked_list_push = linked_list_push_dflt;
    list->linked_list_pop = linked_list_pop_dflt;
    list->linked_list_reverse = linked_list_reverse_dflt;
    
    list->head = ( node_t * ) malloc( sizeof( node_t ) );
    list->tail = ( node_t * ) malloc( sizeof( node_t ) );

    list->head->right = list->tail;
    list->tail->left = list->head;
    list->length = 0;
    }

void * linked_list_get( linked_list_t * list, int index )
    {
    assert( index >= 0 && index < list->length );

    node_t *        jumper_a;
    jumper_a = list->head->right;

    for( int i = 0; i < index; i++ )
        {
        jumper_a = jumper_a->right;
        }

    return jumper_a->val;
    }

int linked_list_length( linked_list_t * list )
    {
    return list->length;
    }

void linked_list_destroy( linked_list_t * list )
    {
    while( list->length > 0 )
        {
        list->linked_list_pop( list, 0 );
        }

    free( list->head );
    free( list->tail );
    }

void linked_list_push_dflt( linked_list_t * list, void * val , int index )
    {
    assert( index >= 0 && index <= list->length );

    node_t *        new_node;
    node_t *        jumper_a;
    node_t *        jumper_b;

    new_node = ( node_t * ) malloc( sizeof( node_t ) );
    new_node->val = val;

    jumper_a = list->head;

    for( int i = 0; i < index; i++ )
        {
        jumper_a = jumper_a->right;
        }

    jumper_b = jumper_a->right;
    jumper_a->right = new_node;
    new_node->left = list->head;
    new_node->right = jumper_b;
    jumper_b->left = new_node;

    list->length++;
    }

void * linked_list_pop_dflt( linked_list_t * list, int index )
    {
    assert( index >= 0 && index < list->length );

    node_t *        node;
    node_t *        jumper_a;
    node_t *        jumper_b;
    void   *        return_val;

    jumper_a = list->head;

    for( int i = 0; i < index; i++ )
        {
        jumper_a = jumper_a->right;
        }

    node = jumper_a->right;
    jumper_b = node->right;
    jumper_a->right = jumper_b;
    jumper_b->left = jumper_a;
    node->left = NULL;
    node->right = NULL ;
    return_val = node->val;
    free( node );

    list->length--;
    return return_val;
    }

void linked_list_reverse_dflt( linked_list_t * list )
    {
    for( int i = 0; i < list->length; i++ )
        {
        list->linked_list_push( list, list->linked_list_pop( list, i ), 0 );
        }
    }

#endif