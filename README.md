# stabilizer-trellis
# Get Minimal trellis for a given stabilizer code

A program to generate the trellis diagram of a given stabilizer code. Two methods of creating a trellis are included; the first based on the work by Ollivier and Tillich [(arxiv.org/abs/quant-ph/0512041)](https://arxiv.org/abs/quant-ph/0512041), and the second method described by Sidorenko et al. [(ieeexplore.ieee.org/document/10461412)](https://ieeexplore.ieee.org/document/10461412) which is based on the BCJR-Wolf method for constructing trellis diagrams for classical codes.

## Package requirements
The following packages are used:
- numpy
- networkx - Package for creating, modifying the trellis network 
- matlpotlib - For visualization
- itertools

## Notes
The methods are referred to as 'Ollivier method' and 'BCJR-Wolf method' respectively.
1. **Ollivier method**:
   
   Generates the trellis diagram of a given stablizer code and a given syndrome. Requires the generators of the normalizer. Input the stabilizer generators and the logical operators of the code. Also input an arbitrary error corresponding to the required syndrome. The obtained trellis is minimal if the stabilizer generators are in a "trellis-oriented form" (refer the paper for more details and exact procedure. For readability, most of the notation in the code follows the notation of the paper)

2. **BCJR-Wolf method**:
   
   Only requires the set of stabilizer generators to construct the trellis. Input the stabilizer generators and the required binary syndrome directly.
   **Note**: When using this method, comment out the sections "Get Normalizer" and "Get lowerbounds", which are based on variables used in the Ollivier method. 


   
