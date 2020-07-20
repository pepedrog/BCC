/* *****************************************************************************
 *  Name:      
 *  NetID:    
 *  Precept:  
 *
 *  Partner Name:     N/A
 *  Partner NetID:    N/A
 *  Partner Precept:  N/A
 *
 *  Hours to complete assignment (optional):
 *
 **************************************************************************** */

Programming Assignment 8: Burrows-Wheeler



/* *****************************************************************************
 *  List in table format which input files you used to test your program.
 *  Fill in columns for how long your program takes to compress and
 *  decompress these instances (by applying BurrowsWheeler, MoveToFront,
 *  and Huffman in succession). Also, fill in the third column for
 *  the compression ratio (number of bytes in compressed message 
 *  divided by the number of bytes in the message).
 *
 *  Use three significant digits for the compression ratio.
 **************************************************************************** */

File     Encoding Time    Decoding time      Compression ratio
------------------------------------------------------------------------



/* *****************************************************************************
 *  Compare the results of your program (compression ratio and running
 *  time) on mobydick.txt to that of the most popular Linux/OS X compression
 *  program (gzip).
 **************************************************************************** */


/* *****************************************************************************
 *  Give the order of growth of the running time of each of the 6
 *  methods as a function of the input size n and the alphabet size R
 *  both in practice (on typical English text inputs) and in theory
 *  (in the worst case), e.g., n, n + R, n log n, n^2, or R n.
 *
 *  Include the time for sorting circular suffixes in Burrows-Wheeler
 *  transform().
 **************************************************************************** */

                                      typical            worst
---------------------------------------------------------------------
BurrowsWheeler transform()
BurrowsWheeler inverseTransform()
MoveToFront encode()
MoveToFront decode()
Huffman compress()                    n + R log R        n + R log R
Huffman expand()                      n                  n





/* *****************************************************************************
 *  Known bugs / limitations.
 **************************************************************************** */



/* *****************************************************************************
 *  Describe whatever help (if any) that you received.
 *  Don't include readings, lectures, and precepts, but do
 *  include any help from people (including course staff, lab TAs,
 *  classmates, and friends) and attribute them by name.
 **************************************************************************** */


/* *****************************************************************************
 *  Describe any serious problems you encountered.                    
 **************************************************************************** */



/* *****************************************************************************
 *  List any other comments here. Feel free to provide any feedback   
 *  on how much you learned from doing the assignment, and whether    
 *  you enjoyed doing it. Additionally, you may include any suggestions
 *  for what to change or what to keep (assignments or otherwise) in future 
 *  semesters.
 **************************************************************************** */
