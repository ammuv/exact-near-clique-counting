/* 
    This file contains the algorithm for listing all cliques
    according to the algorithm of Jain et al. specified in 
    "The power of pivoting for exact clique counting." (WSDM 2020).

    This code is a modified version of the code of quick-cliques-1.0 library for counting 
    maximal cliques by Darren Strash (first name DOT last name AT gmail DOT com).

    Original author: Darren Strash (first name DOT last name AT gmail DOT com)

    Copyright (c) 2011 Darren Strash. This code is released under the GNU Public License (GPL) 3.0.

    Modifications Copyright (c) 2020 Shweta Jain
    
    This program is free software: you can redistribute it and/or modify 
    it under the terms of the GNU General Public License as published by 
    the Free Software Foundation, either version 3 of the License, or 
    (at your option) any later version. 
 
    This program is distributed in the hope that it will be useful, 
    but WITHOUT ANY WARRANTY; without even the implied warranty of 
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
    GNU General Public License for more details. 
 
    You should have received a copy of the GNU General Public License 
    along with this program.  If not, see <http://www.gnu.org/licenses/> 
*/

#include<assert.h>
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<time.h>
#include<limits.h>
#include<unistd.h> 
#include<libgen.h>
    
#include"misc.h"
#include"LinkedList.h"
#include"MemoryManager.h"



int main(int argc,char** argv)
{

    if (argc != 11)
    {
        printf("Incorrect number of arguments.\n");
        printf("./degeneracy_cliques -i <file_path> -t <type> -k <max_clique_size> -d <data_flag> -o <optimize>\n");
        printf("file_path: path to file\n");
        printf("type: A/V/E. A for just k-clique information, V for per-vertex k-cliques, E for per-edge k-cliques\n");
        printf("max_clique_size: max_clique_size. If 0, calculate for all k.\n");
        printf("data_flag: 1 if information is to be output to a file, 0 otherwise.\n");
        printf("optimize: 1 if you want to use near clique new code or 0 for old method.\n");
        return 0;
    }

    int n; // number of vertices
    int m; // 2x number of edges

    // char *opt = NULL;
    int opt;
    char *fpath = (char *)Calloc(1000, sizeof(char));
    char t;
    int flag_d;
    int max_k = 0;
    int flag_o;

    while((opt = getopt(argc, argv, ":i:t:k:d:o:")) != -1)  
    {  
        switch(opt)  
        {  
            case 'i':  
                // printf("In case i. optarg = %s\n", optarg);
                // strcpy(fpath, optarg);
                fpath = optarg;
                // printf("fpath = %s\n", fpath);
                break;
            case 't':  
                t = *optarg;
                if ((t != 'A') && (t != 'V') && (t != 'E'))
                {
                    printf("Incorrect type. Type should be A, V or E.\n");
                    return 0;
                }
                break;
            case 'k':  
                max_k = atoi(optarg);
                break;
            case 'd': 
                flag_d = atoi(optarg);
                if ((flag_d < 0) || (flag_d > 2))
                {
                    printf("Incorrect flag for data. Shoudld be 0, 1 or 2.\n");
                    return 0;
                }
                break;
            case 'o':
                flag_o = atoi(optarg);
                if ((flag_o < 0) || (flag_o > 1))
                {
                    printf("Incorrect flag for data. Shoudld be 0 or 1\n");
                    return 0;
                }
                break;
            default:
                printf("In default case.\n");
                abort ();
        }
    }
    

    printf("New code.\n");
    // printf("Parsed all arguments. t = %c, max_k = %d, flag_d = %d. About to get graph.\n", t, max_k, flag_d);
    LinkedList** adjacencyList = readInGraphAdjListToDoubleEdges(&n, &m, fpath);

    int i;

    char *gname = basename(fpath);

    char *lastdot = strrchr (gname, '.');
    if (lastdot != NULL)
        *lastdot = '\0';


    populate_nCr();
    printf("about to call runAndPrint.\n");
    runAndPrintStatsCliques(adjacencyList, n, gname, t, max_k, flag_d, flag_o);


    i = 0;
    while(i<n)
    {
        destroyLinkedList(adjacencyList[i]);
        i++;
    }

    Free(adjacencyList); 

    return 0;
}

